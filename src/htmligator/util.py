import os
from natsort import natsorted


def get_file_object(name, path):
    return {"name": name, "path": path, "type": "file"}


def get_folder_object(name, path, children):
    return {"name": name, "path": path, "type": "folder", "children": children}


def folder_to_list(root_path, relative_root):
    file_list = []

    items = os.listdir(root_path)
    for item in items:
        absolute_path = os.path.join(root_path, item)
        relative_path = os.path.join(relative_root, item)
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


def get_zip_path(zip_parent_path, folder_name):
    zip_name = f"{folder_name}.zip"

    zip_path = os.path.join(zip_parent_path, zip_name)
    index = 1
    while os.path.exists(zip_path):
        zip_name = f"{folder_name}-{index}.zip"
        zip_path = os.path.join(zip_parent_path, zip_name)
        index += 1
        if index > 100:
            raise RuntimeError(
                "Error: Too many zip files with the same name. "
                "Please remove or rename the existing zip files."
            )

    return zip_path
