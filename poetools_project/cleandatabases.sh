#/bin/bash
rm -r poe/migrations/*
rm -r rango/migrations/*
rm rango.db
dropdb poe_data
createdb poe_data
python /home/adam/workspace1/poe-client/poetools_project/manage.py makemigrations poe
#python /home/adam/workspace1/poe-client/poetools_project/manage.py makemigrations rango
#python manage.py migrate poe --database poe_db
#python manage.py migrate poe --database default
python /home/adam/workspace1/poe-client/poetools_project/manage.py migrate --database poe_db
python /home/adam/workspace1/poe-client/poetools_project/manage.py migrate --database default

#python manage.py loaddata --database=poe_db poe/fixtures/dumpdata.yaml
