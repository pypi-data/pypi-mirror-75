from pathlib import Path
from typing import Union

from lxml import etree
from lxml.html import HtmlElement

from .parser import get_html_parser

TreeOrErrMessage = Union[HtmlElement, str]


def get_html_as_tree(path_to_html_file: Path, custom_element=None) -> TreeOrErrMessage:
    """
    Lower Level Interface - Retrieve Tree from File
    """

    parser = get_html_parser(custom_element=HtmlElement) if custom_element is None \
        else get_html_parser(custom_element=custom_element)

    if path_to_html_file.exists():
        return etree.parse(path_to_html_file.as_uri(), parser=parser).getroot()
    else:
        return "There is no HTML File at the given path location"


def persist_html_tree(html_tree: HtmlElement, path_to_html_file: Path) -> None:
    """
    Lower Level Interface - Persist a given HTML Tree safely at a given file path
    """
    dir_path = path_to_html_file.parent

    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)

    with path_to_html_file.open(mode='wb') as f:
        f.write(etree.tostring(html_tree, pretty_print=True, method="html"))
