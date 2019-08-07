FROM jupyter/minimal-notebook:307ad2bb5fce

COPY environment.yml /
RUN conda env update -n base -f /environment.yml && \
        conda clean -afy

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

COPY jupyterfg /tmp/jupyterfg
RUN cd /tmp/jupyterfg && \
        flit install --symlink

WORKDIR /fastgenomics

# import the default workspace
COPY workspace.json /tmp
RUN jupyter lab workspaces import /tmp/workspace.json
