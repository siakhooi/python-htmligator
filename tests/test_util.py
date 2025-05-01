from htmligator.util import (
    get_folder_from_arguments,
    get_file_object,
    get_folder_object,
    folder_to_list,
)

import pytest


def test_get_folder_from_arguments_no_value(monkeypatch):
    monkeypatch.setattr("sys.argv", ["htmligator.py"])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_folder_from_arguments()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_get_folder_from_arguments_many_values(monkeypatch):
    argv = ["htmligator.py", "a.json", "b.json"]
    monkeypatch.setattr("sys.argv", argv)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_folder_from_arguments()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_get_folder_from_arguments_one_value(monkeypatch):
    monkeypatch.setattr("sys.argv", ["htmligator.py", "xx"])
    assert get_folder_from_arguments() == "xx"


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
