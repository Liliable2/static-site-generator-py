import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
