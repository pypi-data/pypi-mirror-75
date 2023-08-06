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
from wowpy.livestreams import LiveStream

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def live():
    """
    Live Stream commands.
    """
    pass


@live.command(name='query')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def query(id, name):
    """Get data for a Live Stream"""
    wowza_auth()
    if name:
        database = Database()
        if not database.live_streams_table_exist():
            click.echo('In order to use --name parameter please run: wowtool mapper live_streams, first')
            sys.exit()

        id = database.get_live_stream_id_from_name(name)
        if not id:
            click.echo('Live stream not found in current mapping table')
            sys.exit()
    response = LiveStream.get_live_stream(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)

@live.command(name='start')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def start(id, name):
    """Start a Live Stream"""
    wowza_auth()
    LiveStream.start_live_stream(id)
    click.echo('Live Stream started')

@live.command(name='stop')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def stop(id, name):
    """Stop a Live Stream"""
    wowza_auth()
    LiveStream.stop_live_stream(id)
    click.echo('Live Stream stopped')

@live.command(name='state')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def state(id, name):
    """Get state for a Live Stream"""
    wowza_auth()
    state = LiveStream.get_state(id)
    click.echo('Live Stream state is {0}'.format(state))
