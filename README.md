# Introduction

The base image for the fastgenomics jupyter stack.  Based on `jupyter/minimal-notebook`.
There are two major new functionalities added, compared to the minimal-notebook:

1. There is a custom save hook that, on top of saving the notebook, saves a html file
   and sends a status update through a PUT request to a URL specified in a
   `STATUSUPDATEURL`.

2. There is a custom command that executes the notebook and converts it to html in a
   batch mode.  This command sends the status update to `STAUTSUPDATEURL` after
   evaluating every cell.

# Dependencies included

The only additional package on top of the base `jupyter/minimal-notebook` that this
image includes is `flit`.  It is used to install the associated `jupyterfg` python
module that provides the functionality described below.

# Usage

## Interactive execution

Just use the standard jupyter lab command with whatever options you prefer, for example

```
jupyter lab
```

The docker image has WORKDIR set to `/fastgenomics`, where `analysis` and `data` would
be mounted so this would start the jupyter session where only these two directories
would be visible (note, that all the other directories are still accessible, it's just
the UI that is limited to the `/fastgenomics` directory).

The docker image has an altered jupyter config file (in
`/etc/jupyter/jupyter_notebook_config.py`) which attaches a custom save hook that
exports the notebook to an html file on save.  The hook also sends a status update
message with the contents `{"mode": "manual"}` to the predefined endpoint (see below).

## Batch execution

To execute the notebook in batch mode use the custom built-in module `jupyterfg` via

```
python -m jupyterfg /fastgenomics/analysis/analysis.ipynb
```

Or use the fact that the `/fastgenomics` is the WORKDIR of the image and simply
call

```
python -m jupyterfg analysis/analysis.ipynb
```

The command ignores errors in jupyter cells so it will succeed even if the notebook has
errors.  A html file is re-generated after the execution of each cell to allow the user
a peek into the intermediate results, which provides an early feedback.  The notebook
itself is also saved after executing each cell (with the previous outputs overriten).

The batch execution runs all the cells one by one and sends a status update to a
pre-defined hook after every cell.  The payload of these messages looks like so

```
{
    "mode": "batch",
    "total": 10,   # total number of cells
    "progress": 5, # cells executed so far
    "failed": 2    # cells failed so far
}
```

which means that the execution is done in `"batch"` mode (in contrast to the `"manual"`
save hook when running the interactive session).  The remaining data tells us about the
progress of the evaluation (for e.g. a progress bar).  The overall status of the whole
evaluation can then be determined based on the combination of the `"total"`,
`"progress"` and `"failed"`.  For example, the evaluation is complete when
`"total"=="progress"` or the evaluation failed if `"failed">0`, etc.

The `jupyterfg` also takes an additional option `--cell_timeout` to control how much
time (in seconds) we allow each cell to run.  The default is `--cell_timeout=-1`, which
disables the timeout.  To allow only 10 seconds for each cell use

```
python -m jupyterfg --cell_timeout=10 analysis/analysis.ipynb
```

## Export hooks

Both modes support communicating the status via a PUT request to a url defined in the
`STATUSUPDATEURL` environmental variable.  If this variable is undefined, the status
updates will not be sent.  If it is defined, but the url does not exist the whole
command will fail.
