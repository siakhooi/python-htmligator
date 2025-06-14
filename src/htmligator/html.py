from htmligator.util import is_browser_supported_image_files


def get_html_for_file(name: str, folder: str, use_img: bool) -> str:
    if use_img and is_browser_supported_image_files(name):
        return get_html_for_img_file(name, folder)
    else:
        return get_html_for_normal_file(name, folder)


def get_html_for_normal_file(name: str, folder: str) -> str:
    return f'<li><a href="{folder}/{name}">{name}</a></li>'


def get_html_for_folder(name: str, folder: str) -> str:
    return f'<li><a href="{folder}/{name}.html">{name}</a></li>'


def get_html_for_header(folder_name: str) -> str:
    return (
        "<html><head>"
        + "<style type='text/css'>div{width:100%} img{width:100%}</style>"
        + "</head><body>"
        + f"<h1>{folder_name}</h1><ul>"
    )


def get_html_for_footer(folder_name: str) -> str:
    return f"</ul><h1>{folder_name}</h1></body></html>"


def get_html_for_img_file(name: str, folder: str) -> str:
    return f'<li><div><img src="{folder}/{name}" /></div></li>'
