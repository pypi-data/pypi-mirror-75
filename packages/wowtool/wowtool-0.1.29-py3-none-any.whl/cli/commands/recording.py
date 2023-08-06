import json
import sys
import click
from tinydb import TinyDB, Query
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth
from cli.database import Database
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter
from wowpy.recordings import Recording

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def recording():
    """
    Recording commands.
    """
    pass


@recording.command(name='query')
@optgroup.group('Recording identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza recording')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def query(id, name):
    """Get Recording"""
    wowza_auth()
    if name:
        database = Database()
        if not database.recordings_table_exist():
            click.echo('In order to use --name parameter please run: wowtool mapper recordings, first')
            sys.exit()

        id = database.get_recording_id_from_name(name)
        if not id:
            click.echo('Recording not found in current mapping table')
            sys.exit()
    response = Recording.get_recording(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)
