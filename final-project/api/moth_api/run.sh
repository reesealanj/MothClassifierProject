#!/bin/bash
set -e
python manage.py makemigrations users images jobs classifications ml_models
python manage.py migrate

trap 'kill %1; kill %2; kill %3' SIGINT
celery -A moth_api beat -l info >> logs/celery_beat.log 2>&1 &
celery -A moth_api worker -l info >> logs/celery_worker.log 2>&1 &
python manage.py ml_subscribe >> logs/ml_subscribe.log 2>&1 &
python manage.py runserver 0.0.0.0:8000 >> logs/server.log 2>&1
