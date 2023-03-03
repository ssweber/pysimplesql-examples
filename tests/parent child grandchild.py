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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'building',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "building", sg.Combo)]

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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'person',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "person", sg.Combo)]
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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'car',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "car", sg.Combo)]
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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'bike',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "bike", sg.Combo)]
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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'bike_repair',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "bike_repair", sg.Combo)]
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
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings=ss.TableHeadings(sort_enable=True)
    headings.add('id', 'id', width=10)
    headings.add('Name', 'name', width=10)
    headings.add('Example', 'example',  width=20)
    selector = [ss.selector('sel', 'style',sg.Table,num_rows=4,headings=headings,auto_size_columns=True)]
else:
    selector = [ss.selector('sel', "style", sg.Combo)]
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

class ColumnSort:
    
    def __init__(self,window,table_element,ekey):
        self.window = window
        self.widget = self.window[table_element].Widget
        self.ekey = ekey
  
    def double_click(self,event):
        """
        Additional event for double-click on header
        event: class event
        """
        region = self.widget.identify("region", event.x, event.y)
        if region == 'heading':                                 # Only care double-clock on headings
            cid = int(self.widget.identify_column(event.x)[1:])-1     # check which column clicked
            self.window.write_event_value(self.ekey, cid)

sq = dict()
for q, t in frm.queries.items():
    if len(t.selector):
        for e in t.selector:
            element = e["element"].key
            event_key = f'{q}??{element}'
            columns = e["element"].metadata["columns"]
        sq[q] = {}
        sq[q]['columns'] = columns
        sq[q]['order'] = 'DESC'
        sq[q]['widget'] = window[element].Widget
        sq[q]['widget'].bind('<Double-Button-1>', ColumnSort(window=window,table_element=element,ekey=event_key).double_click, add='+')

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

    elif "??" in event:
        table, element = event.split('??')
        column_index = values[event]
        column_index -= 1 if column_index > 0 else 0 # ignore the virtual column
        column_name = sq[table]['columns'][column_index]
        pk = frm[table].get_current_pk()
        frm[table].set_order_clause(f"ORDER by {column_name} {sq[table]['order']}")
        sq[table]['order'] = 'DESC' if sq[table]['order'] == 'ASC' else 'ASC'
        frm[table].prompt_save()
        frm[table].requery(select_first=False) #keep spot in table
        frm[table].set_by_pk(pk,dependents=False,skip_prompt_save=True)
    else:
        logger.info(f"This event ({event}) is not yet handled.")
