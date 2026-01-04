import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a", "Click me", None, {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://example.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "No props")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div", "Content", None, {"id": "main"})
        expected = (
            "HTMLNode(tag='div', value='Content', children=None, props={'id': 'main'})"
        )
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
