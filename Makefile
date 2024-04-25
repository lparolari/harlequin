VENV_NAME = harlequin
VENV = $(shell conda info --base)/envs/$(VENV_NAME)/bin/

.PHONY: help
help:                  ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -F "##" Makefile | grep -F -v fgrep


.PHONY: fmt
fmt:                   ## Format code using black & isort.
	@$(VENV)isort *.py harlequin/
	@$(VENV)black *.py harlequin/

.PHONY: test
test:                  ## Run tests.
	$(VENV)pytest -v -l --tb=short --maxfail=1 tests/

.PHONY: test-cov
test-cov:              ## Run tests and generate coverage report.
	$(VENV)pytest -v --cov-config .coveragerc --cov=harlequin -l --tb=short --maxfail=1 tests/
	$(VENV)coverage html

.PHONY: virtualenv
virtualenv:            ## Create a virtual environment.
	@echo "creating virtualenv ..."
	@conda create -n $(VENV_NAME) python=3.10 -y

.PHONY: install
install:               ## Install dependencies.
	@echo "installing dependencies ..."
	@$(VENV)pip install -r requirements.txt
	@$(VENV)pip install -r requirements.dev.txt

.PHONY: install-precommit
precommit-install:     ## Install pre-commit hooks.
	@echo "installing pre-commit hooks ..."
	@$(VENV)pre-commit install

precommit-uninstall:   ## Uninstall pre-commit hooks.
	@echo "uninstalling pre-commit hooks ..."
	@$(VENV)pre-commit uninstall