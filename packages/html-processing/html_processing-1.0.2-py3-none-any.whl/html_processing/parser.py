from lxml import etree
from lxml.html import HtmlElement


def get_html_parser(custom_element=HtmlElement):
    """
    Returns an HTML Parser configured to an custom_element, if provided
    :param custom_element: an Element drived from lxml ElementBase Class
    :type custom_element: Subclass of etree.ElementBase
    :return: an HTML Parser Object
    :rtype: lxml.etree.HTMLParser
    """

    parser = etree.HTMLParser(encoding="utf-8", remove_comments=True, remove_blank_text=True, remove_pis=True)
    if custom_element is not None:
        parser_lookup = etree.ElementDefaultClassLookup(element=custom_element)
        parser.set_element_class_lookup(parser_lookup)
    return parser
