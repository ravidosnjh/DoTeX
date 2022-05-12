"""Define Bib class.

Classes
-------
Bib
    Configures Bib toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import shutil


class Bib(tk.Toplevel):
    """A class configuring Bib toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    bib_style : str
        stringvar containing bib style entered by user
    bib_file : str
        stringvar containing bib file selected by user

    Methods
    -------
    browse()
        Opens filedialog for user to select bib file; copies selected file to DoTeX root directory
    insert()
        Inserts LaTeX commands for creating bibliography in currently visible scrolled text box
    close()
        Destroys Bib toplevel window
    """

    def __init__(self, controller):
        """Initialises Bib toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Bib object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title, and make window not resizable
        self.title("Insert a Biblography")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create StringVars to store values entered by user and set default value
        self.bib_style = tk.StringVar(value="")
        self.bib_file = tk.StringVar(value="")

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Biblography inserts at cursor position\nSave bib files to DoTeX root folder")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain field entry widgets
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        bib_style_label = ttk.Label(
            frame,
            text="Bibliography style: ",
            padding=(5, 0)
        )
        bib_style_label.grid(row=0, column=0, sticky="ns")

        bib_style_entry = ttk.Combobox(
            frame,
            textvariable=self.bib_style,
            state="readonly"
        )
        bib_style_entry.grid(row=0, column=1, sticky="nesw", padx=(0, 5))
        # Add bib style options to combobox
        bib_style_entry.config(values=("abbrv", "acm", "alpha", "apalike", "ieeetr", "plain", "siam", "unsrt"))

        bib_file_label = ttk.Label(
            frame,
            text="Bib file: ",
            padding=(5, 0)
        )
        bib_file_label.grid(row=1, column=0, sticky="ns", pady=5)

        bib_file_entry = tk.Entry(
            frame,
            textvariable=self.bib_file,
            width=20
        )
        bib_file_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5))

        # Create browse, insert and close buttons
        browse_button = ttk.Button(
            frame,
            text="Browse",
            command=self.browse
        )
        browse_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="ns")

        insert_button = ttk.Button(
            self,
            text="Insert",
            command=self.insert,
        )
        insert_button.grid(row=3, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=1, sticky="ns")

    def browse(self):
        """Opens filedialog for user to select bib file; copies selected file to DoTeX root directory"""
        # Open filedialog for user to select bib file
        file = tk.filedialog.askopenfilename(
            title="Select a Bib file",
            initialdir=".",
            filetypes=(("Bib Files (*.bib)", "*.bib"), ("All Files", "*.*"))
        )
        # Copy selected file to DoTeX root directory if it is not already there
        try:
            shutil.copy(file, ".")
        except shutil.SameFileError:
            pass
        # Set bib_file to name of selected bib file
        file_path, file_name = os.path.split(file)
        file_name = file_name.split(".")[0]
        self.bib_file.set(file_name)

    def insert(self):
        """Inserts LaTeX commands for creating bibliography in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts code
        for bib style and bib file values entered by user current cursor position
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, f"\\bibliographystyle{{{self.bib_style.get()}}}\n"
                                         f"\\biblography{{{self.bib_file.get()}}}")

    def close(self):
        """Destroy Bib toplevel window"""
        self.destroy()
