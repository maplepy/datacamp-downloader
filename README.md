# Datacamp Downloader

[![GitHub license](https://img.shields.io/github/license/maplepy/datacamp-downloader)](https://github.com/maplepy/datacamp-downloader/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/datacamp-downloader.svg)](https://pypi.org/project/datacamp-downloader/)
[![Documentation](https://img.shields.io/badge/docs-commands-informational)](https://github.com/maplepy/datacamp-downloader/blob/master/docs.md)

[![Downloads](https://pepy.tech/badge/datacamp-downloader)](https://pepy.tech/project/datacamp-downloader)
[![GitHub stars](https://img.shields.io/github/stars/maplepy/datacamp-downloader)](https://github.com/maplepy/datacamp-downloader/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/maplepy/datacamp-downloader)](https://github.com/maplepy/datacamp-downloader/network/members)
[![GitHub contributors](https://img.shields.io/github/contributors/maplepy/datacamp-downloader)](https://github.com/maplepy/datacamp-downloader/graphs/contributors)

## Table of Contents

- [Datacamp Downloader](#datacamp-downloader)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
   - [Installation](#installation)
     - [From PyPI](#from-pypi)
     - [Run from this checkout](#run-from-this-checkout)
    - [Autocompletion](#autocompletion)
  - [Documentation](#documentation)
  - [Getting Started](#getting-started)
    - [Login](#login)
    - [Download](#download)
  - [User Privacy](#user-privacy)
  - [Disclaimer](#disclaimer)

## Description

Datacamp Downloader is a command-line interface tool developed in Python
in order to help you download your completed contents on [Datacamp](https://datacamp.com)
and keep them locally on your computer.

Datacamp Downloader helps you download all videos, slides, audios, exercises, transcripts, datasets and subtitles in organized folders.

The design and development of this tool was inspired by [udacimak](https://github.com/udacimak/udacimak)

**Datacampers!**

If you find this CLI helpful, please support the developers by starring this repository.

## Installation

### From PyPI

If you use pip, you can install datacamp-downloader with:

```
pip install datacamp-downloader
```

### Run from this checkout

Clone the repository, create a virtual environment, and install the local
checkout in editable mode. This does not download the application from PyPI;
changes to the source are used immediately:

```console
git clone https://github.com/maplepy/datacamp-downloader.git
cd datacamp-downloader
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m datacamp_downloader --help
```

On Linux/macOS, you can also run directly from a checkout without an editable
install after dependencies are available:

```console
PYTHONPATH=src python -m datacamp_downloader --help
```

### Autocompletion

To allow command autocompletion with `[TAB][TAB]`, run:

```
datacamp --install-completion [bash|zsh|fish|powershell|pwsh]
```

Then restart the terminal.

**Note:** autocompletion might not be supported by all operating systems.

## Documentation

The available commands with full documentation can be found in [docs](https://github.com/maplepy/datacamp-downloader/blob/master/docs.md)

## Getting Started

### Login

- To login using your username or password, run:

```
datacamp login -u [USERNAME] -p [PASSWORD]
```

or simply run:

```
datacamp login
```

- To login using Datacamp authentication token, run:

```
datacamp set-token [TOKEN]
```

Datacamp authentication token can be found in Datacamp website browser _cookies_.
To get your Datacamp authentication, follow these steps:

**Firefox**

1. Visit [datacamp.com](https://datacamp.com) and log in.
2. Open the **Developer Tools** (press `Cmd + Opt + J` on MacOS or `F12` on Windows).
3. Go to **Storage tab**, then **Cookies** > `https://www.datacamp.com`
4. Find `_dct` key, its **Value** is the Datacamp authentication token.

**Chrome**

1. Visit [datacamp.com](https://datacamp.com) and log in.
2. Open the **Developer Tools** (press `Cmd + Opt + J` on MacOS or `F12` on Windows).
3. Go to **Application tab**, then **Storage** > **Cookies** > `https://www.datacamp.com`
4. Find `_dct` key, its **Value** is the Datacamp authentication token.

---

**Security Note**

Datacamp authentication token is a secret key and is unique to you. **You should not share it publicly**.

---

If you provided valid credentials, you should see the following:

```
Hi, YOUR_NAME
Active subscription found
```

> Active subscription is not required anymore.

### Download

First, you should list your completed courses/track.

To list your completed **courses**, run:

```
datacamp courses
```

To list your completed **tracks**, run:

```
datacamp tracks
```

Similar output to this should appear with your completed courses/tracks:

```
+--------+------------------------------------------+------------+------------+------------+
| ID     | Title                                    | Datasets   | Exercises  | Videos     |
+--------+------------------------------------------+------------+------------+------------+
| 1      | Introduction to Python                   | 2          | 46         | 11         |
+--------+------------------------------------------+------------+------------+------------+
| 2      | Introduction to SQL                      | 1          | 40         | 1          |
+--------+------------------------------------------+------------+------------+------------+
| 3      | Intermediate Python                      | 3          | 69         | 18         |
+--------+------------------------------------------+------------+------------+------------+
| 4      | Introduction to Data Science in Python   | 0          | 31         | 13         |
+--------+------------------------------------------+------------+------------+------------+
| 5      | Data Science for Everyone                | 0          | 33         | 15         |
+--------+------------------------------------------+------------+------------+------------+
| 6      | Joining Data in SQL                      | 3          | 40         | 13         |
+--------+------------------------------------------+------------+------------+------------+
| 7      | Data Manipulation with pandas            | 4          | 41         | 15         |
+--------+------------------------------------------+------------+------------+------------+
| 8      | Supervised Learning with scikit-learn    | 7          | 37         | 17         |
+--------+------------------------------------------+------------+------------+------------+
| 9      | Machine Learning for Everyone            | 0          | 25         | 12         |
+--------+------------------------------------------+------------+------------+------------+
| 10     | Python Data Science Toolbox (Part 1)     | 1          | 34         | 12         |
+--------+------------------------------------------+------------+------------+------------+
```

Now, you can download any of the courses/tracks with:

```
datacamp download id1 id2 id3
```

Course slugs work too, for example `datacamp download intermediate-python`.

For example to download the first and second course, run:

```
datacamp download 1 2
```

- To download all your completed courses, run:

```
datacamp download all
```

- To download all your completed tracks, run:

```
datacamp download all-t
```

This by default will download **videos**, **slides**, **datasets**, **exercises**, **english subtitles** and **transcripts** in organized folders in the **current directory**.

To customize this behavior see `datacamp download` command in the [docs](https://github.com/maplepy/datacamp-downloader/blob/master/docs.md).

## User Privacy

`datacamp` creates a session file in the temp folder. It stores the token but
clears the password before saving. If you no longer need to use the tool,
remove the saved session with:

```
datacamp reset
```

## Disclaimer

This CLI is provided to help you download DataCamp courses/tracks for personal use only. Sharing the content of the courses is strictly prohibited under [DataCamp's Terms of Use](https://www.datacamp.com/terms-of-use/).

By using this CLI, the developers of this CLI are not responsible for any law infringement caused by the users of this CLI.
