import click

from slot.store import Store


@click.command()
@click.argument('store_name')
def options(store_name):
    store = Store(store_name)

    for option in store.options:
        is_selected = store.selected_option == option
        prelude = '->' if is_selected else '  '

        click.secho(
            f'{prelude} {option}',
            color='cyan' if is_selected else None,
            bold=is_selected,
        )
