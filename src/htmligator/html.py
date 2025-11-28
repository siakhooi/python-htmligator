from htmligator.util import is_browser_supported_image_files


def get_html_for_file(name: str, folder: str, use_img: bool) -> str:
    if use_img and is_browser_supported_image_files(name):
        return get_html_for_img_file(name, folder)
    else:
        return get_html_for_normal_file(name, folder)


def get_html_for_normal_file(name: str, folder: str) -> str:
    return f'<a href="{folder}/{name}">{name}</a>'


def get_html_for_folder(name: str, folder: str) -> str:
    return f'<a href="{folder}/{name}.html">{name}</a>'


def get_html_for_header(folder_name: str) -> str:
    return (
        "<html><head>"
        + "<style type='text/css'>div{width:100%} img{width:100%}</style>"
        + "</head><body>"
        + f"<h1>{folder_name}</h1>"
    )


def get_html_for_list_start() -> str:
    return "<ul>"


def get_html_for_list_end() -> str:
    return "</ul>"


def get_html_for_list_item_start() -> str:
    return "<li>"


def get_html_for_list_item_end() -> str:
    return "</li>"


def get_html_for_footer(folder_name: str) -> str:
    return f"<h1>{folder_name}</h1></body></html>"


def get_html_for_img_file(name: str, folder: str) -> str:
    return f'<div><img src="{folder}/{name}" /></div>'
