import click

from .create import create
from .ingest import ingest


@click.group()
def stores():
    pass


stores.add_command(create)
stores.add_command(ingest)
