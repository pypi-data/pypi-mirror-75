import click

from slot.store import Store


@click.command()
@click.argument('store_name')
@click.argument('option')
def select(store_name, option):
    store = Store(store_name)

    store.select(option)

    click.secho('Done!', fg='green', bold=True)
