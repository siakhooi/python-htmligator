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
