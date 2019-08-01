from pathlib import Path
from .execute import execute_and_save
import click


@click.command()
@click.argument("notebook")
@click.option(
    "--status_update_url",
    default=None,
    envvar="STATUSUPDATEURL",
    help="Url to send the status updates to.",
)
@click.option("--cell_timeout", default=-1, help="Timeout of executing a single cell.")
def main(notebook, status_update_url, cell_timeout):
    print(f"Sending updates to {status_update_url}")
    nb_file = Path(notebook)
    execute_and_save(
        nb_file, status_update_url=status_update_url, cell_timeout=cell_timeout
    )


main()
