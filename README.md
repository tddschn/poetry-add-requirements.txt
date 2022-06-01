# poetry-add-requirements.txt

Add dependencies specified in requirements.txt to your Poetry project

- [poetry-add-requirements.txt](#poetry-add-requirementstxt)
  - [Features](#features)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Usage](#usage)
  - [Develop](#develop)

## Features

- Auto detect charset of requirements.txt file(s) and feed normalized dependency specs to `poetry`.
- Stop on first `poetry add` error.
## Installation

### pipx

This is the recommended installation method.

```
$ pipx install poetry-add-requirements.txt
```

### [pip](https://pypi.org/project/poetry-add-requirements.txt/)

```
$ pip install poetry-add-requirements.txt
```

## Usage

Run `poetry-add-requirements.txt`, optionally specify your requirements.txt files and `--dev` for dev dependencies.

`poeareq` is provided is an alias to `poetry-add-requirements.txt`.

```
$ poeareq --help

usage: poeareq [-h] [-D] [requirements.txt files ...]

Add dependencies specified in requirements.txt to your Poetry project

positional arguments:
  requirements.txt file(s)
                        Path(s) to your requirements.txt file(s) (default: requirements.txt)

options:
  -h, --help            show this help message and exit
  -D, --dev             Add to development dependencies (default: False)
```


## Develop

```
$ git clone https://github.com/tddschn/poetry-add-requirements.txt.git
$ cd poetry-add-requirements.txt
$ poetry install
```