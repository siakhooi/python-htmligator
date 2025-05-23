import os
from typing import List, Dict, Any
from htmligator.exception import TooManyZipFilesError
from natsort import natsorted


def get_file_object(name: str, path: str) -> Dict[str, str]:
    return {"name": name, "path": path, "type": "file"}


def get_folder_object(
    name: str,
    path: str,
    children: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {"name": name, "path": path, "type": "folder", "children": children}


def folder_to_list(root_path: str, relative_root: str) -> List[Dict[str, Any]]:
    file_list: List[Dict[str, Any]] = []

    items: List[str] = os.listdir(root_path)
    for item in items:
        absolute_path: str = os.path.join(root_path, item)
        relative_path: str = os.path.join(relative_root, item)
        if os.path.isfile(absolute_path):
            file_list.append(get_file_object(item, relative_path))
        elif os.path.isdir(absolute_path):
            file_list.append(
                get_folder_object(
                    item,
                    relative_path,
                    folder_to_list(absolute_path, relative_path),
                )
            )
    return natsorted(file_list, key=lambda x: x["name"])


def get_zip_path(zip_parent_path: str, folder_name: str) -> str:
    zip_name: str = f"{folder_name}.zip"

    zip_path: str = os.path.join(zip_parent_path, zip_name)
    index: int = 1
    while os.path.exists(zip_path):
        zip_name = f"{folder_name}-{index}.zip"
        zip_path = os.path.join(zip_parent_path, zip_name)
        index += 1
        if index > 100:
            raise TooManyZipFilesError()

    return zip_path
