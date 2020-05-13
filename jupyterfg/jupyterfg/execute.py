# from jupyter_contrib_nbextensions.nbconvert_support import EmbedImagesPreprocessor
import logging
import sys
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, ClearOutputPreprocessor

from .convert import to_html

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def execute_and_save(nb_file, cell_timeout=-1):
    nb_file = Path(nb_file)
    html_file = nb_file.with_suffix(".html")

    with open(nb_file) as f:
        nb = nbformat.read(f, as_version=4)

    res = {"metadata": {"path": nb_file.parent}}

    logger.info(f"Stripping output from notebook {nb_file}.")
    clear = ClearOutputPreprocessor(log_level="DEBUG")
    nb, _ = clear.preprocess(nb, res)

    logger.info(f"Executing and converting notebook {nb_file} to html.")
    ep = ExecutePreprocessor(timeout=cell_timeout)
    ep.preprocess(nb, res)

    with open(nb_file, "w") as f:
        nbformat.write(nb, f)

    to_html(nb, html_file)
