#!/usr/bin/env python
import pprint
import sys

import click

import slack
from slack.errors import SlackApiError

import ci_buildbot
from .settings import Settings
from .messages import (
    ArchiveCodeMessage,
    DockerFailureMessage,
    DockerStartMessage,
    DockerSuccessMessage,
    DeployfishDeployFailureMessage,
    DeployfishDeployStartMessage,
    DeployfishDeploySuccessMessage,
    DeployfishTasksDeployFailureMessage,
    DeployfishTasksDeployStartMessage,
    DeployfishTasksDeploySuccessMessage
)


@click.group(invoke_without_command=True)
@click.option('--version/--no-version', '-v', default=False, help="Print the current version and exit.")
@click.pass_context
def cli(ctx, version):
    """
    buildbot command line interaface.
    """

    ctx.obj['settings'] = Settings()
    ctx.obj['slack'] = slack.WebClient(token=ctx.obj['settings'].api_token)

    if version:
        print(ci_buildbot.__version__)
        sys.exit(0)


@cli.command('settings', short_help="Print our application settings.")
@click.pass_context
def settings(ctx):
    """
    Print our settings to stdout.  This should be the completely evaluated settings including
    those imported from any environment variable.
    """
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ctx.obj['settings'].dict())


@cli.command('channels', short_help="Print our available channels.")
@click.pass_context
def channels(ctx):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ctx.obj['slack'].conversations_list(types="private_channel")['channels'])


@cli.group('report', short_help="Report about a build step")
def report():
    pass


@report.command('archive', short_help="Report about an archive-to-code-drop step")
@click.pass_context
def archive(ctx):
    blocks = ArchiveCodeMessage().format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report.group('docker', short_help="A group of commands that report about a Docker bmage build step")
def report_docker():
    pass


@report_docker.command('start', short_help="Report about starting a docker build")
@click.argument('image')
@click.pass_context
def report_docker_start(ctx, image):
    blocks = DockerStartMessage(image=image).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_docker.command('success', short_help="Report a successful docker build")
@click.argument('image')
@click.pass_context
def report_docker_success(ctx, image):
    blocks = DockerSuccessMessage(image=image).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_docker.command('failure', short_help="Report a failed docker build")
@click.argument('image')
@click.pass_context
def report_docker_failure(ctx, image):
    blocks = DockerFailureMessage(image=image).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report.group('deployfish', short_help="A group of commands that report about a Deployfish service build step")
def report_deployfish():
    pass


@report_deployfish.command('start', short_help="Report about starting a deployfish service deploy")
@click.argument('service')
@click.pass_context
def report_deployfish_start(ctx, service):
    blocks = DeployfishDeployStartMessage(service=service).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_deployfish.command('success', short_help="Report a successful deployfish service deploy")
@click.argument('service')
@click.pass_context
def report_deployfish_success(ctx, service):
    blocks = DeployfishDeploySuccessMessage(service=service).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_deployfish.command('failure', short_help="Report a failed deployfish service deploy")
@click.argument('service')
@click.pass_context
def report_deployfish_failure(ctx, service):
    blocks = DeployfishDeployFailureMessage(service=service).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report.group(
    'deployfish-tasks',
    short_help="A group of commands that report about a Deployfish one-off tasks build step"
)
def report_deployfish_tasks():
    pass


@report_deployfish_tasks.command('start', short_help="Report about starting a deployfish one-off tasks deploy")
@click.argument('tasks', nargs=-1, required=True)
@click.pass_context
def report_deployfish_tasks_start(ctx, tasks):
    blocks = DeployfishTasksDeployStartMessage(tasks=tasks).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_deployfish_tasks.command('success', short_help="Report a successful deployfish one-off tasks deploy")
@click.argument('tasks', nargs=-1, required=True)
@click.pass_context
def report_deployfish_tasks_success(ctx, tasks):
    blocks = DeployfishTasksDeploySuccessMessage(tasks=tasks).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


@report_deployfish_tasks.command('failure', short_help="Report a failed deployfish one-off tasks deploy")
@click.argument('tasks', nargs=-1, required=True)
@click.pass_context
def report_deployfish_tasks_failure(ctx, tasks):
    blocks = DeployfishTasksDeployFailureMessage(tasks=tasks).format()
    client = ctx.obj['slack']
    try:
        client.chat_postMessage(
            channel=ctx.obj['settings'].channel,
            blocks=blocks,
            as_user=True
        )
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")

def main():
    cli(obj={})


if __name__ == '__main__':
    main()
