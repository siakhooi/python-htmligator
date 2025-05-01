from htmligator.htmligator import get_html_for_file, get_html_for_folder


def test_get_html_for_file():
    folder = "test_folder"
    name = "test_file.txt"
    expected_html = f'<li><a href="{folder}/{name}">{name}</a></li>'
    result = get_html_for_file(name, folder)
    assert result == expected_html


def test_get_html_for_folder():
    folder = "test_folder"
    name = "test_folder"
    expected_html = f'<li><a href="{folder}/{name}.html">{name}</a></li>'
    result = get_html_for_folder(name, folder)
    assert result == expected_html
