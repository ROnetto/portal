# portal

Requirements:
- Python 3.7
- Mysql

Installation

Create a virtual env:
python3 -m venv <env_name>

Activate virtual env:
source <env_name>/bin/activate

Install libraries:
pip install -r requirements.py

Database:
Set your database in portal/settings.py

Migrations:
python manage.py makemigrations
python manage.py migrate

Create a superuser:
python manage.py createsuperuser

Run local server:
python manage.py runserver 0.0.0.0:<port>
