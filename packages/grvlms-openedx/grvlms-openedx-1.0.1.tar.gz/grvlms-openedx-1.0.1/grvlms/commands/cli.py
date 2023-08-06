#! /usr/bin/env python3
import os
import sys

import appdirs
import click
import click_repl
from collections import namedtuple

from .android import android
from .config import config_command
from .context import Context
from .dev import dev
from .images import images_command
from .k8s import k8s
from .local import local
from .plugins import plugins_command, add_plugin_commands
from .ui import ui
from .webui import webui
from .docker import docker
from ..__about__ import __version__
from .. import exceptions
from .. import fmt
from .. import firebase_rdb
from uuid import getnode as get_mac

user = None
remote_config = None

def main():
    try:
        cli() # pylint: disable=no-value-for-parameter
    except exceptions.GrvlmsError as e:
        fmt.echo_error(click.style("Error: {}".format(e.args[0]), fg='red'))
        sys.exit(1)

def get_user():
    user = None
    mac = hex(get_mac())
    err_msg = "\n\nSORRY! We can not verify your agent.\n\nPlease contact the admin, tell him about your ID is " + mac + "\n\n"
    try:
        users = firebase_rdb.get("users")
        if users[mac]:
            user = users[mac]
        else:
            fmt.echo_error(err_msg)
    except:
        fmt.echo_error(err_msg)
    return user

def check_allow_version():
    is_allow = False
    err_msg = "\n\nSORRY! Your Cli version (v{}) will no longer support. Please upgrade to latest version\n\n".format(__version__)
    try:
        versions = firebase_rdb.get("versions")
        if __version__ in versions:
            is_allow = True
        else:
            fmt.echo_error(err_msg)
            sys.exit(1)
    except:
        fmt.echo_error(err_msg)
        sys.exit(1)
    return is_allow

def get_remote_config():
    remote_config = None
    err_msg = "\n\nSORRY! We can not get remote configuration. Please try again\n\n"
    try:
        remote_config = firebase_rdb.get("config") # pylint: disable=unused-variable
    except:
        fmt.echo_error(err_msg)
    return remote_config


@click.command(help="Print version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")

@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
@click.version_option(version=__version__)
@click.option(
    "-r",
    "--root",
    envvar="GRVLMS_ROOT",
    default=appdirs.user_data_dir(appname="grvlms"),
    show_default=True,
    type=click.Path(resolve_path=True),
    help="Root project directory (environment variable: GRVLMS_ROOT)",
)
@click.pass_context
def cli(context, root):
    if os.getuid() == 0:
        fmt.echo_alert(
            "You are running Grvlms as root. This is strongly not recommended. If you are doing this in order to access the Docker daemon, you should instead add your user to the 'docker' group. (see https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user)"
        )
    context.obj = Context(root, user, remote_config)


@click.command(help="Print this help", name="help")
def print_help():
    with click.Context(cli) as context:
        click.echo(cli.get_help(context))

try:
    is_allow_version = check_allow_version()
    user = get_user()
    remote_config = get_remote_config()
    if user and is_allow_version and remote_config:
        role = user["role"]

        click_repl.register_repl(cli, name="ui")
        cli.add_command(print_version)

        if role == "admin":
            cli.add_command(images_command)
            cli.add_command(k8s)

    cli.add_command(config_command)
    cli.add_command(local)
    cli.add_command(dev)
    # cli.add_command(android)
    cli.add_command(ui)
    cli.add_command(webui)
    cli.add_command(print_help)
    cli.add_command(plugins_command)
    cli.add_command(docker)
    add_plugin_commands(cli)
except:
    fmt.echo_alert('Oh stopped')
    sys.exit(1)

if __name__ == "__main__":
    main()
