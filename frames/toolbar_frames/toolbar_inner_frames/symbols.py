"""Define Symbols class.

Classes
-------
Symbols
    Configures Symbols toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from.latex_code import latex_code
from functools import partial


class Symbols(tk.Toplevel):
    """A class configuring Symbols toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    close()
        Destroys Symbols toplevel window
    insert_symbol()
        Inserts LaTeX command for symbol in currently visible scrolled text box
    """

    def __init__(self, controller):
        """Initialises Symbols toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates notebook, symbol frames and buttons to insert symbols.

        Parameters
        ----------
        self
            Symbols object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Set window title and make window not resizable
        self.title("Insert a Symbol")
        self.resizable(False, False)

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Symbols insert at cursor position")
        label.grid(row=0, column=0, sticky="ns")

        # Create notebook to contain symbol frames
        notebook_frame = ttk.Frame(self)
        notebook_frame.grid(row=1, column=0, sticky="nesw")

        notebook = ttk.Notebook(notebook_frame)
        notebook.pack(fill="both", expand=True)

        # Create symbol frames to contain symbol buttons
        arrows = ttk.Frame(notebook)
        relations = ttk.Frame(notebook)
        miscs = ttk.Frame(notebook)

        # Add symbol frames to notebook
        notebook.add(arrows, text="Arrows")
        notebook.add(relations, text="Relations")
        notebook.add(miscs, text="Misc")

        # Create required packages reminder in each symbol frame
        frames = [arrows, relations, miscs]
        for frame in frames:
            warning_label = ttk.Label(
                frame,
                text="Some symbols require extra packages"
            )
            warning_label.grid(row=0, column=0, columnspan=6, sticky="ns")

        # Create symbol buttons for arrow symbols, using arrows dictionary from latex_code/latex_code.py
        count, count1, count2, count3 = 0, 0, 0, 1
        for pair in latex_code.arrows.items():
            arrow, code = pair
            cmd = partial(self.insert_symbol, code)
            button = ttk.Button(
                arrows,
                text=arrow,
                command=cmd
            )
            # Grid 6 buttons per row
            if count <= 5:
                button.grid(row=1, column=count)
            elif count <= 11:
                button.grid(row=2, column=count1)
                count1 += 1
            elif count <= 17:
                button.grid(row=3, column=count2)
                count2 += 1
            else:
                button.grid(row=4, column=count3, sticky="ns")
                count3 += 1
            count += 1

        # Create symbol buttons for relation symbols, using relations dictionary from latex_code/latex_code.py
        count, count1, count2, count3 = 0, 0, 0, 1
        for pair in latex_code.relations.items():
            relation, code = pair
            cmd = partial(self.insert_symbol, code)
            button = ttk.Button(
                relations,
                text=relation,
                command=cmd
            )
            # Grid 6 buttons per row and centre buttons in final row
            if count <= 5:
                button.grid(row=1, column=count)
            elif count <= 11:
                button.grid(row=2, column=count1)
                count1 += 1
            elif count <= 17:
                button.grid(row=3, column=count2)
                count2 += 1
            else:
                button.grid(row=4, column=count3, sticky="ns")
                count3 += 1
            count += 1

        # Create symbol buttons for misc symbols, using miscs dictionary from latex_code/latex_code.py
        count, count1, count2, = 0, 0, 0
        for pair in latex_code.miscs.items():
            misc, code = pair
            cmd = partial(self.insert_symbol, code)
            button = ttk.Button(
                miscs,
                text=misc,
                command=cmd
            )
            # Grid 6 buttons per row and centre buttons in final row
            if count <= 5:
                button.grid(row=1, column=count)
            elif count <= 11:
                button.grid(row=2, column=count1)
                count1 += 1
            elif count <= 17:
                button.grid(row=3, column=count2, sticky="ns")
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
        """Destroys Symbols toplevel window"""
        self.destroy()

    def insert_symbol(self, symbol):
        """Inserts LaTeX command for symbol in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of symbol at current cursor position, where symbol is determined by button user presses.

        Parameters
        ----------
        symbol : str
            LaTeX code to insert
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, symbol)
