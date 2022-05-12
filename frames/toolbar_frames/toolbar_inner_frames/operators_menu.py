"""Define OperatorsMenu class.

Classes
-------
OperatorsMenu
    Configures OperatorsMenu menu.
"""
import tkinter as tk
from .latex_code import latex_code
from functools import partial


class OperatorsMenu(tk.Menu):
    """A class configuring OperatorsMenu menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    insert_operator()
        Inserts LaTeX operator selected by user in currently visible scrolled text box
    """

    def __init__(self, parent, controller, **kwargs):
        """Initialises Commands menu.

        Takes parent and **kwargs and passes to parent class constructor. Initialises tk.Menu object. Creates necessary
        attributes and sets to default values. Adds commands to menu.

        Parameters
        ----------
        self
            OperatorsMenu object
        parent: ttk.Menubutton object
            Menubutton to associate OperatorsMenu menu with
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of keyword arguments
        """
        super().__init__(parent, **kwargs)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Add commands to OperatorsMenu menu for each operator in operators list form latex_code/latex_code.py
        for operator in latex_code.operators:
            operator_p = partial(self.insert_operator, operator)
            self.add_command(
                label=operator[1:],
                command=operator_p
            )

    def insert_operator(self, operator):
        """Inserts LaTeX operator selected by user in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of operator, determined by which operator user selects, at current cursor position

        Parameters
        ----------
        operator : str
            LaTeX code to be inserted
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, operator)
