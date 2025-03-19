#! /usr/bin/env bash

set -e

python /app/app/celery/...


celery -A app.celery.worker worker --loglevel=INFO -Q main-queue