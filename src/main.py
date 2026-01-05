import sys

from block_markdown import generate_pages_recursive
from file_utils import copy_directory


def main():
    # get basepath from CLI argument, default to /
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # copy static files to docs
    copy_directory("static", "docs")

    # generate all pages from markdown files in content directory
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
