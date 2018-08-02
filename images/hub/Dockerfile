FROM jupyterhub/k8s-hub:d4d1fb7
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

RUN apt-get install --yes --no-install-recommends \
    vim

# RUN pip3 install --upgrade \
#     https://github.com/consideratio/kubespawner/archive/tolerations-pr.zip

COPY jupyterhub_config.py /srv/jupyterhub_config.py

USER ${NB_USER}
