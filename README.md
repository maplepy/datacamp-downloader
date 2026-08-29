# DataCamp Downloader

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-000000?style=for-the-badge&logo=gnubash&logoColor=white)
![DataCamp](https://img.shields.io/badge/DataCamp-03EF62?style=for-the-badge&logo=datacamp&logoColor=white)

![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-009688?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge)

> A command-line tool for downloading and organizing DataCamp course materials.

## Overview

DataCamp Downloader is a command-line tool for downloading DataCamp course
materials for personal use. It saves videos, slides, audio, exercises,
transcripts, datasets, and subtitles in an organized directory structure.

This fork adds support for current ChromeDriver installations and course slug
arguments such as `intermediate-python`.

## Features

- Download completed courses and tracks by ID.
- Download courses by slug, for example `intermediate-python`.
- Download videos, slides, audio, exercises, scripts, datasets, and subtitles.
- Resume downloads without overwriting existing files.
- Run directly from a local checkout or through the `datacamp` command.

## Prerequisites

- Python 3.10 or newer.
- Google Chrome or Chromium.
- A matching `chromedriver` on `PATH`, or a Selenium-compatible driver setup.
- A DataCamp account with access to the courses you download.

## Installation

### From PyPI

```console
python -m pip install datacamp-downloader-reborn
```

### From this checkout

This installs the local source in editable mode. It does not download the
application from PyPI:

```console
git clone https://github.com/maplepy/datacamp-downloader.git
cd datacamp-downloader
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Usage

After installation, use either the installed command or the Python module:

```console
datacamp --help
python -m datacamp_downloader --help
```

To run directly from a checkout without an editable install, make the `src`
directory importable:

```console
PYTHONPATH=src python -m datacamp_downloader --help
```

Log in with credentials:

```console
datacamp login
```

Or set the `_dct` authentication token from your browser cookies:

```console
datacamp set-token YOUR_TOKEN
```

Never share the token. It is a secret that grants access to your DataCamp
account.

List available completed courses and tracks:

```console
datacamp courses
datacamp tracks
```

Download by numeric ID, slug, or the special collection names:

```console
datacamp download 1
datacamp download intermediate-python
datacamp download all
datacamp download all-t
```

See [docs.md](docs.md) for all download options.

## Structure

```text
.
├── pyproject.toml                 # Package metadata and dependencies
├── README.md                      # Project documentation
├── docs.md                        # CLI command reference
├── .github/workflows/release.yml  # PyPI release workflow
└── src/
    └── datacamp_downloader/       # Importable Python package
        ├── __main__.py            # `python -m datacamp_downloader`
        ├── downloader.py          # CLI commands
        ├── datacamp_utils.py      # DataCamp API and download logic
        ├── session.py             # Browser session handling
        ├── helper.py              # Output and file helpers
        └── templates/             # Downloaded-content models
```

The `src` directory is a source root. The nested `datacamp_downloader`
directory is the actual Python package, which is the conventional layout for
modern Python projects and prevents accidental imports from the repository
root.

## Contributing

1. Create a branch for your change.
2. Run `python -m compileall -q src` and the CLI help command.
3. Update documentation when command behavior changes.
4. Open a pull request with a concise description and verification steps.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

Use the downloader only for content you are authorized to access, and follow
DataCamp's [Terms of Use](https://www.datacamp.com/terms-of-use/).
