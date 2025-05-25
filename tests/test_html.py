from htmligator.html import (
    get_html_for_folder,
    get_html_for_header,
    get_html_for_footer,
    get_html_for_file,
    get_html_for_img_file,
    get_html_for_normal_file,
)


def test_get_html_for_normal_file():
    folder = "test_folder"
    name = "test_file.txt"
    expected_html = f'<li><a href="{folder}/{name}">{name}</a></li>'
    result = get_html_for_normal_file(name, folder)
    assert result == expected_html


def test_get_html_for_folder():
    folder = "test_folder"
    name = "test_folder"
    expected_html = f'<li><a href="{folder}/{name}.html">{name}</a></li>'
    result = get_html_for_folder(name, folder)
    assert result == expected_html


def test_get_html_for_header():
    folder_name = "test_folder"
    expected_html = (
        "<html><head>"
        + "<style type='text/css'>div{width:100%} img{width:100%}</style>"
        + "</head><body>"
        + f"<h1>{folder_name}</h1><ul>"
    )
    result = get_html_for_header(folder_name)
    assert result == expected_html


def test_get_html_for_footer():
    folder_name = "test_folder"
    expected_html = f"</ul><h1>{folder_name}</h1></body></html>"
    result = get_html_for_footer(folder_name)
    assert result == expected_html


def test_get_html_for_img_file():
    folder = "test_folder"
    name = "test_file.jpg"
    expected_html = f'<li><div><img src="{folder}/{name}" /></div></li>'
    result = get_html_for_img_file(name, folder)
    assert result == expected_html


def test_get_html_for_file_image_file():
    folder = "test_folder"
    name = "test_file.jpg"
    expected_html = f'<li><div><img src="{folder}/{name}" /></div></li>'
    result = get_html_for_file(name, folder)
    assert result == expected_html


def test_get_html_for_file_normal_file():
    folder = "test_folder"
    name = "test_file.txt"
    expected_html = f'<li><a href="{folder}/{name}">{name}</a></li>'
    result = get_html_for_file(name, folder)
    assert result == expected_html
