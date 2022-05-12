"""Define ReservedChars class.

Classes
-------
ReservedChars
    Configures ReservedChars toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from.latex_code import latex_code
from functools import partial


class ReservedChars(tk.Toplevel):
    """A class configuring ReservedChars toplevel window.

        Attributes
        ----------
        controller : widget object
            a reference to master widget object to provide access to its attributes/methods

        Methods
        -------
        close()
            Destroys ReservedChars toplevel window
        insert_char()
            Inserts LaTeX command for reserved character in currently visible scrolled text box
        """

    def __init__(self, controller):
        """Initialises ReservedChars toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons to insert reserved characters.

        Parameters
        ----------
        self
            ReservedChars object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and make window not resizable
        self.title("Insert a Reserved Character")
        self.resizable(False, False)

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Symbols insert at cursor position")
        label.grid(row=0, column=0, sticky="ns")

        # Create frame to contain reserved character buttons
        reserved = ttk.Frame(self)
        reserved.grid(row=1, column=0, sticky="nesw")

        # Create buttons for reserved characters, using reservedc dictionary from latex_code/latex_code.py
        count, count1, count2 = 0, 0, 0
        for pair in latex_code.reservedc.items():
            char, char_code = pair
            cmd = partial(self.insert_char, char_code)
            button = ttk.Button(
                reserved,
                text=char,
                command=cmd
            )
            # Grid 3 buttons per row
            if count <= 2:
                button.grid(row=0, column=count)
            elif count <= 5:
                button.grid(row=1, column=count1)
                count1 += 1
            else:
                button.grid(row=2, column=count2)
                count2 += 1
            count += 1

        # Create close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=2, column=0, sticky="ns")

    def close(self):
        """Destroys ReservedChars toplevel window"""
        self.destroy()

    def insert_char(self, char_code):
        """Inserts LaTeX command for character in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of char_code at current cursor position, where char_code is determined by button user presses.

        Parameters
        ----------
        char_code : str
            LaTeX code to insert
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, char_code)
