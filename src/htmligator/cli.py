from htmligator.exception import (
    PathIsNotAFolderError,
    PathNotFoundError,
    TooManyZipFilesError,
)
from htmligator.htmligator import Htmligator
import argparse
import sys
from importlib.metadata import version


def print_to_stderr_and_exit(e: Exception, exit_code: int) -> None:
    print(f"Error: {e.message}", file=sys.stderr)
    exit(exit_code)


def run() -> None:
    __version__: str = version("htmligator")

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="generate wrapper html files to navigate folder contents"
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "top_folder", help="folder to start create HTML files", nargs="+"
    )  # NoQA: E501

    args: argparse.Namespace = parser.parse_args()

    for folder in args.top_folder:
        htmligator: Htmligator = Htmligator()

        try:
            htmligator.htmligator(folder)
        except PathNotFoundError as e:
            print_to_stderr_and_exit(e, 1)
        except PathIsNotAFolderError as e:
            print_to_stderr_and_exit(e, 2)
        except TooManyZipFilesError as e:
            print_to_stderr_and_exit(e, 3)
        except Exception as e:
            print_to_stderr_and_exit(e, 4)
