import nbformat
from pathlib import Path
from .convert import to_html
import click
from .status import submit_status


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
    html_file = nb_file.with_suffix(".html")

    with open(nb_file) as f:
        nb = nbformat.read(f, as_version=4)

    state = dict(all=len(nb.cells), progress=0, failed=0, mode="batch")

    to_html(nb, html_file)

    # status raus
    state["progress"] = 1
    submit_status(state, status_update_url)


main()
