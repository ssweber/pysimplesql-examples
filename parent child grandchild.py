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
grandchild = False  # Set this to False to only be parent/child
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
	"example"	TEXT NOT NULL DEFAULT False,
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

# -------------------------
# CREATE PYSIMPLEGUI LAYOUT
# -------------------------

# Building
# -------------------------

# Define the columns for the table selector
if tables:
    # Define the columns for the table selector using the TableHeading convenience class.  This will also allow sorting!
    headings = ss.TableHeadings(sort_enable=True)
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
    headings = ss.TableHeadings(sort_enable=True)
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
    headings = ss.TableHeadings(sort_enable=True)
    headings.add_column("id", "id", width=10)
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
    headings = ss.TableHeadings(sort_enable=True)
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
    headings = ss.TableHeadings(sort_enable=True)
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
    headings = ss.TableHeadings(sort_enable=True)
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
    grab_anywhere=True,
    alpha_channel=0,
    ttk_theme=ss.themepack.ttk_theme,
)

driver = ss.Sqlite(":memory:", sql_commands=sql)  # Create a new database connection
frm = ss.Form(
    driver,
    bind_window=window,
    prompt_save=ss.AUTOSAVE_MODE,  # save_quiet=True
)  # <=== Here is the magic!
if foreign_keys:
    driver.con.execute("PRAGMA foreign_keys = ON")

# frm.set_prompt_save(ss.AUTOSAVE_MODE)
# frm.set_fk_column_cascade("bike_repair", "bike_id", update_cascade=False)
window.SetAlpha(1)

edit = False


def callback(event):
    global edit
    global textvariable  # needs to be global, or ttk entry garbage collects it.

    # only allow 1 edit at a time
    if edit:
        print(edit)
        return

    # if double click a treeview
    if event.widget.__class__.__name__ == "Treeview":
        tk_widget = event.widget

        # identify region
        region = tk_widget.identify("region", event.x, event.y)

        if region == "cell":
            # get row and column
            row = int(tk_widget.identify_row(event.y))
            col_identified = tk_widget.identify_column(event.x)
            if (
                col_identified
            ):  # Sometimes tkinter returns a value of '' which would cause an error if cast to an int
                column = int(tk_widget.identify_column(event.x)[1:]) - 1
        else:
            return

        for data_key in [
            data_key for data_key in frm.datasets if len(frm[data_key].selector)
        ]:
            for e in frm[data_key].selector:
                element = e["element"]
                if element.widget == tk_widget and element.metadata["TableHeading"]:
                    print(data_key)

                    # found a table we can edit, don't allow another double-click
                    edit = True

                    # disable browsing and sorting
                    element.widget.configure(select=sg.TABLE_SELECT_MODE_NONE)
                    element.metadata["TableHeading"]._sort_enable = False
                    frm.edit_protect()

                    # get column name
                    column_names = element.metadata["TableHeading"].columns()
                    heading_column = column_names[column - 1]
                    # get dataset_row
                    if (
                        column > 0
                        and heading_column != frm[data_key].pk_column
                    ):
                        combobox = False
                        rels = ss.Relationship.get_relationships(frm[data_key].table)
                        for rel in rels:
                            if rel.fk_column == heading_column:
                                target_table = frm[rel.parent_table]
                                pk_column = target_table.pk_column
                                fk_column = rel.fk_column
                                description = target_table.description_column
                                combobox = True
                                break

                        # use table_element to distinguish
                        table_element = element.Widget
                        root = table_element.master

                        # get cell text, coordinates, width and height
                        text = table_element.item(row, "values")[column]
                        x, y, width, height = table_element.bbox(row, column)

                        # float a frame over the cell
                        frame = sg.ttk.Frame(root)
                        frame.place(x=x, y=y, anchor="nw", width=width, height=height)

                        # create ttk.Entry / StringVar and place in frame
                        textvariable = sg.tk.StringVar()
                        textvariable.set(text)
                        if not combobox:
                            entry = sg.ttk.Entry(
                                frame, textvariable=textvariable, justify="left"
                            )
                        elif combobox:
                            lst = []
                            for r in target_table.rows:
                                lst.append(ss.ElementRow(r[pk_column], r[description]))

                            # Map the value to the combobox, by getting the description_column
                            # and using it to set the value
                            for r in target_table.rows:
                                if r[target_table.pk_column] == frm[data_key][fk_column]:
                                    for entry in lst:
                                        if entry.get_pk() == frm[data_key][fk_column]:
                                            updated_val = entry
                                            break
                                    break
                            entry = sg.ttk.Combobox(
                                frame, textvariable=textvariable, justify="left"
                            )
                            entry['values'] = lst

                        # bind text to Return (for save), and Escape (for discard)
                        entry.bind(
                            "<Return>",
                            _EditCallbackWrapper(
                                frm,
                                data_key,
                                element.metadata["TableHeading"],
                                table_element,
                                column_names,
                                row,
                                column,
                                text,
                                True,
                            ),
                        )
                        entry.bind(
                            "<Escape>",
                            _EditCallbackWrapper(
                                frm,
                                data_key,
                                element.metadata["TableHeading"],
                                table_element,
                                column_names,
                                row,
                                column,
                                text,
                                False,
                            ),
                        )

                        # buttons
                        save = sg.tk.Button(
                            frame,
                            text="\u2714",
                            relief=sg.tk.GROOVE,
                            command=_EditCallbackWrapper(
                                frm,
                                data_key,
                                element.metadata["TableHeading"],
                                table_element,
                                column_names,
                                row,
                                column,
                                text,
                                True,
                                entry,
                            ),
                        )
                        discard = sg.tk.Button(
                            frame,
                            text="\u274E",
                            relief=sg.tk.GROOVE,
                            command=_EditCallbackWrapper(
                                frm,
                                data_key,
                                element.metadata["TableHeading"],
                                table_element,
                                column_names,
                                row,
                                column,
                                text,
                                False,
                                entry,
                            ),
                        )
                        discard.pack(side="right")
                        save.pack(side="right")

                        # have entry use remaining space
                        entry.pack(side="left", expand=True, fill="both")

                        # select text and focus to begin with
                        entry.select_range(0, sg.tk.END)
                        entry.focus_force()
                    else:
                        # found a table we can edit, don't allow another double-click
                        edit = False

                        # enable browsing and sorting
                        element.widget.configure(select=sg.TABLE_SELECT_MODE_BROWSE)
                        element.metadata["TableHeading"]._sort_enable = True
                        frm.edit_protect()

