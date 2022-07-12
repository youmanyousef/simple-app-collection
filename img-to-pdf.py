# this is the windows version, this requires WSL
# and a few packages on debian they are 
# pdfjam from texlive-extra-utils

from PIL import Image, UnidentifiedImageError
from PyPDF2 import PdfFileMerger
import sys
import os

files_dir = sys.argv[1]
output = f"{files_dir}.pdf"
papersize = "letter" # a4paper, letter, refer to https://github.com/rrthomas/pdfjam#documentation
#------
files = os.listdir(files_dir)
outs = []
merger = PdfFileMerger()
print("Converting...")
for file in files:
    file = f'{files_dir}/{file}'
    ## Validate images -- sanitize filenames later
    try:
        if file.split('.')[-1] == 'pdf':
            print('pass!')
            continue
        with Image.open(file) as img:
            filename = ''.join(file.split('.')[0])
            (img.convert('RGB')).save(filename+'.pdf')
            ##
            # We need to find a better way to do this, convert to letter format.
            ##
            cmd = f'wsl pdfjam "{filename}.pdf" --outfile "{filename}_c.pdf" --paper {papersize}'
            print(cmd)
            os.system(cmd)
            outs.append(f"{filename}.pdf")
            outs.append(f"{filename}_c.pdf")
            merger.append(f"{filename}_c.pdf")
            ##
            
    except UnidentifiedImageError:
        print(f"{file} is not an actual image file. Please input an actual file!")
        exit()

print("Merging...")
merger.write(output)
merger.close()
print("Cleaning...")
for file in outs:  
    os.remove(file)
