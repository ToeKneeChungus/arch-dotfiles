#! /usr/bin/python3
import os 
import click
import subprocess
import sys
import time 
from pathlib import Path
import i3ipc
import signal 


notes_directory = Path("/home/toekneechungus/notes")

def cn():
    notes = [f.name for f in notes_directory.glob("*")]
    ignore = ['template', '.git', '.DS_Store','preamble.tex']
    for i in ignore:
        notes.remove(i)
    rofi_input = "\n".join(notes)
    result = subprocess.run(['rofi','-dmenu','-p','Enter subject name: '],input=rofi_input, capture_output=True, text=True)
    output = result.stdout.strip()
    return(output)

'''
def text(text_dir):
    text_directory = Path("/home/toekneechungus/Documents/textbooks/"+text_dir)
    text= [f.name for f in text_directory.glob("*.pdf")]
    rofi_input = "\n".join(text)
    result = subprocess.run(['rofi','-dmenu','-p','Select textbook title: '],input=rofi_input, capture_output=True, text=True)
    output = result.stdout.strip()
    return(output)
'''


def opennvim(directory):
    os.chdir(directory)        
    command = f"kitty -e nvim master.tex"
    # Run the command to open Neovim in a new Alacritty window
    subprocess.Popen(command, shell=True)


def opennote(directory):
    os.chdir(directory)
    command = f"zathura master.pdf"
    subprocess.Popen(command, shell=True)

def opentext(directory, fname):
    os.chdir(directory)
    command = f"zathura {fname}"
    subprocess.Popen(command, shell=True)

name = cn()
if name=="":
    sys.exit("Error Message")
else:
    #layout with vim zathura
    ranoutofvar = Path("/home/toekneechungus/notes/"+name+"/notes")
    opennote(ranoutofvar)
    opennvim(ranoutofvar)
