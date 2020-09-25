# Introduction

This is the base image for the fastgenomics jupyter stack. Based on `jupyter/minimal-notebook`.
There are two major new functionalities added, compared to the minimal-notebook:

1. There is a custom save hook that, on top of saving the notebook, saves a html file.

2. There is a custom command that executes the notebook and converts it to html in a
   batch mode.

# Dependencies included

The only additional packages on top of the base `jupyter/minimal-notebook` that this
image includes are `flit` and `jupyter_contrib_nbextensions`:

- `flit` is used to install the associated `jupyterfg` python
  module that provides the functionality described below.
- `jupyter_contrib_nbextensions` is installed only for the `EmbedHTMLExporter`, which embeds imageas as base64 into the `html`.

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
exports the notebook to an html file on save.

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
errors. A `html` file is generated after the execution of the notebook. The notebook
itself is also saved after execution.

The `jupyterfg` also takes an additional option `--cell_timeout` to control how much
time (in seconds) we allow each cell to run. The default is `--cell_timeout=-1`, which
disables the timeout. To allow only 10 seconds for each cell use

```
python -m jupyterfg --cell_timeout=10 analysis/analysis.ipynb
```

## Crash Extension

To simulate a crash of the jupyter application the endpoint `/6901a7302f214e38847a60f514798a42/crash` can be used, which will cause jupyter lab to exit with code `123`.

> However, this is working on the FASTGenomics system, but there seems to be a problem with the standalone Docker image. Maybe related to some changes in the the base URL or default URL.
