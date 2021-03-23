.DEFAULT_GOAL := help

clean: ## Clean project files
	rm -rf *.egg-info
	rm -rf dist
	rm -rf bitrise_reports/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage.xml

setup: ## Install dependencies and configure Pyenv
	poetry update
	poetry install
	poetry config virtualenvs.in-project true

inspect: ## Run code analysis
	flake8 bitrise_reports tests
	black --check bitrise_reports tests
	bandit -r bitrise_reports

test: ## Run unit and integration tests
	poetry run pytest -vv --cov-report=xml --cov=bitrise_reports tests/

build: ## Package this project in wheels/zip formats
	poetry build

run: ## Run this project
	poetry run bitrise-reports --token=$(token) --app=$(app) --starting=$(starting) --ending=$(ending) --output=$(output)

deploy: ## Deploy the current build to Pypi
	poetry config pypi-token.pypi $(token)
	poetry build
	poetry publish

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		sort |\
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
