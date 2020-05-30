.PHONY: clean system-packages python-packages python-setup db-init db-migrate db-upgrade install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

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

seed-admin:
	python3 manage.py seed_admin

install: system-packages python-packages python-setup db-init db-migrate db-upgrade

tests:
	python3 manage.py test

run:
	python3 manage.py run

all: clean install tests run
