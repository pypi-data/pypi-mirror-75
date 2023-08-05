import click
from halo import Halo

from .. import convert_to_xlsx, Services


@click.command(context_settings=dict(max_content_width=200))
@click.argument("path", type=click.Path(exists=True))
@click.option("-w", "--workers", default=1, show_default=True, help="amount of workers")
@click.option(
    "-o",
    "--output",
    help="output path for xlsx file relative from current location (ends in .xlsx, overwrites)",
)
@click.pass_context
def to_xlsx(ctx, path, workers, output):
    """ Convert invoice to xlsx """
    # Services available
    spinner = Halo(spinner="dots")
    spinner.start()
    services = Services(ctx, check_up=True)
    spinner.succeed(f"Found dir: {path}\n ")

    # Conversion
    convert_to_xlsx(
        path, services, workers, output,
    )

    spinner.succeed("Converted invoice(s) to xlsx")
