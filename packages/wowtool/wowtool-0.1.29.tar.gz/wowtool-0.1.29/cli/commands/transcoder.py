import json
import click
import sys
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from wowpy.transcoders import Transcoder
from cli.utils import exception_handler, wowza_auth
from cli.database import Database
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def trans():
    """
    Transcoder commands.
    """
    pass


@trans.command(name='query')
@optgroup.group('Transcoder identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza transcoder')
@optgroup.option('--id', help='Transcoder id')
@optgroup.option('--name', help='Transcoder name')
@exception_handler
def query(id, name):
    """Get data for a Transcoder"""
    wowza_auth()
    if name:
        database = Database()
        if not database.live_streams_table_exist():
            click.echo('In order to use --name parameter please run: wowtool mapper live_streams (this maps also transcoders), first')
            sys.exit()

        id = database.get_live_stream_id_from_name(name)
        if not id:
            click.echo('Transcoder not found in current mapping table')
            sys.exit()
    response = Transcoder.get_transcoder(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)

@trans.command(name='start')
@optgroup.group('Transcoder identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza transcoder')
@optgroup.option('--id', help='Transcoder id')
@optgroup.option('--name', help='Transcoder name')
@exception_handler
def start(id, name):
    """Start a Transcoder"""
    wowza_auth()
    Transcoder.start_transcoder(id)
    click.echo('Transcoder started')

@trans.command(name='stop')
@optgroup.group('Transcoder identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza transcoder')
@optgroup.option('--id', help='Transcoder id')
@optgroup.option('--name', help='Transcoder name')
@exception_handler
def stop(id, name):
    """Stop a Transcoder"""
    wowza_auth()
    Transcoder.stop_transcoder(id)
    click.echo('Transcoder stopped')

@trans.command(name='reset')
@optgroup.group('Transcoder identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza transcoder')
@optgroup.option('--id', help='Transcoder id')
@optgroup.option('--name', help='Transcoder name')
@exception_handler
def reset(id, name):
    """Reset a Transcoder"""
    wowza_auth()
    Transcoder.reset_transcoder(id)
    click.echo('Transcoder reset')