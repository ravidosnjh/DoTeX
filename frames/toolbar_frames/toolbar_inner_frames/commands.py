"""Define Commands class.

Classes
-------
Commands
    Configures Commands menu.
"""
import tkinter as tk
from .latex_code import latex_code
from functools import partial


class Commands(tk.Menu):
    """A class configuring Commands menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    insert_cmd()
        Inserts LaTeX command selected by user in currently visible scrolled text box
    """

    def __init__(self, parent, controller, **kwargs):
        """Initialises Commands menu.

        Takes parent and **kwargs and passes to parent class constructor. Initialises tk.Menu object. Creates necessary
        attributes and sets to default values. Adds commands to menu.

        Parameters
        ----------
        self
            Commands object
        parent: ttk.Menubutton object
            Menubutton to associate Commands menu with
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of keyword arguments
        """
        super().__init__(parent, **kwargs)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                    "v", "w", "x", "y", "z"]

        # Create submenus for each letter of the alphabet and associate with Commands menu. Within each submenu add
        # commands for items from commands list of lists from latex_code/latex_code.py that start with the corresponding
        # letter
        count = 0
        for letter in latex_code.commands:
            # Create submenu for letter and associate with Commands menu
            letter_menu = tk.Menu(self, tearoff=0)
            self.add_cascade(
                label=alphabet[count],
                menu=letter_menu
            )
            # Add commands to submenu
            for command in letter:
                command_p = partial(self.insert_cmd, command)
                letter_menu.add_command(
                    label=command,
                    command=command_p
                )
            count += 1

    def insert_cmd(self, command):
        """Inserts LaTeX command selected by user in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of command, determined by which command user selects, at current cursor position

        Parameters
        ----------
        command : str
            LaTeX code to be inserted
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, command)
