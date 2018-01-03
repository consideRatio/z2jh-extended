FROM jupyter/minimal-notebook:0b3ec811c968
# Build from... https://hub.docker.com/r/jupyter/minimal-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/minimal-notebook/Dockerfile
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 16.04

# conda/pip/apt install additional packages here, if desired.

RUN conda install -y -c conda-forge -c damianavila82 \
    ipyvolume \
    ipywidgets \
    numpy \
    rise \
    sympy \
    nbgrader \
    hide_code

RUN pip --no-cache-dir install \
    git+https://github.com/data-8/nbgitpuller \
    plotly

RUN jupyter serverextension enable --py nbgitpuller --sys-prefix


# --- FUTILE ATTEMPT TO SETUP NFS MOUNT ---
# -----------------------------------------------------------------------------
USER root

# So we can actually write the NSF mount
ENV NBGRADER_EXCHANGE_DIR=/srv/nbgrader/exchange

RUN mkdir -p $NBGRADER_EXCHANGE_DIR && \
    chown $NB_USER:$NB_GID $NBGRADER_EXCHANGE_DIR && \
    fix-permissions $NBGRADER_EXCHANGE_DIR

ENV NBGRADER_EXCHANGE_DIR=/srv/nbgrader/exchanged

RUN mkdir -p $NBGRADER_EXCHANGE_DIR && \
    chown $NB_USER:$NB_GID $NBGRADER_EXCHANGE_DIR && \
    /usr/local/bin/fix-permissions $NBGRADER_EXCHANGE_DIR

# preparing the directories...
# https://github.com/jupyterhub/dockerspawner/issues/160#issuecomment-330162308

# create the notebook directory
RUN NBDIR=/srv/nbgrader/newdir && \
    mkdir "$NBDIR" && \
    chown :100 "$NBDIR" && \
    chmod g+rws "$NBDIR"

USER $NB_USER
# -----------------------------------------------------------------------------


# pin jupyterhub to match the Hub version
# set via --build-arg in Makefile
ARG JUPYTERHUB_VERSION=0.8
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION