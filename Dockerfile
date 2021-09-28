# set tag forjupyter/minimal-notebook
ARG IMG_VERISON=e6970b22a504

##############
# BUILDSTAGE #
##############
FROM jupyter/minimal-notebook:${IMG_VERISON} AS build_stage

COPY --chown=1000:100 build_requirements_conda.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install -yq --file /tmp/build_requirements_conda.txt && \
        conda clean -afy && \
        rm -rf /tmp/*

COPY --chown=1000:100 jupyterlab-expose /tmp/jupyterlab-expose
RUN cd /tmp/jupyterlab-expose && \
        python setup.py bdist_wheel



############
# RUNSTAGE #
############
FROM jupyter/minimal-notebook:${IMG_VERISON}

LABEL maintainer="FASTGenomics <contact@fastgenomics.org>"

# overwrite conda default channels
COPY --chown=1000:100 config /tmp/config
RUN (echo; cat /tmp/config/.condarc) >> /opt/conda/.condarc && \
        rm -rf /tmp/*

# Install conda requirements
COPY --chown=1000:100 requirements_conda.txt /tmp
RUN conda config --add channels conda-forge && \
        conda install -yq --file /tmp/requirements_conda.txt && \
        conda clean -afy && \
        rm -rf /tmp/*

# install the jupyter expose extensions
COPY --from=build_stage /tmp/jupyterlab-expose/dist/jupyterlab_expose-2.0.0-py3-none-any.whl /opt/
RUN pip install /opt/jupyterlab_expose-2.0.0-py3-none-any.whl


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
RUN (echo; cat /tmp/config/jupyter_server_config.py) >> /etc/jupyter/jupyter_server_config.py && \
        mkdir -pv /opt/conda/share/jupyter/lab/settings && \
        cp /tmp/config/overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json && \
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
