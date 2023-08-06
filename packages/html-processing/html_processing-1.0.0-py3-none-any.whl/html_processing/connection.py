from time import sleep

import dpp_common_utils.selenium
from requests.exceptions import InvalidURL
from selenium.common.exceptions import WebDriverException

from html_processing.parser import get_html_parser
from lxml import etree
from lxml.html import HtmlElement


def lxml_connect(url):
    """
    Connects to URL and returns the HTML Tree
    :param url: The URL to the target data source
    :type url: str
    :return: a Subclass of etree.ElementBase, dependent on what is specified in the parser
    :rtype: HtmlElement
    """

    parser = get_html_parser()
    driver = dpp_common_utils.selenium.get_driver(True)
    try:
        driver.get(url)
    except WebDriverException:
        return InvalidURL
    sleep(5)  # sleep - the script has to be loaded and this needs time
    res = driver.page_source

    html_tree: HtmlElement = etree.fromstring(res, parser=parser)
    return html_tree
