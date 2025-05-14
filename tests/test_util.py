from htmligator.exception import TooManyZipFilesError
from htmligator.util import (
    get_file_object,
    get_folder_object,
    folder_to_list,
    get_zip_path,
)
import os
import pytest


def test_get_file_object():
    name = "name.txt"
    path = "xx/xx/name.txt"
    assert get_file_object(name, path) == {
        "name": name,
        "path": path,
        "type": "file",
    }


def test_get_folder_object():
    name = "name"
    path = "xx/xx/name"
    children = [
        {"name": "name1.txt", "path": "xx/xx/name/name1.txt", "type": "file"},
        {"name": "name2.txt", "path": "xx/xx/name/name2.txt", "type": "file"},
    ]
    assert get_folder_object(name, path, children) == {
        "name": name,
        "path": path,
        "type": "folder",
        "children": children,
    }


def test_folder_to_list(tmp_path):
    d1 = tmp_path / "sub1"
    d1.mkdir()
    p1 = d1 / "h1.txt"
    p1.write_text("content", encoding="utf-8")
    d2 = tmp_path / "sub2"
    d2.mkdir()
    p2 = d2 / "h2.txt"
    p2.write_text("content", encoding="utf-8")

    root_path = tmp_path
    relative_root = "sample1"

    folder_to_list_result = folder_to_list(root_path, relative_root)
    assert len(folder_to_list_result) == 2
    assert (folder_to_list_result[0]) == {
        "children": [
            {
                "name": "h1.txt",
                "path": "sample1/sub1/h1.txt",
                "type": "file"
            }],
        "name": "sub1",
        "path": "sample1/sub1",
        "type": "folder",
    }
    assert (folder_to_list_result[1]) == {
        "children": [
            {
                "name": "h2.txt",
                "path": "sample1/sub2/h2.txt",
                "type": "file"
            }],
        "name": "sub2",
        "path": "sample1/sub2",
        "type": "folder",
    }


def test_get_zip_path(tmp_path):
    folder_name = "sample"
    zip_path = get_zip_path(tmp_path, folder_name)

    assert zip_path == os.path.join(tmp_path, f"{folder_name}.zip")


def test_get_zip_path_1(tmp_path):
    folder_name = "sample"
    p1 = tmp_path / f"{folder_name}.zip"
    p1.touch()

    zip_path = get_zip_path(tmp_path, folder_name)

    assert zip_path == os.path.join(tmp_path, f"{folder_name}-1.zip")


def test_get_zip_path_3(tmp_path):
    folder_name = "sample"
    p1 = tmp_path / f"{folder_name}.zip"
    p1.touch()
    p1 = tmp_path / f"{folder_name}-1.zip"
    p1.touch()
    p1 = tmp_path / f"{folder_name}-2.zip"
    p1.touch()

    zip_path = get_zip_path(tmp_path, folder_name)

    assert zip_path == os.path.join(tmp_path, f"{folder_name}-3.zip")


def test_get_zip_path_100(tmp_path):
    folder_name = "sample"
    p1 = tmp_path / f"{folder_name}.zip"
    p1.touch()
    for i in range(1, 100):
        p1 = tmp_path / f"{folder_name}-{i}.zip"
        p1.touch()

    with pytest.raises(TooManyZipFilesError):
        get_zip_path(tmp_path, folder_name)
