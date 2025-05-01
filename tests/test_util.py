from htmligator.util import get_folder_from_arguments

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
