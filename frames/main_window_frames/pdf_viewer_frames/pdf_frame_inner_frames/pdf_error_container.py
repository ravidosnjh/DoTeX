"""Define PDFErrorContainer class.

Classes
-------
PDFErrorContainer
    Configures PDFErrorContainer frame.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as scrolled_text
from files import error_functions as err


class PDFErrorContainer(ttk.Frame):
    """A class configuring TexEditorFrame frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    log_file_name : str
        stringvar containing loaded log file name
    error_buttons_frame : ttk.Frame()
        frame to contain tool buttons
    error_frame : ScrolledText()()
        scrolled text to display errors
    context_menu : tk.Menu()
        menu to appear when user right clicks

    Methods
    -------
    popup(event, editor)
        Creates context menu at cursor position when user right clicks
    copy()
        Copies selected text
    retrieve_error_message(log_file_name, log_file_path, tex_file, tex_file_name)
        Retrieves error messages from log file
    _format_error_message(errors)
        Formats retrieved errors and returns line numbers where errors occurred
    _highlight_error_lines(line_numbers)
        Highlights lines in scrolled text where errors occurred
    error_close()
        Removes highlight from lines in editor and destroys PDFErrorContainer frame
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises PDFErrorContainer.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            PDFErrorContainer object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to PDFFrame object to provide access to its attributes/methods
        self.controller = controller
        # Create variable to store log file name
        self.log_file_name = ""

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Create frame to contain error tool buttons
        self.error_buttons_frame = ttk.Frame(self)
        self.error_buttons_frame.grid(row=0, column=0, sticky="nesw")

        # Create scrolled text to display errors
        self.error_frame = scrolled_text.ScrolledText(self)
        self.error_frame.grid(row=1, column=0, sticky="nesw")

        # Create error title label and close and save buttons
        error_title = ttk.Label(
            self.error_buttons_frame,
            text="Compile Errors"
        )
        error_title.place(relx=0.5, rely=0.5, anchor="center")

        error_close = ttk.Button(
            self.error_buttons_frame,
            text="X",
            command=self.error_close,
            style="CloseButtons.TButton"
        )
        error_close.pack(side="right")

        error_save = ttk.Button(
            self.error_buttons_frame,
            text="Save As",
            command=self._save_log_as,
            padding=(0, 0)
        )
        error_save.pack(side="right")

        # Create right click context menu and add command
        self.context_menu = tk.Menu(self.error_frame, tearoff=0)
        self.context_menu.add_command(
            label="Copy",
            command=self.copy,
            accelerator="Ctrl+C"
        )
        self.error_frame.bind("<Button-3>", self.popup)

    def popup(self, event):
        """Creates context menu at cursor position when user right clicks.

        Parameters
        ----------
        event
            tkinter event to handle bind
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    def copy(self):
        """Copies selected text"""
        self.error_frame.event_generate("<<Copy>>")

    def retrieve_error_message(self, log_file_name, log_file_path, tex_file, tex_file_name):
        """Retrieves error messages from log file.

        Calls retrieve_error_message() from files/error_functions.py to retrieve error messages from log file.

        Parameters
        ----------
        log_file_name : str
            log file name
        log_file_path : str
            log file path
        tex_file : str
            tex file path
        tex_file_name : str
            tex file name
        """
        self.log_file_name, line_numbers = err.retrieve_error_message(
            self,
            log_file_name,
            log_file_path,
            tex_file,
            tex_file_name
        )

    def _format_error_message(self, errors):
        """Formats retrieved errors

        Parameters
        ----------
        errors : list
            list of retrieved errors from log file
        """
        err.format_error_message(self, errors)

    def error_close(self):
        """Destroys TexErrorContainer frame and readds welcome label if initial frame"""
        self.grid_forget()
        self.destroy()
        self.controller.error_container = None
        if self.controller.initial_frame:
            self.controller.buttons_frame.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    def _save_log_as(self):
        """Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text
        box
        """
        err.save_log_as(self)
