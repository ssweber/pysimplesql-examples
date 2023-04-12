template = # read SVG file into a str, assign it to template
csv_reader = # open CSV file and read it via Python's csv package
sortname, mbid = csvreader.next()
label = template.format(name=sortname, mbid=mbid)
# write label to a file with .svg extension.

inkscape --export-type="png" --export-height=20 --export-area-drawing original.svg

  <text
     style="font-style:normal;font-variant:normal;font-weight:bold;font-size:22px;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';letter-spacing:0px;word-spacing:0px;font-stretch:normal"
     x="110%"
     y="55%"
     dominant-baseline="middle"
     text-anchor="start">Next</text>
    
    
  <text
     style="font-style:normal;font-variant:normal;font-weight:bold;font-size:22px;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';letter-spacing:0px;word-spacing:0px;font-stretch:normal;fill:#eff0f1"
     x="110%"
     y="55%"
     dominant-baseline="middle"
     text-anchor="start"
     id="text6">Next</text>
     
from pathlib2 import Path
path = Path(file_to_search)
text = path.read_text()
text = text.replace(text_to_search, replacement_text)
path.write_text(text)