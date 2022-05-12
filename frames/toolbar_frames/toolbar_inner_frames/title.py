"""Define Title class.

Classes
-------
Title
    Configures Title toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Title(tk.Toplevel):
    """A class configuring Title toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    entered_title : str
        stringvar containing title entered by user
    entered_author : str
        stringvar containing author entered by user
    entered_thanks : str
        stringvar containing thanks entered by user
    entered_date : str
        stringvar containing date entered by user
    additional_entered_author : str
        stringvar containing additional authors entered by user
    additional_enetered_thanks : str
        stringvar containing additional thanks entered by user

    Methods
    -------
    close()
        Destroys Title toplevel window
    create_preamble()
        Inserts LaTeX commands for defining title in currently visible scrolled text box
    add_additional_author()
        Inserts LaTeX commands for defining additional authors in currently visible scrolled text box
    make_title()
        Inserts LaTeX command for making title in currently visible scrolled text box
    """

    def __init__(self, controller):
        """Initialises Title toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Title object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and make window not resizable
        self.title("Insert a Title")
        self.resizable(False, False)

        # Make row 0 and columns 0, 1 and 2 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Create StringVars to store entered values, and default values
        self.entered_title = tk.StringVar(value="")
        self.entered_author = tk.StringVar(value="")
        self.entered_thanks = tk.StringVar(value="")
        self.entered_date = tk.StringVar(value="")
        self.additional_entered_author = tk.StringVar(value="")
        self.additional_entered_thanks = tk.StringVar(value="")

        # Create labels and entry boxes for title fields
        label = tk.Label(self, text="Title options insert at cursor position")
        label.grid(row=0, column=0, columnspan=3, sticky="ns")

        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=3, sticky="nesw")
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        heading_label = ttk.Label(frame, text="Create title")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ns")

        title_label = ttk.Label(frame, text="Enter a Title: ", padding=(5, 0))
        title_label.grid(row=1, column=0, sticky="ns")
        title_entry = ttk.Entry(frame, textvariable=self.entered_title)
        title_entry.grid(row=1, column=1, sticky="nesw")

        author_label = ttk.Label(frame, text="Enter an Author: ", padding=(5, 0))
        author_label.grid(row=2, column=0, sticky="ns")
        author_entry = ttk.Entry(frame, textvariable=self.entered_author)
        author_entry.grid(row=2, column=1, sticky="nesw")

        thanks_label = ttk.Label(frame, text="Enter a Thanks: ", padding=(5, 0))
        thanks_label.grid(row=3, column=0, sticky="ns")
        thanks_entry = ttk.Entry(frame, textvariable=self.entered_thanks)
        thanks_entry.grid(row=3, column=1, sticky="nesw")

        date_label = ttk.Label(frame, text="Enter a Date: ", padding=(5, 0))
        date_label.grid(row=4, column=0, sticky="ns")
        date_entry = ttk.Entry(frame, textvariable=self.entered_date)
        date_entry.grid(row=4, column=1, sticky="nesw")

        # Create button to insert code
        create_button = ttk.Button(
            frame,
            text="Create Preamble",
            command=self.create_preamble
        )
        create_button.grid(row=5, column=0, columnspan=2, sticky="ns")

        # Create labels and entry boxes for additional authors
        heading_label2 = ttk.Label(frame, text="Enter additional authors")
        heading_label2.grid(row=0, column=2, columnspan=2, sticky="ns")

        info_label = ttk.Label(frame, text="Place cursor before\nclosing brace of \\author", justify="center")
        info_label.grid(row=3, column=2, rowspan=2, columnspan=2, sticky="ns")

        author_label = ttk.Label(frame, text="Enter an Author: ", padding=(5, 0))
        author_label.grid(row=1, column=2, sticky="ns")
        author_entry = ttk.Entry(frame, textvariable=self.additional_entered_author)
        author_entry.grid(row=1, column=3, sticky="nesw")

        thanks_label = ttk.Label(frame, text="Enter a Thanks: ", padding=(5, 0))
        thanks_label.grid(row=2, column=2, sticky="ns")
        thanks_entry = ttk.Entry(frame, textvariable=self.additional_entered_thanks)
        thanks_entry.grid(row=2, column=3, sticky="nesw")

        # Create buttons to insert code for additional authors, insert make title command, and close window
        submit_button = ttk.Button(
            frame,
            text="Submit",
            command=self.add_additional_author
        )
        submit_button.grid(row=5, column=2, columnspan=2, sticky="ns")

        make_button = ttk.Button(
            self,
            text="Insert Make Title Command",
            command=self.make_title
        )
        make_button.grid(row=2, column=0, columnspan=2, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=2, column=2, columnspan=2, sticky="ns")

    def close(self):
        """Destroys StudyTimer toplevel window."""
        self.destroy()

    def create_preamble(self):
        """Inserts LaTeX commands for defining title in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If a value has
        been entered for thanks filed, inserts LaTeX code for defining title with thanks at current cursor position.
        Else inserts LaTeX code for defining title without thanks at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        if self.entered_thanks.get():
            current_editor.insert(tk.INSERT, f"\\title{{{self.entered_title.get()}}}\n"
                                             f"\\author{{{self.entered_author.get()} "
                                             f"\\thanks{{{self.entered_thanks.get()}}}}}\n"
                                             f"\\date{{{self.entered_date.get()}}}"
                                  )
        else:
            current_editor.insert(tk.INSERT, f"\\title{{{self.entered_title.get()}}}\n"
                                             f"\\author{{{self.entered_author.get()}}}\n"
                                             f"\\date{{{self.entered_date.get()}}}"
                                  )

    def add_additional_author(self):
        """Inserts LaTeX commands for defining additional authors in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If a value has
        been entered for additional thanks filed, inserts LaTeX code for defining additional authors with thanks at
        current cursor position. Else inserts LaTeX code for defining additional authors without thanks at current
        cursor position.
        """
        current_editor = self.controller.check_current_editor()
        if self.additional_entered_thanks.get():
            current_editor.insert(tk.INSERT, f"\n\\and {self.additional_entered_author.get()} "
                                             f"\\thanks{{{self.additional_entered_thanks.get()}}}"
                                  )
        else:
            current_editor.insert(tk.INSERT, f"\n\\and {self.additional_entered_author.get()}")

    def make_title(self):
        """Inserts LaTeX command for making title in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for making title at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{titlepage}\n\\maketitle\n\\end{titlepage}")
