FROM jupyterhub/k8s-hub:1898e3b
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

RUN apt-get install --yes --no-install-recommends \
    vim

RUN pip3 install --upgrade \
    https://github.com/minrk/kubespawner/archive/deprecate-config.zip

COPY temp_jupyterhub_config.py /srv/jupyterhub_config.py

USER ${NB_USER}