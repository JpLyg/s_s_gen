from textnode import *
import re
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    mainlist = []
    
    for entry in old_nodes:
        
        count = entry.text.count(delimiter)

        if entry.text_type != TextType.TEXT or count == 0:
            #print("node not needed to process")
            mainlist.append(entry)
        else:
            if count % 2 != 0:
                raise Exception ("Unenclosed tag")
            else:
                #print("node valid for processing")
                sublist = entry.text.split(delimiter)
                tracker= 1
                start = 0
                for part in sublist:
                    if start == tracker:
                        tracker+=2
                        node = TextNode(part,text_type)
                    else:
                        node = TextNode(part,entry.text_type)
                    
                    #print(node)
                    mainlist.append(node)
                    start +=1

    return mainlist

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
    mainlist = []
    #print("test 1")
    for entry in old_nodes:
        #print(entry)
        sublist = extract_markdown_images(entry.text)
        #print(sublist)
        if len(sublist) <1 or entry.text_type != TextType.TEXT:
            mainlist.append(entry)

        else:
            
            #section_list = []
            text_to_proc = entry.text
            sections = []

            for sub in sublist:
                sections = text_to_proc.split(f"![{sub[0]}]({sub[1]})", 1)

                if len(sections[0]) >0:

                    mainlist.append(TextNode(sections[0],TextType.TEXT))

                mainlist.append(TextNode(sub[0],TextType.IMAGE,sub[1]))
                text_to_proc = sections[1]

            if len(text_to_proc) >0:                    
                mainlist.append(TextNode(text_to_proc,TextType.TEXT))

    #print(" fin list:",mainlist)
    return mainlist

def split_nodes_link(old_nodes):
    mainlist = []

    for entry in old_nodes:
        sublist = extract_markdown_links(entry.text)
        
        if len(sublist) <1 or entry.text_type != TextType.TEXT:
            mainlist.append(entry)

        else:
            #section_list = []
            text_to_proc = entry.text
            sections = []
            #print(entry)            
            for sub in sublist:
                sections = text_to_proc.split(f"[{sub[0]}]({sub[1]})", 1)
                #print(sections)
                if len(sections[0]) >0:

                    mainlist.append(TextNode(sections[0],TextType.TEXT))

                mainlist.append(TextNode(sub[0],TextType.LINK,sub[1]))
                text_to_proc = sections[1]

            if len(text_to_proc) >0:                    
                mainlist.append(TextNode(text_to_proc,TextType.TEXT))

    #print(" fin list:",mainlist)
    return mainlist

def text_to_textnodes(text):
    superlist = [TextNode(text,TextType.TEXT)]
    superlist = split_nodes_delimiter(superlist,"**",TextType.BOLD)
    superlist = split_nodes_delimiter(superlist,"_",TextType.ITALIC)
    superlist = split_nodes_delimiter(superlist,"`",TextType.CODE)
    superlist = split_nodes_image(superlist)
    superlist = split_nodes_link(superlist)

    return superlist


def main():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print("start:", text_to_textnodes(text))




if __name__ == "__main__":
    main()
