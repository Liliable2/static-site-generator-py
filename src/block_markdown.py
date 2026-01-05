from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # check for heading (1-6 # characters followed by space)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # check for code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # check for quote (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # check for ordered list (lines start with 1. 2. 3. etc.)
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # default to paragraph
    return BlockType.PARAGRAPH
