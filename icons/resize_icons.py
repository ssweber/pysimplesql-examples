# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import PySimpleGUI as sg
import os
import base64
import pprint
import glob, os
from PIL import Image

'''
    Resize icons in folder
    input:  folder with .png
    output: Writes a output folder with resized images
'''
size = 128, 128

def main():
    folder = sg.popup_get_folder('Source folder for images\nImages will be resized and saved in new folder', title='Image Thumbnails')

    if not folder:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return
    
    for infile in glob.glob(f'{folder}/*.png'):
        folder = os.path.basename(infile)
        new_folder = f'{folder}/{size[0]}x{size[1]}'
        os.mkdir(new_folder)
        with Image.open(infile) as im:
            im.thumbnail(size)
            im.save(f'{new_folder}/', "PNG")
    sg.popup('Completed!')

if __name__ == '__main__':
    main()