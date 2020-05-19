.PHONY: clean system-packages python-packages install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	pip install -r requirements.txt

tests:
	python manage.py test

lint:
	pylint ./app

lint-fix:
	autopep8 --in-place --aggressive --aggressive ./app/**/*.py

run:
	python manage.py run

all: clean install tests run
