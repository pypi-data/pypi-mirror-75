import inspect
from typing import Callable, List, Tuple, Union

from lxml.html import HtmlElement

# Type Definitions
P = Union[HtmlElement, None]
D = Union[dict, None]

OP = Union[  # for Operation Functions
    List[Callable[[HtmlElement, int, D], None]],
    Tuple[Callable[[HtmlElement, int, D], None]],
    Callable[[HtmlElement, int, D], None]
]
CO = Callable[[HtmlElement], int]  # for Child Order Functions


def higher_order_traversal(
        operations: OP,
        child_order: CO = None,
        depth_first=True,
        pre_order=True
) -> Callable[[HtmlElement], Tuple[int, dict]]:
    """
    Abstraction over Traversal Action
    Higher Order Traversal Function that returns customized traversal functions
    :param operations: Tuple of Functions that that perform Operations on the current Node
    :type operations: operations: (func(node, counter))
    :param child_order: Determine Order in which childrens are visited
    :type child_order: func(node) -> int
    :param depth_first:
    :type depth_first:
    :param pre_order: Only meaningful for depth first traversal
           Indicate whether Node (PreOrder) or children (PostOrder) are processed first
    :type: bool
    :return: Customized Traversal Function
    :rtype: Callable[[HtmlElement], Callable]
    """

    def tag_traversal(node: HtmlElement,
                      ops: OP = operations,
                      c_order: CO = child_order,
                      counter: int = 0,
                      collection_dict={}
                      ) -> Tuple[int, dict]:
        """
        :param node: see above
        :type node: HtmlElement
        :param ops: see above
        :type ops: OP
        :param c_order: see above
        :type c_order: CO
        :param counter: Counter
        :type counter: int
        :param collection_dict: Dictionary to Collect Information
        :type collection_dict: dict
        :return: No of tree Elements, updated Collection Dictionary
        :rtype: Tuple[int, dict]
        """

        def process_node(n: HtmlElement,
                         o: OP,
                         c: int,
                         coll: D) -> int:
            """
            :param n: node
            :param o: operations
            :param c: counter
            :param coll: collection_dictionary
            :return updated Counter
            """
            if n.tag is not None:
                if type(o) is not tuple:
                    o = tuple(o) if type(o) is list else (o,)
                    for operation in o:
                        sig = inspect.signature(operation)

                        # Decision whether CollectionDict Updating Operation
                        if 'collection_dict' in sig.parameters:
                            operation(n, c, coll)
                        else:
                            operation(n, c)
                    c += 1
                    # print("Processeing Node")
                    # print("CounterUpdate: " + str(c))
                    return c

        # Actual Traversal
        inner_counter = counter  # Collect Counter Updates within single node

        if depth_first:
            if pre_order:
                inner_counter = process_node(node, ops, inner_counter, collection_dict)

            # Process Children
            if len(node):
                children: list = node.getchildren()
                if c_order is not None:
                    children.sort(key=c_order)

                for child in children:
                    inner_counter, collection_dict = tag_traversal(
                        node=child,
                        counter=inner_counter,
                        collection_dict=collection_dict)

            if not pre_order:  # i.e Post Order
                inner_counter = process_node(node, ops, inner_counter, collection_dict)

        if not depth_first:
            current_level: List[HtmlElement] = [node]
            while len(current_level) > 0:
                next_level = []
                for current_node in current_level:
                    inner_counter = process_node(current_node,
                                                 ops,
                                                 inner_counter,
                                                 collection_dict)

                    # Collect next level Nodes
                    if len(current_node):
                        children: list = current_node.getchildren()
                        if c_order is not None:
                            children.sort(key=c_order)

                        for child in children:
                            next_level.append(child)

                current_level = next_level

        return inner_counter, collection_dict

    return tag_traversal


def empty_tags(node: HtmlElement, counter: int):
    """
    Empties the JSS, Style contents
    """
    if node.get("style"):
        node.set("style", "")

    if node.tag == "script":
        node.text = ""
    elif node.tag == "style":
        node.text = ""
        return
    else:
        return


def count_visit_operation(node: HtmlElement, counter: int):
    visit_counter = int(node.get("visit_counter", 0))
    visit_counter += 1
    node.set("visit_counter", str(visit_counter))
    return


print_operations = [
    lambda node, counter: print(node.tag)
]


def track_tags_operation(node: HtmlElement, counter: int, collection_dict: dict):
    collection_dict['tag-sequence'].append(node.tag)


track_operations = print_operations + [track_tags_operation]

# Customized Traversal Function, ready to be loaded from other modules
simple_track_traversal_pre_order = higher_order_traversal(track_operations)
simple_track_traversal_post_order = higher_order_traversal(track_operations, pre_order=False)
simple_track_traversal_breadth_first = higher_order_traversal(track_operations, depth_first=False)
