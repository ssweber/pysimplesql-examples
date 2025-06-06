import logging

import pathlib
import sys

p = pathlib.Path.cwd().parent
sys.path.append(f"{str(p)}/pysimplesql/")

import PySimpleGUI as sg
import pysimplesql as ss

# PySimpleGUI options
# -----------------------------
sg.change_look_and_feel("SystemDefaultForReal")
sg.set_options(font=("Arial", 11), dpi_awareness=True)

# Setup Logger
# -----------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Use the `xpnative` ttk_theme, and the `crystal_remix` iconset
# -----------------------------
custom = {
    "ttk_theme": "xpnative",
    "marker_sort_asc": " ⬇",
    "marker_sort_desc": " ⬆",
}
custom = custom | ss.tp_crystal_remix
ss.themepack(custom)

# SQL Statement
# ======================================================================================
# While this example uses triggers to calculate prices and sub/totals, they are not
# required for pysimplesql to operate. See simpler examples, like journal.

sql = """
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
    "Quantity" INTEGER NOT NULL,
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
    ('Alice Rodriguez', 'rodriguez.alice@example.com'),
    ('Bryan Patel', 'patel.bryan@example.com'),
    ('Cassandra Kim', 'kim.cassandra@example.com'),
    ('David Nguyen', 'nguyen.david@example.com'),
    ('Ella Singh', 'singh.ella@example.com'),
    ('Franklin Gomez', 'gomez.franklin@example.com'),
    ('Gabriela Ortiz', 'ortiz.gabriela@example.com'),
    ('Henry Chen', 'chen.henry@example.com'),
    ('Isabella Kumar', 'kumar.isabella@example.com'),
    ('Jonathan Lee', 'lee.jonathan@example.com'),
    ('Katherine Wright', 'wright.katherine@example.com'),
    ('Liam Davis', 'davis.liam@example.com'),
    ('Mia Ali', 'ali.mia@example.com'),
    ('Nathan Kim', 'kim.nathan@example.com'),
    ('Oliver Brown', 'brown.oliver@example.com'),
    ('Penelope Martinez', 'martinez.penelope@example.com'),
    ('Quentin Carter', 'carter.quentin@example.com'),
    ('Rosa Hernandez', 'hernandez.rosa@example.com'),
    ('Samantha Jones', 'jones.samantha@example.com'),
    ('Thomas Smith', 'smith.thomas@example.com'),
    ('Uma Garcia', 'garcia.uma@example.com'),
    ('Valentina Lopez', 'lopez.valentina@example.com'),
    ('William Park', 'park.william@example.com'),
    ('Xander Williams', 'williams.xander@example.com'),
    ('Yara Hassan', 'hassan.yara@example.com'),
    ('Zoe Perez', 'perez.zoe@example.com');

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

-- INSERT INTO Orders (CustomerID, OrderDate, Completed)
-- SELECT CustomerID, DATE('now', '-' || (ABS(RANDOM()) % 90) || ' days'), False
-- FROM Customers
-- ORDER BY RANDOM() LIMIT 100;

-- Create a temporary table with a single column
CREATE TEMPORARY TABLE temp(CustomerID INTEGER);

-- Insert 100 random CustomerIDs into the temporary table
INSERT INTO temp(CustomerID)
SELECT CustomerID
FROM Customers
ORDER BY RANDOM()
LIMIT 100;

-- Insert 10,000 records into the Orders table using the temporary table and recursive CTE
WITH RECURSIVE cte AS (
  SELECT 1 AS counter
  UNION ALL
  SELECT counter + 1
  FROM cte
  WHERE counter < 5
)
INSERT INTO Orders (CustomerID, OrderDate, Completed)
SELECT temp.CustomerID, DATE('now', '-' || (ABS(RANDOM()) % 30) || ' days'), 0
FROM temp, cte
ORDER BY RANDOM()
LIMIT 20000;

-- Drop the temporary table
DROP TABLE temp;

INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
SELECT O.OrderID, P.ProductID, (ABS(RANDOM()) % 10) + 1
FROM Orders O
JOIN (SELECT ProductID FROM Products ORDER BY RANDOM() LIMIT 25) P
ON 1=1
ORDER BY 1;
"""


# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

# fmt: off
# Create a basic menu
menu_def = [
    ["&File",["&Save","&Requery All",],],
    ["&Edit", ["&Edit Products", "&Edit Customers"]],
]
# fmt: on
layout = [[sg.Menu(menu_def, key="-MENUBAR-", font="_ 12")]]

