import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """split text nodes by delimiter and apply text type to delimited content"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # if parts returns even amount of indexes, it's invalid markdown
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown: matching delimiter '{delimiter}' not found"
            )

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    """extract image nodes from text and split into separate nodes"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        # if there are no images, it's all text
        if len(images) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text
        for image in images:
            parts = original_text.split(f"![{image[0]}]({image[1]})", 1)
            # the parts should be two, otherwise split failed and
            # the image markdown was malformed
            if len(parts) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            # in the case where there's text before the image
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = parts[1]

        # for leftover text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """extract link nodes from text and split into separate nodes"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        # if there are no links, it's all text
        if len(links) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text
        for link in links:
            parts = original_text.split(f"[{link[0]}]({link[1]})", 1)
            # the parts should be two, otherwise split failed and
            # the link markdown was malformed
            if len(parts) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            # in the case where there's text before the link
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = parts[1]

        # for leftover text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    """extract all image markdown patterns from text, returning tuples of (alt, src)"""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """extract all link markdown patterns from text, returning tuples of (text, url)"""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    """parse text into a list of text nodes with proper formatting types"""
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
