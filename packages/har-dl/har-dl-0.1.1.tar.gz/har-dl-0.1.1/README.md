# HAR-DL (.HAR Downloader)

Utility for downloading content from .HAR files.

## Installation

Python >=3.6 is required.

```
$ pip3 install har-dl
```

## Usage (CLI)

```
$ har-dl <har_path> <output_path> [-h] [-p] [-q]
```

### Options

`-p`, `--proxy`: Enable proxy
`-q`, `--quiet`: Disable console output

## Usage (API)

```py
from har_dl import Downloader

dl = Downloader("path/to/file.har")
dl.download(proxy=True)
```

## License

[MIT](./LICENSE)
