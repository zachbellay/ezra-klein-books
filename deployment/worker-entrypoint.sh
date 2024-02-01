#!/bin/sh
celery -A mysite worker --beat -l INFO --concurrency=1 --scheduler django_celery_beat.schedulers:DatabaseScheduler