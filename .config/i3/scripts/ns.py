#! /usr/bin/python3
import os 
import click
import subprocess
import sys
import time 
from pathlib import Path
import i3ipc
import signal 


notes_directory = Path("/home/toekneechungus/Documents/school")

def cn():
    notes = [f.name for f in notes_directory.glob("*")]
    ignore = ['template']
    for i in ignore:
        notes.remove(i)
    rofi_input = "\n".join(notes)
    result = subprocess.run(['rofi','-dmenu','-p','Enter subject name: '],input=rofi_input, capture_output=True, text=True)
    output = result.stdout.strip()
    return(output)


def text(text_dir):
    text_directory = Path("/home/toekneechungus/Documents/textbooks/"+text_dir)
    text= [f.name for f in text_directory.glob("*.pdf")]
    rofi_input = "\n".join(text)
    result = subprocess.run(['rofi','-dmenu','-p','Select textbook title: '],input=rofi_input, capture_output=True, text=True)
    output = result.stdout.strip()
    return(output)




def opennvim(directory):
    os.chdir(directory)        
    command = f"alacritty -e nvim master.tex"
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
    td = text_dir()
    if td=="":
        #layout with vim zathura
        ranoutofvar = Path("/home/toekneechungus/Documents/notes/"+name)
        opennvim(ranoutofvar)
        opennote(ranoutofvar)
    else:
        title = text(td).replace(" ",r"\ ")
        tbpath = Path("/home/toekneechungus/Documents/textbooks/"+td)
        morevar = Path("/home/toekneechungus/Documents/notes/"+name)
        opennote(morevar)
        opennvim(morevar)
        opentext(tbpath,title)
