from pathlib import Path
from .execute import execute_and_save
import click


@click.command()
@click.argument("notebook")
@click.option("--cell_timeout", default=-1, help="Timeout of executing a single cell.")
def main(notebook, cell_timeout):
    nb_file = Path(notebook)
    execute_and_save(
        nb_file, cell_timeout=cell_timeout
    )


main()
