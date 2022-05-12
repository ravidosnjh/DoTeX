"""Define Brackets class.

Classes
-------
Brackets
    Configures Brackets menu.
"""
import tkinter as tk
from .latex_code import latex_code
from functools import partial


class Brackets(tk.Menu):
    """A class configuring Brackets menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    insert_code()
        Inserts LaTeX code for bracket in currently visible scrolled text box
    """

    def __init__(self, parent, controller, **kwargs):
        """Initialises Brackets menu.

        Takes parent and **kwargs and passes to parent class constructor. Initialises tk.Menu object. Creates necessary
        attributes and sets to default values. Adds commands to menu.

        Parameters
        ----------
        self
            Brackets object
        parent: ttk.Menubutton object
            Menubutton to associate Brackets menu with
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of keyword arguments
        """
        super().__init__(parent, **kwargs)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Add commands for left and right brackets
        left_p = partial(self.insert_code, "\\left")
        self.add_command(
            label="Left",
            command=left_p
        )

        right_p = partial(self.insert_code, "\\right")
        self.add_command(
            label="Right",
            command=right_p
        )

        # Add submenu and commands for bracket sizes
        size_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(
            label="Size",
            menu=size_menu
        )

        big = partial(self.insert_code, "\\big")
        size_menu.add_command(
            label="big",
            command=big
        )

        bigg = partial(self.insert_code, "\\bigg")
        size_menu.add_command(
            label="bigg",
            command=bigg
        )

        Big = partial(self.insert_code, "\\Big")
        size_menu.add_command(
            label="Big",
            command=Big
        )

        Bigg = partial(self.insert_code, "\\Bigg")
        size_menu.add_command(
            label="Bigg",
            command=Bigg
        )

        # For bracket:code pair in brackets dictionary from latex_code/latex_code.py add submenu and add commands to
        # insert code for brackets
        for bracket, code in latex_code.brackets.items():
            l_code = code[0]
            r_code = code[1]
            bracket_menu = tk.Menu(self, tearoff=0)
            self.add_cascade(
                label=bracket,
                menu=bracket_menu
            )
            bracket_l_p = partial(self.insert_code, l_code)
            bracket_r_p = partial(self.insert_code, r_code)
            bracket_menu.add_command(
                label=bracket[0],
                command=bracket_l_p
            )
            bracket_menu.add_command(
                label=bracket[2],
                command=bracket_r_p
            )

    def insert_code(self, code):
        """Inserts LaTeX code for bracket in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of code, determined by which command user selects, at current cursor position

        Parameters
        ----------
        code : str
            LaTeX code to be inserted
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, code)
