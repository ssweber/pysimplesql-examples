import logging
import sys
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

# Film
# -------------------------
# Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
headings = ss.TableHeadings(sort_enable=True)
headings.add_column("CompanyName", "Company", width=30)
headings.add_column("ContactName", "Contact", width=30)
selector = [
    ss.selector(
        "Customers",
        sg.Table,
        num_rows=20,
        headings=headings,
        auto_size_columns=True,
        alternating_row_color="#f2f2f2",
        row_height=25,
    )
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
# driver = ss.Driver.sqlite("./northwind.db")  # Create a new database connection
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
    else:
        logger.info(f"This event ({event}) is not yet handled.")
