"""Define SaveEquation class.

Classes
-------
SaveEquation
    Configures SaveEquation toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from functools import partial
from files import saved_equations


class SaveEquation(tk.Toplevel):
    """A class configuring SaveEquation toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    name : str
        stringvar containing name of equation entered by user
    equation : str
        stringvar containing equation code entered by user

    Methods
    -------
    save()
        Writes name:equation pair entered by user to dictionary in files/saved_equations.py
    close()
        Destroys SaveEquation toplevel window
    """

    def __init__(self, controller):
        """Initialises SaveEquation toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Symbols object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Save an Equation")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create StringVars and set default values
        self.name = tk.StringVar(value="")
        self.equation = tk.StringVar(value="")

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Saved equations appear in Saved Equations list")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain name and equation parameters user can configure
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        # Create labels and entry boxes for name and equation
        name_label = ttk.Label(
            frame,
            text="Name: ",
            padding=(5, 0)
        )
        name_label.grid(row=1, column=0, sticky="ns", pady=5)

        name_entry = ttk.Entry(
            frame,
            textvariable=self.name,
            width=20
        )
        name_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5))

        equation_label = ttk.Label(
            frame,
            text="Equation: ",
            padding=(5, 0)
        )
        equation_label.grid(row=2, column=0, sticky="ns", pady=5)

        equation_entry = ttk.Entry(
            frame,
            textvariable=self.equation,
            width=40
        )
        equation_entry.grid(row=2, column=1, sticky="ew", padx=(0, 5))

        # Create save and close buttons
        save_button = ttk.Button(
            self,
            text="Save",
            command=self.save,
        )
        save_button.grid(row=2, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=2, column=1, sticky="ns")

    def save(self):
        """Writes name:equation pair entered by user to dictionary in files/saved_equations.py and adds to saved
        equations menu

        Gets dictionary from files/saved_equations.py and adds name:equation pair entered by user to it. Opens
        saved_equations.py and overwrites contents with updated dictionary. Adds submenu for equation to saved equtions
        dropdown menu with insert and delete commands
        """
        # Get dictionary from saved_equations.py
        equations = saved_equations.equations
        # Add entered name:equation pair
        equations[self.name.get()] = self.equation.get()
        # Open saved_equations.py to write
        file = open("files/saved_equations.py", "w")
        # Overwrite contents with updated dictionary
        file.write(f"equations = {equations}")
        # Close saved_equations.py
        file.close()

        # Create submenu for equation and associate with saved equations menu
        equation_sub_menu = tk.Menu(self.controller.saved_equations_button_menu, tearoff=0)
        self.controller.saved_equations_button_menu.add_cascade(
            label=self.name.get(),
            menu=equation_sub_menu
        )

        # Add commands to insert and delete equation
        equation_p = partial(self.controller.insert_equation, self.equation.get())
        equation_delete_p = partial(self.controller.delete_equation, self.name.get())
        equation_sub_menu.add_command(
            label="Insert",
            command=equation_p
        )
        equation_sub_menu.add_command(
            label="Delete",
            command=equation_delete_p
        )

    def close(self):
        """Destroys SaveEquation toplevel window"""
        self.destroy()
