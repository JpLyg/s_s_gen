from src.textnode import TextNode, TextType
from src.htmlnode import *
import os
import shutil
import sys

def folder_operation(subroot):
    print(subroot)
    public_dir = os.path.join(subroot,"docs")
    static_dir = os.path.join(subroot,"static")

    print("static dir:",static_dir)

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    os.makedirs(public_dir, exist_ok=True)

    for item in os.listdir(static_dir):
        from_loc = os.path.join(static_dir,item)
        to_loc = os.path.join(public_dir,item)

        if os.path.isdir(from_loc):
            shutil.copytree(from_loc,to_loc)
        else:
            shutil.copy(from_loc,to_loc)

#step1
def extract_title(markdown):
    header = markdown.split("#",1)
    #print(header)
    if header[0].lstrip() != "": raise Exception("invalid header")
    header_1 = header[1].split("\n")[0]
    #print(header_1)

    return header_1
    
    
#step 5
def generate_page(from_path, template_path, dest_path,basepath):
    #step 5.1
    #print(f"generating page from {from_path} to {dest_path} using {template_path}")
    #step 5.2

    with open(from_path) as f:
        content= f.read()

    #step 5.3
    with open(template_path) as f:
        template= f.read()
    #step 5.4
    proc  = markdown_to_html_node(content)
    proc_2 = proc.to_html()
    #step 5.5
    title = extract_title(content)
    #step 5.6
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}",proc_2)
    print(basepath)
    

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    template = template.replace("{{ basepath }}",basepath)
    #step 5.7

    #dir_path = os.path.dirname(dest_path)
    #os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    for item in os.listdir(dir_path_content):
        current = os.path.join(dir_path_content,item)

        if os.path.isdir(current):
            target = os.path.join(dest_dir_path,item)
            generate_pages_recursive(current,template_path,target,basepath)
        else:
            fileset = os.path.splitext(current)
            if fileset[1] == ".md":

                #print("content dir:",dir_path_content)
                #print("public dir:",dest_dir_path)

                os.makedirs(dest_dir_path,exist_ok=True)

                filename = os.path.basename(current).split(".")[0] + ".html"        
                filename = os.path.join(dest_dir_path,filename)

                #print("filename:",filename)
                
                generate_page(current,template_path,filename,basepath)



            

    return

def main():
    #print(TextNode("text text",TextType.BOLD,"https://www.boot.dev"))
    if len(sys.argv) >1:
        basepath  = sys.argv[1]
    else: basepath = "/"

    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"

    sub_root = os.path.dirname(os.path.abspath(__file__))
    #sub_root = os.path.join(sub_root,basepath)
    source_dir = os.path.join(sub_root,"content")
    template_dir = os.path.join(sub_root,"template.html")
    target_dir = os.path.join(sub_root,"docs")

    folder_operation(sub_root)
    generate_pages_recursive(source_dir,template_dir,target_dir,basepath)

if __name__ == "__main__":
    main()


    