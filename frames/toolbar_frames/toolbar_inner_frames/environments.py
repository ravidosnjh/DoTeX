"""Define Environments class.

Classes
-------
Environments
    Configures Environments menu.
"""
import tkinter as tk
from .latex_code import latex_code
from functools import partial


class Environments(tk.Menu):
    """A class configuring Environments menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    insert_environment()
        Inserts LaTeX environment selected by user in currently visible scrolled text box
    """

    def __init__(self, parent, controller, **kwargs):
        """Initialises Environments menu.

        Takes parent and **kwargs and passes to parent class constructor. Initialises tk.Menu object. Creates necessary
        attributes and sets to default values. Adds commands to menu.

        Parameters
        ----------
        self
            Environments object
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

        # For environment in environments list form latex_code/latex_code.py add command to Environments menu
        for environment in latex_code.environments:
            environment_p = partial(self.insert_environment, environment)
            self.add_command(
                label=environment,
                command=environment_p
            )

    def insert_environment(self, environment):
        """Inserts LaTeX environment selected by user in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of environment, determined by which command user selects, at current cursor position

        Parameters
        ----------
        environment : str
            LaTeX code to be inserted
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, environment)
