"""Define Table class.

Classes
-------
Table
    Configures Table toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Table(tk.Toplevel):
    """A class configuring Table toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    rows : int
        intvar containing number of rows entered by user
    columns : int
        intvar containing number of columns entered by user
    text_alignment : str
        stringvar containing text alignment entered by user
    table_alignment : str
        stringvar containing table alignment entered by user
    cells : str
        stringvar containing cell delimiters entered by user
    position : str
        stringvar containing position entered by user
    caption_check : int
        intvar indicating if caption checkbox has been ticked
    caption_position : str
        stringvar containing caption position entered by user
    entered_label : str
        stringvar containing label entered by user
    delimiter_entry : tk.Entry()
        entry widget containing value of cells attribute
    create_button = ttk.Button()
        button inserting LaTeX code into currently visible tex editor

    Methods
    -------
    populate_delimiter()
        Sets cells attributes based on field values entered by user
    create()
        Inserts LaTeX commands for creating table in currently visible scrolled text box
    close()
        Destroys Table toplevel window
    """

    def __init__(self, controller):
        """Initialises Table toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Table object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Insert a Table")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create IntVars and StringVars to store values entered by user and set default values
        self.rows = tk.IntVar(value=0)
        self.columns = tk.IntVar(value=0)
        self.text_alignment = tk.StringVar(value="")
        self.table_alignment = tk.StringVar(value="")
        self.cells = tk.StringVar(value="")
        self.position = tk.StringVar(value="")
        self.caption_check = tk.IntVar(value=0)
        self.caption_position = tk.StringVar(value="")
        self.entered_label = tk.StringVar(value="")

        # Make row 1 and columns 0 and 1 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Tables insert at cursor position\nReplace 'cell' with data")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain table parameters user can configure
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        # Create labels and entry boxes
        rows_label = ttk.Label(
            frame,
            text="Rows: ",
            padding=(5, 0)
        )
        rows_label.grid(row=0, column=0, sticky="ns", pady=5)

        rows_box = ttk.Spinbox(
            frame,
            from_=1,
            to=100,
            textvariable=self.rows
        )
        rows_box.grid(row=0, column=1, sticky="nesw")

        columns_label = ttk.Label(
            frame,
            text="Columns: ",
            padding=(5, 0)
        )
        columns_label.grid(row=0, column=2, sticky="ns")

        columns_box = ttk.Spinbox(
            frame,
            from_=1,
            to=100,
            textvariable=self.columns
        )
        columns_box.grid(row=0, column=3, sticky="nesw", padx=(0, 5))

        text_alignment_label = ttk.Label(
            frame,
            text="Cell text alignment: ",
            padding=(5, 0)
        )
        text_alignment_label.grid(row=1, column=0, sticky="ns")

        text_alignment_entry = ttk.Combobox(
            frame,
            textvariable=self.text_alignment,
            state="readonly"
        )
        text_alignment_entry.grid(row=1, column=1, sticky="nesw")
        text_alignment_entry.config(values=("l", "c", "r", "p"))

        table_alignment_label = ttk.Label(
            frame,
            text="Cell text alignment: ",
            padding=(5, 0)
        )
        table_alignment_label.grid(row=1, column=2, sticky="ns")

        table_alignment_entry = ttk.Combobox(
            frame,
            textvariable=self.table_alignment,
            state="readonly"
        )
        table_alignment_entry.grid(row=1, column=3, sticky="nesw", padx=(0, 5))
        table_alignment_entry.config(values=("\\centering", "None"))

        confirm_button = ttk.Button(
            frame,
            text="Confirm",
            command=self.populate_delimiter
        )
        confirm_button.grid(row=2, column=0, columnspan=4, sticky="ns", pady=5)

        delimiter_label = ttk.Label(
            frame,
            text="Delimiters: \n(enter | for column placement)",
            justify="center",
            padding=(5, 0)
        )
        delimiter_label.grid(row=3, column=0, sticky="ns")

        self.delimiter_entry = tk.Entry(
            frame,
            textvariable=self.cells,
            state="readonly"
        )
        self.delimiter_entry.grid(row=3, column=1, pady=5, sticky="ew")

        position_label = ttk.Label(
            frame,
            text="Position on page: ",
            justify="center",
            padding=(5, 0)
        )
        position_label.grid(row=3, column=2, sticky="ns")

        position_entry = ttk.Combobox(
            frame,
            textvariable=self.position,
            state="readonly"
        )
        position_entry.grid(row=3, column=3, sticky="ew", padx=(0, 5))
        position_entry.config(values=("Here", "Top of Page", "Bottom of Page", "Special Page"))

        caption_checkbox = ttk.Checkbutton(
            frame,
            text="         Caption\nAbove/Below Table: ",
            variable=self.caption_check,
            onvalue=1,
            offvalue=0,
            padding=(5, 0),
        )
        caption_checkbox.grid(row=4, column=0, sticky="ns")

        caption_position = ttk.Combobox(
            frame,
            textvariable=self.caption_position,
            state="readonly"
        )
        caption_position.config(values=("Above", "Below"))
        caption_position.grid(row=4, column=1, sticky="es")

        label_label = ttk.Label(
            frame,
            text="Label: ",
            padding=(5, 0)
        )
        label_label.grid(row=4, column=2, sticky="ns")

        label_entry = ttk.Entry(
            frame,
            textvariable=self.entered_label,
        )
        label_entry.grid(row=4, column=3, sticky="ew", padx=(0, 5))

        # Create label for suggested packages
        packages_label = tk.Label(
            self,
            text="Suggested packages: wrapfig, array, tabularx, multirow, longtable, table{xcolor}",
            justify="center"
        )
        packages_label.grid(row=2, column=0, columnspan=2, sticky="ns", pady=5)

        # Create create and close buttons
        self.create_button = ttk.Button(
            self,
            text="Create",
            command=self.create,
            state="disabled"
        )
        self.create_button.grid(row=3, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=1, sticky="ns")

    def populate_delimiter(self):
        """Sets cells attributes based on field values entered by user. Enables delimiter entry and create buttons."""
        self.cells.set(self.text_alignment.get() * self.columns.get())
        self.delimiter_entry.config(state="normal")
        self.create_button.config(state="normal")

    def create(self):
        """Inserts LaTeX commands for creating table in currently visible scrolled text box.

        Checks values have been entered. Calls check_current_editor() method from controller and assigns return to
        current editor. This returns the scrolled text box widget in the currently selected tab in the currently visible
        tex editor frame. Formats code to be inserted and inserts at current cursor position.
        """
        if self.cells.get():
            current_editor = self.controller.check_current_editor()
            insert = ""
            # Format code for position parameter based on users entry
            position = self.position.get()
            if position == "Here":
                position = "h"
            elif position == "Top of Page":
                position = "t"
            elif position == "Bottom of Page":
                position = "b"
            elif position == "Special Page":
                position = "p"

            # Create code with or without position parameter
            if position:
                insert = f"\\begin{{table}}[{position}]\n"
            else:
                insert = "\\begin{table}\n"

            # Add code for table alignment if entered
            if self.table_alignment.get() and self.table_alignment.get() != "None":
                insert += f"{self.table_alignment.get()}\n"

            # Add code for caption if entered and positioned above figure
            if self.caption_check.get() and self.caption_position.get() == "Above":
                insert += "\\caption{Type caption here}\n"

            # Add code for number of rows and cells entered
            insert += f"\\begin{{tabular}}{{{self.cells.get()}}}\n  \\hline\n"
            insert += (self.rows.get() + 1) * \
                      (("  Cell" + ((self.columns.get() - 1) * " & Cell")) + " \\\\\n  \\hline\n")
            insert += "\\end{tabular}\n"

            # Add code for caption if entered and positioned below figure
            if self.caption_check.get() and self.caption_position.get() == "Below":
                insert += "\\caption{Type caption here}\n"

            # Add code for label if entered
            if self.entered_label.get():
                insert += f"\\label{{{self.entered_label.get()}}}\n"

            # Add command to close table environment
            insert += "\\end{table}\n"

            # Insert code at current cursor position
            current_editor.insert(tk.INSERT, insert)

    def close(self):
        """Destroys Table toplevel window."""
        self.destroy()
