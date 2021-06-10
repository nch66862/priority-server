# Takes data from the database and creates fixture data for each table and puts the files in the root directory
# run sh ./fetch_data.sh from the terminal in the root directory
# it puts the .json files in the fetched_fixtures directory

python3 manage.py dumpdata auth.user --indent 4 > ./fetched_fixtures/users.json
python3 manage.py dumpdata authtoken.token --indent 4 > ./fetched_fixtures/tokens.json
python3 manage.py dumpdata priorityapi.affirmation --indent 4 > ./fetched_fixtures/affirmations.json
python3 manage.py dumpdata priorityapi.history --indent 4 > ./fetched_fixtures/histories.json
python3 manage.py dumpdata priorityapi.priorityuser --indent 4 > ./fetched_fixtures/priority_users.json
python3 manage.py dumpdata priorityapi.priority --indent 4 > ./fetched_fixtures/priorities.json
python3 manage.py dumpdata priorityapi.subscription --indent 4 > ./fetched_fixtures/subscriptions.json
python3 manage.py dumpdata priorityapi.what --indent 4 > ./fetched_fixtures/whats.json