import sys
import os
import zipfile
from htmligator.util import folder_to_list


def get_html_for_file(name, folder):
    return f'<li><a href="{folder}/{name}">{name}</a></li>'


def get_html_for_folder(name, folder):
    return f'<li><a href="{folder}/{name}.html">{name}</a></li>'


def generate_html_files(html_files, file_list, folder_name, parent_path=""):
    html_file_name = os.path.join(parent_path, f"{folder_name}.html")
    file_contents = ""
    file_contents += "<html><body>"
    file_contents += f"<h1>{folder_name}</h1>"
    file_contents += "<ul>"

    for item in file_list:
        if item["type"] == "file":
            file_contents += get_html_for_file(item["name"], folder_name)
        else:
            file_contents += get_html_for_folder(item["name"], folder_name)
            generate_html_files(
                html_files,
                item["children"],
                item["name"],
                os.path.join(parent_path, folder_name)
            )

    file_contents += "</ul>"
    file_contents += f"<h1>{folder_name}</h1>"
    file_contents += "</body></html>"
    html_files.append({"name": html_file_name, "contents": file_contents})


def zip_folder(parent_path, folder_name, html_files, zip_file):

    zip_path = os.path.join(parent_path, zip_file)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        file_path = os.path.join(parent_path, folder_name)
        for root, _, files in os.walk(file_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, parent_path)
                zipf.write(file_path, relative_path)
        for file in html_files:
            zipf.writestr(file["name"], file["contents"])


def htmligator(folder):
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

    html_files = []
    generate_html_files(html_files, file_list, folder_name)

    zip_folder(parent_path, folder_name, html_files, f"{folder_name}.zip")
