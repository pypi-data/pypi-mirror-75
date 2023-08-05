import json
import click
from tinydb import TinyDB
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth 
from cli.database import Database
from wowpy.mappings import Mapper

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""

# TODO: Create a map all, taking into account some resources like targets and recordings will be null

@click.group()
def mapper():
    """
    Mapping of ids to resource names
    """
    pass


@mapper.command(name='live_streams')
@exception_handler
def live_streams():
    """Map live stream ids with resource names"""
    wowza_auth()
    document_batch = Mapper.map_live_streams()
    database = Database()
    database.insert_live_stream_mappings(document_batch)
    click.echo('Mapping of live stream ids with resource names done')

@mapper.command(name='recordings')
@exception_handler
def recordings():
    """Map recording ids with resource names"""
    wowza_auth()
    document_batch = Mapper.map_recordings()
    database = Database()
    database.insert_recording_mappings(document_batch)
    click.echo('Mapping of recording ids with resource names done')
