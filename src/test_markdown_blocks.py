import unittest
from unittest.mock import patch
from markdown_blocks import (
    markdown_to_html_node,
    block_to_html_node,
    text_to_children,
    process_heading,
    process_paragraph,
    process_code,
    process_quote,
    process_list,
    ParentNode,
    LeafNode,
    BlockType
)
from enum import Enum
from unittest.mock import patch

from src.markdown_blocks import markdown_to_blocks, block_to_block_type




class TestInlineMarkdown(unittest.TestCase):
    """
    Unit tests for the `markdown_to_blocks` function.

    This class provides a series of unit tests to verify the correctness and behavior
    of the `markdown_to_blocks` function, which processes markdown-like formatted
    strings to separate them into individual blocks of text. Each test case
    assesses a specific scenario or edge case to ensure reliable functionality
    and handling of different inputs.

    :ivar longMessage: If True, the long message containing the expected and
                       actual values is included in the output upon a test failure.
    :type longMessage: bool
    :ivar maxDiff: The maximum size of the diff output for failed assertions that involve
                   sequences. Set this to None to disable truncation.
    :type maxDiff: int or None
    """
    def test_markdown_to_blocks_empty_string(self):
        result = markdown_to_blocks("")
        self.assertListEqual(result, [])

    def test_markdown_to_blocks_single_block(self):
        result = markdown_to_blocks("This is a single block of text")
        self.assertListEqual(result, ["This is a single block of text"])

    def test_markdown_to_blocks_multiple_blocks(self):
        result = markdown_to_blocks("Block one\n\nBlock two\n\nBlock three")
        self.assertListEqual(result, ["Block one", "Block two", "Block three"])

    def test_markdown_to_blocks_blocks_with_whitespace(self):
        result = markdown_to_blocks("Block one\n\nBlock two\n\nBlock three")
        self.assertListEqual(result, ["Block one", "Block two", "Block three"])

    def test_markdown_to_blocks_empty_blocks_between(self):
        result = markdown_to_blocks("Block one\n\n\n\nBlock two")
        self.assertListEqual(result, ["Block one", "Block two"])

    def test_markdown_to_blocks_with_trailing_and_leading_newlines(self):
        result = markdown_to_blocks("\n\nBlock one\n\nBlock two\n\n")
        self.assertListEqual(result, ["Block one", "Block two"])





class TestMarkdownBlocks(unittest.TestCase):
    """
    Test suite for validating the functionality of block type detection in markdown.

    This class contains unit tests for checking the classification of markdown blocks
    to their respective block types, such as headings, code blocks, quotes, unordered
    lists, ordered lists, and paragraphs.

    :ivar longMessage: If set to True, lengthy failure messages are displayed.
    :type longMessage: bool
    :ivar maxDiff: Limits the number of characters shown in failing test diffs. Defaults to None,
        which does not limit the output.
    :type maxDiff: Optional[int]
    """
    def test_block_to_block_type_heading(self):
        block = "# Heading 1\n## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING.value)

    def test_block_to_block_type_code_block(self):
        block = "```\ndef test():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE.value)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> Another quote line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE.value)

    def test_block_to_block_type_unordered_list(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST.value)

    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST.value)

    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph without any specific markdown structure."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH.value)




