#!/bin/sh
echo "Waiting for MySQL to be available..."
while ! nc -z db 3306
do
  sleep 1
  echo "Waiting..."
done
echo "MySQL is up!"
exec "$@"
