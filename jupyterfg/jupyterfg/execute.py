from nbconvert.preprocessors import (
    ExecutePreprocessor,
    ClearOutputPreprocessor,
    CellExecutionError,
)
from jupyter_contrib_nbextensions.nbconvert_support import EmbedImagesPreprocessor
import nbformat
from pathlib import Path
from .convert import to_html
from .status import submit_status


def execute_and_save(nb_file, status_update_url=None, cell_timeout=-1):
    nb_file = Path(nb_file)
    html_file = nb_file.with_suffix(".html")

    with open(nb_file) as f:
        nb = nbformat.read(f, as_version=4)

    res = {"metadata": {"path": nb_file.parent}}

    clear = ClearOutputPreprocessor()
    nb, _ = clear.preprocess(nb, res)

    embed = EmbedImagesPreprocessor(embed_images=True, embed_remote_images=True)
    nb, _ = embed.preprocess(nb, res)

    execute = ExecutePreprocessor(timeout=cell_timeout)

    state = dict(all=len(nb.cells), progress=0, failed=0, mode="batch")

    with execute.setup_preprocessor(nb, {}):
        for i, c in enumerate(nb.cells):
            try:
                c, _ = execute.preprocess_cell(c, {}, i)
                nb.cells[i] = c
            except CellExecutionError:
                state["failed"] += 1
            to_html(nb, html_file)
            with open(nb_file, "w") as f:
                nbformat.write(nb, f)
            state["progress"] = i + 1
            submit_status(state, status_update_url)
