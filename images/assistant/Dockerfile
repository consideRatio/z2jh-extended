FROM tiangolo/uwsgi-nginx-flask:python3.6

# --- Install JupyterHub and dependencies, for the HubAuth module.
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    apt update && apt install -y nodejs

# TEMP: Bugfixfor jupyterhub until 0.8.2 is released, then use jupyterhub
RUN pip --no-cache-dir install \
    jupyterhub
# -----------------------------------------------------------------------------

RUN echo update plz
COPY ./app /app