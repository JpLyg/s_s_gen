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

    def test_text(self):
        
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
        


if __name__ == "__main__":
    unittest.main()