#!/bin/bash
set -e

flask db upgrade

gunicorn --bind :8080 --workers 2 --threads 8 --access-logfile - 'gogglekaap:create_app()'
