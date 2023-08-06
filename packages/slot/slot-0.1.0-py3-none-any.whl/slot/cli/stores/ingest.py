import os

import click

from slot.store import Store


@click.command()
@click.argument('store_name')
@click.argument('file_name')
@click.option('-n', '--name', type=click.STRING, default=None,
              help='Name of the option this file becomes')
@click.option('-s', '--silent', type=click.BOOL, help='Disable user interaction')
def ingest(store_name, file_name, name, silent):
    store = Store(store_name)

    new_name = name or os.path.basename(file_name)

    if name is None and silent is False:
        if not click.confirm(
            'Is the name {} okay for this option?'.format(
                click.style(
                    new_name,
                    bold=True,
                ),
            ),
        ):
            new_name = click.prompt('Please choose a new name')

    store.ingest(new_name, file_name=file_name)

    click.secho('Done!', fg='green', bold=True)
