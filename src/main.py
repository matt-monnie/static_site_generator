from pathlib import Path

from generate_page import generate_page, generate_pages_recursive
from utils import copy_directory

PUBLIC_DIR = "public"
STATIC_DIR = "static"


def main():
    copy_directory(STATIC_DIR, PUBLIC_DIR)


    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page("content/index.md", "template.html", "public/index.html")

    generate_pages_recursive(Path("content").iterdir(), "template.html", Path("public"))


# Run the main game loop if this script is executed directly
if __name__ == "__main__":
    main()