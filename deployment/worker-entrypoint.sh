#!/bin/sh
celery -A mysite worker --beat -l INFO
