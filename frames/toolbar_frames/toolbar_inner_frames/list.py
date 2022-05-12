"""Define List class.

Classes
-------
List
    Configures List toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class List(tk.Toplevel):
    """A class configuring Table toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    bullet_items : int
        intvar containing number of items in bullet list entered by user
    numbered_items : int
        intvar containing number of items in numbered list entered by user
    labelled_items : int
        intvar containing number of items in labelled list entered by user

    Methods
    -------
    create_bullet()
        Inserts LaTeX commands for creating bullet list in currently visible scrolled text box
    create_numbered()
        Inserts LaTeX commands for creating numbered list in currently visible scrolled text box
    create_labelled()
        Inserts LaTeX commands for creating labelled list in currently visible scrolled text box
    create_lof()
        Inserts LaTeX command for creating list of figures in currently visible scrolled text box
    create_lot()
        Inserts LaTeX command for creating list of tables in currently visible scrolled text box
    close()
        Destroys List toplevel window
    """

    def __init__(self, controller):
        """Initialises List toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            List object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Insert a List")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create IntVars to store values entered by user and set default values
        self.bullet_items = tk.IntVar(value=1)
        self.numbered_items = tk.IntVar(value=1)
        self.labelled_items = tk.IntVar(value=1)

        # Make row 0 fill all available space
        self.rowconfigure(1, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Lists insert at cursor position")
        label.grid(row=0, column=0, sticky="ns")

        # Create frame to contain list type and number of items user can choose, and buttons to insert
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, sticky="nesw")

        bullet_label = ttk.Label(
            frame,
            text="Bullet List"
        )
        bullet_label.grid(row=0, column=0, sticky="ns")

        bullet_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=300,
            textvariable=self.bullet_items
        )
        bullet_spinbox.grid(row=0, column=1, sticky="ns")

        bullet_button = ttk.Button(
            frame,
            text="Create",
            command=self.create_bullet
        )
        bullet_button.grid(row=0, column=2, sticky="ns")

        numbered_label = ttk.Label(
            frame,
            text="Numbered List",
            padding=(5,0)
        )
        numbered_label.grid(row=1, column=0, sticky="ns")

        numbered_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=300,
            textvariable=self.numbered_items
        )
        numbered_spinbox.grid(row=1, column=1, sticky="ns")

        numbered_button = ttk.Button(
            frame,
            text="Create",
            command=self.create_numbered
        )
        numbered_button.grid(row=1, column=2, sticky="ns")

        labelled_label = ttk.Label(
            frame,
            text="Labelled List"
        )
        labelled_label.grid(row=2, column=0, sticky="ns")

        labelled_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=300,
            textvariable=self.labelled_items
        )
        labelled_spinbox.grid(row=2, column=1, sticky="ns")

        labelled_button = ttk.Button(
            frame,
            text="Create",
            command=self.create_labelled
        )
        labelled_button.grid(row=2, column=2, sticky="ns")

        lof_label = ttk.Label(
            frame,
            text="List of Figures"
        )
        lof_label.grid(row=3, column=0, sticky="ns")

        # Create buttons to insert code for list of figures and list of tables
        lof_button = ttk.Button(
            frame,
            text="Create",
            command=self.create_lof
        )
        lof_button.grid(row=3, column=2, sticky="ns")

        lot_label = ttk.Label(
            frame,
            text="List of Tables"
        )
        lot_label.grid(row=4, column=0, sticky="ns")

        lot_button = ttk.Button(
            frame,
            text="Create",
            command=self.create_lot
        )
        lot_button.grid(row=4, column=2, sticky="ns")

        # Create label for suggested packages
        packages_label = tk.Label(
            self,
            text="Suggested packages: enumitem, babel, layouts",
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

    def create_bullet(self):
        """Inserts LaTeX commands for creating bullet list in currently visible scrolled text box

        Formats code for bullet list with entered number of items. Checks values have been entered. Calls
        check_current_editor() method from controller and assigns return to current editor. Inserts code at current
        cursor position
        """
        items = ""
        for count in range(0, self.bullet_items.get()):
            items += ("  \\item\n")

        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, f"\\begin{{itemize}}\n{items}\\end{{itemize}}")

    def create_numbered(self):
        """Inserts LaTeX commands for creating numbered list in currently visible scrolled text box

        Formats code for numbered list with entered number of items. Checks values have been entered. Calls
        check_current_editor() method from controller and assigns return to current editor. Inserts code at current
        cursor position
        """
        items = ""
        for count in range(0, self.numbered_items.get()):
            items += ("  \\item\n")

        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, f"\\begin{{enumerate}}\n{items}\\end{{enumerate}}")

    def create_labelled(self):
        """Inserts LaTeX commands for creating labelled list in currently visible scrolled text box

        Formats code for labelled list with entered number of items. Checks values have been entered. Calls
        check_current_editor() method from controller and assigns return to current editor. Inserts code at current
        cursor position
        """
        items = ""
        for count in range(0, self.labelled_items.get()):
            items += ("  \\item[]\n")

        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, f"\\begin{{description}}\n{items}\\end{{description}}")

    def create_lof(self):
        """Inserts LaTeX command for creating list of figures in currently visible scrolled text box"""
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\listoffigures")

    def create_lot(self):
        """Inserts LaTeX command for creating list of tables in currently visible scrolled text box"""
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\listoftables")

    def close(self):
        """Destroys List toplevel window"""
        self.destroy()
