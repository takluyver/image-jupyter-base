# Changes to be Checked When Updating Base Image

To handle some issues with jupyter lab some changes were made in our image.
It should be checked whether these adaptions are still needed when updating the base image.

## Dockerfile

Sometimes the jupyter server was not shutting down properly.
The reasons is unknown.
However, the problem occured when using `conda env update -f evironment.yml`, where some unpinned dependencies where updated.
Instead we now use `conda install` (and `pip install` in the other images).

## jupyterfg

Widgets were not working in the html, because the righ `ipywidgets_base_url` is not set to `https://unpkg.com/` as a default.
The nbconvert CLI is doing this. We added it manually in `convert.py`.
There is also an [issue](https://github.com/jupyterlab/jupyterlab/issues/7262) on this.

### Open issues

Widgets are not calculated/rendered in batch mode so far.
We tried no fixes until now.
