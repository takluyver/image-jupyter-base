FROM jupyter/minimal-notebook:1386e2046833

COPY requirements.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install -q --file /tmp/requirements.txt && \
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
RUN chown -v -R 1000:100 ~/.jupyter

# import the default workspace
COPY --chown=1000:100 workspace.json /home/jovyan/.jupyter/lab/workspaces/
RUN jupyter lab workspaces import /home/jovyan/.jupyter/lab/workspaces/workspace.json

# overwrite default workspace
RUN sed -i -e 's/workspace = dict(data=dict(), metadata=dict(id=id))/with open("\/home\/jovyan\/.jupyter\/lab\/workspaces\/workspace.json") as file:/' \
        -e 's/return self.finish(json.dumps(workspace))/    return self.finish(json.dumps(json.load(file)))/' \
        /opt/conda/lib/python3.7/site-packages/jupyterlab_server/workspaces_handler.py
