#!/bin/sh
makemigrations.sh
echo 'Executando script migrate.sh'
python manage.py migrate --noinput