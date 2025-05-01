import sys
import os
import zipfile
from htmligator.util import get_folder_from_arguments, folder_to_list


def get_html_for_file(name, folder):
    return f'<li><a href="{folder}/{name}">{name}</a></li>'


def get_html_for_folder(name, folder):
    return f'<li><a href="{folder}/{name}.html">{name}</a></li>'


def create_html(file_list, parent_path, folder_name):
    html_file_name = os.path.join(parent_path, f"{folder_name}.html")
    with open(html_file_name, "w") as html_file:
        html_file.write("<html><body>")
        html_file.write(f"<h1>{folder_name}</h1>")
        html_file.write("<ul>")

        for item in file_list:
            if item["type"] == "file":
                html_file.write(get_html_for_file(item["name"], folder_name))
            else:
                html_file.write(get_html_for_folder(item["name"], folder_name))
                create_html(
                    item["children"],
                    os.path.join(parent_path, folder_name),
                    item["name"],
                )

        html_file.write("</ul>")
        html_file.write(f"<h1>{folder_name}</h1>")
        html_file.write("</body></html>")


def zip_folder(parent_path, list_of_files, zip_file):

    zip_path = os.path.join(parent_path, zip_file)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in list_of_files:
            file_path = os.path.join(parent_path, file)

            if os.path.isfile(file_path):
                zipf.write(file_path, os.path.basename(file_path))

            elif os.path.isdir(file_path):
                for root, _, files in os.walk(file_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, parent_path)
                        zipf.write(file_path, relative_path)


def htmligator():
    folder = get_folder_from_arguments()
    if not os.path.exists(folder):
        print(f"Error: {folder} does not exist")
        sys.exit(1)
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a folder")
        sys.exit(2)

    folder_path = os.path.abspath(folder)

    folder_name = os.path.basename(folder_path)
    parent_path = os.path.dirname(folder_path)

    file_list = folder_to_list(folder_path, folder_name)

    create_html(file_list, parent_path, folder_name)
    zip_contents = [folder_name, f"{folder_name}.html"]
    zip_folder(parent_path, zip_contents, f"{folder_name}.zip")
