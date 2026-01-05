import os
import shutil


def copy_directory(src, dst):
    """
    recursively copy all contents from src directory to dst directory.
    deletes dst contents first for a clean copy.
    """
    # delete destination if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Deleted existing directory: {dst}")

    # create destination directory
    os.mkdir(dst)
    print(f"Created directory: {dst}")

    # copy all contents recursively
    _copy_contents(src, dst)


def _copy_contents(src, dst):
    """helper function to recursively copy contents."""
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        else:
            # it's a directory, create it and recurse
            os.mkdir(dst_path)
            print(f"Created directory: {dst_path}")
            _copy_contents(src_path, dst_path)
