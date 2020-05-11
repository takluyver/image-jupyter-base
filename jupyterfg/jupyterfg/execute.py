from nbconvert.preprocessors import (
    ExecutePreprocessor,
    ClearOutputPreprocessor,
    CellExecutionError,
)
from jupyter_contrib_nbextensions.nbconvert_support import EmbedImagesPreprocessor
import nbformat
from pathlib import Path
from .convert import to_html
import logging, sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def execute_and_save(nb_file, cell_timeout=-1):
    nb_file = Path(nb_file)
    html_file = nb_file.with_suffix(".html")

    with open(nb_file) as f:
        nb = nbformat.read(f, as_version=4)

    res = {"metadata": {"path": nb_file.parent}}

    logger.info(f"Stripping output from notebook {nb_file}.")
    clear = ClearOutputPreprocessor(log_level="DEBUG")
    nb, _ = clear.preprocess(nb, res)

    logger.info(f"Embedding images in markdown cells for notebook {nb_file}.")
    embed = EmbedImagesPreprocessor(embed_images=True, embed_remote_images=True)
    nb, _ = embed.preprocess(nb, res)

    logger.info(f"Executing and converting notebook {nb_file} to html.")
    execute = ExecutePreprocessor(timeout=cell_timeout)

    with execute.setup_preprocessor(nb, {}):
        for i, c in enumerate(nb.cells):
            try:
                logger.debug(f"Executing cell {i}")
                c, _ = execute.preprocess_cell(c, {}, i)
                nb.cells[i] = c
            to_html(nb, html_file)
            with open(nb_file, "w") as f:
                nbformat.write(nb, f)
