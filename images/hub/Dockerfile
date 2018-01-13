ARG TAG=8b3b2ab
FROM jupyterhub/k8s-hub:${TAG}
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    flask \
    git+https://github.com/consideRatio/oauthenticator

# TEMP: Bugfixfor jupyterhub until 0.8.2 is released
RUN pip3 --no-cache-dir install \
    git+https://github.com/consideratio/jupyterhub

COPY school_assistant.py /usr/local/bin/school_assistant.py
COPY whoami.py /usr/local/bin/whoami.py
COPY whoami-oauth.py /usr/local/bin/whoami-oauth.py

USER ${NB_USER}