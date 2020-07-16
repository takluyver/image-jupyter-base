FROM jupyter/minimal-notebook:bfb2be718a58

LABEL maintainer="FASTGenomics <contact@fastgenomics.org>"

COPY --chown=1000:100 requirements.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install -yq --file /tmp/requirements.txt && \
        conda clean -afy

# install the jupyter expose extensions
COPY --chown=1000:100 jupyterlab-expose /tmp/jupyterlab-expose
RUN cd /tmp/jupyterlab-expose && \
        npm install && \
        npm run build && \
        jupyter labextension link --clean . && \
        jupyter lab clean && \
        jlpm cache clean && \
        npm cache clean --force && \
        rm -rf /tmp/*


# install jupyterfg (including the save hook)
COPY --chown=1000:100 jupyterfg /tmp/jupyterfg
RUN cd /tmp/jupyterfg && \
        flit install --symlink && \
        rm -rf /tmp/*

# install crash extension
COPY --chown=1000:100 crash_ext /tmp/crash_ext
RUN cd /tmp/crash_ext && \
        flit install --symlink && \
        rm -rf /tmp/*

# append the save hook to the original config file.
# AND opy overrides.json to settings folder to enable save widget state as default
COPY --chown=1000:100 config /tmp/config
RUN (echo; cat /tmp/config/jupyter_notebook_config.py) >> \
        /etc/jupyter/jupyter_notebook_config.py && \
        cp /tmp/config/overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json && \
        rm -rf /tmp/*

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
