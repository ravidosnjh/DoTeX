"""Define Packages class.

Packages
-------
Table
    Configures Packages toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Packages(tk.Toplevel):
    """A class configuring Table toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    entered_packages : str
        stringvar containing package entered by user

    Methods
    -------
    close()
        Destroys Packages toplevel window
    insert_package()
        Inserts LaTeX command for using package in currently visible scrolled text box
    """

    def __init__(self, controller):
        """Initialises Packages toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Packages object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and size to 400x90, and make window not resizable
        self.title("Insert a Package")
        self.geometry("400x90")
        self.resizable(False, False)

        # Make row 2 and column 1 fill all available space
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        # Create StringVar to store package entered by user and set default value
        self.entered_packages = tk.StringVar(value="")

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Packages insert at cursor position")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create package entry label and entry box
        entry_label = ttk.Label(self, text="Choose packages separated\nby a comma and space: ", padding=(5, 0))
        entry_label.grid(row=1, column=0, sticky="nesw")

        entry_box = ttk.Entry(self, textvariable=self.entered_packages)
        entry_box.grid(row=1, column=1, sticky="nesw")

        # Create submit and close buttons
        submit_button = ttk.Button(
            self,
            text="Submit",
            command=self.insert_package
        )
        submit_button.grid(row=2, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=2, column=1, sticky="ns")

    def close(self):
        """Destroys Packages toplevel window"""
        self.destroy()

    def insert_package(self):
        """Inserts LaTeX command for using package in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts code
        for package entered by user at current cursor position
        """
        current_editor = self.controller.check_current_editor()
        packages = (self.entered_packages.get()).split(", ")
        for package in packages:
            formatted_package = f"\\usepackage{{{package}}}"
            current_editor.insert(tk.INSERT, formatted_package + "\n")
