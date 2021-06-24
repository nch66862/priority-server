# priority-server
The Python/Django API to the Priority React app.

### [Site Is Live](https://nac-priority.netlify.app)

For detailed instructions, samples, and information, please visit the client repository below.

### [Link to Client Repo](https://github.com/nch66862/priority-client)

### Instructions for Local Use - Installing the server
1. Clone down the repo with `git clone git@github.com:nch66862/priority-server.git`
2. Ensure you are in the base directory (`/`) and start a new environment shell by running the command `pipenv shell`
3. Install all of the dependencies with `pipenv install`
4. Make a copy of the `.env.example` file in the base directory (`/`) and remove the .example extension.
5. Acquire an secret key for Django by running the following command in terminal:
`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
6. Paste the resulting SECRET_KEY into your new `.env` file
7. Create a database with the command `python3 manage.py migrate`
8. Seed the database with the command `sh ./seed_data.sh`. If you get a permissions error, run `sudo sh ./seed_data.sh` and enter your machine user password when prompted
9. Run the server with the command `python3 manage.py runserver`
