import click

from .. import config as grvlms_config
from .. import env as grvlms_env
from .. import fmt
from .. import utils


@click.group(help="Build an Android app for your Open edX platform [BETA FEATURE]")
def android():
    pass


@click.group(help="Build the application")
def build():
    pass


@click.command(help="Build the application in debug mode")
@click.pass_obj
def debug(context):
    docker_run(context.root)
    fmt.echo_info(
        "The debuggable APK file is available in {}".format(
            grvlms_env.data_path(context.root, "android")
        )
    )


@click.command(help="Build the application in release mode")
@click.pass_obj
def release(context):
    docker_run(context.root, "./gradlew", "assembleProdRelease")
    fmt.echo_info(
        "The production APK file is available in {}".format(
            grvlms_env.data_path(context.root, "android")
        )
    )


@click.command(help="Pull the docker image")
@click.pass_obj
def pullimage(context):
    config = grvlms_config.load(context.root)
    utils.execute("docker", "pull", config["DOCKER_IMAGE_ANDROID"])


def docker_run(root, *command):
    config = grvlms_config.load(root)
    utils.docker_run(
        "--volume={}:/openedx/config/".format(grvlms_env.pathjoin(root, "android")),
        "--volume={}:/openedx/data/".format(grvlms_env.data_path(root, "android")),
        config["DOCKER_IMAGE_ANDROID"],
        *command
    )


build.add_command(debug)
build.add_command(release)
android.add_command(build)
android.add_command(pullimage)
