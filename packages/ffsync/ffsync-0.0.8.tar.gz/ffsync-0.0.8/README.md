# FFsync
A simple package that uses Argus to sync two videos

![Python package](https://github.com/bchaselab/ffsync/workflows/Python%20package/badge.svg) ![PyPI](https://img.shields.io/pypi/v/sync2vids) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)  [![Maintainability](https://api.codeclimate.com/v1/badges/1d1123518f797046b996/maintainability)](https://codeclimate.com/github/bchaselab/ffsync/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/524a6f629e1642e082167343b606b703)](https://app.codacy.com/gh/bchaselab/ffsync?utm_source=github.com&utm_medium=referral&utm_content=bchaselab/ffsync&utm_campaign=Badge_Grade_Dashboard)

## Install
```bash
$ pip install ffsync
```

## Usage
```python
>>> from ffsync import sync
>>> ffsync.sync(argus_sync_csv_file, videos_directory)
```

