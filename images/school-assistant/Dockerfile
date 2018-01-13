#FROM python:3.6.4-alpine3.7
FROM alpine:3.7

# basic flask environment
RUN apk add --no-cache bash git nginx uwsgi uwsgi-python3 \
	&& pip3 install --upgrade pip \
	&& pip3 install flask

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R
VOLUME [${APP_DIR}]
WORKDIR ${APP_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini
COPY entrypoint.sh /entrypoint.sh

COPY app.py app.py

# exectute start up script
CMD ["/entrypoint.sh"]
