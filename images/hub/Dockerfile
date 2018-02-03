FROM jupyterhub/k8s-hub:v0.6
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    flask \
    git+https://github.com/consideRatio/oauthenticator

COPY assistant.py /usr/local/bin/assistant.py
COPY whoami.py /usr/local/bin/whoami.py
COPY whoami-oauth.py /usr/local/bin/whoami-oauth.py

USER ${NB_USER}