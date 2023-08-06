import click

from cloud_curator.reports.access_keys_rotated import AccessKeysRotated

@click.group()
def cli():
    pass

@cli.command()
def access_keys_rotated():
    """Checks whether the active access keys are rotated within the number
        of days specified in maxAccessKeyAge. The rule is non-compliant if the access
        keys have not been rotated for more than maxAccessKeyAge number of days."""
    report = AccessKeysRotated()
    report.run()