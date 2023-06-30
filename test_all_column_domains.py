# import pathlib
# import sys

# p = pathlib.Path.cwd().parent.parent
# sys.path.append(f"{str(p)}/pysimplesql/")

# jackcess-4.0.5.jar additionally supports `attachment` column, but not datetime_extended

from install_java import java_check_install
import logging
import PySimpleGUI as sg
import pysimplesql as ss  # <=== PySimpleSQL lines will be marked like this.  There's only a few!

# Set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure that Java is installed
if not java_check_install():
    exit(0)

headings = ss.TableHeadings(sort_enable=True)
headings.add_column("short_text", "short_text", width=40)
layout = [[ss.selector("Test", sg.Table, num_rows=10, headings=headings)]]

# Create the Window, Driver and Form
win = sg.Window("Test example: All Column Types", layout, finalize=True)
driver = ss.Driver.msaccess(
#     "test_all_column_domains.accdb", use_newer_jackcess=True,
    "test_all_column_domains.mdb"
)
frm = ss.Form(driver, bind_window=win)  # <=== Here is the magic!
# ---------
# MAIN LOOP
# ---------
while True:
    event, values = win.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        # Ensure proper closing of our resources
        driver.close()
        frm.close()
        win.close()
        break
    elif ss.process_events(
        event, values
    ):  # <=== let PySimpleSQL process its own events! Simple!
        logger.info(f"PySimpleDB event handler handled the event {event}!")
    else:
        logger.info(f"This event ({event}) is not yet handled.")
