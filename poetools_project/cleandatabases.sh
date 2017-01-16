#/bin/bash
rm -r poe/migrations/*
rm -r rango/migrations/*
rm rango.db
dropdb poe_data
createdb poe_data
python manage.py makemigrations poe
#python manage.py makemigrations rango
#python manage.py migrate poe --database poe_db
#python manage.py migrate poe --database default
python manage.py migrate --database poe_db
python manage.py migrate --database default
