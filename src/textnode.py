from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    """
    Represents a collection of text types for specific formatting and content elements.

    This enumeration defines various text types that can be used to style text or
    denote specific content types, such as plain text, bold text, italics, code snippets,
    hyperlinks, or images. It can be employed in text processing, rendering styled
    content, or managing rich text formats.

    :ivar TEXT: Represents plain text.
    :type TEXT: TextType
    :ivar BOLD: Represents bold-styled text.
    :type BOLD: TextType
    :ivar ITALIC: Represents italic-styled text.
    :type ITALIC: TextType
    :ivar CODE: Represents code snippets or monospaced text.
    :type CODE: TextType
    :ivar LINK: Represents hyperlink text.
    :type LINK: TextType
    :ivar IMAGE: Represents image content type.
    :type IMAGE: TextType
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Represents a textual node in a broader context, such as a document or UI component.

    This class encapsulates text content, its type/classification, and an optional
    associated URL. It supports equality comparison based on its attributes and
    provides a developer-friendly string representation for debugging purposes.

    :ivar text: The textual content of the node.
    :type text: str
    :ivar text_type: The type or classification of the text (e.g., header, paragraph).
    :type text_type: Enum or specific type representing text classification
    :ivar url: An optional URL associated with the text node, if applicable.
    :type url: str or None
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text_type == other.text_type
                and self.text == other.text
                and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """
    Converts a TextNode object to a corresponding HTML node representation. The function checks the
    text type of the given TextNode and maps it to an appropriate HTML element encapsulated within
    a LeafNode. This includes mappings for basic text, bold, italic, code, links, and images. If the
    text type is unrecognized, a ValueError is raised.

    :param text_node: The text node object to be converted, containing its type, text content,
        and optional attributes such as URLs.
    :type text_node: TextNode
    :return: A LeafNode object representing the HTML equivalent of the given text node.
    :rtype: LeafNode
    :raises ValueError: If the text_node’s text type does not correspond to any recognized type.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
