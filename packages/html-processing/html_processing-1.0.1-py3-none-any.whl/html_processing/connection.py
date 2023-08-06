from time import sleep

import dpp_common_utils.selenium
import requests
from lxml import etree
from lxml.html import HtmlElement
from selenium.common.exceptions import WebDriverException

from html_processing.parser import get_html_parser


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
    __check_url(url)
    try:
        driver.get(url)
    except WebDriverException:
        raise requests.exceptions.ConnectionError

    sleep(5)  # sleep - the script has to be loaded and this needs time
    res = driver.page_source

    html_tree: HtmlElement = etree.fromstring(res, parser=parser)
    return html_tree


def __check_url(url):
    """
    Sends a request to an URL to check if it's valid and throws Errors if it's not
    Uses snippet from https://stackoverflow.com/questions/62024144/validate-urls-using-python-and-selenium


    :param url: The URL to check
    :type url: str
    :throws: requests.exceptions
    """

    req = requests.get(url)  # This already throws InvalidURL, InvalidSchema etc. if given String is not valid
    if req.status_code != requests.codes['ok']:
        raise requests.exceptions.HTTPError()
