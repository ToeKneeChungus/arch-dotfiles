#! /usr/bin/python3
import os
from sys import exit
from rofi import Rofi
from pathlib import Path
import pynvim
import sys

#get path and file name, current line number 
path = os.getcwd()
loc = sys.argv[1]
fp = loc.split("/")
line = sys.argv[2]
p = fp[-3]
filename = fp[-1]



#prompt figure name with rofi 
r = Rofi()
name = r.text_entry("Figure Name: ")
if (r == ""):
    exit(0)
bashCommand = "maim -s ~/Documents/school/"+p+"/notes/figures/"+name+".png"
os.system(bashCommand) #take screenshot and insert it to figures folder 


#insert file to latex 
def insert(filePath, imgname, ln):
    latex_command = f"\n\\begin{{center}}\n    \\includegraphics[width=7cm]{{{imgname}}}\n  \\end{{center}}\n"

    with open(filePath, 'r') as file:
        lines = file.readlines()
    insertion_index = int(ln)-1
    lines.insert(insertion_index, latex_command + '\n')

    with open(filePath, 'w') as file:
        file.writelines(lines)

img = name+".png"
insert(loc, img, line);
