import click

from .meetup import MeetupCertificator


@click.command()
@click.argument('destination', type=click.Path(exists=True, dir_okay=True), default='.')
@click.option('--urlname', '-u')
@click.option('--event_id', '-e')
@click.option('--meetup-api-key', '-k')
@click.option('--template-path', '-t', type=click.Path(exists=True, dir_okay=True), default=None)
def generate(destination, urlname, event_id, meetup_api_key, template_path):
    assert urlname and event_id and meetup_api_key, ('You must pass the --urlname, --event_id '
                                                     'and --meetup-api-key arguments')

    certifier = MeetupCertificator(
        urlname=urlname,
        event_id=event_id,
        destination_path=destination,
        template_path=template_path,
        api_key=meetup_api_key,
    )
    certifier.generate()


if __name__ == '__main__':
    generate()
