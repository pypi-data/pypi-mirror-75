import argparse
from collections import defaultdict
import copy
import datetime
import json
import logging
import os
from shlex import quote
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, cast, Dict, List, Optional, Tuple
import urllib.request
import uuid

import click
from jsonpatch import JsonPatch
from ray.autoscaler.commands import (
    create_or_update_cluster,
    exec_cluster,
    get_head_node_ip,
    get_worker_node_ips,
    rsync,
)
from ray.autoscaler.util import fillout_defaults
import ray.projects.scripts as ray_scripts
import ray.ray_constants
import ray.scripts.scripts as autoscaler_scripts
import requests
import tabulate
import yaml

from anyscale.auth_proxy import app as auth_proxy_app
from anyscale.autosync_heartbeat import managed_autosync_session
from anyscale.cloudgateway import CloudGatewayRunner
import anyscale.conf
from anyscale.feature_flags import FLAG_KEY_USE_SNAPSHOT
from anyscale.project import (
    ANYSCALE_AUTOSCALER_FILE,
    ANYSCALE_PROJECT_FILE,
    CLUSTER_YAML_TEMPLATE,
    get_project_id,
    load_project_or_throw,
    PROJECT_ID_BASENAME,
    validate_project_name,
)
from anyscale.snapshot import (
    copy_file,
    create_snapshot,
    describe_snapshot,
    download_snapshot,
    get_snapshot_uuid,
    list_snapshots,
)
from anyscale.util import (
    _get_role,
    _resource,
    check_is_feature_flag_on,
    confirm,
    deserialize_datetime,
    execution_log_name,
    get_available_regions,
    get_endpoint,
    humanize_timestamp,
    send_json_request,
    send_json_request_raw,
    slugify,
    wait_for_session_start,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


def get_or_create_snapshot(
    snapshot_uuid: Optional[str], description: str, project_definition: Any, yes: bool,
) -> str:
    # If no snapshot was provided, create a snapshot.
    if snapshot_uuid is None:
        confirm("No snapshot specified for the command. Create a new snapshot?", yes)
        snapshot_uuid = create_snapshot(
            project_definition,
            yes,
            description=description,
            tags=["anyscale:session_startup"],
        )
    else:
        snapshot_uuid = get_snapshot_uuid(project_definition.root, snapshot_uuid)
    return snapshot_uuid


def get_project_sessions(project_id: int, session_name: Optional[str]) -> Any:
    response = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name_match": session_name, "active_only": True},
    )
    sessions = response["results"]
    if len(sessions) == 0:
        raise click.ClickException(
            "No active session matching pattern {} found".format(session_name)
        )
    return sessions


def get_project_session(project_id: int, session_name: Optional[str]) -> Any:
    sessions = get_project_sessions(project_id, session_name)
    if len(sessions) > 1:
        raise click.ClickException(
            "Multiple active sessions: {}\n"
            "Please specify the one you want to refer to.".format(
                [session["name"] for session in sessions]
            )
        )
    return sessions[0]


def get_project_directory_name(project_id: int) -> str:
    resp = send_json_request("/api/v2/projects/", {})
    directory_name = ""
    for project in resp["results"]:
        if project["id"] == project_id:
            directory_name = project["directory_name"]
            break
    assert len(directory_name) > 0
    return directory_name


def setup_ssh_for_head_node(session_id: int) -> Tuple[str, str]:
    resp = send_json_request("/api/v2/sessions/{}/ssh_key".format(session_id), {},)
    key_path = write_ssh_key(resp["result"]["key_name"], resp["result"]["private_key"])

    subprocess.Popen(
        ["chmod", "600", key_path], stdout=subprocess.PIPE,
    )

    resp = send_json_request("/api/v2/sessions/{}/head_ip".format(session_id), {})
    head_ip = resp["result"]["head_ip"]
    return head_ip, key_path


def update_file_mounts(
    cluster_config: Dict[str, Any], project_definition: Any
) -> Dict[str, str]:
    project_id = get_project_id(project_definition.root)
    cluster_config = fillout_defaults(cluster_config)
    for remote_path in cluster_config["file_mounts"]:
        if remote_path == "~/{}".format(
            get_project_directory_name(project_id)
        ) and not os.path.samefile(
            cluster_config["file_mounts"][remote_path], project_definition.root
        ):
            click.confirm(
                '"{remote}: {local}" has been detected in the file mounts.\n'
                'Anyscale needs to sync the local project directory "{proj}" '
                'with "{remote}" in the cluster.\nCan this file mount be replaced for '
                "this command?\nThis action will not change your session "
                "configuration file.".format(
                    remote=remote_path,
                    local=cluster_config["file_mounts"][remote_path],
                    proj=project_definition.root,
                ),
                abort=True,
            )
    cluster_config["file_mounts"].update(
        {"~/{}".format(get_project_directory_name(project_id)): project_definition.root}
    )
    return cluster_config


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    url = anyscale.util.get_endpoint("/api/v2/userinfo/anyscale_version")
    resp = requests.get(url)
    if resp.ok:
        curr_version = anyscale.__version__
        latest_version = resp.json()["result"]["version"]
        if curr_version != latest_version:
            message = "Warning: Using version {0} of anyscale. Please update the package using pip install anyscale -U to get the latest version {1}".format(
                curr_version, latest_version
            )
            print("\033[91m{}\033[00m".format(message), file=sys.stderr)
    else:
        logger.warning(
            "Error {} while trying to get latest anyscale version number: {}".format(
                resp.status_code, resp.text
            )
        )


@click.group("project", help="Commands for working with projects.", hidden=True)
def project_cli() -> None:
    pass


@click.group("session", help="Commands for working with sessions.", hidden=True)
def session_cli() -> None:
    pass


@click.group("snapshot", help="Commands for working with snapshot.", hidden=True)
def snapshot_cli() -> None:
    pass


@click.group(
    "cloud",
    short_help="Configure cloud provider authentication for Anyscale.",
    help="""Configure cloud provider authenticationand setup
to allow Anyscale to launch instances in your account.""",
)
def cloud_cli() -> None:
    pass


@click.group("list", help="List resources (projects, sessions) within Anyscale.")
def list_cli() -> None:
    pass


@click.command(name="version", help="Display version of the anyscale CLI.")
def version_cli() -> None:
    print(anyscale.__version__)


def setup_aws_cross_account_role(
    email: str, region: str, user_id: int, name: str
) -> None:

    response = send_json_request("/api/v2/clouds/anyscale/aws_account", {})
    assert "anyscale_aws_account" in response["result"]

    anyscale_aws_account = response["result"]["anyscale_aws_account"]
    anyscale_aws_iam_role_policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {"AWS": anyscale_aws_account},
            "Action": "sts:AssumeRole",
        },
    }

    aws_iam_anyscale_role_name = f"anyscale-iam-role-{str(uuid.uuid4())[:8]}"

    iam = _resource("iam", region)

    role = _get_role(aws_iam_anyscale_role_name, region)
    if role is None:
        iam.create_role(
            RoleName=aws_iam_anyscale_role_name,
            AssumeRolePolicyDocument=json.dumps(anyscale_aws_iam_role_policy),
        )
        role = _get_role(aws_iam_anyscale_role_name, region)

    assert role is not None, "Failed to create IAM role!"

    role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess")
    role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/IAMFullAccess")

    print(f"Created IAM role {role.arn}")

    send_json_request(
        "/api/v2/clouds/",
        {
            "provider": "AWS",
            "region": region,
            "credentials": role.arn,
            "creator_id": user_id,
            "name": name,
        },
        method="POST",
    )


@list_cli.command(
    name="clouds", help="List the clouds currently available in your account."
)
def list_clouds() -> None:
    response = send_json_request("/api/v2/clouds/", {})
    clouds = response["results"]

    cloud_table = []
    print("Clouds: ")
    for cloud in clouds:
        cloud_table.append(
            [
                cloud["id"],
                cloud["name"],
                cloud["provider"],
                cloud["region"],
                cloud["credentials"],
            ]
        )
    print(
        tabulate.tabulate(
            cloud_table,
            headers=["ID", "name", "PROVIDER", "REGION", "CREDENTIALS"],
            tablefmt="plain",
        )
    )


