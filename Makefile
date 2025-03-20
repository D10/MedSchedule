PYTHON = $(shell which python3 || which python)
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9._-]+:.*?## / {printf "\033[1m\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

fmt: ## format the code
	ruff format
	isort .

lint: ruff mypy isort ## run all linters to check the code

ruff: ## run ruff
	ruff  check src

mypy: ## run mypy
	mypy src

isort: ## run isort
	isort . --check-only

test: ## run pytest
	${PYTHON} -m pytest -s tests --cov=src

fill_test_data: ## insert in db test data
	${PYTHON} deployments/data_seed/fill_db_test_data.py

run_app: ## run public-api
	${PYTHON} src/app/run.py
