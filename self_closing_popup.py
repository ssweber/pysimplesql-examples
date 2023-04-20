import PySimpleGUI as sg


class Popup:
    def __init__(self, window):
        """
        Create a new Popup instance
        :returns: None.
        """
        self.window = window
        self.info_popup = None

    def info(self, title: str, msg: str, auto_close_seconds: int):
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
        self.info_popup = sg.Window(
            title=title,
            layout=layout,
            keep_on_top=True,
            finalize=True,
            enable_close_attempted_event=True,
        )
        self.window.TKroot.after(auto_close_seconds * 1000, self._auto_close)

    def _auto_close(self):
        """
        Use in a tk.after to automatically close the popup_info.
        """
        self.info_popup.close()


layout = [
    [
        sg.Button("Test", key="test"),
    ]
]

window = sg.Window("Non Blocking Info Popup", layout, finalize=True, grab_anywhere=True,)
popup = Popup(window)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "test":
        popup.info(
            title="Self-closing custom popup",
            msg="I'll close in 5 seconds\nAnd I'm non-blocking",
            auto_close_seconds=5,
        )
window.close()
