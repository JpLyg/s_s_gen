from htmlnode import *

def main():
    tag= "p"
    value = "test value"
    chilren = None
    sample_props = {
    "href": "https://www.google.com",
    "target": "_blank",
    }

    test = HTMLNode(tag,value,chilren,sample_props)
    
    print(test)
    print(test.props_to_html())

if __name__ == "__main__":
    main()