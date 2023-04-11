# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import PySimpleGUI as sg
import os
import base64
import pprint

'''
    Make base64 images from a folder of images
    input:  folder with .png .ico .gif 's
    output: Writes a file "output.py" file with dictionary names equal to filename
    
    Copyright 2020 PySimpleGUI
'''

def main():
    OUTPUT_FILENAME = 'output.py'

    folder = sg.popup_get_folder('Source folder for images\nImages will be encoded and results saved to %s'%OUTPUT_FILENAME, title='Base64 Encoder')

    if not folder:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return
    try:
        namesonly = [f for f in os.listdir(folder) if f.endswith('.png') or f.endswith('.ico') or f.endswith('.gif')]
    except:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return
    
    base64_images = {}
    for i, file in enumerate(namesonly):
        contents = open(os.path.join(folder, file), 'rb').read()
        encoded = base64.b64encode(contents)
        base64_images[f'{file[:file.index(".")]}'] = encoded
        sg.OneLineProgressMeter('Base64 Encoding', i+1, len(namesonly), key='-METER-')
    
    outfile = open(os.path.join(folder, OUTPUT_FILENAME), 'w')
    pp = pprint.PrettyPrinter(indent=4, width=10000, stream=outfile)
    outfile.write('output = ')
    pp.pprint(base64_images)
    outfile.close()
    sg.popup('Completed!', 'Encoded %s files'%(i+1))

if __name__ == '__main__':
    main()