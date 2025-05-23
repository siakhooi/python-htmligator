import os
import zipfile
from typing import List, Dict, Any
from htmligator.exception import PathIsNotAFolderError, PathNotFoundError
from htmligator.util import folder_to_list, get_zip_path
from htmligator.html import (
    get_html_for_file,
    get_html_for_folder,
    get_html_for_header,
    get_html_for_footer,
)


class Htmligator:
    def generate_html_files(
        self,
        html_files: List[Dict[str, str]],
        file_list: List[Dict[str, Any]],
        folder_name: str,
        parent_path: str = "",
    ) -> None:
        html_file_name: str = os.path.join(parent_path, f"{folder_name}.html")

        file_contents: str = get_html_for_header(folder_name)

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

    def zip_folder(
        self,
        parent_path: str,
        folder_name: str,
        html_files: List[Dict[str, str]],
        zip_path: str,
    ) -> None:

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_path: str = os.path.join(parent_path, folder_name)
            for root, _, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, parent_path)
                    zipf.write(file_path, relative_path)
            for file in html_files:
                zipf.writestr(file["name"], file["contents"])

    def htmligator(self, folder: str) -> None:
        if not os.path.exists(folder):
            raise PathNotFoundError()
        if not os.path.isdir(folder):
            raise PathIsNotAFolderError()

        folder_path: str = os.path.abspath(folder)

        folder_name: str = os.path.basename(folder_path)
        parent_path: str = os.path.dirname(folder_path)

        zip_path: str = get_zip_path(os.getcwd(), folder_name)

        file_list: List[Dict[str, Any]] = folder_to_list(
            folder_path, folder_name
        )

        html_files: List[Dict[str, str]] = []
        self.generate_html_files(html_files, file_list, folder_name)

        self.zip_folder(parent_path, folder_name, html_files, zip_path)