@cloud_cli.command(name="apply", help="Apply a cloud to a project")
@click.option("--project-name", help="Project to apply to the cloud.", required=True)
@click.option("--cloud-id", help="Cloud to apply to the project.", required=True)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def apply_cloud(project_name: str, cloud_id: str, yes: bool) -> None:
    response = send_json_request(
        "/api/v2/projects/find_by_name", {"name": project_name}
    )
    projects = response["results"]
    if len(projects) == 0:
        print(f"Project '{project_name}' doesn't exist.")
        return

    project = projects[0]

    existing_cloud_id = project["cloud_id"]

    if existing_cloud_id == cloud_id:
        print(f"\nCloud {cloud_id} is already applied to project {project_name}")
        return

    if existing_cloud_id:
        print(
            f"\nProject {project_name} is currently configured with cloud {existing_cloud_id}."
        )
        confirm(
            f"\nYou'll lose access to existing sessions created with cloud {existing_cloud_id} if you overwrite it.\nContinue?",
            yes,
        )

    jsonpatch = JsonPatch([{"op": "replace", "path": "/cloud_id", "value": cloud_id}])
    resp = send_json_request(
        "/api/v2/projects/{}".format(project["id"]), jsonpatch.to_string(), "PATCH"
    )
    assert resp == {}
    print(f"Applied cloud {cloud_id} to project {project_name}")


@cloud_cli.command(name="drop", help="Drop the cloud from a project")
@click.option("--project-name", help="Project to drop the cloud from.", required=True)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def drop_cloud_from_project(project_name: str, yes: bool) -> None:

    response = send_json_request(
        "/api/v2/projects/find_by_name", {"name": project_name}
    )

    projects = response["results"]
    if len(projects) == 0:
        print(f"Project {project_name} doesn't exist.")
        return
    project = projects[0]
    cloud_id = project["cloud_id"]

    if not cloud_id:
        print(f"Project {project_name} doesn't have any cloud configured")
        return

    confirm(
        f"You'll lose access to existing sessions created with cloud {cloud_id} if you drop it.\nContinue?",
        yes,
    )

    jsonpatch = JsonPatch([{"op": "replace", "path": "/cloud_id", "value": None}])
    resp = send_json_request(
        "/api/v2/projects/{}".format(project["id"]), jsonpatch.to_string(), "PATCH"
    )
    assert resp == {}
    print(f"Dropped the cloud from project {project_name}")


@cloud_cli.command(name="setup", help="Set up a cloud provider.")
@click.option("--provider", help="Project to drop the cloud from.", required=True)
@click.option(
    "--region", help="Region to set up the credentials in.", default="us-west-2",
)
@click.option("--name", help="Name of the cloud.", required=True)
def setup_cloud(provider: str, region: str, name: str) -> None:
    if provider == "AWS":
        setup_aws(region, name)


def setup_aws(region: str, name: str) -> None:

    os.environ["AWS_DEFAULT_REGION"] = region
    regions_available = get_available_regions()
    if region not in regions_available:
        raise click.ClickException(
            f"Region '{region}' is not available. Regions availables are {regions_available}"
        )

    confirm(
        "\nYou are about to give anyscale full access to EC2 and IAM in your AWS account.\n\n"
        "Continue?",
        False,
    )

    response = send_json_request("/api/v2/userinfo/", {})

    setup_aws_cross_account_role(
        response["result"]["email"], region, response["result"]["id"], name
    )

    # Sleep for 5 seconds to make sure the policies take effect.
    time.sleep(5)

    print("AWS credentials setup complete!")
    print(
        "You can revoke the access at any time by deleting anyscale IAM user/role in your account."
    )
    print("Head over to the web UI to create new sessions in your AWS account!")


def register_project(project_definition: Any) -> None:
    project_id_path = os.path.join(ray_scripts.PROJECT_DIR, PROJECT_ID_BASENAME)

    project_name = project_definition.config["name"]
    print("Creating project {}".format(project_name))
    description = project_definition.config.get("description", "")

    # Add a database entry for the new Project.
    resp = send_json_request(
        "/api/v2/projects/",
        {"name": project_name, "description": description},
        method="POST",
    )
    result = resp["result"]
    project_id = result["id"]

    if os.path.exists(ray_scripts.PROJECT_YAML):
        with open(project_id_path, "w+") as f:
            f.write(str(project_id))
    else:
        with open(anyscale.project.ANYSCALE_PROJECT_FILE, "w") as f:
            yaml.dump({"project_id": project_id}, f)

    # Create initial snapshot for the project.
    try:
        create_snapshot(
            project_definition,
            False,
            description="Initial project snapshot",
            tags=["anyscale:initial"],
        )
    except click.Abort as e:
        raise e
    except Exception as e:
        # Creating a snapshot can fail if the project is not found or if some
        # files cannot be copied (e.g., due to permissions).
        raise click.ClickException(e)  # type: ignore

    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Project {project_id} created. View at {url}")


def create_new_proj_def(
    name: Optional[str], cluster_config_file: Optional[str]
) -> Tuple[str, Any]:
    project_name = ""
    if not name:
        while project_name == "":
            project_name = click.prompt("Project name", type=str)
            if not validate_project_name(project_name):
                print(
                    '"{}" contains spaces. Please enter a project name without spaces'.format(
                        project_name
                    ),
                    file=sys.stderr,
                )
                project_name = ""
        if not cluster_config_file:
            cluster_config_file = click.prompt(
                "Cluster yaml file (optional)",
                type=click.Path(exists=True),
                default=".",
                show_default=False,
            )
            if cluster_config_file == ".":
                # handling default value from prompt
                cluster_config_file = None
    else:
        project_name = str(name)
    if slugify(project_name) != project_name:
        project_name = slugify(project_name)
        print("Normalized project name to {}".format(project_name))

    # Create startup.yaml.
    if cluster_config_file:
        shutil.copyfile(cluster_config_file, anyscale.project.ANYSCALE_AUTOSCALER_FILE)
    else:
        if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
            with open(anyscale.project.ANYSCALE_AUTOSCALER_FILE, "w") as f:
                f.write(anyscale.project.CLUSTER_YAML_TEMPLATE)
    project_definition = anyscale.project.ProjectDefinition(os.getcwd())
    project_definition.config["name"] = project_name
    return project_name, project_definition


