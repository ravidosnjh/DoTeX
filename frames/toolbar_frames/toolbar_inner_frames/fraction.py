"""Define Fraction class.

Classes
-------
Fraction
    Configures Fraction toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Fraction(tk.Toplevel):
    """A class configuring Fraction toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    numerator : str
        stringvar containing numerator entered by user
    denominator : str
        stringvar containing denominator entered by user

    Methods
    -------
    create()
        Inserts LaTeX command for creating fraction in currently visible scrolled text box
    close()
        Destroys Fraction toplevel window
    """

    def __init__(self, controller):
        """Initialises Fraction toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Fraction object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Insert a Fraction")
        self.resizable(True, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create StringVars to store values entered by user and set default values
        self.numerator = tk.StringVar(value="")
        self.denominator = tk.StringVar(value="")

        # Make row 1 and columns 0 and 1 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Fractions insert at cursor position")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain numerator and denominator entry boxes
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        # Make frame column 0 fill all available space
        frame.columnconfigure(0, weight=1)

        # Create numerator and denominator entry boxes, and seperator to simulate divisor line
        numerator = ttk.Entry(
            frame,
            textvariable=self.numerator,
            width=50,
            justify="center"
        )
        numerator.grid(row=0, column=0, sticky="ew", padx=(10, 10), pady=(10, 0))

        separator = tk.Frame(frame, bg="black", height=1, bd=0)
        separator.grid(row=1, column=0, sticky="ew", pady=(5, 5), padx=(10, 10))

        denominator = ttk.Entry(
            frame,
            textvariable=self.denominator,
            width=50,
            justify="center"
        )
        denominator.grid(row=2, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))

        # Create create and close buttons
        create_button = ttk.Button(
            self,
            text="Create",
            command=self.create,
        )
        create_button.grid(row=3, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=1, sticky="ns")

    def create(self):
        """Inserts LaTeX command for creating fraction in currently visible scrolled text box

        Checks values have been entered. Calls check_current_editor() method from controller and assigns return to
        current editor. This returns the scrolled text box widget in the currently selected tab in the currently visible
        tex editor frame. Inserts code for fraction at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        insert = f"\\frac{{{self.numerator.get()}}}{{{self.denominator.get()}}}"
        current_editor.insert(tk.INSERT, insert)

    def close(self):
        """Destroys Fraction toplevel window"""
        self.destroy()
