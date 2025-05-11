from htmligator.htmligator import htmligator
import argparse


def run():
    parser = argparse.ArgumentParser(
        description="generate wrapper html files to navigate folder contents"
    )

    parser.add_argument("folder_name", help="folder to start create HTML files")  # NoQA: E501

    args = parser.parse_args()

    htmligator(args.folder_name)