@click.command(
    name="init", help="Create a new project or register an existing project."
)
@click.option("--name", help="Project name.", required=False)
@click.option(
    "--cluster-config-file",
    help="Path to autoscaler yaml. Created by default.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--requirements",
    help="Path to requirements.txt. Created by default.",
    required=False,
)
@click.pass_context
def anyscale_init(
    ctx: Any,
    name: Optional[str],
    cluster_config_file: Optional[str],
    requirements: Optional[str],
) -> None:
    # Send an initial request to the server to make sure we are actually
    # registered. We only want to create the project if that is the case,
    # to avoid projects that are created but not registered.
    send_json_request("/api/v2/userinfo/", {})
    project_name = ""
    project_id_path = (
        os.path.join(ray_scripts.PROJECT_DIR, PROJECT_ID_BASENAME)
        if os.path.exists(ray_scripts.PROJECT_DIR)
        else anyscale.project.ANYSCALE_PROJECT_FILE
    )
    if not os.path.exists(
        anyscale.project.ANYSCALE_PROJECT_FILE
    ) and not os.path.exists(project_id_path):
        # Project id doesn't exist.
        project_name, project_definition = create_new_proj_def(
            name, cluster_config_file
        )
    else:
        # Project id exists.
        try:
            project_definition = load_project_or_throw()
            if os.path.exists(anyscale.project.ANYSCALE_PROJECT_FILE):
                project_id = project_definition.config["project_id"]
            else:
                try:
                    with open(project_id_path, "r") as f:
                        project_id = int(f.read())
                except Exception:
                    raise click.ClickException(
                        "The project id file {} is corrupted.".format(project_id_path)
                    )

        except click.ClickException as e:
            raise e

        # Checking if the project is already registered.
        resp = send_json_request("/api/v2/projects/", {})
        for project in resp["results"]:
            if project["id"] == project_id:
                if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
                    # Session yaml file doesn't exist.
                    project_name = get_project_directory_name(project["id"])
                    url = get_endpoint(f"/projects/{project['id']}")
                    if click.confirm(
                        "Session configuration missing in local project. Would "
                        "you like to replace your local copy of {project_name} "
                        "with the version in Anyscale ({url})?".format(
                            project_name=project_name, url=url
                        )
                    ):
                        clone_files(project_name, os.getcwd(), project["id"])
                        print(f"Created project {project['id']}. View at {url}")
                        return
                else:
                    raise click.ClickException(
                        "This project is already created at {url}.".format(
                            url=get_endpoint(f"/projects/{project['id']}")
                        )
                    )
        # Project id exists locally but not registered in the db.
        if click.confirm(
            "The Ansycale project associated with this doesn't "
            "seem to exist anymore. Do you want to re-create it?",
            abort=True,
        ):
            os.remove(project_id_path)
            project_name, project_definition = create_new_proj_def(
                name, cluster_config_file
            )

    register_project(project_definition)


@list_cli.command(name="projects", help="List all accessible projects.")
@click.pass_context
def project_list(ctx: Any) -> None:
    resp = send_json_request("/api/v2/projects/", {})
    projects = resp["results"]
    project_table = []

    print("Projects:")
    for project in projects:
        project_table.append(
            [
                project["name"],
                "{}/project/{}".format(anyscale.conf.ANYSCALE_HOST, project["id"]),
                project["description"],
                project["cloud"],
            ]
        )
    print(
        tabulate.tabulate(
            project_table,
            headers=["NAME", "URL", "DESCRIPTION", "CLOUD"],
            tablefmt="plain",
        )
    )


def remote_snapshot(
    project_id: int,
    session_name: str,
    additional_files: List[str],
    files_only: bool = False,
) -> str:
    session = get_project_session(project_id, session_name)

    resp = send_json_request(
        "/api/v2/sessions/{session_id}/take_snapshot".format(session_id=session["id"]),
        {"additional_files": additional_files, "files_only": files_only},
        method="POST",
    )
    if "id" not in resp["result"]:
        raise click.ClickException(
            "Snapshot creation of session {} failed!".format(session_name)
        )
    snapshot_uuid: str = resp["result"]["id"]
    return snapshot_uuid


@snapshot_cli.command(name="create", help="Create a snapshot of the current project.")
@click.argument(
    "files", nargs=-1, required=False,
)
@click.option("--description", help="A description of the snapshot", default=None)
@click.option(
    "--session-name",
    help="If specified, a snapshot of the remote session"
    "with that name will be taken.",
    default=None,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--include-output-files",
    is_flag=True,
    default=False,
    help="Include output files with the snapshot",
)
@click.option(
    "--files-only",
    is_flag=True,
    default=False,
    help="If specified, files in the project directory are not included in the snapshot",
)
@click.option(
    "--tag",
    type=str,
    help="Tag for this snapshot. Multiple tags can be specified by repeating this option.",
    multiple=True,
)
def snapshot_create(
    files: List[str],
    description: Optional[str],
    session_name: Optional[str],
    yes: bool,
    include_output_files: bool,
    files_only: bool,
    tag: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    files = list(files)
    if len(files) > 0:
        files = [os.path.abspath(f) for f in files]

    if session_name:
        # Create a remote snapshot.
        try:
            snapshot_uuid = remote_snapshot(project_id, session_name, files, files_only)
            print(
                "Snapshot {snapshot_uuid} of session {session_name} created!".format(
                    snapshot_uuid=snapshot_uuid, session_name=session_name
                )
            )
        except click.ClickException as e:
            raise e

    else:
        # Create a local snapshot.
        try:
            snapshot_uuid = create_snapshot(
                project_definition,
                yes,
                description=description,
                include_output_files=include_output_files,
                additional_files=files,
                files_only=files_only,
                tags=tag,
            )
        except click.Abort as e:
            raise e
        except Exception as e:
            # Creating a snapshot can fail if the project is not found or
            # if some files cannot be copied (e.g., due to permissions).
            raise click.ClickException(e)  # type: ignore

    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Snapshot {snapshot_uuid} created. View at {url}")


@snapshot_cli.command(
    name="describe", help="Describe metadata and files of a snapshot."
)
@click.argument("name")
def snapshot_describe(name: str) -> None:
    try:
        description = describe_snapshot(name)
    except Exception as e:
        # Describing a snapshot can fail if the snapshot does not exist.
        raise click.ClickException(e)  # type: ignore

    print(description)


@snapshot_cli.command(name="download", help="Download a snapshot.")
@click.argument("name")
@click.option("--target-directory", help="Directory this snapshot is downloaded to.")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="If set, the downloaded snapshot will overwrite existing directory",
)
def snapshot_download(
    name: str, target_directory: Optional[str], overwrite: bool
) -> None:
    try:
        resp = send_json_request("/api/v2/users/temporary_aws_credentials", {})
    except Exception as e:
        # The snapshot may not exist.
        raise click.ClickException(e)  # type: ignore

    assert "AWS_ACCESS_KEY_ID" in resp["result"]

    download_snapshot(
        name, resp["result"], target_directory=target_directory, overwrite=overwrite,
    )


@session_cli.command(name="attach", help="Open a console for the given session.")
@click.option("--name", help="Name of the session to open a console for.", default=None)
@click.option("--tmux", help="Attach console to tmux.", is_flag=True)
@click.option("--screen", help="Attach console to screen.", is_flag=True)
def session_attach(name: Optional[str], tmux: bool, screen: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, name)
    ray.autoscaler.commands.attach_cluster(
        project_definition.cluster_yaml(),
        start=False,
        use_tmux=tmux,
        use_screen=screen,
        override_cluster_name=session["name"],
        new=False,
    )


