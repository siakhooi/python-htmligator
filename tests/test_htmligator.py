from htmligator.htmligator import Htmligator


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
    htmligator = Htmligator()
    htmligator.generate_html_files(html_files, file_list, folder_name)

    assert len(html_files) == 2
    assert html_files[1]["name"] == "sample1.html"
    assert html_files[0]["name"] == "sample1/folder1.html"

    with open(
        "tests/expected-output/generate_html_files_file_1.txt", "r"
    ) as f:  # noqa: E501
        expected = "".join([line.rstrip() for line in f])

    assert expected == html_files[1]["contents"]

    with open(
        "tests/expected-output/generate_html_files_file_0.txt", "r"
    ) as f:  # noqa: E501
        expected = "".join([line.rstrip() for line in f])

    assert expected == html_files[0]["contents"]


def test_zip_folder(tmp_path):
    folder_name = "sample"
    d1 = tmp_path / folder_name
    d1.mkdir()
    p1 = d1 / "file1.txt"
    p1.touch()
    p2 = d1 / "file2.txt"
    p2.touch()

    zip_path = tmp_path / f"{folder_name}.zip"
    html_files = [{"name": "html_file_name", "contents": "file_contents"}]
    htmligator = Htmligator()
    htmligator.zip_folder(tmp_path, folder_name, html_files, zip_path)

    assert zip_path.exists()
    assert zip_path.is_file()
    assert zip_path.stat().st_size > 0

    import zipfile

    with zipfile.ZipFile(zip_path, "r") as zipf:
        assert len(zipf.namelist()) == 3
        assert "sample/file1.txt" in zipf.namelist()
        assert "sample/file2.txt" in zipf.namelist()
        assert "html_file_name" in zipf.namelist()

        assert zipf.read("html_file_name").decode() == "file_contents"


def test_htmligator(tmp_path, monkeypatch):
    folder_name = "sample"
    d1 = tmp_path / folder_name
    d1.mkdir()
    p1 = d1 / "file1.txt"
    p1.touch()
    p2 = d1 / "file2.txt"
    p2.touch()

    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))

    htmligator = Htmligator()
    htmligator.htmligator(d1)

    zip_path = tmp_path / f"{folder_name}.zip"
    assert zip_path.exists()
    assert zip_path.is_file()
    assert zip_path.stat().st_size > 0

    import zipfile

    with zipfile.ZipFile(zip_path, "r") as zipf:
        assert len(zipf.namelist()) == 3
        assert "sample/file1.txt" in zipf.namelist()
        assert "sample/file2.txt" in zipf.namelist()
        assert "sample.html" in zipf.namelist()


def test_generate_html_files_with_image_files_true():
    file_list = [
        {"name": "file1.txt", "type": "file"},
        {"name": "file2.jpg", "type": "file"},
        {
            "name": "folder1",
            "type": "folder",
            "children": [
                {"name": "file3.txt", "type": "file"},
                {"name": "file4.jpg", "type": "file"},
            ],
        },
    ]
    folder_name = "sample1"

    html_files = []
    htmligator = Htmligator({"use_img": True})
    htmligator.generate_html_files(html_files, file_list, folder_name)

    assert len(html_files) == 2
    assert html_files[1]["name"] == "sample1.html"
    assert html_files[0]["name"] == "sample1/folder1.html"

    expected = ""
    expected += "<html>"
    expected += "<head>"
    expected += (
        "<style type='text/css'>div{width:100%} img{width:100%}</style>"  # noqa: E501
    )
    expected += "</head>"
    expected += "<body>"
    expected += "<h1>sample1</h1>"
    expected += "<ul>"
    expected += '<li><a href="sample1/file1.txt">file1.txt</a></li>'
    expected += '<li><div><img src="sample1/file2.jpg" /></div></li>'
    expected += '<li><a href="sample1/folder1.html">folder1</a></li>'
    expected += "</ul>"
    expected += "<h1>sample1</h1>"
    expected += "</body>"
    expected += "</html>"

    assert expected == html_files[1]["contents"]

    expected = ""
    expected += "<html>"
    expected += "<head>"
    expected += (
        "<style type='text/css'>div{width:100%} img{width:100%}</style>"  # noqa: E501
    )
    expected += "</head>"
    expected += "<body>"
    expected += "<h1>folder1</h1>"
    expected += "<ul>"
    expected += '<li><a href="folder1/file3.txt">file3.txt</a></li>'
    expected += '<li><div><img src="folder1/file4.jpg" /></div></li>'
    expected += "</ul>"
    expected += "<h1>folder1</h1>"
    expected += "</body>"
    expected += "</html>"

    assert expected == html_files[0]["contents"]


def test_generate_html_files_with_image_files_false():
    file_list = [
        {"name": "file1.txt", "type": "file"},
        {"name": "file2.jpg", "type": "file"},
        {
            "name": "folder1",
            "type": "folder",
            "children": [
                {"name": "file3.txt", "type": "file"},
                {"name": "file4.jpg", "type": "file"},
            ],
        },
    ]
    folder_name = "sample1"

    html_files = []
    htmligator = Htmligator({"use_img": False})
    htmligator.generate_html_files(html_files, file_list, folder_name)

    assert len(html_files) == 2
    assert html_files[1]["name"] == "sample1.html"
    assert html_files[0]["name"] == "sample1/folder1.html"

    expected = ""
    expected += "<html>"
    expected += "<head>"
    expected += (
        "<style type='text/css'>div{width:100%} img{width:100%}</style>"  # noqa: E501
    )
    expected += "</head>"
    expected += "<body>"
    expected += "<h1>sample1</h1>"
    expected += "<ul>"
    expected += '<li><a href="sample1/file1.txt">file1.txt</a></li>'
    expected += '<li><a href="sample1/file2.jpg">file2.jpg</a></li>'
    expected += '<li><a href="sample1/folder1.html">folder1</a></li>'
    expected += "</ul>"
    expected += "<h1>sample1</h1>"
    expected += "</body>"
    expected += "</html>"

    assert expected == html_files[1]["contents"]

    expected = ""
    expected += "<html>"
    expected += "<head>"
    expected += (
        "<style type='text/css'>div{width:100%} img{width:100%}</style>"  # noqa: E501
    )
    expected += "</head>"
    expected += "<body>"
    expected += "<h1>folder1</h1>"
    expected += "<ul>"
    expected += '<li><a href="folder1/file3.txt">file3.txt</a></li>'
    expected += '<li><a href="folder1/file4.jpg">file4.jpg</a></li>'
    expected += "</ul>"
    expected += "<h1>folder1</h1>"
    expected += "</body>"
    expected += "</html>"

    assert expected == html_files[0]["contents"]