class _EditCallbackWrapper:

    """Internal class used when sg.Table cells are double-clicked."""

    def __init__(
        self,
        frm_reference,
        data_key,
        table_heading,
        table_element,
        column_names,
        row,
        column,
        text,
        save,
        entry=None,
    ):
        """
        Create a new _EditCallbackWrapper object.

        :param frm_reference: `Form` object
        :param data_key: `DataSet` key
        :param element: PySimpleGUI sg.Table element
        :param table_heading: `TableHeading` object
        :returns: None
        """
        self.frm: Form = frm_reference
        self.data_key = data_key
        self.table_heading: TableHeadings = table_heading
        self.table_element = table_element
        self.column_names = column_names
        self.row = row
        self.column = column
        self.text = text
        self.save = save
        self.entry = entry

    def __call__(self, event=None):
        # create our callback (to be used below)
        global edit

        if event is None:
            event = self.entry

        # if a button got us here, event is actually Entry element
        if event.__class__.__name__ in ["Entry","Combobox"]:
            widget = event

        # otherwise, use event widget
        else:
            widget = event.widget

        #
        if self.save:
            # get current entry text
            self.text = widget.get()             

            # get current table row
            values = list(self.table_element.item(self.row, "values"))

            # update cell with new text
            values[self.column] = self.text

            # push changes to table element row
            self.table_element.item(self.row, values=values)

            # update dataset row
            # TODO. We need to have a backup current row handy to compare.
            # -------------------
            # get current row
            current_index = self.frm[self.data_key].current_index
            current_row = self.frm[self.data_key].get_current_row().copy()
            
            if widget.__class__.__name__ == "Combobox":
                self.text = 2 # cheating for the example

            # update cell with new text
            current_row[self.column_names[self.column - 1]] = self.text
            # push row to dataset
            self.frm[self.data_key].rows[current_index] = current_row
            self.frm[self.data_key].save_record()

        # destroy window
        widget.destroy()
        widget.master.destroy()

        # enable browsing and sorting
        self.table_element.configure(select=sg.TABLE_SELECT_MODE_BROWSE)
        self.table_heading._sort_enable = True
        self.frm.edit_protect()

        # reset edit
        edit = False


def update_table_row(table, row, values):
    table.item(row, values=values)


window.TKroot.bind("<Double-Button-1>", callback)

frm.force_save = True


def test_set_by_pk(number):
    for i in range(number):
        frm["person"].set_by_pk(2)
        frm["person"].set_by_pk(1)


# variables for updating our sg.StatusBar
seconds_to_display = 3
last_val = ""
new_val = ""
counter = 1
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
