import json
import pprint
import importlib.util
import sys

import PySimpleGUI as sg

def main():
    OUTPUT_FILENAME = 'mapped.py'

    file = sg.popup_get_file('Select File that has freedesktop icons saved as base64 values in a dictionary output images. Results saved to %s'%OUTPUT_FILENAME, title='Resize and Map Icons')

    if not file:
        sg.popup_cancel('Cancelled - No valid file entered')
        return
    
    spec = importlib.util.spec_from_file_location("output", file)
    output = importlib.util.module_from_spec(spec)
    sys.modules["output"] = output
    spec.loader.exec_module(output)
   
    mapped_theme = map_freedesktop_icons(output.output)

    with open('mapped.py', 'w') as file:
        pp = pprint.PrettyPrinter(indent=4, width=10000, stream=file)
        pp.pprint(mapped_theme)

def map_freedesktop_icons(theme):
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
    mapped_theme = {}
    for ss_name, mapped_name in mapping.items():
        mapped_theme[ss_name] = theme[mapped_name]
    return mapped_theme
    
if __name__ == '__main__':
    main()
