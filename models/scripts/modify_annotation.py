#-------------------------------------------------------------------------------
# Name:        moidfy_annotation_path
# Purpose:     strips old path from the annotaion
# Environment: Windows 10 OS, Python 3.6
# Author:      No This Is Patrick
#
# Created:     17/02/2018
# Modify XML File Library: https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# Get current directory: https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
# XML manipulation: https://stackoverflow.com/questions/37868881/how-to-search-and-replace-text-in-an-xml-file-using-python
#
# Commands: 1. You can provide no arguments, where you will be prompted to
#              select the .xml file's directory and the new path string for the files
#           2. You can provide a single command line argument for the new path string
#              and you will be prompted to select the .xml file's directory
#           3. You may provide two arguments where you provide the .xml file's directory
#              and the newly desired path string
#-------------------------------------------------------------------------------
import os # directory library
import sys # sys.argv library
import xml.etree.ElementTree as ET
from tkinter.filedialog import askdirectory
from PIL import Image
"""
#
"""
def replace_file_path(f_name, new_path, label):
    array = []
    name = f_name.split("\\")
    name = name[len(name)-1]
    #print(name, new_path)

    try:
        with open(f_name, encoding='utf-8') as f:
          tree = ET.parse(f)
          root = tree.getroot()

          for path in root.iter(label):
            print(label)
            if(label == "filename"):
                name = name.split("/")
                name = name[len(name)-1]
                if(not name.endswith(".jpg")):
                    name += ".jpg"
                path.text = str(name)
                print(path.text)
            else:
                name = name[:len(name)-4]
                path.text = str(new_path + "/" + name + ".jpg")
          tree.write(f_name)
    except:
        print("Error: Unable to extract .xml file contents!!!", f_name)
        exit(1)

# modify <name> </name>
# modify <filename>

def main():
    label = ""

    if(len(sys.argv) > 1 and sys.argv[1] == "-filename"):
        label = "filename"
        if(len(sys.argv) == 4):
            directory = sys.argv[2]
            new_path = sys.argv[3]
        elif(len(sys.argv) == 3):
            print("Select the directory containing the annotated files")
            directory = askdirectory()
            new_path = sys.argv[2]
        elif(len(sys.argv) == 2):
            print("Select the directory containing the annotated files")
            directory = askdirectory()
            print("Select the directory containing the new path for the files")
            new_path = askdirectory()
        else:
            print("Usage: <program name> <directory of .xml files> <new path name>")
            print("OR")
            print("Usage: <program name>")
            exit(1)
    else:
        label = "path"
        if(len(sys.argv) == 3):
            directory = sys.argv[1]
            new_path = sys.argv[2]
        elif(len(sys.argv) == 2):
            print("Select the directory containing the annotated files")
            directory = askdirectory()
            new_path = sys.argv[1]
        elif(len(sys.argv) == 1):
            print("Select the directory containing the annotated files")
            directory = askdirectory()
            print("Select the directory containing the new path for the files")
            new_path = askdirectory()
        else:
            print("Usage: <program name> <directory of .xml files> <new path name>")
            print("OR")
            print("Usage: <program name>")
            exit(1)

    try:
        for file in os.listdir(directory):
            if(file.endswith(".xml")):
                file = os.path.join(directory, file)
                replace_file_path(file, new_path, label)
    except:
        print("Error: Wut?!")
        exit(1)

if __name__ == '__main__':
    main()