# Define the columns for the table selector using the TableHeading class.
order_heading = ss.TableHeadings(
    # Click a heading to sort
    sort_enable=True,
    # Double-click a cell to make edits.
    # Exempted: Primary Key columns, Generated columns, and columns set as readonly
    edit_enable=True,
    # Click 💾 in sg.Table Heading to trigger DataSet.save_record()
    save_enable=True,
    # Filter rows as you type in the search input
    apply_search_filter=True,
)

# Add columns
order_heading.add_column(column="OrderID", heading_column="ID", width=5)
order_heading.add_column("CustomerID", "Customer", 30)
order_heading.add_column("OrderDate", "Date", 20)
order_heading.add_column(
    "Total", "Total", width=10, readonly=True
)  # set to True to disable editing for individual columns!)
order_heading.add_column("Completed", "✔", 8)

# Layout
layout.append(
    [
        [sg.Text("Orders", font="_16")],
        [
            ss.selector(
                "Orders",
                ss.LazyTable,
                num_rows=5,
                headings=order_heading,
                row_height=25,
            )
        ],
        [ss.actions("Orders")],
        [sg.Sizer(h_pixels=0, v_pixels=20)],
    ]
)

# OrderDetails TableHeadings:
details_heading = ss.TableHeadings(sort_enable=True, edit_enable=True, save_enable=True)
details_heading.add_column("ProductID", "Product", 30)
details_heading.add_column("Quantity", "Quantity", 10)
details_heading.add_column("Price", "Price/Ea", 10, readonly=True)
details_heading.add_column("SubTotal", "SubTotal", 10)

orderdetails_layout = [
    [sg.Sizer(h_pixels=0, v_pixels=10)],
    [ss.field("Orders.CustomerID", sg.Combo, label="Customer")],
    [
        ss.field("Orders.OrderDate", label="Date"),
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
    [ss.field("OrderDetails.Price", sg.Text)],
    [ss.field("OrderDetails.SubTotal", sg.Text)],
    [sg.Sizer(h_pixels=0, v_pixels=10)],
]

layout.append([sg.Frame("Order Details", orderdetails_layout, expand_x=True)])

win = sg.Window(
    "Order Example",
    layout,
    finalize=True,
    # Below is Important! pysimplesql progressbars/popups/quick_editors use
    # ttk_theme and icon as defined in themepack.
    ttk_theme="xpnative",
    icon=ss.themepack.icon,
)

# Expand our sg.Tables so they fill the screen
win["Orders:selector"].expand(True, True)
win["Orders:selector"].table_frame.pack(expand=True, fill="both")
win["OrderDetails:selector"].expand(True, True)
win["OrderDetails:selector"].table_frame.pack(expand=True, fill="both")

# Init pysimplesql Driver and Form
# --------------------------------

# Create sqlite driver, keeping the database in memory
driver = ss.Driver.sqlite(":memory:", sql_commands=sql)
frm = ss.Form(
    driver,
    bind_window=win,
    live_update=True,  # this updates the `Selector`, sg.Table as we type in fields.
)

# Few more settings
# -----------------

frm.edit_protect()  # Comment this out to edit protect when the window is created.
# Reverse the default sort order so Orders are sorted by date
frm["Orders"].set_order_clause("ORDER BY OrderDate ASC")
# Requery the data since we made changes to the sort order
frm["Orders"].requery()
# Set the column order for search operations.
frm["Orders"].set_search_order(["CustomerID", "OrderID"])

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

    # Code to automatically save and refresh OrderDetails:
    # ----------------------------------------------------
    elif (
        "current_row_updated" in event
        and values["current_row_updated"]["data_key"] == "OrderDetails"
    ):
        dataset = frm["OrderDetails"]
        current_row = dataset.get_current_row()
        # after a product and quantity is entered, save and requery
        print(current_row["ProductID"])
        if (
            dataset.row_count
            and current_row["ProductID"] not in [None, ss.PK_PLACEHOLDER]
            and current_row["Quantity"]
        ):
            pk_is_virtual = dataset.pk_is_virtual()
            dataset.save_record(display_message=False)
            frm["Orders"].requery(select_first=False)
            frm.update_selectors("Orders")
            # will need to requery if updating, rather than inserting a new record
            if not pk_is_virtual:
                pk = current_row[dataset.pk_column]
                dataset.requery(select_first=False)
                dataset.set_by_pk(pk, skip_prompt_save=True)
    # ----------------------------------------------------

    # Display the quick_editor for products and customers
    elif "Edit Products" in event:
        frm["Products"].quick_editor()
    elif "Edit Customers" in event:
        frm["Customers"].quick_editor()
    # call a Form-level save
    elif "Save" in event:
        frm.save_records()
    # call a Form-level requery
    elif "Requery All" in event:
        #         frm.requery_all()
        print(win["OrderDetails.Quantity"].get())
    else:
        logger.info(f"This event ({event}) is not yet handled.")
