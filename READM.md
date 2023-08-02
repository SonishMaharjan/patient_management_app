Create virtualenv

python3.10 -m venv env

Run virtual env
source env/bin/activate

Install dependencies
pip install -r requirements.txt

Run application
flask run

Initialize migration
flask db init // setups alembic

flask db migrate

flask db upgrade

