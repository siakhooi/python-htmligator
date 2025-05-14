from htmligator.cli import run

import pytest


@pytest.mark.parametrize("options", [[], ["-v"], ["-v", "-i"]])
def test_run(monkeypatch, capsys, options):
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py"] + options,
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    expected_output = ""
    expected_output += "usage: cli.py [-h] folder_name\n"
    expected_output += "cli.py: error: the following arguments are required: folder_name\n"  # noqa: E501
    captured = capsys.readouterr()
    assert captured.err == expected_output


@pytest.mark.parametrize("option_help", ["-h", "--help"])
def test_run_help(monkeypatch, capsys, option_help):
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", option_help],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    with open("tests/expected-output/cli-help.txt", "r") as f:
        expected_output = f.read()

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_run_on_special_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", "/dev/null"],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    expected_output = "Error: Path is not a folder\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output


def test_run_on_a_file(monkeypatch, capsys, tmp_path):
    p1 = tmp_path / "sample.txt"
    p1.touch()

    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", str(p1)],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    expected_output = "Error: Path is not a folder\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output


def test_run_on_not_exist_file(monkeypatch, capsys, tmp_path):
    p1 = tmp_path / "sample"

    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", str(p1)],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    expected_output = "Error: Path not found\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output