@click.command(
    name="up",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start or update a session based on the current project configuration.",
)
@click.argument("session-name", required=False)
@click.option(
    "--cluster-config-file",
    "cluster_config_file",
    help="Cluster to start session with.",
    default=None,
)
@click.option(
    "--no-restart",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip restarting Ray services during the update. "
        "This avoids interrupting running jobs."
    ),
)
@click.option(
    "--restart-only",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip running setup commands and only restart Ray. "
        "This cannot be used with 'no-restart'."
    ),
)
@click.option(
    "--min-workers",
    required=False,
    type=int,
    help="Override the configured min worker node count for the cluster.",
)
@click.option(
    "--max-workers",
    required=False,
    type=int,
    help="Override the configured max worker node count for the cluster.",
)
def anyscale_up(
    session_name: Optional[str],
    cluster_config_file: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    no_restart: bool,
    restart_only: bool,
) -> None:
    """Create or update a Ray cluster."""

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    if not cluster_config_file:
        cluster_config_file = project_definition.config["cluster"]["config"]
    cluster_config_file = cast(str, cluster_config_file)

    if not os.path.exists(cluster_config_file):
        raise ValueError("Project file {} not found".format(cluster_config_file))
    with open(cluster_config_file) as f:
        cluster_config = yaml.safe_load(f)

    resp_out_up = send_json_request(
        "/api/v2/sessions/up",
        {
            "project_id": project_id,
            "name": session_name,
            "cluster_config": {"config": json.dumps(cluster_config)},
        },
        method="POST",
    )

    prev_head_ip = send_json_request(
        "/api/v2/sessions/{}".format(resp_out_up["result"]["session_id"]), {}
    )["result"]["head_node_ip"]

    key_dir = "~/.ssh/session-{session_id}".format(
        session_id=resp_out_up["result"]["session_id"]
    )
    key_path = write_ssh_key(
        "ray-autoscaler_4_us-west-2", resp_out_up["result"]["private_key"], key_dir
    )

    cluster_config = resp_out_up["result"]["cluster_config"]
    cluster_config["auth"].update({"ssh_private_key": key_path})
    cluster_config["head_node"].update({"KeyName": "ray-autoscaler_4_us-west-2"})
    cluster_config["worker_nodes"].update({"KeyName": "ray-autoscaler_4_us-west-2"})

    resp_out_credentials = send_json_request(
        "/api/v2/sessions/{session_id}/autoscaler_credentials".format(
            session_id=resp_out_up["result"]["session_id"]
        ),
        {},
    )
    cluster_config["provider"].update(
        {"aws_credentials": resp_out_credentials["result"]["credentials"]}
    )

    cluster_config = fillout_defaults(cluster_config)

    anyscale.util.install_anyscale_hooks(cluster_config)

    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        try:
            command = [
                "ray",
                "up",
                config_file.name,
                "--no-restart" if no_restart else "",
                "--restart-only" if restart_only else "",
                "--cluster-name",
                "{}".format(resp_out_up["result"]["cluster_name"]),
                "--max-workers {}".format(max_workers) if max_workers else "",
                "--min-workers {}".format(min_workers) if min_workers else "",
                "--yes",
            ]
            command_lst = [c for c in command if c]

            proc = subprocess.Popen(
                command_lst, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            startup_log = []
            while True:
                if proc.stdout:
                    line = proc.stdout.readline().decode()
                    if not line:
                        break
                    print(line, end="")
                    startup_log.append(line)
            startup_log_str = "".join(startup_log)

            proc = subprocess.Popen(
                ["anyscale", "list", "ips", session_name, "--json"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            out = proc.communicate()[0].decode()
            curr_head_ip = json.loads(out[:-1])[0]["head-ip"]

            # Rsync file mounts and project directory after cluster started
            rsync(
                config_file.name,
                None,
                None,
                resp_out_up["result"]["cluster_name"],
                down=False,
                all_nodes=True,
            )

            if curr_head_ip != prev_head_ip:
                print("Setting up Jupyter lab, Ray dashboard, and autosync ...")

            send_json_request(
                "/api/v2/sessions/{session_id}/finish_up".format(
                    session_id=resp_out_up["result"]["session_id"]
                ),
                {
                    "startup_log": startup_log_str,
                    "new_session": curr_head_ip != prev_head_ip,
                    "head_node_ip": curr_head_ip,
                },
                "POST",
            )
            url = get_endpoint(f"/projects/{project_id}")
            print(f"Session {session_name} started. View at {url}")
        except Exception:
            send_json_request(
                f"/api/v2/sessions/{resp_out_up['result']['session_id']}/stop",
                {"terminate": True, "workers_only": False, "keep_min_workers": False},
                method="POST",
            )
            raise click.ClickException("Session startup failed.")


@click.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start a session based on the current project configuration.",
    hidden=True,
)
@click.option("--session-name", help="The name of the created session.", default=None)
# TODO(pcm): Change this to be
# anyscale session start --arg1=1 --arg2=2 command args
# instead of
# anyscale session start --session-args=--arg1=1,--arg2=2 command args
@click.option(
    "--session-args",
    help="Arguments that get substituted into the cluster config "
    "in the format --arg1=1,--arg2=2",
    default="",
)
@click.option(
    "--snapshot",
    help="If set, start the session from the given snapshot.",
    default=None,
)
@click.option(
    "--cluster-config-file",
    help="If set, use this cluster file rather than the default"
    " listed in project.yaml.",
    default=None,
)
@click.option(
    "--min-workers",
    help="Overwrite the minimum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--max-workers",
    help="Overwrite the maximum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--run", help="Command to run.", default=None,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell",
    help="If set, run the command as a raw shell command instead "
    "of looking up the command in the project.yaml.",
    is_flag=True,
)
@click.option("--cloud-id", help="Id of the cloud to use", default=None)
def anyscale_start(
    session_args: str,
    snapshot: Optional[str],
    session_name: Optional[str],
    cluster_config_file: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    run: Optional[str],
    args: List[str],
    shell: bool,
    cloud_id: Optional[str],
) -> None:
    # TODO(pcm): Remove the dependence of the product on Ray.
    from ray.projects.projects import make_argument_parser

    command_name = run

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    # Parse the session arguments.
    if cluster_config_file:
        project_definition.config["cluster"]["config"] = cluster_config_file

    cluster_params = project_definition.config["cluster"].get("params")
    if cluster_params:
        parser, choices = make_argument_parser("session params", cluster_params, False)
        session_params = vars(parser.parse_args(session_args.split(",")))
    else:
        session_params = {}

    if command_name and shell:
        command_name = " ".join([command_name] + list(args))
    session_runs = ray_scripts.get_session_runs(session_name, command_name, {})

    assert len(session_runs) == 1, "Running sessions with a wildcard is deprecated"
    session_run = session_runs[0]

    snapshot_uuid = get_or_create_snapshot(
        snapshot,
        description="Initial snapshot for session {}".format(session_run["name"]),
        project_definition=project_definition,
        yes=True,
    )

    session_name = session_run["name"]
    resp = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name": session_name, "active_only": False},
    )
    if len(resp["results"]) == 0:
        resp = send_json_request(
            "/api/v2/sessions/create_from_snapshot",
            {
                "project_id": project_id,
                "name": session_name,
                "snapshot_id": snapshot_uuid,
                "session_params": session_params,
                "command_name": command_name,
                "command_params": session_run["params"],
                "shell": shell,
                "min_workers": min_workers,
                "max_workers": max_workers,
                "cloud_id": cloud_id,
            },
            method="POST",
        )
    elif len(resp["results"]) == 1:
        if session_params != {}:
            raise click.ClickException(
                "Session parameters are not supported when restarting a session"
            )
        send_json_request(
            "/api/v2/sessions/{session_id}/start".format(
                session_id=resp["results"][0]["id"]
            ),
            {"min_workers": min_workers, "max_workers": max_workers},
            method="POST",
        )
    else:
        raise click.ClickException(
            "Multiple sessions with name {} exist".format(session_name)
        )
    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_name} starting. View progress at {url}")


@session_cli.command(name="sync", help="Synchronize a session with a snapshot.")
@click.option(
    "--snapshot",
    help="The snapshot UUID the session should be synchronized with.",
    default=None,
)
@click.option("--name", help="The name of the session to synchronize.", default=None)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation. Confirmation is needed when "
    "no snapshot name is provided.",
)
def session_sync(snapshot: Optional[str], name: Optional[str], yes: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, name)
    if not snapshot:
        # Sync with latest snapshot by default
        snapshots = list_snapshots(project_definition.root)
        snapshot = snapshots[0]

    print("Syncing session {0} to snapshot {1}".format(session["name"], snapshot))

    send_json_request(
        "/api/v2/sessions/{session_id}/sync".format(session_id=session["id"]),
        {"snapshot_id": snapshot},
        method="POST",
    )

    session_name = session["name"]
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_name} synced. View at {url}")


@click.command(
    name="run",
    context_settings=dict(ignore_unknown_options=True,),
    help="Execute a command in a session.",
)
@click.argument("command_name", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell",
    help="If set, run the command as a raw shell command instead "
    "of looking up the command in the project.yaml.",
    is_flag=True,
)
@click.option(
    "--session-name", help="Name of the session to run this command on", default=None
)
@click.option(
    "--stop", help="If set, stop session after command finishes running.", is_flag=True,
)
def anyscale_run(
    command_name: Optional[str],
    args: List[str],
    shell: bool,
    session_name: Optional[str],
    stop: bool,
) -> None:

    if not shell and not command_name:
        raise click.ClickException(
            "No shell command or registered command name was specified."
        )
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)

    if command_name and shell:
        command_name = " ".join([command_name] + list(args))

    if shell:
        send_json_request(
            "/api/v2/sessions/{session_id}/execute_shell_command".format(
                session_id=session["id"]
            ),
            {"shell_command": command_name, "stop": stop},
            method="POST",
        )
    else:
        send_json_request(
            "/api/v2/sessions/{session_id}/execute/{command_name}".format(
                session_id=session["id"], command_name=command_name
            ),
            {"params": {}},
            method="POST",
        )


