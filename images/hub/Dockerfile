FROM jupyterhub/k8s-hub:36a8dcb
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

RUN pip3 install --upgrade \
    git+https://github.com/jupyterhub/kubespawner.git    

USER ${NB_USER}