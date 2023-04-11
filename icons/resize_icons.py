# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import PySimpleGUI as sg
import os
import base64
import pprint
from PIL import Image, ImageOps
from pathlib import Path

'''
    Resize icons in folder
    input:  folder with .png
    output: Writes a output folder with resized images
'''
mapping = {
    "edit_protect": 'system-lock-screen',
    "quick_edit": 'document-edit',
    "save": 'document-save',
    "first": 'go-first',
    "previous": 'go-previous',
    "next": 'go-next',
    "last": 'go-last',
    "insert": 'document-new',
    "delete": 'edit-delete',
    "duplicate": 'edit-copy',
    "search": 'system-search',
    }

def main():
    folder = sg.popup_get_folder('Source folder for images\nImages will be resized and saved in new folder', title='Image Thumbnails')

    if not folder:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return
    
    answer = sg.popup_yes_no('Only resize icons with pysimplesql maps?')
    
    mapping = {
    "edit_protect": 'system-lock-screen',
    "quick_edit": 'document-edit',
    "save": 'document-save',
    "first": 'go-first',
    "previous": 'go-previous',
    "next": 'go-next',
    "last": 'go-last',
    "insert": 'document-new',
    "delete": 'edit-delete',
    "duplicate": 'edit-copy',
    "search": 'system-search',
    }
    
    global map_names
    map_names = []
    if answer == 'Yes':
        map_names = mapping.values()
    
    resize(folder, (16,16), '16', only_pysimplesql_names=True)

# folder = 'images'
# new_dimension = (width, height)
def resize(folder, new_dimension, new_subdir, only_pysimplesql_names=False):
    images_folder = Path(folder)
    for child in images_folder.iterdir():
        if only_pysimplesql_names:
            if child.stem not in map_names:
                continue
        image_path = child.absolute()

        image = Image.open(image_path)
        resized_image = ImageOps.contain(image, new_dimension, method=Image.Resampling.BICUBIC)

        # create if the subdir not exists
        subdir = images_folder.joinpath(new_subdir)
        if not subdir.exists():
            subdir.mkdir(parents=True, exist_ok=True)
        
        to_path = subdir.joinpath(child.name)  # join adds the path-separators
        print("Saving resized to:", to_path)
        resized_image.save(to_path)


if __name__ == '__main__':
    main()