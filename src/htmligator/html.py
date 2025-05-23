def get_html_for_file(name: str, folder: str) -> str:
    return f'<li><a href="{folder}/{name}">{name}</a></li>'


def get_html_for_folder(name: str, folder: str) -> str:
    return f'<li><a href="{folder}/{name}.html">{name}</a></li>'


def get_html_for_header(folder_name: str) -> str:
    return f"<html><body><h1>{folder_name}</h1><ul>"


def get_html_for_footer(folder_name: str) -> str:
    return f"</ul><h1>{folder_name}</h1></body></html>"
