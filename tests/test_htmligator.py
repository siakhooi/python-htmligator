from htmligator.htmligator import (
    get_html_for_file,
    get_html_for_folder,
    generate_html_files,
)


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


def test_generate_html_files():
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
    folder_name = "sample1"

    html_files = []
    generate_html_files(html_files, file_list, folder_name)

    assert len(html_files) == 2
    assert html_files[1]["name"] == "sample1.html"
    assert html_files[0]["name"] == "sample1/folder1.html"

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

    assert expected == html_files[1]["contents"]

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

    assert expected == html_files[0]["contents"]
