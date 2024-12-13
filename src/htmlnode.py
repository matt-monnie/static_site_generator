class HTMLNode:
    """
    Represents a general-purpose HTML node.

    This class is designed to model a generic HTML element, providing the ability
    to store essential attributes such as the tag name, inner value, child nodes,
    and HTML properties. It is primarily intended to enable structured HTML element
    manipulation and rendering.

    :ivar tag: The tag name of the HTML element (e.g., 'div', 'span'). Defaults to None.
    :type tag: str or None
    :ivar value: The text or inner value of the HTML element. Defaults to None.
    :type value: str or None
    :ivar children: A list of child HTMLNode elements. Defaults to None.
    :type children: list or None
    :ivar props: A dictionary of HTML attributes and their corresponding values. Defaults to None.
    :type props: dict or None
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
    Represents a leaf node in an HTML document structure.

    This class extends the HTMLNode class and is used to represent an HTML
    element that does not have any child elements. It supports rendering
    the HTML representation of the element as a string.

    :ivar tag: The tag name of the HTML element (e.g., "div", "p").
    :ivar value: The content or text contained within the HTML element.
    :ivar props: A dictionary of properties or attributes for the HTML
        element (e.g., style, class). Default is None.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """
    Represents an HTML parent node in the DOM hierarchy.

    This class extends the HTMLNode class and serves as a
    representation of an HTML node that contains child nodes.
    It manages the HTML generation and provides a textual
    representation for debugging purposes. This class requires
    a tag name and a list of child nodes to be specified during
    initialization.

    :ivar tag: The HTML tag name of the node (e.g., "div", "p"). Must not be None.
    :type tag: str
    :ivar children: A list of child nodes contained within this node. Must not be None.
    :type children: list[HTMLNode]
    :ivar props: Optional properties or attributes for the node (e.g., style, class).
    :type props: dict or None
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
