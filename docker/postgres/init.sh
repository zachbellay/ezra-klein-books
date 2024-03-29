#!/bin/bash
set -e

psql -v ON_ERROR_STOP=0 --username $DJANGO_POSTGRES_USER --dbname $DJANGO_POSTGRES_DB <<-EOSQL
    CREATE USER $DJANGO_POSTGRES_USER WITH PASSWORD '$DJANGO_POSTGRES_PASSWORD' LOGIN;
    CREATE DATABASE $DJANGO_POSTGRES_DB;
    GRANT ALL PRIVILEGES ON DATABASE $DJANGO_POSTGRES_DB TO $DJANGO_POSTGRES_USER;
EOSQL
