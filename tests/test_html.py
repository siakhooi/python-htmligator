from htmligator.html import (
    get_html_for_folder,
    get_html_for_header,
    get_html_for_footer,
    get_html_for_file,
    get_html_for_img_file,
    get_html_for_normal_file,
)
import pytest


def test_get_html_for_normal_file():
    folder = "test_folder"
    name = "test_file.txt"
    expected_html = f'<a href="{folder}/{name}">{name}</a>'
    result = get_html_for_normal_file(name, folder)
    assert result == expected_html


def test_get_html_for_folder():
    folder = "test_folder"
    name = "test_folder"
    expected_html = f'<a href="{folder}/{name}.html">{name}</a>'
    result = get_html_for_folder(name, folder)
    assert result == expected_html


def test_get_html_for_header():
    folder_name = "test_folder"
    expected_html = (
        "<html><head>"
        + "<style type='text/css'>div{width:100%} img{width:100%}</style>"
        + "</head><body>"
        + f"<h1>{folder_name}</h1>"
    )
    result = get_html_for_header(folder_name)
    assert result == expected_html


def test_get_html_for_footer():
    folder_name = "test_folder"
    expected_html = f"<h1>{folder_name}</h1></body></html>"
    result = get_html_for_footer(folder_name)
    assert result == expected_html


def test_get_html_for_img_file():
    folder = "test_folder"
    name = "test_file.jpg"
    expected_html = f'<div><img src="{folder}/{name}" /></div>'
    result = get_html_for_img_file(name, folder)
    assert result == expected_html


def test_get_html_for_file_image_file():
    folder = "test_folder"
    name = "test_file.jpg"
    expected_html = f'<div><img src="{folder}/{name}" /></div>'
    result = get_html_for_file(name, folder, use_img=True)
    assert result == expected_html


@pytest.mark.parametrize("options", [True, False])
def test_get_html_for_file_normal_file(options):
    folder = "test_folder"
    name = "test_file.txt"
    expected_html = f'<a href="{folder}/{name}">{name}</a>'
    result = get_html_for_file(name, folder, use_img=options)
    assert result == expected_html


def test_get_html_for_file_image_file_without_img():
    folder = "test_folder"
    name = "test_file.jpg"
    expected_html = f'<a href="{folder}/{name}">{name}</a>'
    result = get_html_for_file(name, folder, use_img=False)
    assert result == expected_html
