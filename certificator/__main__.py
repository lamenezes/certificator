import click

from . import config
from .meetup import MeetupCertificator
from .certificator import CSVCertificator


@click.group()
def main():
    pass


@main.command()
@click.argument('destination', type=click.Path(exists=True, dir_okay=True), default='.')
@click.option('--urlname', '-u')
@click.option('--event-id', '-e')
@click.option('--meetup-api-key', '-k', default=config.MEETUP_API_KEY,
              help="Your API key for Meetup")
@click.option('--template-path', '-t', type=click.Path(exists=True, dir_okay=True), default=None,
              help="The path of your template.html file")
@click.option('--filename-format', '-f', default='certificate-{id:0>3}.pdf',
              help="The file name format of the generated certificates")
def meetup(destination, urlname, event_id, meetup_api_key, template_path, filename_format):
    """
    Generate the certificates using your Meetup event
    """

    assert urlname and event_id and meetup_api_key, ('You must pass the --urlname, --event_id '
                                                     'and --meetup-api-key arguments')

    certifier = MeetupCertificator(
        urlname=urlname,
        event_id=event_id,
        destination_path=destination,
        template_path=template_path,
        api_key=meetup_api_key,
        filename_format=filename_format,
    )
    certifier.generate()


@main.command()
@click.argument('destination', type=click.Path(exists=True, dir_okay=True), default='.')
@click.option('--meta-file', '-m', prompt="Please enter your meta json file name",
              help="Your meta json file name")
@click.option('--data-file', '-d', prompt="Please enter your data csv file name",
              help="Your data csv file name")
@click.option('--template-path', '-t', type=click.Path(exists=True, dir_okay=True), default=None,
              help="The path of your template.html file")
@click.option('--delimiter', default=',',
              help="The delimiter used in your data csv file. Example: --delimiter ';'")
@click.option('--filename-format', '-f', default='certificate-{id:0>3}.pdf',
              help="The file name format of the generated certificates")
def csv(destination, meta_file, data_file, template_path, delimiter, filename_format):
    """
    Generate the certificates using local csv file
    """

    certifier = CSVCertificator(
        delimiter=delimiter,
        meta_path=meta_file,
        data_path=data_file,
        template_path=template_path,
        destination_path=destination,
        filename_format=filename_format,
    )
    certifier.generate()


if __name__ == '__main__':
    main()
