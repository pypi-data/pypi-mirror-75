import os

import click

from . import compose
from .context import Context
from .. import env as grvlms_env
from .. import fmt
from .. import utils

# pylint: disable=too-few-public-methods
class DevContext(Context):
    @staticmethod
    def docker_compose(root, config, *command):
        args = [
            "-f",
            grvlms_env.pathjoin(root, "local", "docker-compose.yml"),
        ]
        override_path = grvlms_env.pathjoin(root, "local", "docker-compose.override.yml")
        if os.path.exists(override_path):
            args += ["-f", override_path]
        args += [
            "-f",
            grvlms_env.pathjoin(root, "dev", "docker-compose.yml"),
        ]
        override_path = grvlms_env.pathjoin(root, "dev", "docker-compose.override.yml")
        if os.path.exists(override_path):
            args += ["-f", override_path]
        return utils.docker_compose(
            *args, "--project-name", config["DEV_PROJECT_NAME"], *command,
        )


@click.group(help="Run Open edX locally with development settings")
@click.pass_context
def dev(context):
    context.obj = DevContext(context.obj.root, context.obj.user, context.obj.remote_config)


@click.command(
    help="Run a development server", context_settings={"ignore_unknown_options": True},
)
@click.argument("options", nargs=-1, required=False)
@click.argument("service")
def runserver(options, service):
    if service in ["lms", "cms"]:
        port = 8000 if service == "lms" else 8001
        fmt.echo_info(
            "The {} service will be available at http://lms.local.groove.education:{}".format(
                service, port
            )
        )
    args = [
        "--service-ports", *options, service]
    compose.run.callback(args)


dev.add_command(runserver)
compose.add_commands(dev)
