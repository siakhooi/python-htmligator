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
