FROM jupyter/minimal-notebook:8a1b90cbcba5
# Build from... https://hub.docker.com/r/jupyter/minimal-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/minimal-notebook/Dockerfile
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 16.04

# kubespawner requires the singleuser image to be started with a script
# provided by the jupyterhub package, and will hence override the CMD with 
# ["jupyterhub-singleuser"] instead of the jupyter/docker-stacks images CMD
# of ["start-notebook.sh"]
ARG JUPYTERHUB_VERSION=0.8.*
RUN pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION



# nodejs
USER root
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - && \
    apt-get install -y nodejs
USER ${NB_USER}



# conda packages
RUN conda install -y -c conda-forge -c damianavila82 \
    jupyterlab \
    numpy \
    sympy \
    ipyvolume \
    ipywidgets \
    seaborn \
    bokeh \
    altair \
    rise
    # nbgrader \  # excluded until successful usage demonstrated



# pip packages
RUN pip --no-cache-dir install \
    git+https://github.com/data-8/nbgitpuller \
    plotly \
    bqplot

# more pip packages
RUN pip --no-cache-dir install \
    jupyter_contrib_nbextensions \
    jupyterlab_iframe \
    jupyterlab_latex

# Removed...
#    jupyterlab_github \
#    jupyterlab_templates \
#    jupyterlab-discovery 



# extensions
RUN jupyter serverextension enable --sys-prefix --python nbgitpuller

# modern jupyterlab extensions
RUN jupyter labextension install @jupyterlab/hub-extension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install @mflevine/jupyterlab_html && \
    jupyter labextension install @jupyterlab/latex && \
    jupyter serverextension enable --sys-prefix jupyterlab_latex && \    
    jupyter labextension install @jupyterlab/plotly-extension && \
    jupyter labextension install jupyterlab_bokeh && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install bqplot 

# Removed...
#    jupyter labextension install jupyterlab_iframe && \
#    jupyter serverextension enable --py jupyterlab_iframe && \
#    jupyter labextension install @jupyterlab/github && \
#    jupyter serverextension enable --sys-prefix jupyterlab_github && \
#    jupyter labextension install jupyterlab_templates && \
#    jupyter serverextension enable --py jupyterlab_templates && \
#    jupyter serverextension enable --sys-prefix jupyterlab_discovery && \

# classical notebook extensions
RUN jupyter nbextension enable --sys-prefix comment-uncomment/main && \
    jupyter nbextension enable --sys-prefix hide_input/main && \
    jupyter nbextension enable --sys-prefix splitcell/splitcell && \
    jupyter nbextension enable --sys-prefix tree-filter/index && \
    jupyter nbextension enable --sys-prefix rubberband/main && \
    jupyter nbextension enable --sys-prefix toc2/main && \
    jupyter nbextension enable --sys-prefix export_embedded/main && \
    jupyter nbextension enable --sys-prefix hide_header/main



# startup scripts
COPY start pre-startup-bash pre-startup-python /usr/local/bin/


RUN pip --no-cache-dir install --upgrade https://github.com/consideratio/nbgitpuller/archive/jupyterlab-pr.zip