@session_cli.command(name="logs", help="Show logs for the current session.")
@click.option("--name", help="Name of the session to run this command on", default=None)
@click.option("--command-id", help="ID of the command to get logs for", default=None)
def session_logs(name: Optional[str], command_id: Optional[int]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    # If the command_id is not specified, determine it by getting the
    # last run command from the active session.
    if not command_id:
        session = get_project_session(project_id, name)
        resp = send_json_request(
            "/api/v2/session_commands/?session_id={}".format(session["id"]), {}
        )
        # Search for latest run command
        last_created_at = datetime.datetime.min
        last_created_at = last_created_at.replace(tzinfo=datetime.timezone.utc)
        for command in resp["results"]:
            created_at = deserialize_datetime(command["created_at"])
            if created_at > last_created_at:
                last_created_at = created_at
                command_id = command["session_command_id"]
        if not command_id:
            raise click.ClickException(
                "No comand was run yet on the latest active session {}".format(
                    session["name"]
                )
            )
    resp_out = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "out", "start_line": 0, "end_line": 1000000000},
    )
    resp_err = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "err", "start_line": 0, "end_line": 1000000000},
    )
    # TODO(pcm): We should have more options here in the future
    # (e.g. show only stdout or stderr, show only the tail, etc).
    print("stdout:")
    print(resp_out["result"]["lines"])
    print("stderr:")
    print(resp_err["result"]["lines"])


@session_cli.command(
    name="upload_command_logs", help="Upload logs for a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to upload logs for", type=int, default=None
)
def session_upload_command_logs(command_id: Optional[int]) -> None:
    resp = send_json_request(
        "/api/v2/session_commands/{session_command_id}/upload_logs".format(
            session_command_id=command_id
        ),
        {},
        method="POST",
    )
    assert resp["result"]["session_command_id"] == command_id

    allowed_sources = [
        execution_log_name(command_id) + ".out",
        execution_log_name(command_id) + ".err",
    ]

    for source, target in resp["result"]["locations"].items():
        if source in allowed_sources:
            copy_file(True, source, target, download=False)


@session_cli.command(
    name="finish_command", help="Finish executing a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to finish", type=int, required=True
)
@click.option(
    "--stop", help="Stop session after command finishes executing.", is_flag=True
)
def session_finish_command(command_id: int, stop: bool) -> None:
    with open(execution_log_name(command_id) + ".status") as f:
        status_code = int(f.read().strip())
    send_json_request(
        f"/api/v2/session_commands/{command_id}/finish",
        {"status_code": status_code, "stop": stop},
        method="POST",
    )


@click.command(
    name="cloudgateway",
    help="Run private clusters via anyscale cloud gateway.",
    hidden=True,
)
@click.option("--gateway-id", type=str, required=True)
def anyscale_cloudgateway(gateway_id: str) -> None:
    # Make sure only registered users can start the gateway.
    logger.info("Verifying user ...")
    try:
        send_json_request("/api/v2/userinfo/", {})["result"]
    except Exception:
        raise click.ClickException(
            "Invalid user. Did you set up the cli_token credentials?"
            + ' To setup your credentials, follow the instructions in the "credentials" tab'
            + " after logging in to your anyscale account."
        )
    anyscale_address = f"/api/v2/cloudgateway/{gateway_id}"
    cloudgateway_runner = CloudGatewayRunner(anyscale_address)
    logger.info(
        "Your gateway-id is: {}. Store it in the provider section in the".format(
            gateway_id
        )
        + " cluster yaml file of the remote cluster that interacts with this gateway."
        + ' E.g., config["provider"]["gateway_id"]={gateway_id}.'.format(
            gateway_id=gateway_id
        )
    )
    cloudgateway_runner.gateway_run_forever()


