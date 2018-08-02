FROM jupyter/base-notebook:45e010d9e849
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 18.04

ARG JUPYTERHUB_VERSION=0.9.*
RUN pip --no-cache-dir install \
    jupyterhub==$JUPYTERHUB_VERSION

RUN jupyter labextension install @jupyterlab/hub-extension

# Startup Scripts
COPY start pre-startup-bash pre-startup-python /usr/local/bin/