class TestMarkdownToHtml(unittest.TestCase):
    """
    Contains unit tests for Markdown processing functions, which include converting Markdown
    syntax to HTML-like structures. This class uses mock patches to simulate outputs from
    different utility functions for testing purposes and ensures the proper error handling
    mechanisms are in place.

    :ivar None None: Test class does not have specific attributes.
    :type None: None
    """
    def setUp(self):
        # Any common setup if required
        pass

    def test_markdown_to_html_node(self):
        with patch('markdown_blocks.markdown_to_blocks', return_value=["# Heading"]) as mock_blocks, \
                patch('markdown_blocks.block_to_html_node') as mock_html_node:
            mock_html_node.return_value = ParentNode("h1", [LeafNode(None, "Heading")])
            result = markdown_to_html_node("# Heading")
            self.assertEqual(result.tag, "div")
            self.assertEqual(len(result.children), 1)
            self.assertEqual(result.children[0].tag, "h1")
            self.assertEqual(result.children[0].children[0].value, "Heading")
            mock_blocks.assert_called_once_with("# Heading")

    def test_block_to_html_node_heading(self):
        with patch('markdown_blocks.block_to_block_type', return_value=BlockType.HEADING) as mock_block_type, \
                patch('markdown_blocks.process_heading') as mock_process_heading:
            mock_process_heading.return_value = ParentNode("h1", [LeafNode(None, "Heading")])
            result = block_to_html_node("# Heading")
            self.assertEqual(result.tag, "h1")
            self.assertEqual(result.children[0].value, "Heading")
            mock_block_type.assert_called_once_with("# Heading")
            mock_process_heading.assert_called_once_with("# Heading")

    def test_block_to_html_node_invalid_type(self):
        with patch('markdown_blocks.block_to_block_type', return_value=None):
            with self.assertRaises(ValueError) as context:
                block_to_html_node("## Unsupported Block")
            self.assertIn("Invalid block type", str(context.exception))

    def test_text_to_children(self):
        with patch('markdown_blocks.text_to_textnodes', return_value=["plain", "text"]) as mock_text_nodes, \
                patch('markdown_blocks.text_node_to_html_node') as mock_text_node_to_html:
            mock_text_node_to_html.side_effect = [LeafNode(None, "plain"), LeafNode(None, "text")]
            result = text_to_children("plain text")
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].value, "plain")
            self.assertEqual(result[1].value, "text")
            mock_text_nodes.assert_called_once_with("plain text")

    def test_process_heading_valid(self):
        with patch('markdown_blocks.text_to_children',
                   return_value=[LeafNode(None, "Heading Content")]) as mock_text_to_children:
            block = "# Heading Content"
            result = process_heading(block)
            self.assertEqual(result.tag, "h1")
            self.assertEqual(len(result.children), 1)
            self.assertEqual(result.children[0].value, "Heading Content")
            mock_text_to_children.assert_called_once_with("Heading Content")

    def test_process_heading_invalid(self):
        block = "###"
        with self.assertRaises(ValueError) as context:
            process_heading(block)
        self.assertIn("Invalid heading block", str(context.exception))

    def test_process_paragraph(self):
        with patch('markdown_blocks.text_to_children',
                   return_value=[LeafNode(None, "This is a paragraph.")]) as mock_text_to_children:
            block = "This is a paragraph.\nAnother line."
            result = process_paragraph(block)
            self.assertEqual(result.tag, "p")
            self.assertEqual(len(result.children), 1)
            self.assertEqual(result.children[0].value, "This is a paragraph.")
            mock_text_to_children.assert_called_once_with("This is a paragraph. Another line.")

    def test_process_code_invalid(self):
        block = "```code"
        with self.assertRaises(ValueError) as context:
            process_code(block)
        self.assertIn("Invalid code block", str(context.exception))

    def test_process_code_valid(self):
        with patch('markdown_blocks.text_to_children',
                   return_value=[LeafNode(None, "print('Hello')")]) as mock_text_to_children:
            block = "```\nprint('Hello')\n```"
            result = process_code(block)
            self.assertEqual(result.tag, "code")
            self.assertEqual(len(result.children), 1)
            self.assertEqual(result.children[0].value, "print('Hello')")
            mock_text_to_children.assert_called_once_with("print('Hello')")

    def test_process_quote(self):
        with patch('markdown_blocks.text_to_children',
                   return_value=[LeafNode(None, "Quoted text. Another quote line.")]) as mock_text_to_children:
            block = "> Quoted text.\n> Another quote line."
            result = process_quote(block)
            self.assertEqual(result.tag, "blockquote")
            self.assertEqual(len(result.children), 1)
            self.assertEqual(result.children[0].value, "Quoted text. Another quote line.")
            mock_text_to_children.assert_called_once_with("Quoted text. Another quote line.")

    def test_process_quote_invalid(self):
        block = "Quoted text without leading >"
        with self.assertRaises(ValueError) as context:
            process_quote(block)
        self.assertIn("Invalid quote block", str(context.exception))

    def test_process_list_valid_unordered(self):
        with patch('markdown_blocks.text_to_children') as mock_text_to_children:
            # Mock children creation for first and second list items
            mock_text_to_children.side_effect = [
                [LeafNode(None, "First item")],
                [LeafNode(None, "Second item")]
            ]
            block = "- First item\n- Second item"
            result = process_list(block, "ul", r"^[\*\-]\s", 2)
            self.assertEqual(result.tag, "ul")
            self.assertEqual(len(result.children), 2)
            self.assertEqual(result.children[0].tag, "li")
            self.assertEqual(result.children[0].children[0].value, "First item")
            self.assertEqual(result.children[1].children[0].value, "Second item")

    def test_process_list_invalid(self):
        block = "* Item\nThis line is invalid"
        with self.assertRaises(ValueError) as context:
            process_list(block, "ul", r"^[\*\-]\s", 2)
        self.assertIn("Invalid list block", str(context.exception))


if __name__ == '__main__':
    unittest.main()
