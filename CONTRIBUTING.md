# How to develop on this project

## TL;DR

1. Create a branch `git checkout -b my-contribution`
2. Add your contribution
3. Run the code formatter with `make fmt`
4. Ensure everything is okay with `make test`
5. Commit (follow [conventional git commit messages](https://www.conventionalcommits.org/en/v1.0.0/) 🙏)
6. Push with `git push origin my-contribution`
7. Create a pull request from the [github interface](https://github.com/lparolari/harlequin)

## Setting up your own virtual environment

You can easily setup your environment through the following two commands:

```
make virtualenv
make install
```

Requirements: 
- `make`
- `conda`

The `make virtualenv` automatically creates a virtualenv for this project, named `harlequin`. The `make install` command instead installs project requirements. 

*Optional*: You may chose to install pre-commit hooks. Hooks are actions executed once events happen (e.g. commit). We defined some hooks that run before commit to ensure code consistency. In particular, we run a code formatter and execute unit test.

### Manual setup (NOT ROCOMMENDED)

> Skip this section if the previous worked

In some cases you might want to manually setup the environment (e.g. if you are on another OS, if you don't want to follow some of ours conventions):

1. Create the virtualenv

```
conda create -n harlequin python=3.10
```

You may also use `venv`:

```
python -m virtualen venv
source venv/bin/activate
```

In this case ensure that your Python version is at least 3.10.

2. Install prject requirements (and development requirements)

```
pip -r requirements.dev.txt
pip -r requirements.txt
```

3. (Optional) Install commit hooks

Commit message hooks

```
pre-commit install --hook-type commit-msg
```

Pre-commit hooks (not recommended if `make fmt` and `make test` do not work, you may become unable to commit)

```
pre-commit install --hook-type pre-commit
```

## Run the tests to ensure everything is working

Run `make test` to run the tests.

## Create a new branch to work on your contribution

Run `git checkout -b my-contribution`

The branch name should be something meaningful, related to the contribution you are developing. We do not follow strict convention on branch's names but the following will be appreciated: `feature/cross-attention`, `fix/bb-post-processing`.

## Make your changes

Edit the files using your preferred editor. We suggest vscode.

## Format the code

Run `make fmt` to format the code.

## Test your changes

Run `make test` to run the tests.

## Commit your changes

This project uses [conventional git commit messages](https://www.conventionalcommits.org/en/v1.0.0/). 

Example: `fix(package): update setup.py arguments 🎉` (emojis are fine too)

On each commit we run some hooks to enforce code style, test the code and format the commit message. However, those conventions are not strictly mandatory, you may skip pre-commit hooks through the `--no-verify` option.


## Push your changes to your fork

Run `git push origin my-contribution`

Use meaningful names for your branches, e.g. `feature/my-new-dataset` if you are implementing a new dataset. 

## Submit a pull request

On github interface, click on `Pull Request` button.

## Makefile utilities

This project comes with a `Makefile` that contains a number of useful utility.

```bash 
❯ make
Usage: make <target>

Targets:
help:                  ## Show the help.
fmt:                   ## Format code using black & isort.
test:                  ## Run tests.
test-cov:              ## Run tests and generate coverage report.
virtualenv:            ## Create a virtual environment.
install:               ## Install dependencies.
precommit-install:     ## Install pre-commit hooks.
precommit-uninstall:   ## Uninstall pre-commit hooks.
```