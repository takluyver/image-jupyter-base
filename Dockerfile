FROM jupyter/minimal-notebook:bfb2be718a58

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

# Copy overrides.json to settings folder to enable save widget state as default
RUN cp /tmp/config/overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

USER root
RUN mkdir /fastgenomics && \
        chown -v -R 1000:100 /fastgenomics && \
        chown -v -R 1000:100 /home/jovyan/.jupyter
USER jovyan

# import the default FG workspace and overwrite jupyter fallback WS
COPY --chown=1000:100 workspace.json /home/jovyan/.jupyter/lab/workspaces/
RUN jupyter lab workspaces import /home/jovyan/.jupyter/lab/workspaces/workspace.json && \
        sed -i -e 's/workspace = dict(data=dict(), metadata=dict(id=id))/with open("\/home\/jovyan\/.jupyter\/lab\/workspaces\/workspace.json") as file:/' \
        -e 's/return self.finish(json.dumps(workspace))/    return self.finish(json.dumps(json.load(file)))/' \
        /opt/conda/lib/python3.7/site-packages/jupyterlab_server/workspaces_handler.py

WORKDIR /fastgenomics
