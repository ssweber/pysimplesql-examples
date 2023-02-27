## NOTES FROM THIS EXAMPLE

## Delete from parent, only cascades to child. Grandchildren are not deleted
## Duplicate from parent, only cascades to child. Grandchildren are not duplicated
import PySimpleGUI as sg  ## pysimplegui 4.60.4
import pysimplesql as ss
import logging
import time

tables = True # Set this to False to use sg.Combo for selectors.
sz = (600, 250) # for layouts
grandchild = True  # Set this to False to only be parent/child
quick_editor = True  # quick_editor=quick_editor
enable_id = 1 # to see ID on tables.
_tabs_ = "-TABGROUP-"

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)  # <=== You can set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

sql_grandchild = """
CREATE TABLE IF NOT EXISTS "bike_repair" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	"bike_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_id") REFERENCES "bike"("id") ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "style" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Repair Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	"bike_repair_id"	INTEGER NOT NULL,
	FOREIGN KEY("bike_repair_id") REFERENCES "bike_repair"("id") ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""
sql_grandchild_insert = """
INSERT INTO "bike_repair" VALUES (1,'Wheel Repair',1,1);
INSERT INTO "bike_repair" VALUES (2,'Seat Repair',1,1);
INSERT INTO "style" VALUES (1,'Basic',1,1);
INSERT INTO "style" VALUES (2,'Premium',1,1);
"""

if not grandchild:
    sql_grandchild = ""
    sql_grandchild_insert = ""

sql = f"""
CREATE TABLE IF NOT EXISTS "car" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Car Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "bike" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL DEFAULT 'Bike Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	"person_id"	INTEGER NOT NULL,
	FOREIGN KEY("person_id") REFERENCES "person"("id") ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "person" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Person Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "building" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT DEFAULT 'Building Placeholder',
	"example"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
{sql_grandchild}
INSERT INTO "car" VALUES (1,'Landrover',1,1);
INSERT INTO "car" VALUES (2,'Jeep',1,2);
INSERT INTO "car" VALUES (3,'GTO',1,3);
INSERT INTO "bike" VALUES (1,'Unicycle',1,1);
INSERT INTO "bike" VALUES (2,'Street Bike',1,2);
INSERT INTO "bike" VALUES (3,'Moped',1,3);
INSERT INTO "person" VALUES (1,'Bill',0);
INSERT INTO "person" VALUES (2,'Jessica',0);
INSERT INTO "person" VALUES (3,'Drake',0);
INSERT INTO "building" VALUES (1,'Tower',0);
INSERT INTO "building" VALUES (2,'Mall',0);
INSERT INTO "building" VALUES (3,'Cabin',0);
{sql_grandchild_insert}
"""

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

# Building
# -------------------------

# Define the columns for the table selector
if tables:
    building_headings = ["id    ", "Name             ", "example"]
    building_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selBuilding_','building',sg.Table,num_rows=4,headings=building_headings,visible_column_map=building_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selBuilding_", "building", sg.Combo)]

building_layout = [
    [sg.Text("Buildings - Childless Parent")],
    selector,
    [ss.record("building.name"), ss.record("building.example", sg.Checkbox)],
    [ss.actions("_actBuilding_", "building", default=True)],
    [sg.HorizontalSeparator()],
]

# Person
# -------------------------
if tables:
    person_headings = ["id    ", "Name             ", "example"]
    person_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selPerson_','person',sg.Table,num_rows=4,headings=person_headings,visible_column_map=person_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selPerson_", "person", sg.Combo)]
# Define the columns for the table selector
person_layout = [
    [sg.Text("Person - Parent w/ cascade")],
    selector,
    [ss.record("person.name"), ss.record("person.example", sg.Checkbox)],
    [ss.actions("_actPerson_", "person", default=True)],
    [sg.HorizontalSeparator()],
]


# car
# -------------------------
# Define the columns for the table selector
if tables:
    car_headings = ["id    ", "Name             ", "example"]
    car_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selCar_','car',sg.Table,num_rows=4,headings=car_headings,visible_column_map=car_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selCar_", "car", sg.Combo)]
car_layout = [
    [sg.Text("Car - Child of Person/ Sibling of Bike")],
    selector,
    [ss.record("car.name"), ss.record("car.example", sg.Checkbox)],
    [
        ss.record("car.person_id", sg.Combo),
    ],
    [ss.actions("_actcar_", "car", default=True)],
]

# bike
# -------------------------
# Define the columns for the table selector
if tables:
    bike_headings = ["id    ", "Name             ", "example"]
    bike_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selBike_','bike',sg.Table,num_rows=4,headings=bike_headings,visible_column_map=bike_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selBike_", "bike", sg.Combo)]
bike_layout = [
    [sg.Text("Bike - Child of Person/ Sibling of Car")],
    selector,
    [ss.record("bike.name"), ss.record("bike.example", sg.Checkbox)],
    [ss.record("bike.person_id", sg.Combo)],
    [ss.actions("_actbike_", "bike", default=True)],
]

# bike_repair
# -------------------------
# Define the columns for the table selector
if tables:
    bike_repair_headings = ["id    ", "Name             ", "example"]
    bike_repair_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selRepair_','bike_repair',sg.Table,num_rows=4,headings=bike_repair_headings,visible_column_map=bike_repair_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selRepair_", "bike_repair", sg.Combo)]
bike_repair_layout = [
    [sg.HorizontalSeparator()],
    [sg.Text("Bike Repair - Bike child, Person Grandchild")],
    selector,
    [ss.record("bike_repair.name"), ss.record("bike_repair.example", sg.Checkbox)],
    [ss.record("bike_repair.bike_id", sg.Combo)],
    [ss.actions("_actrepair_", "bike_repair", default=True)],
]

# style
# -------------------------
# Define the columns for the table selector
if tables:
    style_headings = ["id    ", "Name             ", "example"]
    style_visible = [enable_id, 1, 1]
    selector = [ss.selector('_selStyle_','style',sg.Table,num_rows=4,headings=style_headings,visible_column_map=style_visible,auto_size_columns=True)]
else:
    selector = [ss.selector("_selStyle_", "style", sg.Combo)]
style_layout = [
    [sg.HorizontalSeparator()],
    [sg.Text("Repair Upgrade - Child of BikeRepair / Grandgrandchild of Person")],
    selector,
    [ss.record("style.name"), ss.record("style.example", sg.Checkbox)],
    [ss.record("style.bike_repair_id", sg.Combo)],
    [ss.actions("_actstyle_", "style", default=True)],
]

# -------------------------
# Main Layout
# -------------------------

layout = [[sg.Button("Form Prompt_Save", key="save")],[sg.Button("50 selector switch test", key="-timeit-")]]
layout.append([sg.Col(person_layout, size=sz), sg.Col(building_layout, size=sz)])
layout.append([sg.Col(bike_layout, size=sz), sg.Col(car_layout, size=sz)])
if grandchild:
    layout.append([sg.Col(bike_repair_layout, size=sz), sg.Col(style_layout, size=sz)])

window = sg.Window(
    "People and Vehicles",
    layout,
    finalize=True,
    grab_anywhere=True,
    alpha_channel=0,
)

driver = ss.Sqlite(":memory:", sql_commands=sql)  # Create a new database connection
frm = ss.Form(driver, bind=window)  # <=== Here is the magic!

frm.set_prompt_save(True)

window.SetAlpha(1)
print('start')

def test_set_by_pk(number):
    for i in range(number):
        frm['person'].set_by_pk(2)
        frm['person'].set_by_pk(1)
    
# ---------
# MAIN LOOP
# ---------

while True:
    event, values = window.read()
    if ss.process_events(
        event, values
    ):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f"PySimpleDB event handler handled the event {event}!")
        # handle button clicks
    elif event in (sg.WIN_CLOSED, "Exit", "-ESCAPE-"):
        frm.close()  # <= ensures proper closing of the sqlite database and runs a database optimization
        window.close()
        break
    elif event == "save":
        frm.prompt_save()  # Prompt save when tabs change
    elif event == "-timeit-":    
        st = time.time()
        test_set_by_pk(50)
        et = time.time()
        elapsed_time = et - st
        print(elapsed_time)
    else:
        logger.info(f"This event ({event}) is not yet handled.")
