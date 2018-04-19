FROM jupyterhub/k8s-hub:36188c8
# https://hub.docker.com/r/jupyterhub/k8s-hub/

USER root

RUN pip3 --no-cache-dir install \
    git+https://github.com/consideRatio/oauthenticator

# COPY assistant.py /usr/local/bin/assistant.py
# COPY whoami.py /usr/local/bin/whoami.py
# COPY whoami-oauth.py /usr/local/bin/whoami-oauth.py

RUN pip3 install --upgrade \
    git+https://github.com/consideratio/kubespawner.git@labels-pr

USER ${NB_USER}