from htmligator.cli import run

import pytest


@pytest.mark.parametrize("option_help", ["-h", "--help"])
def test_run_help(monkeypatch, capsys, option_help):
    monkeypatch.setattr(
        "sys.argv",
        ["htmligator", option_help],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    with open("tests/expected-output/cli-help.txt", "r") as f:
        expected_output = f.read()

    captured = capsys.readouterr()
    assert captured.out == expected_output


@pytest.mark.parametrize("option_version", ["-v", "--version"])
def test_run_show_version(monkeypatch, capsys, option_version):
    monkeypatch.setattr(
        "sys.argv",
        ["htmligator", option_version],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    with open("tests/expected-output/cli-version.txt", "r") as f:
        expected_output = f.read()

    captured = capsys.readouterr()
    assert captured.out == expected_output


@pytest.mark.parametrize("options", [[], ["-p"], ["-p", "-i"]])
def test_run_wrong_options(monkeypatch, capsys, options):
    monkeypatch.setattr(
        "sys.argv",
        ["htmligator"] + options,
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    with open("tests/expected-output/cli-wrong-options.txt", "r") as f:
        expected_output = f.read()

    captured = capsys.readouterr()
    assert captured.err == expected_output


def test_run_on_special_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["htmligator", "/dev/null"],
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
        ["htmligator", str(p1)],
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
        ["htmligator", str(p1)],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    expected_output = "Error: Path not found\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output


def test_run_100_zip(monkeypatch, capsys, tmp_path):
    folder_name = "sample"
    d1 = tmp_path / folder_name
    d1.mkdir()
    p1 = tmp_path / f"{folder_name}.zip"
    p1.touch()
    for i in range(1, 100):
        p1 = tmp_path / f"{folder_name}-{i}.zip"
        p1.touch()

    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

    monkeypatch.setattr(
        "sys.argv",
        ["htmligator", str(tmp_path / folder_name)],
    )
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3
    expected_output = "Error: Too many zip files with the same name\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output
