#! /usr/bin/python3
import os
from sys import exit
from rofi import Rofi
from pathlib import Path
import pynvim
import cv2
import numpy as np
import sys
import time

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
bashCommand = "maim -s ~/notes/"+p+"/notes/figures/"+name+".png"
os.system(bashCommand) #take screenshot and insert it to figures folder 

# mark transparent 
imgpath = os.path.expanduser("~/notes/"+p+"/notes/figures/"+name+".png")
print(imgpath)
image = cv2.imread(imgpath)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)


lower_bound = np.array([0, 0, 200], dtype=np.uint8)  # Light colors (white)
upper_bound = np.array([180, 50, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, lower_bound, upper_bound)
mask_inv = cv2.bitwise_not(mask)

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
b, g, r = cv2.split(image)
alpha = mask_inv  # Use the inverted mask as alpha channel
transparent_image = cv2.merge([b, g, r, alpha])
# Save the transparent image
cv2.imwrite(imgpath, transparent_image)



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
