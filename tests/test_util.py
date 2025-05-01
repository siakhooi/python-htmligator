from htmligator.util import (
    get_folder_from_arguments,
    get_file_object,
    get_folder_object,
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
