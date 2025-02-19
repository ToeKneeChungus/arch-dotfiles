#! /usr/bin/python3
import os
from pathlib import Path
import click 
import platform 
import subprocess
import time
import sys
import signal

#file path to template
template = Path("/home/toekneechungus/.config/nvim/templates/template.svg")
#subprocess.Popen(['inkscape', str(file_path)])

#get path and file name, current line number 
path = os.getcwd()
loc = sys.argv[1]
fp = loc.split("/")
line = sys.argv[2]
p = fp[-3]
filename = fp[-1]


#rofi script prompting figure name 
def picker():
    path = os.getcwd()
    p = path.split("/")[-1]
    figures_directory = Path(f"/home/toekneechungus/Documents/school/{p}/notes/figures")
    svg_files = [f.name[:-4] for f in figures_directory.glob("*.svg")]
    rofi_input = "\n".join(svg_files)
    result = subprocess.run(['rofi','-dmenu','-p','Enter figure name: '],input=rofi_input, capture_output=True, text=True)
    figure_name = result.stdout.strip()
    return figure_name



#quit inkscape when figure is saved 
def polling(file_path, initial_mtime):
    while True:
        current_mtime = os.path.getmtime(file_path)
        if current_mtime != initial_mtime:
            print("modification detected")
            break
        time.sleep(1)


#insert figure after saved
def insert(filePath, fig, ln):

    latex_command = f"\n\\begin{{center}}\n     \\def\\svgwidth{{10cm}}\n    \\input{{./figures/{fig}.pdf_tex}}\n  \\end{{center}}\n"
    with open(filePath, 'r') as file:
        lines = file.readlines()
    insertion_index = int(ln)-1
    lines.insert(insertion_index, latex_command + '\n')

    with open(filePath, 'w') as file:
        file.writelines(lines)   






figure_name = picker()
if figure_name=="":
    sys.exit("Error Message")
else:
    print(figure_name)

#choose current path of notes 
svg_output_path = Path("/home/toekneechungus/Documents/school/"+p+"/notes/figures/"+figure_name+".svg")
pdf_output_path = Path("/home/toekneechungus/Documents/school/"+p+"/notes/figures/"+figure_name+".pdf")
tex_output_path = Path("/home/toekneechungus/Documents/school/"+p+"/notes/figures/"+figure_name+".pdf_tex")


#check if the figure is a duplicate and if not, make a copy
update = False
if not(svg_output_path.exists()):
    subprocess.run(['cp', str(template), str(svg_output_path)])
else:
    update = True


#open inkscape 
initial_mtime = os.path.getmtime(svg_output_path)
inkscape_process = subprocess.Popen(['inkscape',str(svg_output_path)], stderr=subprocess.DEVNULL)
polling(svg_output_path, initial_mtime)
#export to pdf
subprocess.run(['inkscape', str(svg_output_path), '--export-latex','--export-filename',str(pdf_output_path)])
inkscape_process.terminate()

#only insert when the figure is new
if update==False:
    insert(filename,figure_name,line)
else:
    print("updated figure")
