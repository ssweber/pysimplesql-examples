sql = f"""
CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT
);

CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    OrderDate INTEGER NOT NULL DEFAULT (date('now')),
    TotalPrice REAL,
    Completed BOOLEAN,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderDetails (
    OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    Price REAL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL DEFAULT "New Product",
    Price REAL NOT NULL,
    Quantity INTEGER DEFAULT 0
);

INSERT INTO Customers (Name, Email) VALUES
    ('Alice Johnson', 'alice.johnson@example.com'),
    ('Bob Williams', 'bob.williams@example.com'),
    ('Charlie Brown', 'charlie.brown@example.com'),
    ('David Lee', 'david.lee@example.com'),
    ('Emily Davis', 'emily.davis@example.com'),
    ('Frank Smith', 'frank.smith@example.com'),
    ('Gina Rodriguez', 'gina.rodriguez@example.com'),
    ('Henry Lee', 'henry.lee@example.com'),
    ('Isabella Martinez', 'isabella.martinez@example.com'),
    ('Jacob Green', 'jacob.green@example.com'),
    ('Karen Wilson', 'karen.wilson@example.com'),
    ('Larry White', 'larry.white@example.com'),
    ('Maria Perez', 'maria.perez@example.com'),
    ('Nancy Thompson', 'nancy.thompson@example.com'),
    ('Oliver Davis', 'oliver.davis@example.com'),
    ('Paul Kim', 'paul.kim@example.com'),
    ('Rachel Lee', 'rachel.lee@example.com'),
    ('Sarah Jones', 'sarah.jones@example.com'),
    ('Thomas Brown', 'thomas.brown@example.com'),
    ('Ursula Rodriguez', 'ursula.rodriguez@example.com'),
    ('Victor Garcia', 'victor.garcia@example.com'),
    ('William Johnson', 'william.johnson@example.com'),
    ('Xavier Hernandez', 'xavier.hernandez@example.com'),
    ('Yvonne Lee', 'yvonne.lee@example.com'),
    ('Zachary Perez', 'zachary.perez@example.com');

INSERT INTO Products (Name, Price, Quantity) VALUES
    ('Thingamabob', 5.00, 200),
    ('Doohickey', 15.00, 75),
    ('Whatchamacallit', 25.00, 50),
    ('Gizmo', 10.00, 100),
    ('Widget', 20.00, 60),
    ('Doodad', 30.00, 40),
    ('Sprocket', 7.50, 150),
    ('Flibbertigibbet', 12.50, 90),
    ('Thingamajig', 22.50, 30),
    ('Dooberry', 17.50, 50),
    ('Whirligig', 27.50, 25),
    ('Gadget', 8.00, 120),
    ('Contraption', 18.00, 65),
    ('Thingummy', 28.00, 35),
    ('Dinglehopper', 9.50, 100),
    ('Doodlywhatsit', 19.50, 55),
    ('Whatnot', 29.50, 20),
    ('Squiggly', 6.50, 175),
    ('Fluffernutter', 11.50, 80),
    ('Goober', 21.50, 40),
    ('Doozie', 16.50, 60),
    ('Whammy', 26.50, 30),
    ('Thingy', 7.00, 130),
    ('Doodadery', 17.00, 70);
    
INSERT INTO Orders (CustomerID, OrderDate, Completed) 
SELECT CustomerID, DATE('now', '-' || (ABS(RANDOM()) % 30) || ' days'), False
FROM Customers 
ORDER BY RANDOM() LIMIT 100;

INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Price) 
SELECT O.OrderID, P.ProductID, (ABS(RANDOM()) % 10) + 1, P.Price 
FROM Orders O 
JOIN (SELECT ProductID, Price FROM Products ORDER BY RANDOM() LIMIT 25) P 
ON 1=1 
ORDER BY RANDOM() LIMIT 1000;
"""

# To keep examples concise, avoid Black formatting. Remove # fmt: off to use Black formatting.
# fmt: off

## NOTES FROM THIS EXAMPLE
import platform
import ctypes

# Fix Bug on Windows when using multiple screens with different scaling
if platform.system() == "Windows":
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

from pathlib import Path

p = Path.cwd().parent
import sys

sys.path.append(f"{str(p)}/pysimplesql/")
import PySimpleGUI as sg  ## pysimplegui 4.60.4

sg.change_look_and_feel("SystemDefaultForReal")
# sg.change_look_and_feel("SystemDefault1")
# sg.set_options(font=('Helvetica', 12))  # Set the font and font size for the table
sg.set_options(font=("Roboto", 11))  # Set the font and font size for the table

import pysimplesql as ss  # <=== PySimpleSQL lines will be marked like this.  There's only a few!


custom = {
    "ttk_theme": "xpnative",
    "default_label_size": (10, 1),
    "default_element_size": (20, 1),
    "default_mline_size": (30, 7),
}

custom = custom | ss.tp_crystal_remix
ss.themepack(custom)

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # <=== Set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------
# Define the columns for the table selector using the TableHeading convenience class.
headings = ss.TableHeadings(
    sort_enable=True, # Click a header to sort
    edit_enable=True # Double-click a cell to make edits
    )
headings.add_column('OrderID', 'ID', width=5)
headings.add_column('OrderDate', 'Date', width=25)
headings.add_column('CustomerID', 'Customer', width=30)
headings.add_column('Completed', 'Completed?', width=10)

layout = [
    [ss.selector('Orders', sg.Table, num_rows=10, headings=headings, row_height=25)],
    [ss.actions('Orders')],
    [ss.field('Orders.CustomerID', sg.Combo, size=(30, 10), label='Customer')],
    [ss.field('Orders.OrderDate'),
        sg.CalendarButton(
            "Select Date", close_when_date_chosen=True, target="Orders.OrderDate",  # <- target matches field() name
            format="%Y-%m-%d", size=(10, 1), key='datepicker'
        )
    ],
    [ss.field("Orders.Completed", sg.Checkbox, default=False)],
]

win = sg.Window('Order Exapmle', layout, finalize=True)
driver = ss.Driver.sqlite(":memory:", sql_commands=sql)
# Here is the magic!
frm = ss.Form(
    driver,
    bind_window=win,
    live_update=True # this updates the `Selector`, sg.Table as we type in fields!
    )
# Note:  sql_commands in only run if Journal.db does not exist!  This has the effect of creating a new blank
# database as defined by the sql_commands if the database does not yet exist, otherwise it will use the database!

# ------------------------------------------
# How to Edit Protect your sg.CalendarButton
# ------------------------------------------
# By default, action() includes an edit_protect() call, that disables edits in the window.
# You can toggle it off with:
frm.edit_protect()  # Comment this out to edit protect elements when the window is created.
# Set initial CalendarButton state to the same as pysimplesql elements
win['datepicker'].update(disabled=frm.get_edit_protect())
# Then watch for the 'edit_protect' event in your Main Loop

# ---------
# MAIN LOOP
# ---------
while True:
    event, values = win.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        win.close()
        break
    elif ss.process_events(event, values):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f'PySimpleDB event handler handled the event {event}!')
        if "edit_protect" in event:
            win['datepicker'].update(disabled=frm.get_edit_protect())
    else:
        logger.info(f'This event ({event}) is not yet handled.')