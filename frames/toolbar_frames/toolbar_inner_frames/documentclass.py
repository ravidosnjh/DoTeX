"""Define Documentclass class.

Classes
-------
Documentclass
    Configures Documentclass toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Documentclass(tk.Toplevel):
    """A class configuring Documentclass toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    entered_documentclass : str
        stringvar containing documentclass entered by user
    entered_parameters : str
        stringvar containing documentclass parameters entered by user

    Methods
    -------
    close()
        Destroys Documentclass toplevel window
    insert_documentclass()
        Inserts LaTeX command for documentclass in currently visible scrolled text box
    """

    def __init__(self, controller):
        """Initialises Packages toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Documentclass object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and size to 400x150, and make window not resizable
        self.title("Insert a Documentclass")
        self.geometry("400x150")
        self.resizable(False, False)

        # Make rows 1 and 2 and column 1 fill all available space
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        # Create StringVars to store values entered by user and set default value
        self.entered_documentclass = tk.StringVar()
        self.entered_parameters = tk.StringVar()

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Documentclass inserts at first line")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create documentclass and parameters entry labels and entry boxs
        entry_label = ttk.Label(self, text="Choose a Document type: ", padding=(5, 0))
        entry_label.grid(row=1, column=0, sticky="ns")
        entry_box = ttk.Combobox(self, textvariable=self.entered_documentclass)
        entry_box.config(values=("article", "report", "book", "letter", "slides"))
        entry_box.grid(row=1, column=1, sticky="nesw")

        entry_label = ttk.Label(
            self,
            text="Choose other parameters\nseparated by a comma and\nspace (e.g. font size): ",
            padding=(5, 0)
        )
        entry_label.grid(row=2, column=0, sticky="ns")
        entry_box = ttk.Entry(self, textvariable=self.entered_parameters)
        entry_box.grid(row=2, column=1, sticky="nesw")

        # Create submit and close buttons
        submit_button = ttk.Button(
            self,
            text="Submit",
            command=self.insert_documentclass
        )
        submit_button.grid(row=3, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=1, sticky="ns")

    def close(self):
        """Destroys Documentclass toplevel window"""
        self.destroy()

    def insert_documentclass(self):
        """Inserts LaTeX command for documentclass in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts code
        for documentclass with parameters if entered at start of file
        """
        current_editor = self.controller.check_current_editor()
        # If a documentclass value was entered insert code with value. Else insert code without documentclass value.
        if self.entered_documentclass.get():
            # If no parameters entered, insert code without parameters field, else insert code with parameters
            if not self.entered_parameters.get():
                documentclass = f"\\documentclass{{{self.entered_documentclass.get()}}}"
            else:
                documentclass = \
                    f"\\documentclass[{self.entered_parameters.get()}]{{{self.entered_documentclass.get()}}}"
            current_text = current_editor.get("1.0", "1.end")

            if not current_text:
                current_editor.insert("1.0", documentclass)
            elif "\\documentclass" in current_text:
                current_editor.delete("1.0", "1.end")
                current_editor.insert("1.0", documentclass)
            else:
                current_editor.insert("1.0", documentclass + "\n")
        else:
            # If parameters entered, insert code with parameters field, else insert code without parameters
            if self.entered_parameters.get():
                current_editor.insert("1.0", f"\\documentclass[{self.entered_parameters.get()}]{{}}")
            else:
                current_editor.insert("1.0", "\\documentclass[]{}")
