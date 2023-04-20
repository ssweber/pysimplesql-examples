import PySimpleGUI as sg

def info(title: str, msg: str, auto_close_seconds: int):
    """
    Displays a popup window with the passed message string and auto-closes after the specified time.

    :param title: String to display as title.
    :param msg: String to display as message. Use '\n' for newlines.
    :param auto_close_seconds: Time in seconds after which the window will automatically close.
    :return: None
    """
    # Split the message string into lines
    msg_lines = msg.splitlines()

    # Create the layout for the window
    layout = [[sg.Text(line)] for line in msg_lines]

    # Create the window
    window = sg.Window(
        title=title,
        layout=layout,
        keep_on_top=True,
        finalize=True,
        enable_close_attempted_event=True
    )

    # Wait for events until the timeout or close event occurs
    while True:
        event, values = window.read(timeout=auto_close_seconds * 1000)
        if event in ['__TIMEOUT__', '-WINDOW CLOSE ATTEMPTED-']:
            break

    # Close the window
    window.close()
       
info(title="Self-closing custom popup", msg="I'll close in 5 seconds\nAnd I'm non-blocking,", auto_close_seconds = 5)
