import os
from pathlib import Path

import nbformat

from .convert import to_html


def post_save_hook(model, os_path, contents_manager):
    """post-save hook for converting notebooks to .html"""
    os_path = Path(os_path)

    if model["type"] != "notebook":
        return  # only do this for notebooks

    with open(os_path) as f:
        nb = nbformat.read(f, as_version=4)

    html_file = os_path.with_suffix(".html")
    to_html(nb, html_file)
