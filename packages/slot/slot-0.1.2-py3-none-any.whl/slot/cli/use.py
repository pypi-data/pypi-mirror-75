import click
from click import echo, style, secho

from slot.store import Store


@click.command()
@click.argument('store_name')
@click.argument('option')
def use(store_name, option):
    store = Store(store_name)

    echo('Registering {} in {}'.format(
        style(option, fg='cyan', bold=True),
        style(store_name, fg='cyan', bold=True),
    ))
    store.select(option)

    secho('Done!', fg='green', bold=True)
