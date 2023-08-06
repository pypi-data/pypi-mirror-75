import click
from click import echo, style

from slot.config import Config
from slot.store import Store


@click.command()
def list_stores():
    stores = [Store(name) for name in Config().stores.keys()]

    for store in stores:
        echo(
            '{} -> {}{}'.format(
                style(
                    store.name,
                    fg='cyan',
                    bold=True,
                ),
                style(
                    'installed' if store.registered else 'not installed',
                    fg='green' if store.registered else 'red',
                    bold=True,
                ),
                style(
                    f' [{store.selected_option}]' if store.registered else '',
                    fg='blue',
                    bold=True,
                ),
            ),
        )
