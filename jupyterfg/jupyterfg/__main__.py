import argparse
import os
from pathlib import Path

from .execute import execute_and_save


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Execute a Jupyter ".ipynb" file and save it as ".html".'
    )

    parser.add_argument(
        "notebook", type=file_path, help='The path to the ".ipynb" file.'
    )
    parser.add_argument(
        "--cell_timeout",
        dest="cell_timeout",
        type=int,
        default=-1,
        help="Timeout of executing a single cell in seconds.",
    )

    args = parser.parse_args()

    return args


def main(notebook, cell_timeout):
    nb_file = Path(notebook)
    execute_and_save(nb_file, cell_timeout=cell_timeout)


if __name__ == "__main__":
    args = get_parser()
    main(args.notebook, args.cell_timeout)
