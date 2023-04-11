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
    'delete': b'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',
    'duplicate': b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAD+klEQVRYhbWXy24jRRSG/64qZxycCCNbQblB2JANqyRiD5s8BYN4hGHBhk22g3gIeAA2GTaMvIMRIwWECMow0xe3L7HTbZk4jh3buKvqsLC7Yzudy5Ceso7ktqvP+eqc/3R1GUSE28bOzs7HqVSKp1JzaYq9gaC1hlIaWivc5pNzzj3Pq5RKJUvcGh3AYDB4u1Ao/JDNZheV0rFziEYQRITb1pROz+Hx42++A/DFnQAAQEplSKkQBMGN8wzDuJM/pVQKAK4F2N3dZWtraxkAeaVUDgAbre7m5d2lpON5NAXAGOPZbDa3vv7e+sbG+xsPH37+aT6fq/i+39ja2v6WMeMtpdSdnL/OEADw6NGXXx0c/PbZ0tLSu/l8Pjc/n2bhhPPzDvb392+t670AVldXNre3tz4KAgmlFHq9PoBRPfv9HqSUbyZ6CHB4+NffAG4UWFj/u9b4tQBs27KU0jAM49oASQOEXgQAVKvVUrvdHmYymbk4oYWdlWgGxn4YAPi+X/d9v8k5j503MoLWyVjoMwIIguDUdd1jzvlUqvXE99FHJ2IaFBWBjVOrHMd2DAPTwfVE3QkgnZCpGQ0AwMuXr8ywzlGJJoCSFCGRjmoQAZimaUmppgEQBkwa4NJHBFAul4qdTgdCCCitoxxNAiUJMCVCADg5OTluNpunhsFi0g7MZuG+NiVCAOh2u81qtVrngica6HqbyQAR9YtFx+WMTan/sgXjBfn/MzCjAQAwTcsyGJuaELYgEhYhYaYLAMCyTFNKOfpzHEeHGUi6C8ZupgCKxaLT7/dHDx2K2iC6JtKjHr43gMYVEQJArVYvt1qtC4MZkVAmFXu5LyRg45hTAKen/zTq9brH2WwnJCtACilmAbTW7XKpVJndlC4fRm+4CwDAtm2bMfbJbFDGGIQQ0DpGA8b1l5oIggukUqnot4WFRcw9eGDEAjiOYxKmV72ysopCoQDGGBA10MQgjPd5PTqcAGDMAGMciwuL8H2v1Wq1/hBCMABIp9Pzz5//+mcswIsXR0f9fj8KzhhHLpcD5wzh2xJFqzTAGAMXHIJzMMZAAILhEJ1uF2et1sC7uDh7+vSn73988uRrAHwiQRIAjNm+zmQyH/z8y7OD5eXlnAwkiDSkUuCMjwIJAc4FAMLw3yHa7Tb8hn9eq9UarutWbdtyik7RrNWO3Wazedztdo+JyCei2DfeKxno9XqNhu/XNj/czA2DAABBSolup0N+zWtXqpUTx3bKlm255ivTLFfKdsP3K4PBwAfQIqJhXKDrxhUAIrrY29v7XUq5eHh4eGRZpuW6pWK1Wil6nlfu9XoegDYRJXJYuFICABBCvKO1ZkR0RkTJn8cmxn+A59n5AYSivAAAAABJRU5ErkJggg==',
    'edit_protect': b'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',
    'first': b'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',
    'insert': b'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',
    'last': b'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',
    'next': b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFLUlEQVRYhb2WWWwd1RnHf993Zq59V49tYuIGx8lNHOzEBAKhFS+VCiQChBAPSAhB0qoYQTBlUQtUYpOo1D71pZRCxRM88cIinthBKAEclizNJSRExFl8neslNHbs3Jk7M4eHa4s6+DqucTjSJ50Zjeb/O7+zzIi1lrPbZfe89mxrcrzHl+zxD45kb7KvXFv40UOL1HS2mwf7ixu7Lr0q8bd7rsnXJ8z2+ts+2PKzApRDy7NvDXC4NMm9m5Z5dUZeSt3x4fOZrR8lfxYAY4RIoK8YcNsta7hxcx6x3B1ZdmZ/t33deQcQEVxV9muS3gJ8lV/OhuvW0pRxusMo/jj7+x095xUAAVGhHMGJMoxMwuDyFvI3baC9LZcLw+iFTM/HL2Tv+iR7XgBEFFRRERwBIxAGcKQuSW7TJay/4iKMtT2xtX25uz/tXnQAhGqqyIxbGsFgZJi4PM/633TgpdyuMLJ9uW192xYZQFCj1dSzmrEwVobBthby16+jrTWTiiL7r1zvzhcb7vvMWyQAQAWsxQYWW4lmlFQigomIfpPC+3UnXd0tSMzW2PJJw/2fX7YIAIKoYmNLHFRmLRtUYKLMsQnLZEcb3b9qI5tyOqOYPu/BL+/7yQA4ClGM9cPaFYSoH/DfMZ9ig0f7xnaWXpBMRLF9xnto18uNf9zdtCAAmTJAbLHlCtafu8Sv4I+X6a8YcmuXkV/hgXBrDDsaH97zywUYAIxgo5jYrxD74TnL+iGcCTh+qkJ5iUdHRzP1CdMZxuzwHtn7h1oAzuwAgqiB2FZfHsdzDeJHIzpZhslEHas6mhgcGHeGxyr/aHrsP1eLyp2jf+k+OQ8DAo5g4/kb+N9yopBEFBAo3Lt5KY9eeSGVgt5c3i+7vAcKv52HAVBjiMbPEBw7TYwgIlPnglS36FRfpvtSfcZ1hGza0JhQWhxD4LscOx3iZgyB2pI4dvTcACpYI9VFGERYwKpWD0aZGWinrkWFuoTSmDR4KUt7owGU5z/6jqFSicyaln/WW/408tRa/5wAgiCiGEdR12ARRKdGLz8YmLaiqmTqFS9jaM4a2ptcSmOWnUd9Jo8emMy2Xbxl5MmLX50tq+YUYAQxghhTtX2W6mkTriPkkgYvY2j1DC0Zlz3FkH279mGi4EByZfd1I0+s6Z81p6YBnToHtLoYYab+6Xmvcw2NGcVLKSuaXcDw7qGAoW/22/TKrr8T28dHHl/tz5Yxt4HpEav+YEC0Og1SnY5MvcFLKRdkDcsbXYpjli8GfCb7959Or+zaMvzn/OtzBc8NoFr9Fqggjk6tiWq4Y4Rs0uClldaGqvLdgxFf7d6Hhv7XqdXrNw0/svL4fMJrA0z/D8wwINS5QkNa8VKGfLNDbA3vfFth5GDBZlZ1/ZXYPj308IpgvuG1AQC0usfFCIKQrlcaUsqSrKG90eXoKcvuExXK3+47lV69buvQQ8vf+H+C5wZQQYyCUYxryNYrXlr5Rc7QlHLZVYo4dLiIHR38OrXm0qtLD7YNLiS8JoBIVb86Sjbj4KWVVU0OkTW8fzRk9EABxzH/ruvc0Fu6f1m00PCaABYhRuhsSXBzV5Jjp0I+K8UURkP8b/aezHSsv/1Eb+ubPyV4TgBRUEcZH1A2XpikMHaGLw4eRoaLhdTayzed2LZ0wcrnCSBoILz9Xkj/oQn2lvdYx5Hnvnvmht7FCp4TwMbCmSPKKmMYco4Pup3r7hjpWfL+YofXBHByrdsrA8XVw3XFfveiK28c6WleNOVnt+8Bfz9FSi10CPQAAAAASUVORK5CYII=',
    'previous': b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFOklEQVRYhbWXW2wc1R3Gf+cysxd27V3b69okXsdOsL3YikFBqUCKEG3Vpz60aqUqlUqrKlUShVtVhfIAQq1UwQMBIZEKJHgAhFD7UCHUh7aBoEaJaNKWJI6dOCEKDmAbJ8GbOL7t5Zx/H3ajBmdN7cT+SyOdGZ2Z75vv+58z3ygRYbVK/fC93gfar74bkatrx+eSrx57+Qe7Fs7RqwUe3frBT6OhOfjMjm935vrvDc+MjN1Ta55daeDEgwdi3vsXIkZt3/at2/lkYpa9fxulVK6t9IoqkPz5wV4nHFHC9u99t5OtP+ri8FgRp8AYVfOeFVMg+YtD28rO72lI2LqO+zZwsqOZXUOQ1jECrXFqlQgkf/lhUkSed2W3rb2tjsyWbsbiMYqzoAOIOVBaQW38WyNQt/2ffV7kT1Yk17tpLbKxnfNiUEUwqnJopUBrlKrt9k0TqNt5eGfZyXPpeBDv3NxOvr2ZKwUwC3tNVZmslAL1D/0rJSIvOicPtrUmaL5vPePxOMV5MLVuUKDNCvVA/SP/vssLb2tPT66vGZNrY0QC1IxDAQtfXkSDCKxED6Qe++gh59lTF7dhR28L+W80cXlGMDKPqBvBAZTXiBeU1hUrboZA+tfHGsTLH5yXH7c0xcjkWhkLYxSmCmhqA18rcRqcB3uTBNK7j2/28LpS9HSuS2HWNjJSVKjCfE3JbyBQ1lBVQC2XQOrxgYed5/l4aGw2W89U4jbyV0qYKvBSPmHKKET75a2CxqcGG8TLa2VR38+kQlrXJPmsZJm/XMDopQFfK681RASlzdIsSD069LPSqPqdLqvsb36SIdoe8sdTM4SuSNkJrrQMdACtkACwamkElFVfqriaCLzKfjZdpr0ArbaIwZEveaZmHKWyICKV5SUgvmqIANeNRQSN4NoSaGMWteAr+2N+z51/ia5ni+ripdePnuXlA3mSRrM+bcjEhcYYRJSHskNKleN/4zJSHfuSQ4plpOjAC1LZk/+/AgCXns4VgIebfqs+mBw5/eY+3xPfnI3Q3Rrj/GSJIHRcnnZMz3u899WOvE4BERSCeI1GMNaglEctIsGieeDS091/jrX39M6NDJ7ef+gEJ77wdDRFyGYCMumAdNIShAaMRhmDMrqy3q2G6nnl+td/C742kFx6qmsk2rmx/7aO3HNDx0/Ke2dLJKMhXS0hzWlLUyogGrUoq1BWXweqwZpK82lV2QeWasENJJ7cUAB2Z55Vhy6ePfnm38u5xKY1Id0tUT7Nlwis4/KsZnregQdEEA9KPAoDWoP2iz5/yZHs4hOd78Q778zNnTsxfODDQQYmhHWNEbJNAZl6SzoREAQVFbRVKGtQViNVBdC1oZaVCS8+3vF5/I7+/sT63O9PHR+UfefKJKIh3S0hmZSlod4SiZiv9ABar2weuLB7XRF4svkFdWTy48E39rm++rtaLLmWCOerllyZ9czMexRS8X4R/+EWUvGFX2XfjW/oy82fPT58+NQYRyeEtnSEdU0BmZQllbSY4Noq0YuSuKVYPvFY23i85+4+PTf1ypmBIfZ/6ohFQrqaQxrrLcmERVtdzYSrlIonHlnjYM2Olr3j7+RPD7z1vt/Y0Nto2ZINaKu3DH/pODZZQJa7ES23vtjV+td4d39fYfjo0H/OjDI1ZbnHxrg6qtFWs0goRq3Gz2n6iX/s9WXZuTHar84MO2SLZ3bg/SPTr2395sK5q/Jzmn/2/l1BT+93LtjPx1uNYe68RvwqW7CwLm3L7C+svX3Txcjhj9zo2KStaz1Ya95/AdVeAp1ltJoNAAAAAElFTkSuQmCC',
    'quick_edit': b'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',
    'save': b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFZ0lEQVRYha2XzY9cRxXFf7fqvW53j40JMSBPYicOyBCQkfEKIjFBkcIifGwQkjdI/CUsYIGyYAMjEcSW/8ARChIR2IJsYYFICDjYjgJI4IwBe/q9V3XvZVH1errHtFi0S7p631XnnnPqVj1xd548d/7CyZOnX3cIk7b1r37ty/9sm4g7WzcRYRgS11792ZmUEoI0X9jb2//Jj/dfBhB3J8b42y+99PXLZx5/jLfffotf/fJ1ZtNm+9FrO+wGXnjhRZ48/3GatuGNG7+4fef2zacBGgB3ZzabYR5wd7q+ZzZt8EdAgYiQUsLdyDkhAqq6fF7TFFSNxWKBiJDV6PrEO+/c2hrAMx+7QFbHvQwcY1x7XgE4KSX6rgd3TB0RuPDMU1sDEAEzw90xM1QN54jZpdBmhpri7gw5c9ilRyJBECFlxSkArI7xEIARobtjapgZt2/d2RrAU0+fJ6vi5kcSrOS1BKCqZWB3kiopZc7unt0aQEqZnEtiqorqJgbMlgyoGlnt0cyCEAoD/88DqrrUJ2clq/LunXe3BnDu/DlyVsytSqBrBW7dhFWrrEZS46O7u1sDSFqzNsdUMVX4XxLYigRZlZz00RWifCSBHZN2HYAWqoaUCSL87b2/bg3g7BO75JyXALLqZg9oZUFVEWk5+8T2s0AE1HzZbwhhTYIwnowM5Jz541tvEpuW2LSE2KyFhLgxjr8bY0vTTnjzD78n51wYyBumoWoGEU6d+hDf/953aNu2ZiCICAgECUgo10I5OqWIHUUxnLsXqh1SSpz+4IerDBtmgZoiBLJmJExRE2IMIAEJgbASIlKoXGFvFcTRjDLMjdg0qGbcQYJsXgvAEBHatgERBOj7AXcIQeq9wkZJzteuWWEjxsh0OingcKxmLy4bJMhFAhHBpABpYsNXXnqRq1e/wXw+Q+BosBHMQ81ZdD0/+OGPuHHjN0gQNGfcjfnJUyPKTQxUzUPAzDhxYsrze5/HtOeVV37KtVevEUPgE89+mm998ypnzjxOzhkQpKITgRPTKZcuPcv1X79B27a0kwn/undAOwyEGDeZUI8AuOPVsffvP2BnZ85rP38N9ZYYW/7051u8//49ptMpKaWlUd0dEaGf9hweLoocZrgIIUgdQ1YXw3UG3L0Yblm1MiklcsqAIxIItbOUEyklzIpcpXZUEEAaBkwVLdQsZwCUhW8DAw5meJXAzBiGnq7vKiBHtbg/58wwDOSc17IvUpYdlqliIVQmHDMv+W+qA+5OqIODk3Om63v6vsfN0ArA3ckpobVwjc4fJYwxkHIqU7oyYKaIQNM2G6aharntDjUjratXSgnVCsAKU/0w0Pf9koGxiQg5ayFTDZXy/pj0aNqNHvAVQxUPlFBVhqFsr2MMpJQYhmFp3lUGRk+oZkIda9zomPnDDLi7LSvVCgBVo+97+q7j8mevcPPmX2ialitXLoM7wzCs7SXHb0MIDEO/ZkIzY+g7YtOUPcExBj53cPfvvzv92Ec+BYLV1Wtx+J9/Z8079x88iM/vPccX957DvFQ/d6PrumVHo3/GY0qZISVq1SLGSEoDufykyHEAMef03bv/eO/bUtoQQpDd3d2bN65f/8B8PpeaWSjrgUgIyx+MsbO13cvBwUHTH977ZF/1LxKVxHZ2Tr68/HjUbjabyf7+fnvx4sVp0zSzyWQybZpm1jRNnE6nk6ZpZiGEEzHGaQhhIiIt0IrIuCq5u5u7ZzMbUhqyO4Oqdqq5zykvUk5d13X35/P53UuXPmMi4ksTLhYLBwYg10g1ZjXLBog1wkrm47kDuvJtD3THYlEjALbGwLE2dior56v3VuN482NhNVavx3P+C8rLX/5PvFqmAAAAAElFTkSuQmCC',
    'search': b'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'}

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
    [ss.field("building.person_id", sg.Combo)],
    [
        ss.field("building.name"),
        ss.field("building.example", sg.Checkbox, default=False),
    ],
    [ss.actions("building", default=True,)],
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
    driver, bind_window=window, prompt_save=ss.AUTOSAVE_MODE, save_quiet=True
)  # <=== Here is the magic!
if foreign_keys:
    driver.con.execute("PRAGMA foreign_keys = ON")

frm.set_prompt_save(ss.AUTOSAVE_MODE)
frm.set_fk_column_cascade("bike_repair", "bike_id", update_cascade=False)
window.SetAlpha(1)


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
