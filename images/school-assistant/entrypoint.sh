#!/bin/bash
if [ -e /debug0 ]; then
	echo "Running app in debug mode!"
	python3 app.py
else
	echo "Running app in production mode!"
	nginx && uwsgi --ini /app.ini
fi