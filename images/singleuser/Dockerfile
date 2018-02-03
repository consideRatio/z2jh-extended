FROM jupyter/minimal-notebook:9089b66a9813
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



# conda packages
RUN conda install -y -c conda-forge -c damianavila82 \
    ipyvolume \
    ipywidgets \
    numpy \
    rise \
    sympy \
    jupyter_contrib_nbextensions
    # nbgrader \  # excluded until successful usage demonstrated
    # hide_code \ # excluded in favor of hide_input contrib_extension


# pip packages
RUN pip --no-cache-dir install \
    git+https://github.com/data-8/nbgitpuller \
    plotly

# activation
RUN jupyter serverextension enable --python nbgitpuller --sys-prefix
RUN jupyter nbextension enable gist_it/main && /
    jupyter nbextension enable hinterland/hinterland && /
    jupyter nbextension enable export_embedded/main && /
    jupyter nbextension enable comment-uncomment/main && /
    jupyter nbextension enable init_cell/main && /
    jupyter nbextension enable hide_header/main && /
    jupyter nbextension enable hide_input/main && /
    jupyter nbextension enable rubberband/main

COPY --chown start /usr/local/bin
COPY --chown pre-startup-bash /usr/local/bin
COPY --chown pre-startup-python /usr/local/bin