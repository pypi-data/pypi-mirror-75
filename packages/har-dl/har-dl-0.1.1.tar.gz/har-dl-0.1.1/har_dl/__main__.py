import sys
import argparse
from . import Downloader


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("har_path", type=str, help="The path to the .HAR file")
    ap.add_argument(
        "output_path",
        type=str,
        help="The path to the output directory"
    )
    ap.add_argument("-p", "--proxy", action="store_true", help="Enables the proxy")
    ap.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Disables console output"
    )

    args = vars(ap.parse_args())

    dl = Downloader(**args)
    dl.download()


if __name__ == "__main__":
    main()
