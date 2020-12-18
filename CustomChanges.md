# Changes to be Checked When Updating Base Image

To handle some issues with jupyter lab some changes were made in our image.
It should be checked whether these adaptions are still needed when updating the base image.

## Dockerfile

Sometimes the jupyter server was not shutting down properly.
The reasons is unknown.
However, the problem occured when using `conda env update -f evironment.yml`, where some unpinned dependencies where updated.
Instead we now use `conda install` (and `pip install` in the other images).

## jupyterfg

- Widgets were not working in the html, because the righ `ipywidgets_base_url` is not set to `https://unpkg.com/` as a default. The nbconvert CLI is doing this. We added it manually in `convert.py`. There is also an [issue](https://github.com/jupyterlab/jupyterlab/issues/7262) on this.
- There are multiple [issues](https://github.com/jupyterlab/jupyterlab/issues/7743) because Jupyter reports that the "file changed on disk" since the last save. The reason are different server and client times. There is a 500ms buffer build in, but this is not enough. There are [plans](https://github.com/jupyterlab/jupyterlab/issues/8556) to make this configurable. However, patching the [code](https://github.com/jupyterlab/jupyterlab/blob/34a94a4e65d5606dfb82d33b0f172d579bab5e0b/packages/docregistry/src/context.ts#L647) is not an option, as after clearing caches and rebuiling JLab (e.g., when installing extensions) the values are reset as the package is pulled from the sources again. For this reasons the post save hook is modified such, that the modificaiton date for the `.ipynb` and `.html` file get predated by 5 seconds after save.

### Open issues

Widgets are not calculated/rendered in batch mode so far.
We tried no fixes until now.
