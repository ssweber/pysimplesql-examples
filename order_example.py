sql = f"""
CREATE TABLE IF NOT EXISTS Customers (
    "CustomerID" INTEGER NOT NULL,
    "Name" TEXT NOT NULL,
    "Email" TEXT,
    PRIMARY KEY("CustomerID" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS Orders (
    "OrderID" INTEGER NOT NULL,
    "CustomerID" INTEGER NOT NULL,
    "OrderDate" DATE NOT NULL DEFAULT (date('now')),
    "Total" REAL,
    "Completed" BOOLEAN NOT NULL,
    FOREIGN KEY ("CustomerID") REFERENCES Customers(CustomerID),
	PRIMARY KEY("OrderID" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS Products (
    "ProductID" INTEGER NOT NULL,
    "Name" TEXT NOT NULL DEFAULT "New Product",
    "Price" REAL NOT NULL,
    "Inventory" INTEGER DEFAULT 0,
    PRIMARY KEY("ProductID" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS OrderDetails (
    "OrderDetailID" INTEGER NOT NULL,
    "OrderID" INTEGER,
    "ProductID" INTEGER NOT NULL,
    "Quantity" INTEGER,
    "Price" REAL,
    "SubTotal" REAL GENERATED ALWAYS AS ("Price" * "Quantity") STORED,
    FOREIGN KEY ("OrderID") REFERENCES "Orders"("OrderID") ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY ("ProductID") REFERENCES "Products"("ProductID"),
	PRIMARY KEY("OrderDetailID" AUTOINCREMENT)
);

-- Create a compound index on OrderID and ProductID columns in OrderDetails table
CREATE INDEX idx_orderdetails_orderid_productid ON OrderDetails (OrderID, ProductID);

-- Trigger to set the price value for a new OrderDetail
CREATE TRIGGER IF NOT EXISTS set_price
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE OrderDetails
    SET Price = Products.Price
    FROM Products
    WHERE Products.ProductID = NEW.ProductID
    AND OrderDetails.OrderDetailID = NEW.OrderDetailID;
END;

-- Trigger to update the price value for an existing OrderDetail
CREATE TRIGGER IF NOT EXISTS set_price_update
AFTER UPDATE ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE OrderDetails
    SET Price = Products.Price
    FROM Products
    WHERE Products.ProductID = NEW.ProductID
    AND OrderDetails.OrderDetailID = NEW.OrderDetailID;
END;

-- Trigger to set the total value for a new OrderDetail
CREATE TRIGGER IF NOT EXISTS set_total
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET Total = (
        SELECT SUM(SubTotal) FROM OrderDetails WHERE OrderID = NEW.OrderID
    )
    WHERE OrderID = NEW.OrderID;
END;

-- Trigger to update the total value for an existing OrderDetail
CREATE TRIGGER IF NOT EXISTS update_total
AFTER UPDATE ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET Total = (
        SELECT SUM(SubTotal) FROM OrderDetails WHERE OrderID = NEW.OrderID
    )
    WHERE OrderID = NEW.OrderID;
END;

-- Trigger to update the total value for an existing OrderDetail
CREATE TRIGGER IF NOT EXISTS delete_order_detail
AFTER DELETE ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET Total = (
        SELECT SUM(SubTotal) FROM OrderDetails WHERE OrderID = OLD.OrderID
    )
    WHERE OrderID = OLD.OrderID;
END;

CREATE TRIGGER IF NOT EXISTS update_product_price
AFTER UPDATE ON Products
FOR EACH ROW
BEGIN
    UPDATE OrderDetails
    SET Price = NEW.Price
    WHERE ProductID = NEW.ProductID;
END;

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

INSERT INTO Products (Name, Price, Inventory) VALUES
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

INSERT INTO OrderDetails (OrderID, ProductID, Quantity) 
SELECT O.OrderID, P.ProductID, (ABS(RANDOM()) % 10) + 1
FROM Orders O
JOIN (SELECT ProductID FROM Products ORDER BY RANDOM() LIMIT 25) P 
ON 1=1 
ORDER BY 1;
"""
from pathlib import Path

p = Path.cwd().parent
import sys

sys.path.append(f"{str(p)}/pysimplesql/")
import PySimpleGUI as sg  ## pysimplegui 4.60.4

sg.change_look_and_feel("SystemDefaultForReal")
sg.set_options(font=("Roboto", 11))  # Set the font and font size for the table

import pysimplesql as ss  # <=== PySimpleSQL lines will be marked like this.  There's only a few!


custom = {
    "ttk_theme": "xpnative",
    "default_label_size": (15, 1),
    "default_element_size": (20, 1),
    "default_mline_size": (30, 7),
    "marker_unsaved": "💾",
}

