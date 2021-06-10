#!/bin/bash
# type this (sh ./seed_data.sh) into terminal to run

rm db.sqlite3
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata priority_users
python manage.py loaddata priorities
python manage.py loaddata subscriptions
python manage.py loaddata affirmations
python manage.py loaddata whats
python manage.py loaddata histories