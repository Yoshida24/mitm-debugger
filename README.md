# preset-python-venv

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=686856069&skip_quickstart=true)

Preset for development on Python using venv.

**included:**
- Lint and Format
- Task runner
- Env support

## Usage

depends on:
- Python: 3.11.2
- pip: 22.3.1
- GNU Make: 3.81

support:
- OS: M1 Macbook Air Ventura 13.4.1


## Gettig Started
First of all, install VSCode recommended extensions. This includes Linter, Formatter, and so on. Recommendation settings is written on `.vscode/extensions.json`.

Then, install dependencies:

```bash
make setup
```

Now you can run script:

```bash
make run
```

> **Note**
This project *does not* depends on `dotenv-python`. Instead, using below script.
> `set -a && source ./.env && set +a`

## Develop App
On usual develop, first you activate `venv` first like below.

```bash
source .venv/bin/activate
```

Save requirements:

```bash
pip freeze > requirements.txt
```

Deactivate venv:

```bash
deactivate
```
