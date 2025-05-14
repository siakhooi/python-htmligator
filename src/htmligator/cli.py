from htmligator.exception import (
    PathIsNotAFolderError,
    PathNotFoundError,
    TooManyZipFilesError,
)
from htmligator.htmligator import htmligator
import argparse
import sys


def print_to_stderr_and_exit(e, exit_code):
    print(f"Error: {e.message}", file=sys.stderr)
    exit(exit_code)


def run():
    parser = argparse.ArgumentParser(
        description="generate wrapper html files to navigate folder contents"
    )

    parser.add_argument(
        "folder_name", help="folder to start create HTML files"
    )  # NoQA: E501

    args = parser.parse_args()

    try:
        htmligator(args.folder_name)
    except PathNotFoundError as e:
        print_to_stderr_and_exit(e, 1)
    except PathIsNotAFolderError as e:
        print_to_stderr_and_exit(e, 2)
    except TooManyZipFilesError as e:
        print_to_stderr_and_exit(e, 3)
    except Exception as e:
        print_to_stderr_and_exit(e, 4)
