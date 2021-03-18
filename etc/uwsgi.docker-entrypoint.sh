#!/bin/bash
set -e

flask db upgrade
uwsgi ./etc/uwsgi/uwsgi.ini
