FROM jupyter/minimal-notebook:c54800018c2c
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



# nodejs
USER root
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - && \
    apt-get install -y nodejs
USER ${NB_USER}



# conda packages
RUN conda install -y -c conda-forge -c damianavila82 \
    jupyterlab \
    numpy \
    sympy \
    ipyvolume \
    ipywidgets \
    seaborn \
    bokeh \
    altair \
    rise \
    jupyter_contrib_nbextensions
    # nbgrader \  # excluded until successful usage demonstrated



# pip packages
RUN pip --no-cache-dir install \
    git+https://github.com/data-8/nbgitpuller \
    plotly



# jupyterlab extensions
RUN jupyter labextension install @jupyterlab/hub-extension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager



# activation
RUN jupyter serverextension enable --sys-prefix --python nbgitpuller

RUN jupyter nbextension enable --sys-prefix comment-uncomment/main && \
    jupyter nbextension enable --sys-prefix hide_input/main && \
    jupyter nbextension enable --sys-prefix gist_it/main && \
    jupyter nbextension enable --sys-prefix init_cell/main && \
    jupyter nbextension enable --sys-prefix splitcell/splitcell && \
    jupyter nbextension enable --sys-prefix tree-filter/index && \
    jupyter nbextension enable --sys-prefix rubberband/main && \
    jupyter nbextension enable --sys-prefix toc2/main && \
    jupyter nbextension enable --sys-prefix collapsible_headings/main && \
    jupyter nbextension enable --sys-prefix export_embedded/main && \
    jupyter nbextension enable --sys-prefix hide_header/main



# startup scripts
COPY start pre-startup-bash pre-startup-python \
    /usr/local/bin/