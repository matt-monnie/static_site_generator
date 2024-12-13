from utils import copy_directory

PUBLIC_DIR = "public"
STATIC_DIR = "static"


def main():
    copy_directory(STATIC_DIR, PUBLIC_DIR)


# Run the main game loop if this script is executed directly
if __name__ == "__main__":
    main()