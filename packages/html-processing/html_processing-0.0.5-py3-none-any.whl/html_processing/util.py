import unicodedata

from lxml.html import HtmlElement
from lxml.etree import _ElementTree
from typing import List


class NoHTMLElementFound(Exception):
    def __init__(self, exception_msg):
        self.exception_msg = exception_msg


class MultipleHTMLElementsFound(Exception):
    def __init__(self, exception_msg):
        self.exception_msg = exception_msg


class HTMLUtility:
    @staticmethod
    def get_html_element_by_custom_id(current_tree: HtmlElement,
                                      html_attr_name: str,
                                      custom_element_id: int) -> HtmlElement:
        """
        Focused on unique identifiers
        Note: could even be abstracted to find elements given <any_value> for <any_html_attr>
        :param current_tree:  the current HTML Page In Memory representation
        :param html_attr_name: The custom attr name
        :param custom_element_id: An Identifier for an instance in the custom Namestance
        :rtype: HtmlElement
        """

        pseudo_xpath = "//*[@" + html_attr_name + "='{ELEMENT_ID}']".format(
            ELEMENT_ID=custom_element_id
        )
        found_elements: List[HtmlElement] = current_tree.xpath(pseudo_xpath)

        if len(found_elements) == 0:
            raise NoHTMLElementFound("There is no element for {ATTR_NAME}={ELEMENT_ID} in the current HTML Tree".format(
                ATTR_NAME=html_attr_name,
                ELEMENT_ID=custom_element_id
            ))
        elif len(found_elements) > 1:
            raise MultipleHTMLElementsFound(
                "Inconsistency: There are multiple elements found for {ATTR_NAME}={ELEMENT_ID}. "
                "But the result should be one unique element".format(
                    ATTR_NAME=html_attr_name,
                    ELEMENT_ID=custom_element_id
                ))
        else:
            return found_elements[0]

    @staticmethod
    def construct_canonical_xpath(current_tree: HtmlElement, html_attr_name: str, custom_element_id: int) -> str:
        """
        :param current_tree:  the current HTML Page In Memory representation
        :param html_attr_name: the custom attr name
        :param custom_element_id: An Identifier for an instance in the custom Namestance
        :rtype: HtmlElement
        """
        root_tree: _ElementTree = current_tree.getroottree()
        target_element = HTMLUtility.get_html_element_by_custom_id(current_tree, html_attr_name, custom_element_id)
        return root_tree.getpath(target_element)

    @staticmethod
    def collect_text_content(element: HtmlElement) -> str:
        """
        Collect all text content associated with an Element safely

        Accounts for the following constellation <parent> <child>text_content</child>tail_content</parent>
        Where the child.tail holds the tail_content
        """
        element_text = element.text if hasattr(element, "text") else ""
        element_text = "" if element_text is None else element_text

        element_tail = element.tail if hasattr(element, "tail") else ""
        element_tail = "" if element_tail is None else element_tail

        element_text_content = element_text + " " + element_tail
        element_text_content = unicodedata.normalize('NFKC', element_text_content)
        element_text_content.rstrip()

        return element_text_content

    @staticmethod
    def check_only_children_of_one_kind(element: HtmlElement) -> bool:
        children = element.getchildren()
        if len(children) == 0:
            return False  # children of None kind not of one kind

        tag_to_be = children[0].tag
        for child in children:
            if child.tag != tag_to_be:
                return False
        return True

    @staticmethod
    def check_has_multiple_childs(element: HtmlElement) -> bool:
        no_of_children = len(element.getchildren())
        return no_of_children > 2
