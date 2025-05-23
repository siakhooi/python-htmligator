import os
import zipfile
from htmligator.exception import PathIsNotAFolderError, PathNotFoundError
from htmligator.util import folder_to_list, get_zip_path
from htmligator.html import (
    get_html_for_file,
    get_html_for_folder,
    get_html_for_header,
    get_html_for_footer,
)


class Htmligator:
    def generate_html_files(self, html_files,
                            file_list, folder_name, parent_path=""):
        html_file_name = os.path.join(parent_path, f"{folder_name}.html")

        file_contents = get_html_for_header(folder_name)

        for item in file_list:
            if item["type"] == "file":
                file_contents += get_html_for_file(item["name"], folder_name)
            else:
                file_contents += get_html_for_folder(item["name"], folder_name)
                self.generate_html_files(
                    html_files,
                    item["children"],
                    item["name"],
                    os.path.join(parent_path, folder_name),
                )

        file_contents += get_html_for_footer(folder_name)

        html_files.append({"name": html_file_name, "contents": file_contents})

    def zip_folder(self, parent_path, folder_name, html_files, zip_path):

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_path = os.path.join(parent_path, folder_name)
            for root, _, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, parent_path)
                    zipf.write(file_path, relative_path)
            for file in html_files:
                zipf.writestr(file["name"], file["contents"])

    def htmligator(self, folder):
        if not os.path.exists(folder):
            raise PathNotFoundError()
        if not os.path.isdir(folder):
            raise PathIsNotAFolderError()

        folder_path = os.path.abspath(folder)

        folder_name = os.path.basename(folder_path)
        parent_path = os.path.dirname(folder_path)

        zip_path = get_zip_path(os.getcwd(), folder_name)

        file_list = folder_to_list(folder_path, folder_name)

        html_files = []
        self.generate_html_files(html_files, file_list, folder_name)

        self.zip_folder(parent_path, folder_name, html_files, zip_path)
