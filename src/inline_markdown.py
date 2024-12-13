import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits `TextNode` elements in the provided list of `old_nodes` based on a specified delimiter, while
    preserving non-`TextType.TEXT` nodes and maintaining the specified `text_type` for delimited sections.
    The function processes the text content of `TextNode` instances, separates elements by `delimiter`,
    and alternates the text type between regular text and the specified `text_type`. Non-`TextNode`
    elements are added to the result without alteration. If an invalid markdown format is detected (e.g.,
    when there's an uneven number of delimiter-separated sections), a `ValueError` is raised.

    :param old_nodes: List of nodes to be split. Each node is an instance of a class that has a `text`
        attribute for its content and a `text_type` attribute describing its type.
    :type old_nodes: list
    :param delimiter: String that represents the delimiter used to split text within `TextNode` instances.
    :type delimiter: str
    :param text_type: Defines the text type to assign to sections that are delimited by the `delimiter`.
    :type text_type: TextType
    :return: A new list of nodes where text sections within `TextNode` elements are split based on
        the delimiter and converted to the specified `text_type`. Non-`TextType.TEXT` nodes are preserved
        and included in the resulting list without changes.
    :rtype: list
    :raises ValueError: If the content of a `TextNode` results in an invalid markdown with an even
        number of delimiter-separated sections.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    print(new_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Splits a list of nodes containing text and Markdown images into individual nodes. Text nodes with
    Markdown image syntax are parsed and split into separate text and image nodes.

    The function processes each node in the input, checking for Markdown image syntax. If text content
    contains images, it splits the text into appropriate text and image nodes, retaining
    the original sequence of content and ensuring that the Markdown image structure is valid.

    :param old_nodes: List of nodes to process, containing both text and image types.
    :type old_nodes: List[TextNode]
    :return: A new list of nodes where Markdown image syntax is split into standalone text and image
        nodes. Text and image nodes are appropriately structured while maintaining the original content
        sequence.
    :rtype: List[TextNode]
    :raises ValueError: If invalid Markdown syntax is detected or the image section is not properly
        closed.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits text nodes containing markdown links into separate nodes, where each
    link and the surrounding text sections become individual nodes. If a node
    does not contain markdown links, it is appended as-is. Raises an exception
    if a link section is improperly formatted or unclosed.

    :param old_nodes: A list of input nodes, each representing a segment of
        text or a textual entity.
    :type old_nodes: list
    :return: New list of text nodes where markdown links have been separated
        out and represented as individual nodes.
    :rtype: list
    :raises ValueError: If a markdown link section is improperly formatted
        or a link is not properly closed.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    """
    Extracts all the image descriptions and URLs from a markdown-formatted
    string. This function utilizes a regular expression to parse and find
    matches for image definitions in markdown format, which typically follow
    the syntax: `![description](url)`.

    :param text: A string containing markdown-formatted text.
    :type text: str
    :return: A list of tuples where each tuple contains two elements: the
        image description and the image URL extracted from the markdown text.
    :rtype: list[tuple[str, str]]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract all markdown links from the given text.

    This function identifies all occurrences of markdown-formatted links in the
    provided string and returns them as a list of tuples. Each tuple contains the
    link text and the URL.

    :param text: The input string containing markdown links.
    :type text: str
    :return: A list of tuples where each tuple contains the link text and the URL.
    :rtype: list[tuple[str, str]]
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    """
    Converts a plain text input into a list of text nodes with structured types, such
    as bold, italic, image, and code. This function processes the input string by
    splitting it based on specific delimiters and categorizing segments into their
    respective text types.

    :param text: A string containing the input text to be converted into structured
        text nodes.
    :type text: str
    :return: A list of structured text nodes where each node represents a segment
        of text with its associated type (e.g., TEXT, BOLD, ITALIC, CODE). The
        sequence of nodes retains the order of appearance in the input text.
    :rtype: list[TextNode]
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        nodes,
                        "**",
                        TextType.BOLD,
                    ),
                    "*",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
    return nodes

        

