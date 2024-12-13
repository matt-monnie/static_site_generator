import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode


class TestHTMLNode(unittest.TestCase):
    """
    Unit tests for validating the behavior and output of HTMLNode, LeafNode,
    and ParentNode classes in relation to constructing HTML elements and
    hierarchies dynamically.

    The tests ensure correct rendering of HTML strings with proper handling
    of attributes, textual content, child elements, and edge cases like
    missing tags.

    :ivar test_to_html_props: Verifies if HTML attributes are correctly
        converted to HTML-compatible properties string for a single node.
    :type test_to_html_props: callable
    :ivar test_values: Validates the direct attribute values of a node
        (tag, value, children, and props) when constructed.
    :type test_values: callable
    :ivar test_repr: Tests the string representation (__repr__) of an
        HTMLNode object for accuracy.
    :type test_repr: callable
    :ivar test_to_html_no_children: Confirms HTML string generation for
        a node without child elements.
    :type test_to_html_no_children: callable
    :ivar test_to_html_no_tag: Confirms that nodes without a tag render
        only their value as plain text in the HTML output.
    :type test_to_html_no_tag: callable
    :ivar test_to_html_with_children: Validates HTML construction for a
        parent node containing child nodes.
    :type test_to_html_with_children: callable
    :ivar test_to_html_with_grandchildren: Tests correct HTML generation
        for nested structures involving children and grandchildren elements.
    :type test_to_html_with_grandchildren: callable
    :ivar test_to_html_many_children: Ensures proper rendering of nodes with
        multiple children having varying content like bold and italic nodes.
    :type test_to_html_many_children: callable
    :ivar test_headings: Verifies the correct rendering of heading tags
        (e.g., h2) with mixed inline child elements.
    :type test_headings: callable
    """
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
