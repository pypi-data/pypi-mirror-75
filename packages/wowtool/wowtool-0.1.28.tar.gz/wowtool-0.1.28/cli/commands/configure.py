import click
import json
import os
from pathlib import Path
from cli.utils import exception_handler, wowza_auth, credentials_file_exist

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group(invoke_without_command=True)
def configure():
    """
    Setup credentials file.
    """

    if credentials_file_exist():
        if click.confirm('Credentials file already exist, override?'):
            wowza_auth()
            click.echo('Credentials file successfully created!')
    else: 
        wowza_auth()
        click.echo('Credentials file successfully created!')
