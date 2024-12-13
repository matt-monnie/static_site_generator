from inline_markdown import *
from markdown_blocks import markdown_to_blocks
from textnode import TextNode, TextType

def main():
    textnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(textnode)

    cleaned_image_text = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    #print(cleaned_image_text)

    cleaned_link_text = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    #print(cleaned_link_text)

    #node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
    #split_image_text = split_nodes_images([node])
    #print(split_image_text)

    #link_node = TextNode(
    #    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #    TextType.TEXT,
    #)
    #new_link_node = split_nodes_links([link_node])
    #print(new_link_node)

    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    text_to_textnodes(text)

    markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
    markdown_to_blocks(markdown)



# Run the main game loop if this script is executed directly
if __name__ == "__main__":
    main()