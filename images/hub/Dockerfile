FROM jupyterhub/k8s-hub:7d17a57
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

RUN pip3 install --upgrade \
    git+https://github.com/consideratio/kubespawner.git@labels-pr

USER ${NB_USER}