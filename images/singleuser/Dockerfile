FROM jupyter/minimal-notebook:0b3ec811c968
# Build from... https://hub.docker.com/r/jupyter/minimal-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/minimal-notebook/Dockerfile
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 16.04

# kubespawner requires the singleuser image to be started with a script
# provided by the jupyterhub package, and will hence override the CMD with 
# ["jupyterhub-singleuser"] instead of the jupyter/docker-stacks images CMD
# of ["start-notebook.sh"]
ARG JUPYTERHUB_VERSION=0.8.*
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION


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

USER root

# --- FUTILE ATTEMPT TO SETUP NFS MOUNT ---
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------

COPY start /usr/local/bin
COPY pre-startup-bash /usr/local/bin
COPY pre-startup-python /usr/local/bin
RUN chmod o+rx \
    /usr/local/bin/start \
    /usr/local/bin/pre-startup-bash \
    /usr/local/bin/pre-startup-python

# TEMP: Bugfixfor jupyterhub until 0.8.2 is released
RUN pip --no-cache-dir install \
    git+https://github.com/consideratio/jupyterhub

USER $NB_USER