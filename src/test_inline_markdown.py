import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_split_nodes_multiple(self):
        node = TextNode("`code` and `more code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[1].text, " and ")
        self.assertEqual(new_nodes[2].text, "more code")

    def test_split_nodes_no_split(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text")

    def test_split_nodes_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_nodes_missing_delimiter(self):
        node = TextNode("This is `invalid markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zcew34n.png) and another ![second](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zcew34n.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://www.example.com/another"),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode("[link](https://boot.dev) is at the start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zcew34n.png) and ![another](https://i.imgur.com/3elNhQu.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("image", "https://i.imgur.com/zcew34n.png"))
        self.assertEqual(matches[1], ("another", "https://i.imgur.com/3elNhQu.png"))

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("link", "https://www.example.com"))
        self.assertEqual(matches[1], ("another", "https://www.example.com/another"))

    def test_extract_links_ignores_images(self):
        text = (
            "This is an ![image](https://url.com/img.png) and a [link](https://url.com)"
        )
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "https://url.com"))

    def test_extract_images_ignores_links(self):
        text = (
            "This is an ![image](https://url.com/img.png) and a [link](https://url.com)"
        )
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("image", "https://url.com/img.png"))


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )

    def test_bold_only(self):
        nodes = text_to_textnodes("**bold text**")
        self.assertListEqual(
            [TextNode("bold text", TextType.BOLD)],
            nodes,
        )

    def test_italic_only(self):
        nodes = text_to_textnodes("*italic text*")
        self.assertListEqual(
            [TextNode("italic text", TextType.ITALIC)],
            nodes,
        )

    def test_code_only(self):
        nodes = text_to_textnodes("`code block`")
        self.assertListEqual(
            [TextNode("code block", TextType.CODE)],
            nodes,
        )

    def test_image_only(self):
        nodes = text_to_textnodes("![alt text](https://example.com/img.png)")
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")],
            nodes,
        )

    def test_link_only(self):
        nodes = text_to_textnodes("[click here](https://example.com)")
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://example.com")],
            nodes,
        )

    def test_all_types_combined(self):
        text = "This is **bold** and *italic* and `code` and an ![image](https://url.com/img.png) and a [link](https://url.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://url.com/img.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://url.com"),
            ],
            nodes,
        )

    def test_multiple_bold(self):
        nodes = text_to_textnodes("**first** and **second**")
        self.assertListEqual(
            [
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.BOLD),
            ],
            nodes,
        )

    def test_multiple_italic(self):
        nodes = text_to_textnodes("*one* *two* *three*")
        self.assertListEqual(
            [
                TextNode("one", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("three", TextType.ITALIC),
            ],
            nodes,
        )

    def test_multiple_code(self):
        nodes = text_to_textnodes("`a` and `b`")
        self.assertListEqual(
            [
                TextNode("a", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.CODE),
            ],
            nodes,
        )

    def test_multiple_images(self):
        nodes = text_to_textnodes("![one](https://a.com) ![two](https://b.com)")
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://a.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://b.com"),
            ],
            nodes,
        )

    def test_multiple_links(self):
        nodes = text_to_textnodes("[a](https://a.com) [b](https://b.com)")
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
            ],
            nodes,
        )

    def test_bold_and_italic_adjacent(self):
        nodes = text_to_textnodes("**bold***italic*")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_code_with_special_chars(self):
        nodes = text_to_textnodes("run `print('hello')`")
        self.assertListEqual(
            [
                TextNode("run ", TextType.TEXT),
                TextNode("print('hello')", TextType.CODE),
            ],
            nodes,
        )

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual(
            [],
            nodes,
        )

    def test_image_and_link_mixed(self):
        nodes = text_to_textnodes(
            "![img](https://img.com) and [link](https://link.com)"
        )
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://img.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
            ],
            nodes,
        )

    def test_text_before_and_after_formatting(self):
        nodes = text_to_textnodes("start **bold** middle *italic* end")
        self.assertListEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
            ],
            nodes,
        )

    def test_unclosed_bold_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unclosed bold")

    def test_unclosed_italic_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is *unclosed italic")

    def test_unclosed_code_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is `unclosed code")

    def test_link_with_formatting_around(self):
        nodes = text_to_textnodes("**bold** [link](https://url.com) *italic*")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://url.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