@click.command(
    name="autosync",
    short_help="Automatically synchronize a local project with a session.",
    help="""
This command launches the autosync service that will synchronize
the state of your local project with the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
def anyscale_autosync(session_name: Optional[str], verbose: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    print("Active project: " + project_definition.root)
    print()

    session = get_project_session(project_id, session_name)

    wait_for_session_start(project_id, session["name"])

    # Get project directory name:
    directory_name = get_project_directory_name(project_id)

    print("Autosync with session {} is starting up...".format(session["name"]))
    head_ip, key_path = setup_ssh_for_head_node(session["id"])

    source = project_definition.root
    target = "~/{}".format(directory_name)

    with managed_autosync_session(session["id"]):
        ssh_command = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile={}".format(os.devnull),
            "-i",
            key_path,
        ]
        # Performing initial full synchronization with rsync.
        command = " ".join(
            [
                "rsync",
                "--rsh",
                '"' + " ".join(ssh_command) + '"',
                "-avz",
                source,
                "ubuntu@{}:{}".format(head_ip, target),
            ]
        )
        subprocess.check_call(command, shell=True)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        if sys.platform.startswith("linux"):
            env: Dict[str, str] = {}
            fswatch_executable = os.path.join(current_dir, "fswatch-linux")
            fswatch_command = [
                fswatch_executable,
                source,
                "--batch-marker",
                "--monitor=poll_monitor",
                "-r",
            ]
        elif sys.platform.startswith("darwin"):
            env = {"DYLD_LIBRARY_PATH": current_dir}
            fswatch_executable = os.path.join(current_dir, "fswatch-darwin")
            fswatch_command = [fswatch_executable, source, "--batch-marker"]
        else:
            raise NotImplementedError(
                "Autosync not supported on platform {}".format(sys.platform)
            )

        # Perform synchronization whenever there is a change. We batch together
        # multiple updates and then call rsync on them.
        with subprocess.Popen(
            fswatch_command, stdout=subprocess.PIPE, env=env,
        ) as proc:
            while True:
                files = []
                while True and proc.stdout:
                    path = proc.stdout.readline().strip().decode()
                    if path == "NoOp":
                        break
                    else:
                        relpath = os.path.relpath(path, source)
                        files.append(relpath)
                if files:
                    with tempfile.NamedTemporaryFile(mode="w") as modified_files:
                        for f in files:
                            modified_files.write(f + "\n")
                        modified_files.flush()
                        command = " ".join(
                            [
                                "rsync",
                                "--rsh",
                                '"' + " ".join(ssh_command) + '"',
                                "-avz",
                                # TODO(pcm): This seems to not be supported on some versions
                                # of macOS. We might need to ship an up-to-date version of
                                # rsync to make it possible to have files deleted on the server.
                                # "--delete-missing-args",
                                "--files-from={}".format(modified_files.name),
                                source,
                                "ubuntu@{}:{}".format(head_ip, target),
                            ]
                        )
                        try:
                            logger.info("Calling rsync due to detected file update.")
                            logger.debug("Command: {command}".format(command=command))
                            subprocess.check_call(command, shell=True)
                        except Exception:
                            pass


@session_cli.command(name="auth_start", help="Start the auth proxy", hidden=True)
def auth_start() -> None:
    from aiohttp import web

    web.run_app(auth_proxy_app)


@click.command(name="stop", help="Stop the current session.")
@click.argument("session-name", required=False, default=None)
@click.option(
    "--terminate", help="Terminate the session instead of stopping it.", is_flag=True
)
@click.option(
    "--workers-only", is_flag=True, default=False, help="Only destroy the workers."
)
@click.option(
    "--keep-min-workers",
    is_flag=True,
    default=False,
    help="Retain the minimal amount of workers specified in the config.",
)
@click.pass_context
def anyscale_stop(
    ctx: Any,
    session_name: Optional[str],
    terminate: bool,
    workers_only: bool,
    keep_min_workers: bool,
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    sessions = get_project_sessions(project_id, session_name)

    if not session_name and len(sessions) > 1:
        raise click.ClickException(
            "Multiple active sessions: {}\n"
            "Please specify the one you want to stop with --session-name.".format(
                [session["name"] for session in sessions]
            )
        )

    for session in sessions:
        # Stop the session and mark it as stopped in the database.
        send_json_request(
            f"/api/v2/sessions/{session['id']}/stop",
            {
                "terminate": terminate,
                "workers_only": workers_only,
                "keep_min_workers": keep_min_workers,
            },
            method="POST",
        )

    session_names = [session["name"] for session in sessions]
    session_names_str = ", ".join(session_names)
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_names_str} stopping. View progress at {url}")


# Consolidate this once this https://github.com/anyscale/product/pull/497 gets merged.
def get_session_status(session: Any) -> str:
    status = ""
    if session["active"]:
        if session["starting_up"]:
            status = str(session["startup_progress"]).upper()
        else:
            status = "ACTIVE"
    else:
        if session["terminated"]:
            status = "TERMINATED"
        else:
            if session["stop_progress"] is not None:
                status = str(session["stop_progress"]).upper()
            else:
                status = "STOPPED"

    return status


def session_list_json(sessions: List[Any]) -> None:
    output = []
    for session in sessions:
        resp = send_json_request(
            "/api/v2/session_commands/?session_id={}".format(session["id"]), {}
        )
        record = {"name": session["name"]}
        commands = []
        is_session_idle = True
        for command in resp["results"]:
            if command["killed_at"] is not None:
                command_status = "KILLED"
            elif command["finished_at"] is not None:
                command_status = "FINISHED"
            else:
                command_status = "RUNNING"
                is_session_idle = False

            command_record = {
                "session_command_id": command["session_command_id"],
                "name": command["name"],
                "params": command["params"],
                "created_at": humanize_timestamp(
                    deserialize_datetime(command["created_at"])
                ),
                "status": command_status,
            }
            commands.append(command_record)

        status = get_session_status(session)
        if status == "ACTIVE":
            status = "IDLE" if is_session_idle else "TASK_RUNNING"
        record["status"] = status
        record["startup_error"] = session["startup_error"]
        record["stop_error"] = session["stop_error"]

        record["created_at"] = humanize_timestamp(
            deserialize_datetime(session["created_at"])
        )

        record["commands"] = commands
        output.append(record)

    print(json.dumps(output))


@list_cli.command(name="sessions", help="List all sessions within the current project.")
@click.option(
    "--name",
    help="Name of the session. If provided, this prints the snapshots that "
    "were applied and commands that ran for all sessions that match "
    "this name.",
    default=None,
)
@click.option("--all", help="List all sessions, including inactive ones.", is_flag=True)
@click.option("--json", "show_json", help="Return the results in json", is_flag=True)
def session_list(name: Optional[str], all: bool, show_json: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    resp = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name": name, "active_only": not all},
    )
    sessions = resp["results"]

    if show_json:
        session_list_json(sessions)
        sys.exit()

    print("Active project: " + project_definition.root)

    if name is None:
        print()
        table = []
        for session in sessions:
            created_at = humanize_timestamp(deserialize_datetime(session["created_at"]))
            if not session["snapshots_history"]:
                session["snapshots_history"].append("N/A")
            record = [
                session["name"],
                " {}".format(get_session_status(session)),
                created_at,
                session["snapshots_history"][0],
            ]
            if all:
                table.append([" Y" if session["active"] else " N"] + record)
            else:
                table.append(record)
        if not all:
            print(
                tabulate.tabulate(
                    table,
                    headers=["SESSION", "STATUS", "CREATED", "SNAPSHOT"],
                    tablefmt="plain",
                )
            )
        else:
            print(
                tabulate.tabulate(
                    table,
                    headers=["ACTIVE", "STATUS", "SESSION", "CREATED", "SNAPSHOT"],
                    tablefmt="plain",
                )
            )
    else:
        sessions = [session for session in sessions if session["name"] == name]
        for session in sessions:
            resp = send_json_request(
                "/api/v2/sessions/{}/describe".format(session["id"]), {}
            )

            print()
            snapshot_table = []
            for applied_snapshot in resp["result"]["applied_snapshots"]:
                snapshot_uuid = applied_snapshot["snapshot_uuid"]
                created_at = humanize_timestamp(
                    deserialize_datetime(applied_snapshot["created_at"])
                )
                snapshot_table.append([snapshot_uuid, created_at])
            print(
                tabulate.tabulate(
                    snapshot_table,
                    headers=[
                        "SNAPSHOT applied to {}".format(session["name"]),
                        "APPLIED",
                    ],
                    tablefmt="plain",
                )
            )

            print()
            command_table = []
            for command in resp["result"]["commands"]:
                created_at = humanize_timestamp(
                    deserialize_datetime(command["created_at"])
                )
                command_table.append(
                    [
                        " ".join(
                            [command["name"]]
                            + [
                                "{}={}".format(key, val)
                                for key, val in command["params"].items()
                            ]
                        ),
                        command["session_command_id"],
                        created_at,
                    ]
                )
            print(
                tabulate.tabulate(
                    command_table,
                    headers=[
                        "COMMAND run in {}".format(session["name"]),
                        "ID",
                        "CREATED",
                    ],
                    tablefmt="plain",
                )
            )


@click.command(name="pull", help="Pull session")
@click.argument("session-name", type=str, required=False, default=None)
@click.confirmation_option(
    prompt="Pulling a session will override the local project directory. Do you want to continue?"
)
def anyscale_pull_session(session_name: str) -> None:

    project_definition = load_project_or_throw()

    try:
        print("Collecting files from remote.")
        project_id = get_project_id(project_definition.root)
        directory_name = get_project_directory_name(project_id)
        source_directory = "~/{}/".format(directory_name)

        cluster_config = get_cluster_config(session_name, "")
        cluster_config = fillout_defaults(cluster_config)
        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            json.dump(cluster_config, config_file)
            config_file.flush()
            rsync(
                config_file.name,
                source_directory,
                project_definition.root,
                None,
                down=True,
            )
        print("Pull completed.")

    except Exception as e:
        raise click.ClickException(e)  # type: ignore


@click.command(name="pull-snapshot", help="Pull snapshot", hidden=True)
@click.argument("snapshot-id", type=str, required=False, default=None)
@click.confirmation_option(
    prompt="Pulling a snapshot will override the local project directory. Do you want to continue?"
)
def anyscale_pull_snapshot(snapshot_id: str) -> None:

    project_definition = load_project_or_throw()

    try:
        snapshots = list_snapshots(project_definition.root)
        if not snapshot_id:
            snapshot_id = snapshots[0]
            print("Pulling latest snapshot: {}".format(snapshot_id))
        elif snapshot_id not in snapshots:
            raise click.ClickException(
                "Snapshot {0} not found in project {1}".format(
                    snapshot_id, project_definition.config["name"]
                )
            )

        print("Collecting files from remote.")
        resp = send_json_request("/api/v2/users/temporary_aws_credentials", {})
        print("Downloading files.")
        download_snapshot(
            snapshot_id,
            resp["result"],
            os.path.abspath(project_definition.root),
            overwrite=True,
        )
    except Exception as e:
        raise click.ClickException(e)  # type: ignore


@click.command(name="push", help="Push current project to session.")
@click.argument("session-name", type=str, required=False, default=None)
@click.option(
    "--snapshot-id",
    help="Synchronize session with this snapshot rather than taking a new one of the current project.",
    default=None,
)
@click.option(
    "--apply-config",
    is_flag=True,
    default=False,
    help="Take a snapshot and update the cluster if the cluster configuration changes.",
)
def anyscale_push_session(
    session_name: str, snapshot_id: Optional[str], apply_config: bool
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)
    session_name = session["name"]

    cluster_config = get_cluster_config(session_name, "")
    cluster_config = update_file_mounts(cluster_config, project_definition)
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name, None, None, None, down=False, all_nodes=True,
        )

    if apply_config:
        resp = send_json_request(
            "/api/v2/sessions/{session_id}/take_snapshot".format(
                session_id=session["id"]
            ),
            {"additional_files": [], "files_only": False},
            method="POST",
        )
        snapshot_uuid: str = resp["result"]["id"]

        send_json_request(
            "/api/v2/sessions/{session_id}/sync".format(session_id=session["id"]),
            {"snapshot_id": snapshot_uuid},
            method="POST",
        )

    url = get_endpoint(f"/projects/{project_id}")
    print(f"Pushed to session {session_name}. View at {url}")


@click.command(
    name="push-snapshot",
    help="Create a snapshot of the current project and push to anyscale.",
    hidden=True,
)
@click.option("--description", help="A description of the snapshot", default=None)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--include-output-files",
    is_flag=True,
    default=False,
    help="Include output files with the snapshot",
)
@click.option(
    "--tag",
    type=str,
    help="Tag for this snapshot. Multiple tags can be specified by repeating this option.",
    multiple=True,
)
def anyscale_push_snapshot(
    description: Optional[str], yes: bool, include_output_files: bool, tag: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    # Create a local snapshot.
    try:
        snapshot_id = create_snapshot(
            project_definition,
            yes,
            description=description,
            include_output_files=include_output_files,
            additional_files=[],
            files_only=False,
            tags=tag,
        )
    except click.Abort as e:
        raise e
    except Exception as e:
        # Creating a snapshot can fail if the project is not found or
        # if some files cannot be copied (e.g., due to permissions).
        raise click.ClickException(e)  # type: ignore

    url = get_endpoint(f"/projects/{project_id}")
    print(f"Snapshot {snapshot_id} pushed. View at {url}")


@click.command(
    name="clone",
    short_help="Clone a project that exists on anyscale, to your local machine.",
    help="""Clone a project that exists on anyscale, to your local machine.
This command will create a new folder on your local machine inside of
the current working directory and download the most recent snapshot.

This is frequently used with anyscale push or anyscale pull to download, make
changes, then upload those changes to a currently running session.""",
)
@click.argument("project-name", required=True)
def anyscale_clone(project_name: str) -> None:
    resp = send_json_request("/api/v2/projects/", {})
    project_names = [p["name"] for p in resp["results"]]
    project_ids = [p["id"] for p in resp["results"]]

    if project_name not in project_names:
        raise click.ClickException(
            "No project with name {} found.".format(project_name)
        )
    project_id = project_ids[project_names.index(project_name)]

    os.makedirs(project_name)
    clone_files(project_name, project_name, project_id)


def clone_files(project_name: str, directory: str, project_id: int) -> None:
    if check_is_feature_flag_on(FLAG_KEY_USE_SNAPSHOT):
        os.makedirs(os.path.join(directory, "ray-project"))
        with open("{}/ray-project/project-id".format(directory), "w") as f:
            f.write("{}".format(project_id))

        snapshots = list_snapshots(os.path.abspath(project_name))
        snapshot_id = snapshots[-1]

        try:
            resp = send_json_request("/api/v2/users/temporary_aws_credentials", {})
            print(f'Downloading snapshot "{snapshot_id}"')
            download_snapshot(
                snapshot_id, resp["result"], os.path.abspath(directory), overwrite=True,
            )
        except Exception as e:
            raise click.ClickException(e)  # type: ignore
    else:
        with open("{}/{}".format(directory, ANYSCALE_PROJECT_FILE), "w") as f:
            f.write("{}".format("project_id: {}".format(project_id)))

        sessions_resp = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id}
        )
        sessions = sessions_resp["results"]

        if len(sessions) > 0:
            lastest_session = sessions[0]

            cluster_config_resp = send_json_request(
                "/api/v2/sessions/{}/cluster_config".format(lastest_session["id"]), {}
            )
            cluster_config = cluster_config_resp["result"]["config"]
        else:
            cluster_config = CLUSTER_YAML_TEMPLATE

        with open("{}/{}".format(directory, ANYSCALE_AUTOSCALER_FILE), "w") as f:
            f.write(cluster_config)


def write_ssh_key(key_name: str, key_val: str, file_dir: str = "~/.ssh") -> str:
    file_dir = os.path.expanduser(file_dir)
    os.makedirs(file_dir, exist_ok=True)
    key_path = os.path.join(file_dir, "{}.pem".format(key_name))
    if not os.path.exists(key_path):
        with open(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o600), "w") as f:
            f.write(key_val)
    return key_path


@click.command(name="ssh", help="SSH into head node of cluster.")
@click.argument("session-name", type=str, required=False, default=None)
def anyscale_ssh(session_name: str) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)
    head_ip, key_path = setup_ssh_for_head_node(session["id"])

    cluster_config = get_cluster_config(session_name)
    container_name = cluster_config.get("docker", {}).get("container_name")

    # TODO(ilr) Convert this "ubuntu" to "{config[auth_user][ssh_user]}""
    subprocess.run(
        [
            "ssh",
            "-tt",
            "-i",
            key_path,
            "ubuntu@{}".format(head_ip),
            f"docker exec -it {container_name} sh -c 'which bash && bash || sh'"
            if container_name
            else "",
        ]
    )


def get_cluster_config(
    session_name: Optional[str] = None, cluster_config_file: Optional[str] = None
) -> Any:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)
    if not cluster_config_file:
        cluster_config_file = project_definition.config["cluster"]["config"]
    cluster_config_file = cast(str, cluster_config_file)
    cluster_config: Dict[str, Any] = defaultdict(dict)
    cluster_config.update(yaml.safe_load(open(cluster_config_file).read()))
    resp = send_json_request("/api/v2/sessions/{}/details".format(session["id"]), {})
    cluster_config["cluster_name"] = resp["result"]["cluster_name"]
    # Get temporary AWS credentials for the autoscaler.
    resp = send_json_request(
        "/api/v2/sessions/{}/autoscaler_credentials".format(session["id"]), {}
    )
    cluster_config["provider"].update(
        {"aws_credentials": resp["result"]["credentials"]}
    )
    # Get the SSH key from the session.
    resp = send_json_request("/api/v2/sessions/{}/ssh_key".format(session["id"]), {})
    key_name = resp["result"]["key_name"]
    private_key = resp["result"]["private_key"]
    # Write key to .ssh folder.
    key_path = write_ssh_key(key_name, private_key)
    # Store key in autoscaler cluster config.
    cluster_config["auth"]["ssh_private_key"] = key_path
    cluster_config["head_node"]["KeyName"] = key_name
    cluster_config["worker_nodes"]["KeyName"] = key_name

    return cluster_config


@cli.command(name="rsync-down", help="Download specific files from cluster.")
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
def anyscale_rsync_down(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"], "")
    cluster_config = fillout_defaults(cluster_config)
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(config_file.name, source, target, cluster_name, down=True)


@cli.command(name="rsync-up", help="Upload specific files to cluster.")
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Upload to all nodes (workers and head).",
)
def anyscale_rsync_up(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
    all_nodes: bool,
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"], "")
    cluster_config = fillout_defaults(cluster_config)
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name,
            source,
            target,
            cluster_name,
            down=False,
            all_nodes=all_nodes,
        )


cli.add_command(project_cli)
cli.add_command(session_cli)
cli.add_command(snapshot_cli)
cli.add_command(cloud_cli)
cli.add_command(version_cli)
cli.add_command(list_cli)


@click.group("ray", help="Open source Ray commands.")
@click.pass_context
def ray_cli(ctx: Any) -> None:
    subcommand = autoscaler_scripts.cli.commands[ctx.invoked_subcommand]
    # Replace the cluster_config_file argument with a session_name argument.
    if subcommand.params[0].name == "cluster_config_file":
        subcommand.params[0] = click.Argument(["session_name"])

    original_autoscaler_callback = copy.deepcopy(subcommand.callback)

    if "--help" not in sys.argv and ctx.invoked_subcommand in ["up", "down"]:
        args = sys.argv[3:]

        if ctx.invoked_subcommand == "up":
            old_command = "anyscale ray up {}".format(" ".join(args))
            new_command = "anyscale start --cluster-config-file {}".format(
                " ".join(args)
            )
        else:
            old_command = "anyscale ray down {}".format(" ".join(args))
            new_command = "anyscale stop SESSION_NAME {}".format(" ".join(args[1:]))

        print(
            "\033[91m\nYou called\n  {}\nInstead please call\n  {}\033[00m".format(
                old_command, new_command
            )
        )

        sys.exit()

    def autoscaler_callback(*args: Any, **kwargs: Any) -> None:
        try:
            if "session_name" in kwargs:
                # Get the cluster config. Use kwargs["session_name"] as the session name.
                cluster_config = get_cluster_config(kwargs["session_name"])
                del kwargs["session_name"]
                with tempfile.NamedTemporaryFile(mode="w") as config_file:
                    json.dump(cluster_config, config_file)
                    config_file.flush()
                    kwargs["cluster_config_file"] = config_file.name
                    original_autoscaler_callback(*args, **kwargs)
            else:
                original_autoscaler_callback(*args, **kwargs)
        except Exception as e:
            raise click.ClickException(e)  # type: ignore

    subcommand.callback = autoscaler_callback


def install_autoscaler_shims(ray_cli: Any) -> None:
    for name, command in autoscaler_scripts.cli.commands.items():
        if isinstance(command, click.core.Group):
            continue
        ray_cli.add_command(command, name=name)


@click.command(name="exec", help="Execute shell commands in interactive session.")
@click.option(
    "--session-name",
    "-n",
    type=str,
    required=False,
    default=None,
    help="Session name optional if only one running session.",
)
@click.option(
    "--screen", is_flag=True, default=False, help="Run the command in a screen."
)
@click.option("--tmux", is_flag=True, default=False, help="Run the command in tmux.")
@click.option(
    "--port-forward",
    "-p",
    required=False,
    multiple=True,
    type=int,
    help="Port to forward. Use this multiple times to forward multiple ports.",
)
@click.option(
    "--sync",
    is_flag=True,
    default=False,
    help="Rsync all the file mounts before executing the command.",
)
@click.argument("commands", nargs=-1, type=str)
def anyscale_exec(
    session_name: str,
    screen: bool,
    tmux: bool,
    port_forward: Tuple[int],
    sync: bool,
    commands: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)

    session_name = session["name"]

    # Create a placeholder session command ID
    resp = send_json_request(
        "/api/v2/sessions/{}/execute_interactive_command".format(session["id"]),
        {"shell_command": " ".join(commands)},
        method="POST",
    )
    session_command_id = resp["result"]["command_id"]
    directory_name = resp["result"]["directory_name"]

    # Save the PID of the command so we can kill it later.
    shell_command_prefix = (
        "echo $$ > {execution_log_name}.pid; "
        "export ANYSCALE_HOST={anyscale_host}; "
        "export ANYSCALE_SESSION_COMMAND_ID={session_command_id}; ".format(
            execution_log_name=execution_log_name(session_command_id),
            anyscale_host=anyscale.conf.ANYSCALE_HOST,
            session_command_id=session_command_id,
        )
    )

    # Note(simon): This section is largely similar to the server side exec command but simpler.
    # We cannot just use the server command because we need to buffer the output to
    # user's terminal as well and handle interactivity.
    redirect_to_dev_null = "&>/dev/null"
    shell_command = shell_command_prefix + " ".join(commands)
    remote_command = (
        "touch {execution_log_name}.out; "
        "touch {execution_log_name}.err; "
        "cd ~/{directory_name}; "
        "script -q -e -f -c {shell_command} {execution_log_name}.out; "
        "echo $? > {execution_log_name}.status; "
        "ANYSCALE_HOST={anyscale_host} anyscale session "
        "upload_command_logs --command-id {session_command_id} {redirect_to_dev_null}; "
        "ANYSCALE_HOST={anyscale_host} anyscale session "
        "finish_command --command-id {session_command_id} {stop_cmd} {redirect_to_dev_null}".format(
            directory_name=directory_name,
            execution_log_name=(execution_log_name(session_command_id)),
            anyscale_host=anyscale.conf.ANYSCALE_HOST,
            session_command_id=session_command_id,
            stop_cmd="",
            shell_command=quote(shell_command),
            redirect_to_dev_null=redirect_to_dev_null,
        )
    )

    cluster_config = get_cluster_config(session_name)
    cluster_config = fillout_defaults(cluster_config)

    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        config_file_path = config_file.name

        # Rsync file mounts if sync flag is set
        if sync:
            rsync(
                config_file.name, None, None, None, down=False, all_nodes=True,
            )

        # Suppress autoscaler logs, we don't need to show these to user
        ray.logger.setLevel(logging.ERROR)
        exec_cluster(
            config_file_path,
            cmd=remote_command,
            screen=screen,
            tmux=tmux,
            port_forward=[(port, port) for port in list(port_forward)],
        )

    if tmux or screen:
        launched_in_mode = "tmux" if tmux else "screen"
        # TODO(simon): change the message to anyscale attach when implemented
        click.echo(
            "Command launched in {mode}, use `anyscale ray attach {name} --{mode}` to check status.".format(
                mode=launched_in_mode, name=session_name
            )
        )


@list_cli.command(name="ips", help="List IP addresses of head and worker nodes.")
@click.argument("session-name", required=False, type=str)
@click.option("--json", "show_json", help="Return the results in json", is_flag=True)
@click.option(
    "--all", "all_sessions", help="List IPs of all active sessions.", is_flag=True
)
def list_ips(session_name: Optional[str], show_json: bool, all_sessions: bool) -> None:
    """List IP addresses of head and worker nodes."""
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if all_sessions:
        sessions = get_project_sessions(project_id, session_name)
        sessions = [session["name"] for session in sessions]
    else:
        sessions = [get_project_session(project_id, session_name)["name"]]

    output_json = []
    output_table = []
    for name in sessions:
        cluster_config = get_cluster_config(name, "")
        cluster_config = fillout_defaults(cluster_config)
        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            json.dump(cluster_config, config_file)
            config_file.flush()
            head_ip = get_head_node_ip(config_file.name, None)
            worker_ips = get_worker_node_ips(config_file.name, None)
        if show_json:
            output_json.append(
                {"session-name": name, "head-ip": head_ip, "worker-ips": worker_ips}
            )
        else:
            output_table.append([name, head_ip, "head"])
            for worker_ip in worker_ips:
                output_table.append([name, worker_ip, "worker"])

    if show_json:
        print(json.dumps(output_json))
    else:
        print(
            tabulate.tabulate(
                output_table,
                headers=["SESSION", "IP ADDRESS", "NODE TYPE"],
                tablefmt="plain",
            )
        )


install_autoscaler_shims(ray_cli)
cli.add_command(ray_cli)

cli.add_command(anyscale_init)
cli.add_command(anyscale_run)
cli.add_command(anyscale_start)
cli.add_command(anyscale_up)
cli.add_command(anyscale_stop)
cli.add_command(anyscale_cloudgateway)
cli.add_command(anyscale_autosync)
cli.add_command(anyscale_clone)
cli.add_command(anyscale_ssh)
cli.add_command(anyscale_rsync_down)
cli.add_command(anyscale_rsync_up)
cli.add_command(anyscale_exec)
cli.add_command(anyscale_push_session)
cli.add_command(anyscale_push_snapshot)
cli.add_command(anyscale_pull_session)
cli.add_command(anyscale_pull_snapshot)


def main() -> Any:
    return cli()


if __name__ == "__main__":
    main()
