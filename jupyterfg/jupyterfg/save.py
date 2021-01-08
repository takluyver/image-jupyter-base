import os
import time
from pathlib import Path

import nbformat

from .convert import to_html


def mod_time(files: dict, t_offset: int = -5):
    """Change access and modification time of a file by `offset`.

    To deal with the time buffer issue in Jupyter lab

    Parameters
    ----------
    files : dict
        dict containing the files to modifiy
    t_offset : int, optional
        Offset in seconds, by default 5
    """

    now = round(time.time())
    for file in files:
        os.utime(file, (now + t_offset, now + t_offset))


def post_save_hook(model, os_path, contents_manager):
    """post-save hook for converting notebooks to .html"""
    os_path = Path(os_path)

    if model["type"] != "notebook":
        return  # only do this for notebooks

    if (
        not os_path.suffix == ".ipynb"
    ):  # e.g. for markdown files with jupytext installed
        return  # We might add a converter for markdown Rmarkdown in the future

    with open(os_path) as f:
        nb = nbformat.read(f, as_version=4)

    html_file = os_path.with_suffix(".html")
    to_html(nb, html_file)

    # mod_time([os_path, html_file])
