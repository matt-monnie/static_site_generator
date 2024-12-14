import os
import shutil

def copy_directory(src, dest):
    """Recursively copies the entire content of 'static' directory to 'public' directory."""
    if not os.path.exists(src):
        print(f"No {src} directory found")
        return

    # Delete the existing public directory if present
    delete_directory(dest)

    # Recursively copy contents from static to public
    recursive_copy(src, dest)
    print(f"Copied all files from {src} to {dest}")


def delete_directory(dest):
    """Deletes the existing 'public' directory along with its contents."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted current {dest} directory")
    else:
        print(f"No {dest} directory found")


def recursive_copy(src, dst):
    """Recursively copies files and directories from src to dst."""
    if os.path.isdir(src):
        # Ensure the destination directory exists
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            # Recursive call for subdirectories and files
            recursive_copy(src_path, dst_path)
    else:
        # Copy file from src to dst
        shutil.copy2(src, dst)


