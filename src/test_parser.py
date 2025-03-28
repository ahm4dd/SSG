import unittest

from parser import *

class TestParser(unittest.TestCase):
    def test_no_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([TextNode("Hello world", TextType.TEXT)], "", TextType.TEXT)

    def test_split_nodes_delimiter(self):

        nodes = split_nodes_delimiter([TextNode("Hello _test_ world", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "test")
        self.assertEqual(nodes[2].text, " world")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

        nodes = split_nodes_delimiter([TextNode("Hello **test** world", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "test")
        self.assertEqual(nodes[2].text, " world")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multilple_nodes_split_nodes(self):
        nodes = split_nodes_delimiter([TextNode("Hello _test_ world", TextType.TEXT), TextNode("Hello test _world_", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "test")
        self.assertEqual(nodes[2].text, " world")
        self.assertEqual(nodes[3].text, "Hello test ")
        self.assertEqual(nodes[4].text, "world")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.TEXT)
        self.assertEqual(nodes[4].text_type, TextType.ITALIC)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)
    
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_extract_title(self):
        title = "# Hello"
        self.assertEqual('Hello', extract_title(title))
        
        title = "# Hello \nWhats up"
        self.assertEqual('Hello', extract_title(title))

        title = "# Hello \n\nWhats up"
        self.assertEqual('Hello', extract_title(title))
        
        title = 'htehto\n## Hello \n# this is the title \n#NOTITLE\n hello\n\n\n\n### HELLO THERE'
        self.assertEqual('this is the title', extract_title(title))