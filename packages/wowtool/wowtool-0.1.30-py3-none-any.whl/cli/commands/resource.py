import json
import click
import sys
import yaml
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth, display_message
from cli.database import Database
from wowpy.resources import get_resource_info
from wowpy.resources import validate_resource, create_resource, delete_resource, update_resource
from wowpy.utils import compare_specs, clean_changes
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def resource():
    """
    Resource commands.
    """
    pass


@resource.command(name='create')
@click.option('--spec-file', '-f', required=True, type=click.File(lazy=False),
              help='File that contains your streaming resource specification')
@exception_handler
def create(spec_file):
    """Create streaming resource"""
    specification = yaml.load(spec_file, Loader=yaml.SafeLoader)
    valid = validate_resource(specification)
    if not valid:
        click.echo('The specification template is invalid')
    else:
        click.echo('The specification template is valid')
        
    wowza_auth()
    database = Database()
    
    resource_name = specification['name']
    stored_specification = database.get_specification_by_name(resource_name)
    if stored_specification:
        click.echo('Specification already exist for the resource')
        # TODO: Show changes, Ask to continue
        sys.exit()

    response = create_resource(specification)
    database.insert_specification(response)
    document = {
        'live_stream_name': response['name'],
        'live_stream_id': response['id']
    }
    database.insert_live_stream_mapping(document)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)


@resource.command(name='delete')
@optgroup.group('Resource identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for resource')
@optgroup.option('--id', help='Resource stream id')
@optgroup.option('--name', help='Resource stream name')
@exception_handler
def delete(id, name):
    """Delete streaming resource"""  
    wowza_auth()
    database = Database()
    if name:   
        if not database.live_streams_table_exist():
            click.echo('In order to use --name parameter please run: wowtool mapper live_streams, first')
            sys.exit()

        id = database.get_live_stream_id_from_name(name)
        if not id:
            click.echo('Live stream not found in current mapping table')
            sys.exit()
    
    stored_specification = database.get_specification_by_id(id)
    if not stored_specification:
        click.echo('Specification does not exist for the resource')
        sys.exit()

    delete_resource(id)
    database.delete_specification(id)
    database.delete_live_stream_mapping(id)
    click.echo('Streaming resource deleted')


@resource.command(name='update')
@click.option('--spec-file', '-f', required=True, type=click.File(lazy=False),
              help='File that contains your streaming resource specification')
@exception_handler
def update(spec_file):
    """Update streaming resource"""  
    specification = yaml.load(spec_file, Loader=yaml.SafeLoader)
    valid = validate_resource(specification)
    if not valid:
        click.echo('The specification template is invalid')
    else:
        click.echo('The specification template is valid')
        
    wowza_auth()
    database = Database()
    
    resource_name = specification['name']
    stored_specification = database.get_specification_by_name(resource_name)
    changes = compare_specs(spec_src=stored_specification, spec_dst=specification)
    changes = clean_changes(changes)
    click.echo('The following changes will be applied:')
    display_message(changes)
    
    # TODO: Ask for apply changes
    specification_with_ids = update_resource(stored_specification, changes)
    click.echo('Updated specification is:')
    display_message(specification_with_ids)
    database.update_specification(specification_with_ids)
    click.echo('Streaming resource succesfully updated')

@resource.command(name='validator')
@click.option('--spec-file', '-f', required=True, type=click.File(lazy=False),
              help='File that contains your streaming resource specification')
@exception_handler
def validator(spec_file):
    """Validate streaming resource specification"""
    specification = yaml.load(spec_file, Loader=yaml.SafeLoader)
    valid = validate_resource(specification)
    if not valid:
        click.echo('The specification template is invalid')
    else:
        click.echo('The specification template is valid')


@resource.command(name='query')
@optgroup.group('Resource identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for resource')
@optgroup.option('--id', help='Resource stream id')
@optgroup.option('--name', help='Resource stream name')
@exception_handler
def query(id, name):
    """Get data for a resource"""
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
    response = get_resource_info(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)