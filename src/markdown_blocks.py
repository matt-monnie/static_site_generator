import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    """
    Represents various types of content blocks.

    This Enum class is used to define and categorize different types of content
    blocks that can appear in a document or an application. It provides a way to
    identify and handle these content types programmatically.

    :ivar HEADING: Represents a heading block, typically used for titles or headers
        in a document.
    :type HEADING: str
    :ivar CODE: Represents a block of code, used for embedding snippets of code or
        programming content.
    :type CODE: str
    :ivar PARAGRAPH: Represents a paragraph block, used for standard textual content.
    :type PARAGRAPH: str
    :ivar QUOTE: Represents a quote block, used for embedding quotations or cited
        text.
    :type QUOTE: str
    :ivar UNORDERED_LIST: Represents an unordered list block, used for bullet points
        or non-sequential items.
    :type UNORDERED_LIST: str
    :ivar ORDERED_LIST: Represents an ordered list block, used for numbered or sequenced
        items.
    :type ORDERED_LIST: str
    """
    HEADING = "heading"
    CODE = "code"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """
    Convert a given markdown string into a list of blocks.

    The provided markdown string will be split into blocks separated by double
    line breaks. Any empty blocks within the resulting list are discarded, and
    all blocks are stripped of leading and trailing whitespace.

    :param markdown: A string containing markdown content.
    :type markdown: str
    :return: A list of strings, where each string represents an individual block of
             the input markdown content with whitespace stripped.
    :rtype: list[str]
    """
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            blocks.remove(block)
        block = block.strip()

    return blocks


def block_to_block_type(block):
    """
    Determines the type of a given text block and returns its corresponding block type
    value from the BlockType enumeration.

    This function evaluates the structure and content of the input text block to
    identify its type. Supported types include headings, code blocks, quotes,
    unordered lists, ordered lists, and regular paragraphs. The function enforces
    specific formatting rules to classify the block type accurately.

    :param block: A string representing a text block to identify its type. The block
        must conform to specific structural rules to match a valid type.

    :return: A string representing the block type value from the BlockType
        enumeration. Possible values include 'HEADING', 'CODE', 'QUOTE',
        'UNORDERED_LIST', 'ORDERED_LIST', or 'PARAGRAPH'.
    """
    if block.startswith("#"):
        lines = block.split("\n")
        if all(1 <= len(line.split()[0]) <= 6 and line[0] == "#" for line in lines):
            return BlockType.HEADING.value
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE.value
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE.value
    elif all(line.startswith(("*", "-")) and line[1] == " " for line in block.split("\n")):
        return BlockType.UNORDERED_LIST.value
    elif all(re.match(r"^\d\.\s", line) for line in block.split("\n")):
        return BlockType.ORDERED_LIST.value
    else:
        return BlockType.PARAGRAPH.value


def markdown_to_html_node(markdown):
    """
    Converts a markdown string into an HTML node by processing it through
    a series of transformations. It first parses the markdown into blocks,
    then transforms these blocks into HTML nodes, and finally wraps the
    resulting HTML nodes into a parent node.

    :param markdown: The markdown formatted string to be converted.
    :type markdown: str
    :return: A parent HTML node containing transformed HTML child nodes
             derived from the input markdown.
    :rtype: ParentNode
    """
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


