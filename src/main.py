from block_markdown import generate_pages_recursive
from file_utils import copy_directory


def main():
    # copy static files to public
    copy_directory("static", "public")

    # generate all pages from markdown files in content directory
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
