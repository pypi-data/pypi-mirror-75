import click

from .. import config as grvlms_config
from .. import env as grvlms_env
from .. import fmt
from .. import interactive as interactive_config
from .. import scripts
from .. import utils


@click.group(help="Docker Operations")
def docker():
    pass

@click.command(help="Configure and create infrastructure")
@click.pass_obj
@click.option("-I", "--non-interactive", is_flag=True, help="Run non-interactively")
def login(context, non_interactive):
    user = context.user
    cred = context.remote_config["ecrAdmin"] if user["role"] == "admin" else context.remote_config["ecrRead"]
    config = grvlms_config.load(context.root)
    if config["DOCKER_USE_AWS_ECR"]:
        click.echo(fmt.title("Generating command for docker login"))
        utils.aws(
            cred["id"],
            cred["key"],
            "grvlms-aws-registry",
            "ecr",
            "get-login",
            "--no-include-email",
            "--region",
            config["ECR_REGISTRY_REGION"]
        )
        click.echo(fmt.title("Please copy and run command above"))
    else:
        utils.docker("login")


docker.add_command(login) 