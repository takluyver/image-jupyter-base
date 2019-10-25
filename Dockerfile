FROM jupyter/minimal-notebook:1386e2046833

COPY requirements.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install --file /tmp/requirements.txt && \
	conda clean -afy

# install jupyterfg (including the save hook)
COPY jupyterfg /tmp/jupyterfg
RUN cd /tmp/jupyterfg && \
    flit install --symlink

# append the save hook to the original config file.
COPY config /tmp/config
RUN (echo; cat /tmp/config/jupyter_notebook_config.py) >> \
        /etc/jupyter/jupyter_notebook_config.py

# install the jupyter extensions (quit button)
COPY --chown=1000:100 jupyterlab-quit /tmp/jupyterlab-quit
RUN jupyter labextension install jupyterlab-topbar-extension && \
        cd /tmp/jupyterlab-quit && \
        npm install && \
        npm run build && \
        jupyter labextension link .

WORKDIR /fastgenomics

# import the default workspace
COPY workspace.json /tmp
RUN jupyter lab workspaces import /tmp/workspace.json