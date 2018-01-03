ARG TAG=8b3b2ab
FROM jupyterhub/k8s-hub:${TAG}
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

USER ${NB_USER}