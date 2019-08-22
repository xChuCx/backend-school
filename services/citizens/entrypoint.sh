#!/bin/sh

echo "Waiting for couch..."

while ! nc -z couch 8091; do
  sleep 0.1
done

echo "Couch started"

sleep 10

gunicorn -c gconfig.py manage:app

