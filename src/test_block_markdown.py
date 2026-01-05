import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
# This is a heading


This is a paragraph of text.


- This is a list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text.",
                "- This is a list",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = "   # Heading with spaces   \n\n   Paragraph with spaces   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "Paragraph with spaces",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_heading_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote_missing_one(self):
        block = ">First line\nSecond line without >\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_not_unordered_list_no_space(self):
        block = "-NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. Only item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list_wrong_start(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_skip_number(self):
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_no_space(self):
        block = "1.NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is just a regular paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    def test_paragraph_with_inline(self):
        md = "This is **bold** and *italic* text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><p>This is <b>bold</b> and <i>italic</i> text.</p></div>"
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_heading_with_inline(self):
        md = "# This is **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is <b>bold</b> heading</h1></div>")

    def test_code_block(self):
        md = "```\ndef hello():\n    print('world')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><pre><code>def hello():\n    print('world')</code></pre></div>"
        )

    def test_code_block_no_inline_parsing(self):
        md = "```\nThis has **bold** but should not be parsed\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This has **bold** but should not be parsed</code></pre></div>",
        )

    def test_quote(self):
        md = ">This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_quote_multiline(self):
        md = ">First line\n>Second line"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>First line Second line</blockquote></div>"
        )

    def test_quote_with_inline(self):
        md = ">This is **bold** in a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is <b>bold</b> in a quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = "- Item with **bold**\n- Item with *italic*"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <i>italic</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        md = "1. Item with `code`\n2. Item with [link](https://example.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>Item with <code>code</code></li><li>Item with <a href="https://example.com">link</a></li></ol></div>',
        )

    def test_full_document(self):
        md = """# Welcome

This is a **paragraph**.

- Item 1
- Item 2

```
code here
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Welcome</h1><p>This is a <b>paragraph</b>.</p><ul><li>Item 1</li><li>Item 2</li></ul><pre><code>code here</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
