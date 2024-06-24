#!/usr/bin/env bash

sleep 60

echo "Migrating DB and running server"

sleep 15 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000 &

wait