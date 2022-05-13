TESTS = tests

VENV ?= .venv
CODE = tests app

DB_URI = 'sqlite+aiosqlite:///app/db/primary.db'
DB_URI_SYNC = 'sqlite:///app/db/primary.db'

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
TOKEN_TTL = 100

ADMIN_KEY='key'

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

.PHONY: test
test: ## Runs pytest
	$(VENV)/bin/pytest -v --asyncio-mode=strict tests

.PHONY: lint
lint: ## Lint code
	$(VENV)/bin/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/bin/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/bin/mypy $(CODE)
	$(VENV)/bin/black --skip-string-normalization --check $(CODE)

.PHONY: format
format: ## Formats all files
	$(VENV)/bin/isort $(CODE)
	$(VENV)/bin/black --skip-string-normalization $(CODE)
	$(VENV)/bin/autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(VENV)/bin/unify --in-place --recursive $(CODE)

.PHONY: ci
ci:	lint test ## Lint code then run tests

.PHONY: up
up:
	SECRET_KEY=$(SECRET_KEY) ALGORITHM=$(ALGORITHM) TOKEN_TTL=$(TOKEN_TTL) \
	DB_URI=$(DB_URI) DB_URI_SYNC=$(DB_URI_SYNC) ADMIN_KEY=$(ADMIN_KEY) \
	$(VENV)/bin/uvicorn --factory app:create_app --reload

.PHONY: admin
admin:
	SECRET_KEY=$(SECRET_KEY) ALGORITHM=$(ALGORITHM) TOKEN_TTL=$(TOKEN_TTL) \
	DB_URI=$(DB_URI) DB_URI_SYNC=$(DB_URI_SYNC) ADMIN_KEY=$(ADMIN_KEY) \
   	FLASK_APP=app.admin:create_admin FLASK_ENV=development flask run

.PHONY: up-docker
up-docker:
	docker-compose up