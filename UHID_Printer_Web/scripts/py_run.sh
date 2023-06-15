#!/bin/sh

set -e


python manage.py collectstatic --noinput

uwsgi --ini /uhid_label_printer/uwsgi/uwsgi.ini
