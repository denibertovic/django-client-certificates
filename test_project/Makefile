MANAGE=python manage.py
PROJECT_NAME=project
SETTINGS=--settings=$(PROJECT_NAME).settings.test

FLAKE8_OPTS=--exclude=.git,migrations --max-complexity=10

DOCKER_VERSION=0.6.5
DATA_DIR="__data"
POSTGRES_VERSION=9.3
PORT=5432

.PHONY: all test coverage clean requirements update \
	ensure_virtualenv reqs dev-setup \
	docker-check docker-version postgres
all: coverage

test:
	$(MANAGE) test --where=. $(SETTINGS) --with-xunit --nocapture

coverage:
	$(MANAGE) test --where=. $(SETTINGS) \
		--with-xcoverage --with-xunit --cover-html  --cover-erase

clean:
	rm -rf .coverage cover nosetests.xml coverage.xml
	rm -rf $(PROJECT_NAME)/static/CACHE
	find . -name '*.pyc' -exec rm '{}' ';'

lint:
	flake8 $(FLAKE8_OPTS) .

ensure_virtualenv:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "Please run me inside virtualenv.";  \
		exit 1; \
	fi

reqs: ensure_virtualenv
	pip install -r requirements.txt

dev-setup: ensure_virtualenv reqs
	if [ ! -f $(PROJECT_NAME)/settings/local.py ]; then \
		echo 'from .dev import *' > $(PROJECT_NAME)/settings/local.py; \
	fi
	$(MANAGE) syncdb --all
	$(MANAGE) migrate --fake

test-setup: ensure_virtualenv reqs/test

dev-update: ensure_virtualenv reqs/dev
	$(MAKE) update

prod-update: ensure_virtualenv reqs/prod
	$(MAKE) update

update: ensure_virtualenv
	$(MAKE) clean
	$(MANAGE) syncdb
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput


docker-check:
	@command -v docker >/dev/null 2>&1 || \
		{ echo >&2 "Docker needs to be installed and on your PATH.  Aborting."; exit 1; }

docker-version: docker-check
	@if ! docker version | grep "Server version" | grep $(DOCKER_VERSION) > /dev/null; \
		then \
			echo "ERROR: Wrong docker version. Recommended version: $(DOCKER_VERSION)"; \
			exit 1; \
	fi

postgres: docker-version
	@if nmap -PS localhost | grep -q $(PORT); then \
		echo "ERROR: Port $(PORT) is already in use..."; \
		echo "Maybe Postgres is already running?!"; \
		exit 1; \
	fi
	@if [ ! -d $(DATA_DIR)/postgresql ]; then \
		echo 'Preparing Postgres persistent data storage...'; \
		mkdir -p $(DATA_DIR); \
		docker run -v $$PWD/$(DATA_DIR):/tmp/$(DATA_DIR) -i -t \
			denibertovic/postgres:$(POSTGRES_VERSION)\
			/bin/bash -c "cp -rp var/lib/postgresql /tmp/$(DATA_DIR)"; \
	fi
	@echo "Persistent data storage found.";
	@echo "Starting postgres...";
	@docker run -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -d -p $(PORT):$(PORT) \
		denibertovic/postgres:$(POSTGRES_VERSION) /usr/local/bin/start_postgres.sh;
