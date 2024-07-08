#!/usr/bin/env bash

echo "Waiting 35 seconds..."

sleep 35

echo "Migrating DB and running server"

echo "Waiting 10 seconds..."

sleep 10 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py seed && python3 manage.py runserver 0.0.0.0:8000 &

wait