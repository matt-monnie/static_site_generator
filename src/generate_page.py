from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    """Extracts the title from a markdown file."""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No title found in the markdown file")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    title = extract_title(markdown)

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)

    html = node.to_html()

    with open(dest_path, "w") as f:
        f.write(template.replace("{{ Title }}", title).replace("{{ Content }}", html))


def generate_pages_recursive(dir_path_content, template_path, dest_path):
    for file in dir_path_content:
        if file.is_dir():
            (dest_path / file.name).mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(file.iterdir(), template_path, dest_path / file.name)
        else:
            generate_page(
                file,
                template_path,
                dest_path / file.with_suffix(".html").name,
            )