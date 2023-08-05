import functools
import click
import datetime
import json
import os
from pathlib import Path
from benedict import benedict
from jsondiff import diff
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter
from boltons.iterutils import remap
from cli.constants import CONFIG_PATH, DATABASE_FILENAME, CREDENTIALS_FILENAME


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = 'There was an error in the CLI: {}'.format(str(e))
            click.echo(message, err=True)
            exit(1)

    return wrapper

# core auth

def wowza_auth():
    if credentials_file_exist():
        __set_credentials_envars()
    else:
        __create_creds_file()
        __set_credentials_envars()

def __set_credentials_envars():
    credentials_file_path = get_base_file_path(filename=CREDENTIALS_FILENAME)
    with open(credentials_file_path) as json_file:
        credentials_data = json.load(json_file)
        os.environ["WSC_ACCESS_KEY"] = credentials_data['WSC_ACCESS_KEY']
        os.environ["WSC_API_KEY"] = credentials_data['WSC_API_KEY']

def __create_creds_file():
    config_path=__get_config_path()
    wsc_access_key = click.prompt('Please enter wowza access key')
    wsc_api_key = click.prompt('Please enter wowza api key')
    keys = {
            'WSC_ACCESS_KEY': wsc_access_key,
            'WSC_API_KEY': wsc_api_key
            }
    Path(config_path).mkdir(parents=True, exist_ok=True)
    credentials_file_path = get_credentials_file_path()
    with open(credentials_file_path, 'w') as json_file:
        json_file.write(json.dumps(keys, indent=4))

def credentials_file_exist():
    exist = config_file_exist(filename=CREDENTIALS_FILENAME)
    return exist

def get_credentials_file_path():
    file_path = get_base_file_path(CREDENTIALS_FILENAME)
    return file_path

# core utils paths

def __get_config_path():
    home_path = str(Path.home())
    config_path = home_path + CONFIG_PATH
    return config_path

# def __get_config_filename():
#     config_filename = DATABASE_FILENAME
#     return config_filename

def config_file_exist(filename, config_path=__get_config_path()):
    base_file_path = get_base_file_path(filename, config_path=config_path)
    if os.path.exists(base_file_path):
        return True
    else:
        return False

def get_base_file_path(filename, config_path=__get_config_path()):
    full_file_path = config_path + filename
    return full_file_path

# core utils compare

def compare_specs(spec_src, spec_dst):
    changes = diff(spec_src, spec_dst, marshal=True)
    changes = json.loads(json.dumps(changes)) # turn integer keys into string keys
    return changes

def clean_changes(changes):
    drop_empty = lambda path, key, value: bool(value)
    clean = remap(changes, visit=drop_empty)
    drop_delete_name = lambda path, key, value: not value == {'parameters': {'$delete': ['name']}}
    clean = remap(clean, visit=drop_delete_name)
    return clean

def display_message(message):
    formatted_json = json.dumps(message, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)