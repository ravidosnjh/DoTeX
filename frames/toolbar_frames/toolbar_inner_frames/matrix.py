"""Define Matrix class.

Classes
-------
Matrix
    Configures Matrix toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class Matrix(tk.Toplevel):
    """A class configuring Table toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    bracket : str
        stringvar containing bracket entered by user
    rows : int
        intvar containing number of rows entered by user
    columns : int
        intvar containing number of columns entered by user
    mode : str
        stringvar containing mode entered by user
    create_button = ttk.Button()
        button inserting LaTeX code into currently visible tex editor

    Methods
    -------
    create()
        Inserts LaTeX commands for creating matrix in currently visible scrolled text box
    close()
        Destroys Matrix toplevel window
    """

    def __init__(self, controller):
        """Initialises Table toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Matrix object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Insert a Matrix")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create IntVars and StringVars to store values entered by user and set default values
        self.bracket = tk.StringVar(value="")
        self.rows = tk.IntVar(value=0)
        self.columns = tk.IntVar(value=0)
        self.mode = tk.StringVar(value="")

        # Make row 1 and columns 0 and 1 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Matrices insert at cursor position\nReplace 'cell' with data")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain brackets user can choose
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        # Create radio buttons
        brackets = ttk.Label(
            frame,
            text="Brackets:",
            justify="center"
        )
        brackets.grid(row=0, column=0, columnspan=9, sticky="ns")

        button = ttk.Radiobutton(
            frame,
            text="None",
            variable=self.bracket,
            value="none"
        )
        button.grid(row=1, column=0, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="( )",
            variable=self.bracket,
            value="round"
        )
        button.grid(row=1, column=1, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="[ ]",
            variable=self.bracket,
            value="square"
        )
        button.grid(row=1, column=2, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="{ }",
            variable=self.bracket,
            value="curly"
        )
        button.grid(row=1, column=3, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="< >",
            variable=self.bracket,
            value="angle"
        )
        button.grid(row=1, column=4, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="| |",
            variable=self.bracket,
            value="straight"
        )
        button.grid(row=1, column=5, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="|| ||",
            variable=self.bracket,
            value="dbl straight"
        )
        button.grid(row=1, column=6, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="⌈ ⌉",
            variable=self.bracket,
            value="ceiling"
        )
        button.grid(row=1, column=7, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame,
            text="⌊ ⌋",
            variable=self.bracket,
            value="floor"
        )
        button.grid(row=1, column=8, sticky="ns", padx=5)

        # Create frame to contain matrix parameters user can configure
        frame2 = ttk.Frame(frame)
        frame2.grid(row=2, column=0, columnspan=9, sticky="nesw", pady=(10, 0))

        # Create labels and entry boxes
        rows_label = ttk.Label(
            frame2,
            text="Rows: ",
            padding=(5, 0)
        )
        rows_label.grid(row=0, column=0, sticky="ns", pady=5)

        rows_box = ttk.Spinbox(
            frame2,
            from_=1,
            to=100,
            textvariable=self.rows
        )
        rows_box.grid(row=0, column=1, sticky="nesw")

        columns_label = ttk.Label(
            frame2,
            text="Columns: ",
            padding=(5, 0)
        )
        columns_label.grid(row=0, column=2, sticky="ns")

        columns_box = ttk.Spinbox(
            frame2,
            from_=1,
            to=100,
            textvariable=self.columns
        )
        columns_box.grid(row=0, column=3, sticky="nesw", padx=(0, 5))

        # Create frame to contain matrix size user can choose
        frame3 = ttk.Frame(frame)
        frame3.grid(row=3, column=0, columnspan=9, sticky="nesw")
        frame3.columnconfigure(0, weight=1)
        frame3.columnconfigure(1, weight=1)

        # Create radio buttons
        button = ttk.Radiobutton(
            frame3,
            text="Normal",
            variable=self.mode,
            value="normal"
        )
        button.grid(row=1, column=0, sticky="ns", padx=5)

        button = ttk.Radiobutton(
            frame3,
            text="Small",
            variable=self.mode,
            value="small"
        )
        button.grid(row=1, column=1, sticky="ns", padx=5)

        # Create label for suggested packages
        packages_label = tk.Label(
            self,
            text="amsmath package required",
            justify="center"
        )
        packages_label.grid(row=2, column=0, columnspan=2, sticky="ns", pady=5)

        # Create create and close buttons
        self.create_button = ttk.Button(
            self,
            text="Create",
            command=self.create
        )
        self.create_button.grid(row=3, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=3, column=1, sticky="ns")

    def create(self):
        """Inserts LaTeX commands for creating matrix in currently visible scrolled text box

        Checks values have been entered. Calls check_current_editor() method from controller and assigns return to
        current editor. This returns the scrolled text box widget in the currently selected tab in the currently visible
        tex editor frame. Formats code to be inserted and inserts at current cursor position
        """
        current_editor = self.controller.check_current_editor()
        insert = ""
        # Format code for bracket and matrix size based on options selected by user
        if self.mode.get() == "small":
            if self.bracket.get() == "round":
                bracket = "\\big("
                end_bracket = "\\big)"
            elif self.bracket.get() == "square":
                bracket = "\\big["
                end_bracket = "\\big]"
            elif self.bracket.get() == "curly":
                bracket = "\\big{"
                end_bracket = "\\big}"
            elif self.bracket.get() == "straight":
                bracket = "\\big|"
                end_bracket = "\\big|"
            elif self.bracket.get() == "dbl straight":
                bracket = "\\big\\|"
                end_bracket = "\\big\\|"
            elif self.bracket.get() == "angle":
                bracket = "\\big \\langle"
                end_bracket = "\\big \\rangle"
            elif self.bracket.get() == "ceiling":
                bracket = "\\big \\lceil"
                end_bracket = "\\big \\rceil"
            elif self.bracket.get() == "floor":
                bracket = "\\big \\lfloor"
                end_bracket = "\\big \\rfloor"
            else:
                bracket = ""
                end_bracket = ""
        else:
            if self.bracket.get() == "round":
                bracket = "pmatrix"
                end_bracket = "pmatrix"
            elif self.bracket.get() == "square":
                bracket = "bmatrix"
                end_bracket = "bmatrix"
            elif self.bracket.get() == "curly":
                bracket = "Bmatrix"
                end_bracket = "Bmatrix"
            elif self.bracket.get() == "straight":
                bracket = "vmatrix"
                end_bracket = "vmatrix"
            elif self.bracket.get() == "dbl straight":
                bracket = "Vmatrix"
                end_bracket = "Vmatrix"
            elif self.bracket.get() == "angle":
                bracket = "\\left \\langle"
                end_bracket = "\\right \\rangle"
            elif self.bracket.get() == "ceiling":
                bracket = "\\left \\lceil"
                end_bracket = "\\right \\rceil"
            elif self.bracket.get() == "floor":
                bracket = "\\left \\lfloor"
                end_bracket = "\\right \\rfloor"
            else:
                bracket = "matrix"
                end_bracket = "matrix"

        # Create code for small or normal matrix with selected brackets
        if self.mode.get() == "small":
            insert += f"{bracket}\\begin{{smallmatrix}}\n"
        else:
            insert += f"\\begin{{{bracket}}}\n"

        # Add code for number of rows and columns entered
        insert += (self.rows.get() - 1) * ("  Cell" + ((self.columns.get() - 1) * " & Cell") + " \\\\\n")
        insert += ("  Cell" + ((self.columns.get() - 1) * " & Cell") + "\n")

        # Add correct command for closing environment
        if self.mode.get() == "small":
            insert += f"\\end{{smallmatrix}}{end_bracket}"
        else:
            insert += f"\\end{{{end_bracket}}}"

        # Insert code at current cursor position
        current_editor.insert(tk.INSERT, insert)

    def close(self):
        """Destroys Matrix toplevel window"""
        self.destroy()
