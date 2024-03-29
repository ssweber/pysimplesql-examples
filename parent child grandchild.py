## NOTES FROM THIS EXAMPLE
## Duplicate from parent, only cascades to child.
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
import pysimplesql as ss
import logging
import time

custom = {
    "ttk_theme": "xpnative",
    "default_label_size": (10, 1),
    "default_element_size": (20, 1),
    "default_mline_size": (30, 7),
}

custom = custom | ss.tp_crystal_remix

ss.languagepack(ss.lp_monty_python)
ss.themepack(custom)

tables = True  # Set this to False to use sg.Combo for selectors.
sz = (900, 300)  # for layouts
grandchild = True  # Set this to False to only be parent/child
quick_editor = True  # quick_editor=quick_editor
enable_id = 1  # to see ID on tables.
_tabs_ = "-TABGROUP-"
foreign_keys = False  # toggle to False to see default behavior

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)  # <=== You can set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

sql_grandchild = """
CREATE TABLE IF NOT EXISTS "bike_repair" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	TEXT NOT NULL DEFAULT 'True',
	"bike_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_id") REFERENCES "bike"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "service" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	TEXT NOT NULL DEFAULT True,
	"bike_repair_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_repair_id") REFERENCES "bike_repair"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""
sql_grandchild_insert = """
INSERT INTO "bike_repair" VALUES (1,'Wheel Repair','True',1);
INSERT INTO "bike_repair" VALUES (2,'Seat Repair','TRUE',1);
INSERT INTO "bike_repair" VALUES (3,'Seat Repair','true',2);
INSERT INTO "service" VALUES (1,'Basic',True,1);
INSERT INTO "service" VALUES (2,'Premium',TRUE,1);
INSERT INTO "service" VALUES (3,'Gold',true,2);
"""

if not grandchild:
    sql_grandchild = ""
    sql_grandchild_insert = ""

sql = f"""
CREATE TABLE IF NOT EXISTS "person" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Person Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "car" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Car Placeholder',
	"example"	TEXT NOT NULL DEFAULT 'False',
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "bike" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Placeholder',
	"example"	BOOLEAN NOT NULL DEFAULT False,
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "building" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Building Placeholder',
	"person_id"	INTEGER,
	"example"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON DELETE SET NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
{sql_grandchild}
INSERT INTO "person" VALUES (1,'Bill',0);
INSERT INTO "person" VALUES (2,'Jessica',0);
INSERT INTO "person" VALUES (3,'Drake',0);
INSERT INTO "car" VALUES (1,'Landrover','False',1);
INSERT INTO "car" VALUES (2,'Jeep','FALSE',2);
INSERT INTO "car" VALUES (3,'GTO','false',3);
INSERT INTO "bike" VALUES (1,'Unicycle',False,1);
INSERT INTO "bike" VALUES (2,'Street Bike',false,2);
INSERT INTO "bike" VALUES (3,'Moped',FALSE,3);
INSERT INTO "building" VALUES (1,'Tower',1,1);
INSERT INTO "building" VALUES (2,'Mall',1,1);
INSERT INTO "building" VALUES (3,'Cabin',1,1);
{sql_grandchild_insert}
"""

# INSERT INTO person (name, example) 
# SELECT 'Person Placeholder', 0 
# FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) a,
#      (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) b,
#      (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) c,
#      (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) d,
#      (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) e,
#      (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5);

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

# Building
# -------------------------

# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("person_id", "Owner", width=20)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "building",
            sg.Table,
            num_rows=4,
            headings=headings,
            auto_size_columns=True,
            alternating_row_color="#f2f2f2",
            row_height=25,
        )
    ]
else:
    selector = [ss.selector("building", sg.Combo)]

building_layout = [
    [sg.Text("Buildings - Childless Parent, default int 1")],
    selector,
    [
        ss.actions(
            "building",
            default=True,
        )
    ],
    [sg.HorizontalSeparator()],
]

# Person
# -------------------------
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "person", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("person", sg.Combo)]
# Define the columns for the table selector
person_layout = [
    [sg.Text("Person - Parent w/ cascade, default int 0")],
    selector,
    [ss.field("person.name"), ss.field("person.example", sg.Checkbox, default=True)],
    [ss.actions("person", default=True)],
    [sg.HorizontalSeparator()],
]


# car
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    #    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "car", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("car", sg.Combo)]
car_layout = [
    [sg.Text("Car - Child of Person/ Sibling of Bike, default str False")],
    selector,
    [ss.field("car.name"), ss.field("car.example", sg.Checkbox)],
    [
        ss.field("car.person_id", sg.Combo),
    ],
    [ss.actions("car", default=True)],
]

# bike
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "bike", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("bike", sg.Combo)]
bike_layout = [
    [sg.Text("Bike - Child of Person/ Sibling of Car, default bool False")],
    selector,
    [ss.field("bike.name"), ss.field("bike.example", sg.Checkbox)],
    [ss.field("bike.person_id", sg.Combo)],
    [ss.actions("bike", default=True)],
]

# bike_repair
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "bike_repair",
            sg.Table,
            num_rows=4,
            headings=headings,
            auto_size_columns=True,
        )
    ]
else:
    selector = [ss.selector("bike_repair", sg.Combo)]
bike_repair_layout = [
    [sg.HorizontalSeparator()],
    [sg.Text("Bike Repair - Bike child, Person Grandchild, default str True")],
    selector,
    [ss.field("bike_repair.name"), ss.field("bike_repair.example", sg.Checkbox)],
    [ss.field("bike_repair.bike_id", sg.Combo)],
    [ss.actions("bike_repair", default=True)],
]

# service
# -------------------------
# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True, edit_enable=True)
    headings.add_column("id", "id", width=10)
    headings.add_column("name", "Name", width=10)
    headings.add_column("example", "Example", width=20)
    selector = [
        ss.selector(
            "service", sg.Table, num_rows=4, headings=headings, auto_size_columns=True
        )
    ]
else:
    selector = [ss.selector("service", sg.Combo)]
service_layout = [
    [sg.HorizontalSeparator()],
    [
        sg.Text(
            "Repair service - Child of BikeRepair / Grandgrandchild of Person, default bool True"
        )
    ],
    selector,
    [ss.field("service.name"), ss.field("service.example", sg.Checkbox)],
    [ss.field("service.bike_repair_id", sg.Combo)],
    [ss.actions("service", default=True)],
]

# -------------------------
# Main Layout
# -------------------------
print(ss.themepack.ttk_theme)
layout = [
    [sg.Button("Form Prompt_Save", key="save", use_ttk_buttons=True)],
    [sg.Button("50 selector switch test", key="-timeit-", use_ttk_buttons=True)],
    [sg.Button("Display all", key="-display-", use_ttk_buttons=True)],
]
layout.append([sg.Col(person_layout, size=sz), sg.Col(building_layout, size=sz)])
layout.append([sg.Col(bike_layout, size=sz), sg.Col(car_layout, size=sz)])
if grandchild:
    layout.append(
        [sg.Col(bike_repair_layout, size=sz), sg.Col(service_layout, size=sz)]
    )

layout.append([sg.StatusBar(" " * 100, key="status_bar")])

window = sg.Window(
    "People and Vehicles",
    layout,
    finalize=True,
    #     grab_anywhere=True,
    alpha_channel=0,
    ttk_theme=ss.themepack.ttk_theme,
)

driver = ss.Sqlite(":memory:", sql_commands=sql)  # Create a new database connection
frm = ss.Form(
    driver,
    bind_window=window,
    live_update = True
#     prompt_save=ss.AUTOSAVE_MODE,  # save_quiet=True
)  # <=== Here is the magic!
if foreign_keys:
    driver.con.execute("PRAGMA foreign_keys = ON")

# frm.set_prompt_save(ss.AUTOSAVE_MODE)
# frm.set_fk_column_cascade("bike_repair", "bike_id", update_cascade=False)
window.SetAlpha(1)

# frm.force_save = True


def test_set_by_pk(number):
    for i in range(number):
        frm["person"].set_by_pk(2)
        frm["person"].set_by_pk(1)


# variables for updating our sg.StatusBar
seconds_to_display = 3
last_val = ""
new_val = ""
counter = 1

print(frm["bike"]["person_id"])
print(window["bike.person_id"].get())
# ---------
# MAIN LOOP
# ---------

while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, "Exit", "-ESCAPE-"):
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        window.close()
        break
    elif ss.process_events(
        event, values
    ):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f"PySimpleDB event handler handled the event {event}!")
        # handle button clicks
    elif event == "__TIMEOUT__":
        # --------------------------------------------------
        # Status bar updating
        # --------------------------------------------------
        # Using the same timeout, we can update our sg.StatusBar with save messages
        counter += 1
        new_val = frm.popup.last_info_msg
        # If there is a new info popup msg, reset our counter and update the sg.StatusBar
        if new_val != last_val:
            counter = 0
            window["status_bar"].update(value=new_val)
            last_val = new_val
        # After counter reaches seconds limit, clear sg.StatusBar and frm.popup.last_info_msg
        if counter > seconds_to_display * 10:
            counter = 0
            frm.popup.last_info_msg = ""
            window["status_bar"].update(value="")
    elif event == "save":
        frm.prompt_save()  # Prompt save when tabs change
    elif event == "-timeit-":
        st = time.time()
        test_set_by_pk(50)
        et = time.time()
        elapsed_time = et - st
        print(elapsed_time)
    elif event == "-display-":
        frm["bike"].requery(filtered=False)
        frm["bike_repair"].requery(filtered=False)
        frm.update_elements()
    else:
        logger.info(f"This event ({event}) is not yet handled.")
