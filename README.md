# Introduction

This is the base image for the fastgenomics jupyter stack. Based on `jupyter/minimal-notebook`.
There are two major new functionalities added, compared to the minimal-notebook:

1. There is a custom save hook that, on top of saving the notebook, saves a html file.

2. There is a custom command that executes the notebook and converts it to html in a
   batch mode.

# Dependencies included

Only few additional packages on top of the base `jupyter/minimal-notebook` are included:

- `curl` to allow downloading via `curl`
- `flit` is used to install the associated `jupyterfg` python
  module that provides the functionality described below.
- `jupytext` for markdown / Rmarkdown support
- `openssh` to provide `ssh` from within the container

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
`/etc/jupyter/jupyter_server_config.py`) which attaches a custom save hook that
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

To simulate a crash of the jupyter application the endpoint `/6901a7302f214e38847a60f514798a42/crash` can be used, which will cause jupyter lab to exit with code `123`. This path has to be appended directly to the basepath without `api`.

# Custom Changes

To handle some issues with jupyter lab some changes were made in our image.
It should be checked whether these adaptions are still needed when updating the base image.

## Dockerfile

Sometimes the jupyter server was not shutting down properly.
The reasons is unknown.
However, the problem occured when using `conda env update -f evironment.yml`, where some unpinned dependencies where updated.
Instead we now use `conda install` (and `pip install` in the other images).

## jupyterfg

- Widgets were not working in the html, because the righ `ipywidgets_base_url` is not set to `https://unpkg.com/` as a default.
  The nbconvert CLI is doing this. We added it manually in `convert.py`.
  There is also an [issue](https://github.com/jupyterlab/jupyterlab/issues/7262) on this.
- There are multiple [issues](https://github.com/jupyterlab/jupyterlab/issues/7743) because Jupyter reports that the "file changed on disk" since the last save.
  The reason are different server and client times.
  There is a 500ms buffer build in, but this is not enough.
  There are [plans](https://github.com/jupyterlab/jupyterlab/issues/8556) to make this configurable.
  However, patching the [code](https://github.com/jupyterlab/jupyterlab/blob/34a94a4e65d5606dfb82d33b0f172d579bab5e0b/packages/docregistry/src/context.ts#L647) is not an option, as after clearing caches and rebuiling JLab (e.g., when installing extensions) the values are reset as the package is pulled from the sources again.
  For this reasons, the post save hook is modified such, that the modification date for the `.ipynb` and `.html` file get predated by 5 seconds after save.

# Additional Files and folders

- File `config/jupyter_server_config.py`  
  Gets appended to the Jupyter Lab config and adds the custom save hook and the crash extension
- File `config/overrides.json`  
  For configuration of the Jupyter Lab
- Folder `crash_ext`  
  see [Crash Extension](#crash-extension)
- Folder `jupyter_fg`  
  Python module to generate a html fromt he notebook in interactive and batch mode
- Folder `jupyterlab-expose`  
  Jupyter Lab extension to expose Jupyter functionalities
- File `CustomChanges.md`  
  Documents custom changes, required to work around some issues
