from htmligator.htmligator import (
    get_html_for_file,
    get_html_for_folder,
    create_html,
)  # noqa: E501


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


def test_create_html(tmp_path):
    d1 = tmp_path / "sample1"
    d1.mkdir()
    file_list = [
        {"name": "file1.txt", "type": "file"},
        {"name": "file2.txt", "type": "file"},
        {
            "name": "folder1",
            "type": "folder",
            "children": [
                {"name": "file3.txt", "type": "file"},
                {"name": "file4.txt", "type": "file"},
            ],
        },
    ]
    parent_path = tmp_path
    folder_name = "sample1"

    create_html(file_list, parent_path, folder_name)

    # Check if the HTML file was created
    html_file = parent_path / f"{folder_name}.html"
    assert html_file.exists()
    with open(html_file, "r") as f:
        content = f.read()
        expected = ""
        expected += "<html>"
        expected += "<body>"
        expected += "<h1>sample1</h1>"
        expected += "<ul>"
        expected += '<li><a href="sample1/file1.txt">file1.txt</a></li>'
        expected += '<li><a href="sample1/file2.txt">file2.txt</a></li>'
        expected += '<li><a href="sample1/folder1.html">folder1</a></li>'
        expected += "</ul>"
        expected += "<h1>sample1</h1>"
        expected += "</body>"
        expected += "</html>"

        assert content == expected

    # Check if the folder HTML file was created
    folder_html_file = parent_path / "sample1" / "folder1.html"
    assert folder_html_file.exists()
    with open(folder_html_file, "r") as f:
        content = f.read()
        expected = ""
        expected += "<html>"
        expected += "<body>"
        expected += "<h1>folder1</h1>"
        expected += "<ul>"
        expected += '<li><a href="folder1/file3.txt">file3.txt</a></li>'
        expected += '<li><a href="folder1/file4.txt">file4.txt</a></li>'
        expected += "</ul>"
        expected += "<h1>folder1</h1>"
        expected += "</body>"
        expected += "</html>"

        assert content == expected
