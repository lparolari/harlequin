# Harlequin: Color-driven Generation of Synthetic Data for Referring Expression Comprehension

[Luca Parolari](https://github.com/lparolari), [Elena Izzo](https://www.linkedin.com/in/elena-izzo-b87b69164), [Lamberto Ballan](http://www.lambertoballan.net/)

[[Paper]](todo.pdf)

![teaser.jpg](docs/teaser.jpg)

## About

Referring Expression Comprehension (REC) aims to identify a particular object in a scene by a natural language expression, and is an important topic in visual language understanding.

State-of-the-art methods for this task are based on deep learning, which generally requires expensive and manually labeled annotations. Some works tackle the problem with limited-supervision learning or relying on Large Vision and Language Models. However, the development of techniques to synthesize labeled data is overlooked. 

In this paper, we propose a novel framework that generates artificial data for the REC task, taking into account both textual and visual modalities. 
At first, our pipeline processes existing data to create variations in the annotations. 

Then, it generates an image using altered annotations as guidance. The result of this pipeline is a new dataset, called *Harlequin*, made by more than 1M queries. 

This approach eliminates manual data collection and annotation, enabling scalability and facilitating arbitrary complexity.

We pre-train two REC models on Harlequin, then fine-tuned and evaluated on human-annotated datasets. Our experiments show that the pre-training on artificial data is beneficial for performance.

## Our pipeline

![docs/pipeline.jpg](docs/pipeline.jpg)

## Usage

TBD: installation?

```python
from harlequin import Harlequin

harlequin = Harlequin(
    "data/harlequin/images",
    "data/harlequin/annotations/instances_test.json"
)

print(len(harlequin))  # 13434
```

## Data

We release Harlequin annotations and images at this link: [[Google Drive]](https://drive.google.com/drive/folders/138PNh5tBOPM8eBlpS6hfN1e_6NYvkz4I?usp=sharing).

Harlequin is exported in coco format, and provides three annotations file in the `annotations` folder, while images are in the `images` folder.

```
data
`-- harlequin
    |-- annotations
    |   |-- instances_train.json
    |   |-- instances_val.json
    |   `-- instances_test.json
    `-- images
```

You can download it in the `data` folder.

## Setup

> **NOTE**: if you want to contribute, please see Sec. [Development](#development). The following instuctions are for a production environment (e.g. cluster).

### Requirements

* Python 3.10
* Anaconda (we suggest [Miniconda](https://docs.anaconda.com/free/miniconda/index.html))

```
pip install -r requirements.txt
```

Our code uses in PyTorch 2 and Pytorch Lightning 2.

## Development

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file to setup a development environment and submit your contribution.

This repository is structured as follows:

- `data` contains datasets (images, annotations, etc)
- `docs` contains documentation about the project
- `notebooks` contains `*.ipynb` files
- `harlequin` is the main package
- `tests` contains possible unit tests
- `tools` contains useful scripts and commands for the project

### Utils

Our [Makefile](Makefile) provides some utilities for testing and formatting the code:

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

Specifically, 

* `test` runs pytest and executes all the unit tests listed in [`tests`](tests) folder
* `fmt` formats the code using black and organizes the import though `isort`

**Manual commands**

If you want to manually run those utilities use:

* `pytest -v --cov-config .coveragerc --cov=harlequin -l --tb=short --maxfail=1 tests/` for testing
* `coverage html` for the coverage report
* `isort *.py harlequin/` to organize imports
* `black *.py harlequin/` for the code style

## Citation

```
TODO
```
