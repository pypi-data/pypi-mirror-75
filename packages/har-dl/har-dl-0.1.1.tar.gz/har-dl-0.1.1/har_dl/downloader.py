import errno
from tqdm import tqdm
from pathlib import Path
from urllib.parse import urlparse, unquote, urlsplit, urlunsplit
from urllib.request import (
    ProxyHandler,
    build_opener,
    install_opener,
    urlretrieve
)
from .harfile import HARFile


class Downloader:
    def __init__(
        self,
        har_path: str,
        output_path: str,
        proxy: bool = False,
        quiet: bool = False
    ):
        self.har_path = Path(har_path)
        self.output_path = Path(output_path)

        self.proxy = proxy
        self.quiet = quiet

        self.har = HARFile(self.har_path.as_posix())

    def _error(self, name: str, message: str) -> None:
        if not self.quiet:
            tqdm.write(
                f"\n\033[93mThis is not normal, please submit an issue with "
                "this error attached. Sorry!\033[0m"
            )
            tqdm.write(f"\033[91m{name}: {message}\033[0m")

    def _create_proxy(self) -> None:
        handler = ProxyHandler()

        opener = build_opener(handler)
        # TODO: Generate a random UA instead
        opener.addheaders = [
            (
                "User-Agent",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 "
                "Safari/537.36"
            )
        ]

        install_opener(opener)

    def _download_entries(self) -> None:
        self.har.load()

        _tqdm = tqdm if not self.quiet else lambda x: x

        for entry in _tqdm(self.har.entries):
            unquoted = urlparse(unquote(entry))
            without_scheme = unquoted.geturl().replace(
                f"{unquoted.scheme}://", "", 1
            )

            filename = urlunsplit(
                urlsplit(without_scheme)._replace(query="", fragment="")
            )

            path = self.output_path.joinpath(filename)

            try:
                path.parent.mkdir(parents=True, exist_ok=True)

                if entry.endswith("/"):
                    if not path.exists():
                        path.mkdir()
                    path = path.joinpath("index.html")

                urlretrieve(entry, path.as_posix())
            except Exception as e:
                self._error(e.__class__.__name__, e)

    def download(self) -> None:
        if self.proxy:
            self._create_proxy()

        self._download_entries()
