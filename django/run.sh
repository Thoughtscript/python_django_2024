#!/usr/bin/env bash

echo "Waiting 25 seconds..." && sleep 25 && echo "Migrating DB and running server" && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py seed &

# https://dev.to/pragativerma18/unlocking-performance-a-guide-to-async-support-in-django-2jdj
# https://www.uvicorn.org/settings/#application
echo "Waiting 25 seconds..." && sleep 25 && echo "Waiting 5-10 seconds..." && sleep 10 && uvicorn djangoexample.asgi:application --host 0.0.0.0 --port 8000 --workers 4 & 

wait