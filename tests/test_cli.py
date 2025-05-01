def test_run(mocker):
    mock = mocker.patch("htmligator.htmligator.htmligator")

    from htmligator.cli import run

    run()

    mock.assert_called_once()
