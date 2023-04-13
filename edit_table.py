import logging
import sys
import locale
from pathlib import Path 
    
import PySimpleGUI as sg  ## pysimplegui 4.60.4
sg.set_options(dpi_awareness=True)
sg.change_look_and_feel("SystemDefaultForReal")
sg.set_options(font=("Arial", 11))  # Set the font and font size for the table

p = Path.cwd().parent
sys.path.append(f"{str(p)}/pysimplesql/")
import pysimplesql as ss

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG
)  # <=== You can set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

def edit_cell(window, key, row, col, justify='left'):

    global textvariable, edit

    def callback(event, row, col, text, key, dataset):
        global edit
        widget = event.widget
        if key == 'Return':
            text = widget.get()
        widget.destroy()
        widget.master.destroy()
        values = list(table.item(row, 'values'))
        values[col] = text
        table.item(row, values=values)
        print(frm[dataset].get_current_row().copy())
        edit = False

    if edit or row <= 0:
        return

    edit = True
    table = window[key].Widget
    root = table.master

    text = table.item(row, "values")[col]
    x, y, width, height = table.bbox(row, col)

    frame = sg.tk.Frame(root)
    frame.place(x=x, y=y, anchor="nw", width=width, height=height)
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    entry.pack(expand=True, fill="both")
    entry.select_range(0, sg.tk.END)
    entry.icursor(sg.tk.END)
    entry.focus_force()
    entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Return', dataset=key:callback(e, r, c, t, k, dataset))
    entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='Escape', dataset=key:callback(e, r, c, t, k, dataset))

custom = {
    "ttk_theme": "xpnative",
    "default_label_size": (10, 1),
    "default_element_size": (20, 1),
    "default_mline_size": (30, 7),
    "search": "  Search  ",
}
ss.themepack(custom)

_tabs_ = "-TABGROUP-"

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

edit = False

# Film
# -------------------------
# Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
headings = ss.TableHeadings(sort_enable=True)
headings.add_column("CustomerName", "Company", width=30)
headings.add_column("ContactName", "Contact", width=30)
headings.add_column("Country", "Country", width=30)
selector = [
    ss.selector(
        "Customers",
        sg.Table,
        key = 'Customers',
        num_rows=20,
        headings=headings,
        auto_size_columns=True,
        alternating_row_color="#f2f2f2",
        row_height=25,
        enable_click_events=True,
    ),
]

# Define the columns for the table selector
layout = [selector,]

# --------------------------------------------------------------------------------------
# Main Layout
# --------------------------------------------------------------------------------------
window = sg.Window(
    "Northwind Example",
    layout,
    finalize=True,
    grab_anywhere=True,
    alpha_channel=0,
    ttk_theme=ss.themepack.ttk_theme,
    icon=ss.themepack.icon
)

driver = ss.Driver.sqlite(":memory:", sql_script='northwind.sql')  # Create a new database connection

# Here is the magic!
frm = ss.Form(
    driver,
    bind_window=window,
)

window.SetAlpha(1)
frm.update_elements()

# --------------------------------------------------------------------------------------
# MAIN LOOP
# --------------------------------------------------------------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit", "-ESCAPE-"):
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        window.close()
        break
    elif ss.process_events(
        event, values
    ):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f"PySimpleDB event handler handled the event {event}!")
    if isinstance(event, tuple):
        cell = row, col = event[2]
        edit_cell(window, event[0], row+1, col, justify='left')
    else:
        logger.info(f"This event ({event}) is not yet handled.")
