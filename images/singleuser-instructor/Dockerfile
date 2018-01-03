FROM consideratio/singleuser-base

USER root



ENV NBGRADER_EXCHANGE_DIR=/home/jovyan/exchange

# Update permissions to the nbgrader exchange directory
# TODO: finetune these brute permissions
chown $NB_USER:$NB_GID $NBGRADER_EXCHANGE_DIR



USER ${NB_USER}