custom = custom | ss.tp_crystal_remix
ss.themepack(custom)

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG
)  # <=== Set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------
# Define the columns for the table selector using the TableHeading convenience class.
order_heading = ss.TableHeadings(
    sort_enable=True,  # Click a header to sort
    edit_enable=True,  # Double-click a cell to make edits
    save_enable=True,
)
order_heading.add_column("OrderID", "ID", width=5)
order_heading.add_column(
    column="CustomerID",
    heading_column="Customer",
    width=30,
    readonly=False,  # set to True to disable editing for individual columns!
)
order_heading.add_column("OrderDate", "Date", width=20)
order_heading.add_column("Total", "Total", width=10, readonly=True)
order_heading.add_column("Completed", "✔", width=8)
font = ("Roboto", 16)
orders_layout = [
    [sg.Text("Orders", font=font)],
    [ss.actions("Orders")],
    [
        ss.selector(
            "Orders", sg.Table, num_rows=5, headings=order_heading, row_height=25
        )
    ],
    [sg.HorizontalSeparator()]
]

details_heading = ss.TableHeadings(
    sort_enable=True,  # Click a header to sort
    edit_enable=True,  # Double-click a cell to make edits
)
details_heading.add_column("ProductID", "Product", width=25)
details_heading.add_column("Quantity", "Quantity", width=10)
details_heading.add_column("Price", "Price/Ea", width=10)
details_heading.add_column("SubTotal", "SubTotal", width=10)

details_layout = [
    [sg.Text("Order Details", font=font)],
    [ss.field("Orders.CustomerID", sg.Combo, label="Customer")],
    [
        ss.field("Orders.OrderDate", sg.Text, label="Date"),
    ],
    [ss.field("Orders.Completed", sg.Checkbox, default=False)],
    [
        ss.selector(
            "OrderDetails",
            sg.Table,
            num_rows=10,
            headings=details_heading,
            row_height=25,
        )
    ],
    [ss.actions("OrderDetails", default=False, save=True, insert=True, delete=True)],
    [ss.field("OrderDetails.ProductID", sg.Combo)],
    [ss.field("OrderDetails.Quantity")],
]

menu_def = [["&File", ["&Save"]], ["&Edit", ["&Edit Products", "&Edit Customers"]]]

orders_layout.append(details_layout)

layout = [
    [
        sg.Menu(
            menu_def,
            key="-MENUBAR-",
            font="_ 12",
        )
    ],
    [orders_layout],
]

win = sg.Window(
    "Order Example",
    layout,
    finalize=True,
    ttk_theme="xpnative",
    icon=ss.themepack.icon,
)
win["Orders:selector"].expand(True, True)
win["Orders:selector"].table_frame.pack(expand=True, fill="both")
win["OrderDetails:selector"].expand(True, True)
win["OrderDetails:selector"].table_frame.pack(expand=True, fill="both")

driver = ss.Driver.sqlite(":memory:", sql_commands=sql)
# Here is the magic!
frm = ss.Form(
    driver,
    bind_window=win,
    live_update=True,  # this updates the `Selector`, sg.Table as we type in fields!
)
# Note:  sql_commands in only run if Journal.db does not exist!  This has the effect of creating a new blank
# database as defined by the sql_commands if the database does not yet exist, otherwise it will use the database!

frm.edit_protect()  # Comment this out to edit protect elements when the window is created.
# Reverse the default sort order so new journal entries appear at the top
frm["Orders"].set_order_clause("ORDER BY OrderDate ASC")
# Set the column order for search operations.  By default, only the designated description column is searched
frm["Orders"].set_search_order(["CustomerID"])
# Requery the data since we made changes to the sort order
frm["Orders"].requery()

ss.add_placeholder_to(win["Orders:search_input"],"🔍 Search...",)

# ---------
# MAIN LOOP
# ---------
while True:
    event, values = win.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        win.close()
        break
    # <=== let PySimpleSQL process its own events! Simple!
    elif ss.process_events(event, values):  
        logger.info(f"PySimpleDB event handler handled the event {event}!")
    if "set_current" in event and values["set_current"]["data_key"] == "OrderDetails":
        dataset = frm["OrderDetails"]
        current_row = dataset.get_current_row()
        if dataset.row_count and dataset.get_current_row()["Quantity"]:
            row_is_virtual = dataset.row_is_virtual()
            dataset.save_record(display_message=False)
            frm["Orders"].requery(select_first=False)
            frm.update_selectors("Orders")
            if not row_is_virtual:
                dataset.requery(select_first=False)
                frm.update_elements("OrderDetails")
    elif "Edit Products" in event:
        frm["Products"].quick_editor()
    elif "Edit Customers" in event:
        frm["Customers"].quick_editor()
    elif "Save" in event:
        frm.save_records()
