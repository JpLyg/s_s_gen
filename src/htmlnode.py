from textnode import *

class HTMLNode:
    def __init__(self,tag = None,value = None,children= None,props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""

        if self.props == None: return string
        for content in self.props:
            pre_string = None
            if self.props[content] != None:
                string+= f" {content}= \"{self.props[content]}\""

        return string
    
    def __repr__(self):
        
        tag = None
        value = None
        child = None
        props = None

        if self.tag != None: tag = f"'{self.tag}'"
        if self.value != None: value = f"'{self.value}'"
        if self.children != None: child = f"'{self.children}'"
        if self.props != None: props = f"'{self.props}'"


        return f"""HTMLNode=(tag={tag}, value={value}, 
        children = {child}, 
        props={props})"""

class LeafNode(HTMLNode):
    #def __init__(self, tag=None, value=None, children=None, props=None):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None: raise ValueError
        if self.tag == None: return self.value
        #props = self.props
        #if props:#props aint blank
        #print(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        #props is blank
        #return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children, props)

    def to_html(self):
        if self.tag == None: raise ValueError("No tag")

        if self.children == None: raise ValueError("No children")

        children_set = "".join(child.to_html() for child in self.children)
        #print(f"<{self.tag}{self.props_to_html()}>{children_set}</{self.tag}>")
        return f"<{self.tag}{self.props_to_html()}>{children_set}</{self.tag}>"
    
        #props is blank
        #return f"<{self.tag}>{children_set}</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType: raise Exception("invalid text type")

    if text_node.text_type == TextType.TEXT:#plain text
        return LeafNode(None,text_node.text,None)
    
    if text_node.text_type == TextType.BOLD:#bold text
        tag = "b"
        return LeafNode(tag,text_node.text,None)
    
    if text_node.text_type == TextType.ITALIC:#itatlic text
        tag = "i"
        return LeafNode(tag,text_node.text,None)   
    
    if text_node.text_type == TextType.CODE: #code text
        tag = "code"
        return LeafNode(tag,text_node.text,None)
    
    if text_node.text_type == TextType.LINK: #link
        tag = "a"
        prop = {
            "href": text_node.url
        }
        return LeafNode(tag,text_node.text,prop)
    
    if text_node.text_type == TextType.IMAGE: #image
        tag = "img"
        prop = {
            "src": text_node.url,
            "alt": text_node.text
        }
        return LeafNode(tag,"",prop)   

#return f"<{self.tag}{self.props_to_html()}>{children_set}</{self.tag}>"