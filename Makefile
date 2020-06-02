.PHONY: clean system-packages python-packages python-setup db-init db-migrate db-upgrade install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	rm -rf instance/*
	rm -rf migrations
	rm -rf flask_qldb_boilerplate.egg-info

system-packages:
	#sudo apt install python-pip -y

python-packages:
	pip3 install -r requirements.txt

python-setup:
	pip3 install -e .

db-init:
	python3 manage.py db init

db-migrate:
	python3 manage.py db migrate --message "${message:='database migration'}"

db-upgrade:
	python3 manage.py db upgrade

seed-users:
	python3 manage.py seed_users

install: clean system-packages python-packages python-setup db-init db-migrate db-upgrade seed-users

tests:
	python3 manage.py test

run:
	python3 manage.py run

qldb-migrate:
	python3 manage.py qldb_migrate -d $(direction)

all: clean install tests run
