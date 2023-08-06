import json
from pkg_resources import resource_string

# Load config
cli_config = resource_string(__name__, 'config.json')
cli_settings = json.loads(cli_config)['properties']

DATABASE_FILENAME = cli_settings['DATABASE_FILENAME']
CREDENTIALS_FILENAME = cli_settings['CREDENTIALS_FILENAME']
CONFIG_PATH = cli_settings['CONFIG_PATH']
LOG_LEVEL = cli_settings['LOG_LEVEL']