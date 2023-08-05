import logging
from logging import Logger
import click
from cli.__version__ import VERSION
from cli.constants import LOG_LEVEL
from cli.commands.livestream import live
from cli.commands.transcoder import trans
from cli.commands.configure import configure
from cli.commands.resource import resource 
from cli.commands.recording import recording
from cli.commands.mapping import mapper

class NaturalOrderGroup(click.Group):
    # Link: https://github.com/pallets/click/issues/513
    def list_commands(self, ctx):
        return self.commands.keys()

@click.group(cls=NaturalOrderGroup)
@click.version_option(version=VERSION)
def cli():
    pass

cli.add_command(mapper)
cli.add_command(resource)
cli.add_command(live)
cli.add_command(trans)
cli.add_command(recording)
cli.add_command(configure)

# Logger setup
logger = Logger('')
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)