sql = """
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers
(      
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName TEXT,
    ContactName TEXT,
    Address TEXT,
    City TEXT,
    PostalCode TEXT,
    Country TEXT
);

INSERT INTO Customers VALUES(1,'Alfreds Futterkiste','Maria Anders','Obere Str. 57','Berlin','12209','Germany');
INSERT INTO Customers VALUES(2,'Ana Trujillo Emparedados y helados','Ana Trujillo','Avda. de la Constitución 2222','México D.F.','5021','Mexico');
INSERT INTO Customers VALUES(3,'Antonio Moreno Taquería','Antonio Moreno','Mataderos 2312','México D.F.','5023','Mexico');
INSERT INTO Customers VALUES(4,'Around the Horn','Thomas Hardy','120 Hanover Sq.','London','WA1 1DP','UK');
INSERT INTO Customers VALUES(5,'Berglunds snabbköp','Christina Berglund','Berguvsvägen 8','Luleå','S-958 22','Sweden');
INSERT INTO Customers VALUES(6,'Blauer See Delikatessen','Hanna Moos','Forsterstr. 57','Mannheim','68306','Germany');
INSERT INTO Customers VALUES(7,'Blondel père et fils','Frédérique Citeaux','24, place Kléber','Strasbourg','67000','France');
INSERT INTO Customers VALUES(8,'Bólido Comidas preparadas','Martín Sommer','C/ Araquil, 67','Madrid','28023','Spain');
INSERT INTO Customers VALUES(9,'Bon app''''','Laurence Lebihans','12, rue des Bouchers','Marseille','13008','France');
INSERT INTO Customers VALUES(10,'Bottom-Dollar Marketse','Elizabeth Lincoln','23 Tsawassen Blvd.','Tsawassen','T2F 8M4','Canada');
INSERT INTO Customers VALUES(11,'B''''s Beverages','Victoria Ashworth','Fauntleroy Circus','London','EC2 5NT','UK');
INSERT INTO Customers VALUES(12,'Cactus Comidas para llevar','Patricio Simpson','Cerrito 333','Buenos Aires','1010','Argentina');
INSERT INTO Customers VALUES(13,'Centro comercial Moctezuma','Francisco Chang','Sierras de Granada 9993','México D.F.','5022','Mexico');
"""

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

def edit_cell(window, element, key, row, col, justify='left'):
    global textvariable, edit

    def callback(event, row, col, text, key):
        global edit
        widget = event.widget
        if key == 'Return':
            text = widget.get()
            values = list(table.item(row, 'values'))
            values[col] = text
            table.item(row, values=values)
            dataset_row[column_names[col-1]] = text
            frm[data_key].save_record(display_message=False) # threaded info close has error here
        widget.destroy()
        widget.master.destroy()
        edit = False

    if edit or row <= 0:
        return

    edit = True
    column_names = element.metadata["TableHeading"].columns()
    data_key = key
    dataset_row = frm[key].rows[frm[key].current_index]
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
    entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Return':callback(e, r, c, t, k))
    entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='Escape':callback(e, r, c, t, k))

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

driver = ss.Driver.sqlite(":memory:", sql_commands=sql)  # Create a new database connection

# Here is the magic!
frm = ss.Form(
    driver,
    bind_window=window,
)

window.SetAlpha(1)
frm.force_save = True

window["Customers"].bind('<Double-Button-1>' , "+-double click-")

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
    elif event == 'Customers+-double click-':
        row, col = window['Customers'].get_last_clicked_position()
        edit_cell(window, window['Customers'], 'Customers', row+1, col, justify='left')
    else:
        logger.info(f"This event ({event}) is not yet handled.")
