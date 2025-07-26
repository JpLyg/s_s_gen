import unittest
from htmlnode import *

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    '''
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,None)
        self.assertEqual(node, node2)

    def test_nq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_nq_2(self):
        node = TextNode("This is a text node2", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,None)
        self.assertNotEqual(node, node2)
    
    def test_nq_3(self):
        node = TextNode("This is a text node", TextType.BOLD,"")
        node2 = TextNode("This is a text node", TextType.BOLD,None)
        self.assertNotEqual(node, node2)
    

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    '''

    def _test_text(self):
        
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **text** node", TextType.TEXT)
        list1 = [node1,node2]
        node3 = TextNode("**This** is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.TEXT)
        list2 = [node3,node4]
        new_list1 = split_nodes_delimiter(list1,"**",TextType.BOLD)
        new_list2 = split_nodes_delimiter(list2,"**",TextType.BOLD)
        print("n1:",new_list1)
        print("n2:",new_list2)
        self.assertNotEqual(new_list1,new_list2)
        
    def _test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def _test_split_images(self):
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
   
    
    def _test_superlist(self):
        text1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text2 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) 2nd entry"

        self.assertNotEqual(text_to_textnodes(text1),text_to_textnodes(text2))
    
    def _test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def _test_block_to_block_type(self):
        name1=""">All that glitters
>is not gold."""
        name2 = """>All that glitters
>is indeed not gold.
"""
        self.assertEqual(block_to_block_type(name1),block_to_block_type(name2))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        print("node:\n",node.to_html())
        print ("expected:\n",expected)
        print("---------------------------------------------------------------------------")
        print(repr(html))
        print(repr("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"))
        print("---------------------------------------------------------------------------")
        print(html.encode('utf-8'))
        print(expected.encode('utf-8'))
        self.assertEqual(
            html,
            expected,
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        a = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()

        
        print("node:\n",node.to_html())
        print ("expected:\n",a)
        print("---------------------")

        self.assertEqual(
        html,
        a,
    )
        
        
if __name__ == "__main__":
    unittest.main()