def block_to_html_node(block):
    """
    Converts a block of text into its corresponding HTML node representation based on the block's type.

    This function determines the type of the block using the `block_to_block_type` function
    and processes it accordingly by invoking the appropriate corresponding processing function.
    If the block type is unknown, an exception is raised indicating the invalid block type.

    :param block: The input block of text to be converted to an HTML node.
    :type block: Any
    :return: The HTML representation of the input block as a node.
    :rtype: Any
    :raises ValueError: If the block type is invalid or unrecognized.
    """
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return process_heading(block)
        case BlockType.PARAGRAPH:
            return process_paragraph(block)
        case BlockType.CODE:
            return process_code(block)
        case BlockType.QUOTE:
            return process_quote(block)
        case BlockType.UNORDERED_LIST:
            return process_list(block, "ul", r"^[\*\-]\s", 2)
        case BlockType.ORDERED_LIST:
            return process_list(block, "ol", r"^\d\.\s", 3)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def text_to_children(text):
    """
    Converts a plain text input into a list of HTML-compatible nodes by
    parsing the input text into intermediate text nodes, and then
    transforming each text node into an equivalent HTML node.

    The function is intended to be used where plain text needs to be
    transformed into structured HTML content.

    :param text: The input text as a string that needs to be converted
        into HTML nodes.
    :type text: str
    :return: A list of HTML nodes derived from the input text after
        processing and transformation.
    :rtype: list
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def process_heading(block):
    """
    Processes a heading block and converts it into a parent node.

    This function takes a string representing a heading block, determines the
    heading level based on the number of leading `#` symbols, extracts the text
    of the heading, and generates a `ParentNode` object with the heading's level
    and its textual content converted into child nodes.

    :param block: str
        A string representing the heading block. The block must start with
        `#` symbols followed by a space and then the heading text. The number
        of `#` symbols indicates the heading level.
    :raises ValueError:
        If the heading block is invalid, meaning there are either not enough
        characters to form a heading or the heading does not follow the expected
        structure.
    :return: ParentNode
        A `ParentNode` object that represents the heading and its content, with
        the heading's level encoded in the node tag (e.g., `h1`, `h2`).
    """
    level = block.count("#", 0, block.find(" "))
    if level + 1 >= len(block):
        raise ValueError("Invalid heading block")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children, None)


def process_paragraph(block):
    """
    Processes a block of text to generate a paragraph node.

    This function takes a block of text with possible line breaks, merges all lines
    into a single string, and converts this text into a structured "ParentNode"
    object with the tag `"p"`. The function internally uses the `text_to_children`
    helper to transform the textual content into child nodes.

    :param block: A string representing a block of text with possible line breaks.
    :type block: str
    :return: A `ParentNode` object containing the given text as children under
        the `"p"` node.
    :rtype: ParentNode
    """
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children, None)


def process_code(block):
    """
    Processes a code block string and converts it into a structured `ParentNode` object.

    This function validates the input `block` to ensure it starts and ends with
    the correct code block delimiters (```), removes these delimiters and extra
    whitespace, and processes the remaining text into child nodes using the
    `text_to_children` function. The resulting structured representation is
    returned as a `ParentNode` object.

    :param block: A string representing a code block, with leading and trailing
                  ``` delimiters.
    :type block: str

    :raises ValueError: Raised if the input block does not start and end with
                        the required ``` delimiters.

    :return: A `ParentNode` object containing the processed representation
             of the code block.
    :rtype: ParentNode
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3].strip()
    children = text_to_children(text)
    return ParentNode("code", children, None)\

def process_quote(block):
    """
    Processes a blockquote-styled string into a structured node representation
    suitable for further processing. Each line in the blockquote must
    begin with '>' followed by a space. This method strips the '>'
    markers from each line and combines the remaining content into
    a single textual structure.

    :param block: A string containing a blockquote-style text where each
       line starts with '> '.
    :type block: str

    :return: A structured node representing the processed blockquote with
       its contained text converted to children nodes.
    :rtype: ParentNode

    :raises ValueError: If any line in the `block` does not start with '> '.
    """
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line[2:])
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children, None)


def process_list(block, list_type, list_item_pattern, list_item_prefix_length):
    """
    Processes a text block containing a list structure and converts it into a hierarchy
    of nodes representing the list and its items. Validates the list block lines based on
    the provided pattern and extracts the list items and their contents. Creates a
    parent node representing the entire list and child nodes for each individual list
    item.

    :param block: The input text block containing structured list content to process.
    :type block: str
    :param list_type: The type of the list to be constructed (e.g., "ul", "ol").
    :type list_type: str
    :param list_item_pattern: The regular expression pattern to validate and extract
        individual list item lines.
    :type list_item_pattern: str
    :param list_item_prefix_length: The length of the prefix in each list item line to
        be stripped prior to processing its content.
    :type list_item_prefix_length: int
    :return: A parent node object representing the structured list, with child nodes
        for each list item.
    :rtype: ParentNode
    :raises ValueError: If a line in the text block does not match the provided
        list_item_pattern.
    """
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if not re.match(list_item_pattern, line):
            raise ValueError("Invalid list block")
        text = (line[list_item_prefix_length:])
        children = text_to_children(text)
        list_items.append(ParentNode("li", children, None))
    return ParentNode(list_type, list_items, None)