# from jupyter_contrib_nbextensions.nbconvert_support import EmbedImagesPreprocessor
import logging
import sys
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

from .convert import to_html

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def execute_and_save(nb_file, cell_timeout=-1):
    nb_file = Path(nb_file)
    html_file = nb_file.with_suffix(".html")

    with open(nb_file) as f:
        nb = nbformat.read(f, as_version=4)

    res = {"metadata": {"path": nb_file.parent}}

    # not working so far, image still as link
    # logger.info(f"Embedding images in markdown cells for notebook {nb_file}.")
    # embed = EmbedImagesPreprocessor(embed_images=True, embed_remote_images=True)
    # nb, _ = embed.preprocess(nb, res)

    logger.info(f"Executing and converting notebook {nb_file} to html.")
    ep = ExecutePreprocessor(timeout=cell_timeout)
    ep.preprocess(nb, res)

    with open(nb_file, "w") as f:
        nbformat.write(nb, f)

    to_html(nb, html_file)
