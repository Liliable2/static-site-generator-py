from block_markdown import generate_page
from file_utils import copy_directory


def main():
    # copy static files to public
    copy_directory("static", "public")

    # generate index page from markdown
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
