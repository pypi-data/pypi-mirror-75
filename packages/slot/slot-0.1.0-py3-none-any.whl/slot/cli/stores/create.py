import click
from click import echo, style, secho

from slot.store import Store


@click.command()
@click.argument('name')
@click.argument('target')
def create(name, target):
    obj = Store(name)

    if obj.registered:
        echo('Store {} is already installed!'.format(style(obj.name, fg='red', bold=True)))
        return 1

    obj.create(target)
    echo(
        'Successfully created store: {} -> {}'.format(
            style(
                obj.name,
                fg='green',
                bold=True
            ), style(
                obj.target,
                fg='green',
                bold=True
            ),
        )
    )

    if click.confirm('Do you want to move the current file into the store?'):
        new_name = click.prompt(
            'Please enter a name for this option (e.g. default)',
            confirmation_prompt=True
        )
        obj.ingest(new_name, link=True)
        secho('Done!', fg='green', bold=True)
