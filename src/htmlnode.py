from textnode import *
import re
class HTMLNode:
    def __init__(self,tag = None,value = None,children= None,props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception("Not set")
    
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

def text_node_to_html_node(text_node): #returns a leaf nodes
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
                #print("delimeter:",delimiter)
                #print("entry text:",entry.text)
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

def text_to_textnodes(text): #returns a list of textnodes
    #print("text:",text)
    superlist = [TextNode(text,TextType.TEXT)]
    superlist = split_nodes_delimiter(superlist,"**",TextType.BOLD)
    superlist = split_nodes_delimiter(superlist,"_",TextType.ITALIC)
    superlist = split_nodes_delimiter(superlist,"`",TextType.CODE)
    superlist = split_nodes_image(superlist)
    superlist = split_nodes_link(superlist)

    return superlist

def _markdown_to_blocks(markdown):
    content_list = markdown.split("\n\n")
    content_list = list(map(lambda x: x.strip(),content_list))
    content_list = list(filter(lambda x: len(x)>0, content_list))

    #print(content_list)
    return content_list

def markdown_to_blocks_phar(markdown):
    # splits on 2 or more consecutive line breaks, possibly with whitespace
    blocks = re.split(r"\n\s*\n", markdown)
    blocks = [block.strip() for block in blocks if block.strip()]
    blocks = [block.replace("\n", " ") for block in blocks]
    return blocks

def markdown_to_blocks(markdown):
    # splits on 2 or more consecutive line breaks, possibly with whitespace
    blocks = re.split(r"\n\s*\n", markdown)
    blocks = [block.strip() for block in blocks if block.strip()]
    #blocks = [block.replace("\n", " ") for block in blocks]
    return blocks


def block_to_block_type (markdown):

    parts = list(filter(lambda x: len(x)>0, markdown.split()))
    #print(parts)

    if len(parts[0]) <= 6 and parts[0].count("#") == len(parts[0]):
        #print(parts[0])
        #print("heading")
        return BlockType.HEADING
    
    if markdown[:3] == "```" and markdown[-1:-4:-1] == "```":
        #print (markdown[:3],"--",markdown[-1:-3])
        #print("code")
        return BlockType.CODE
    
    parts = list(filter(lambda x: len(x)>0, markdown.split("\n")))
    #print("parts",parts)
    quoute_check = list(filter(lambda x: x[0] == ">", parts))

    

    if len(parts) == len(quoute_check):
        #print(quoute_check)
        #print("quote")
        return BlockType.QUOTE

    unlist_check = list(
        filter(lambda x: x[:2] == "- "  
               and len(x.split("-",1)[1].strip())>0, 
               parts)
        )

    if len(parts) == len(unlist_check):
        #print(unlist_check)
        #print("unoredered list")
        return BlockType.UNORDERED_LIST
    
    list_check = True
    for i in range(len(parts)):
        splits = parts[i].split(".",1)

        if splits[0].isdigit() == False: 
            list_check = False
            break #check if the first part is numerical
        if i == 0 and splits[0] != "1": 
            list_check = False
            break #check if the first entry is 1
        if str(i+1) != splits[0]: 
            list_check = False
            break # check if they are in order
        if splits[1][0] != " ": 
            list_check = False
            break # no space after dot
        if len(splits[1].strip()) <1: 
            list_check = False
            break #no character after numerator

    if list_check: 
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text): #returns a list of leafnodes
    # Convert text to TextNodes (handling inline markdown)
    text_nodes = text_to_textnodes(text)  # You should have this function
    
    # Convert TextNodes to HTMLNodes
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # You should have this function
        html_nodes.append(html_node)
    
    return html_nodes

def to_list(child,delimiter):
    output = []
    for entry in child:
        a = ParentNode(delimiter,[entry])
        output.append(a)
    return a

def markdown_to_html_node(markdown):
    #step 1
    step1 = markdown_to_blocks(markdown)
    mainlist = []
    #print(step1)
    #step 2
    for units in step1:
        
        #step 2.1
        blocktype = block_to_block_type(units)
        #print("blocktype:",blocktype)

        #step 2.2
        #print(blocktype)
        if blocktype == BlockType.PARAGRAPH:
            mod_units = units.replace("\n"," ")            
            child = text_to_children(mod_units)
            node = ParentNode("p",child)

        if blocktype == BlockType.HEADING:
            level = units.split()[0].count("#")
            child = text_to_children(units)
            node = ParentNode(f"h{level}",child)

        if blocktype == BlockType.CODE:
            a = units[3:-3]
            a = a.lstrip("\n")
            child = LeafNode(None,a)
            pre_node = ParentNode("code",[child])
            node = ParentNode("pre",[pre_node])

        if blocktype == BlockType.QUOTE:
            child = text_to_children(units)
            node = ParentNode("blockquote",child)

        if blocktype == BlockType.UNORDERED_LIST:
            child = text_to_children(units)
            child = to_list(child,"li")
            node = ParentNode("ul",child)

        if blocktype == BlockType.ORDERED_LIST:
            child = text_to_children(units)
            child = to_list(child,"li")
            node = ParentNode("ol",[])
        mainlist.append(node)
        #print("node:",node)
        
    exert = ParentNode("div",mainlist)
    
    #print(exert.to_html())
    return exert

    #return ParentNode("div",mainlist)
        #step 2.3





        




def main():
    text = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    markdown_to_html_node(text)




if __name__ == "__main__":
    main()
