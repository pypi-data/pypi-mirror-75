import click

from .stores import stores
from .list import list_stores
from .use import use
from .options import options


@click.group()
def cli():
    pass


cli.add_command(stores)
cli.add_command(use)
cli.add_command(list_stores, name='list')
cli.add_command(options)
