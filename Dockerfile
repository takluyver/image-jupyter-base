# set tag forjupyter/minimal-notebook
ARG IMG_VERISON=703d8b2dcb88

##############
# BUILDSTAGE #
##############
FROM jupyter/minimal-notebook:${IMG_VERISON} AS build_stage

COPY --chown=1000:100 jupyterlab-expose /tmp/jupyterlab-expose

RUN cd /tmp/jupyterlab-expose && \
        npm install && \
        npm run build && \
        npm pack


############
# RUNSTAGE #
############
FROM jupyter/minimal-notebook:${IMG_VERISON}

LABEL maintainer="FASTGenomics <contact@fastgenomics.org>"

# Install conda requirements
COPY --chown=1000:100 requirements_conda.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install -yq --file /tmp/requirements_conda.txt && \
        conda clean -afy && \
        rm -rf /tmp/*

# install the jupyter expose extensions
COPY --from=build_stage /tmp/jupyterlab-expose/jupyterlab-expose-1.0.0.tgz /opt/
RUN jupyter labextension install /opt/jupyterlab-expose-1.0.0.tgz && \
        jupyter lab clean && \
        jlpm cache clean && \
        npm cache clean --force


# install jupyterfg (including the save hook)
COPY --chown=1000:100 jupyterfg /tmp/jupyterfg
RUN cd /tmp/jupyterfg && \
        flit install && \
        rm -rf /tmp/*

# install crash extension
COPY --chown=1000:100 crash_ext /tmp/crash_ext
RUN cd /tmp/crash_ext && \
        flit install && \
        rm -rf /tmp/*

# append the save hook to the original config file.
# AND copy overrides.json to settings folder to enable save widget state as default
COPY --chown=1000:100 config /tmp/config
RUN (echo; cat /tmp/config/jupyter_notebook_config.py) >> \
        /etc/jupyter/jupyter_notebook_config.py && \
        mkdir -pv /opt/conda/share/jupyter/lab/settings && \
        cp /tmp/config/overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json && \
        (echo; cat /tmp/config/.condarc) >> \
        /opt/conda/.condarc && \
        rm -rf /tmp/*

USER root
RUN mkdir /fastgenomics && \
        chown -v -R 1000:100 /fastgenomics && \
        chown -v -R 1000:100 /home/jovyan/.jupyter
USER jovyan

# import default workspace (only for local testing)
COPY --chown=1000:100 workspace.json /home/jovyan/.jupyter/lab/workspaces/
RUN jupyter lab workspaces import /home/jovyan/.jupyter/lab/workspaces/workspace.json

WORKDIR /fastgenomics
