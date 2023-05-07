#!/bin/sh
set -e
service ssh start
# exec python -m flask run --host=0.0.0.0
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app