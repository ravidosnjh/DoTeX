"""Define GreekLetters class.

Classes
-------
GreekLetters
    Configures GreekLetters toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from.latex_code import latex_code
from functools import partial


class GreekLetters(tk.Toplevel):
    """A class configuring GreekLetters toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    close()
        Destroys GreekLetters toplevel window
    insert_letter()
        Inserts LaTeX command for greek letter in currently visible scrolled text box
    """

    def __init__(self, controller):
        """Initialises Symbols toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates notebook, greek letter frames and buttons to insert greek letters.

        Parameters
        ----------
        self
            GreekLetters object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and make window not resizable
        self.title("Insert a Greek Letter")
        self.resizable(False, False)

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Greek Letters insert at cursor position")
        label.grid(row=0, column=0, sticky="ns")

        # Create notebook to contain greek letter frames
        notebook_frame = ttk.Frame(self)
        notebook_frame.grid(row=1, column=0, sticky="nesw")

        notebook = ttk.Notebook(notebook_frame)
        notebook.pack(fill="both", expand=True)

        # Create greek letter frames to contain symbol buttons
        lowercase = ttk.Frame(notebook)
        uppercase = ttk.Frame(notebook)
        var = ttk.Frame(notebook)

        # Add greek letter frames to notebook
        notebook.add(lowercase, text="Lower")
        notebook.add(uppercase, text="Upper")
        notebook.add(var, text="Var")

        # Create buttons for lowercase greek letters, using greek_letters dictionary from latex_code/latex_code.py
        count, count1, count2, count3 = 0, 0, 0, 0
        for pair in latex_code.greek_letters.items():
            letter, letter_code = pair
            cmd = partial(self.insert_letter, letter_code)
            button = ttk.Button(
                lowercase,
                text=letter,
                command=cmd
            )
            # Grid 6 buttons per row
            if count <= 5:
                button.grid(row=0, column=count)
            elif count <= 11:
                button.grid(row=1, column=count1)
                count1 += 1
            elif count <= 17:
                button.grid(row=2, column=count2)
                count2 += 1
            else:
                button.grid(row=3, column=count3)
                count3 += 1
            count += 1

        # Create buttons for capital greek letters, using capital_greek_letters dictionary from latex_code/latex_code.py
        count, count1, count2, count3 = 0, 0, 0, 0
        for pair in latex_code.capital_greek_letters.items():
            letter, letter_code = pair
            cmd = partial(self.insert_letter, letter_code)
            button = ttk.Button(
                uppercase,
                text=letter,
                command=cmd
            )
            # Grid 6 buttons per row
            if count <= 5:
                button.grid(row=0, column=count)
            elif count <= 11:
                button.grid(row=1, column=count1)
                count1 += 1
            elif count <= 17:
                button.grid(row=2, column=count2)
                count2 += 1
            else:
                button.grid(row=3, column=count3)
                count3 += 1
            count += 1

        # Create buttons for variation greek letters, using var_greek_letters dictionary from latex_code/latex_code.py
        count = 0
        for pair in latex_code.var_greek_letters.items():
            letter, letter_code = pair
            cmd = partial(self.insert_letter, letter_code)
            button = ttk.Button(
                var,
                text=letter,
                command=cmd
            )
            button.grid(row=0, column=count)
            count += 1

        # Create label for suggested packages
        packages_label = tk.Label(
            self,
            text="Suggested packages: upgreek, textgreek, babel",
            justify="center"
        )
        packages_label.grid(row=2, column=0, sticky="ns", pady=5)

        # Create close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=0, sticky="ns")

    def close(self):
        """Destroys GreekLetters toplevel window"""
        self.destroy()

    def insert_letter(self, letter):
        """Inserts LaTeX command for greek letter in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of letter at current cursor position, where letter is determined by button user presses.

        Parameters
        ----------
        letter : str
            LaTeX code to insert
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, letter)
