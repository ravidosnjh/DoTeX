"""Define BibEntry class.

Classes
-------
BibEntry
    Configures BibEntry toplevel window.
"""
import tkinter as tk
from tkinter import ttk


class BibEntry(tk.Toplevel):
    """A class configuring Math frame; also creates Brackets and OperatorsMenu menus.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    entry_type : str
        stringvar containing entry type entered by user
    reference : str
        stringvar containing reference entered by user
    author : str
        stringvar containing author entered by user
    title : str
        stringvar containing title entered by user
    year : str
        stringvar containing year entered by user
    journal : str
        stringvar containing journal entered by user
    pages : str
        stringvar containing pages entered by user
    publisher : str
        stringvar containing publisher entered by user

    Methods
    -------
    create()
        Inserts LaTeX code for bib entry in currently visible scrolled text box
    close()
        Destroys BibEntry toplevel window
    """

    def __init__(self, controller):
        """Initialises BibEntry toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            BibEntry object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title, and make window not resizable
        self.title("Create a Bibliogarphy Entry")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create StringVars to store values entered by user and set default value
        self.entry_type = tk.StringVar(value="")
        self.reference = tk.StringVar(value="")
        self.author = tk.StringVar(value="")
        self.title = tk.StringVar(value="")
        self.year = tk.StringVar(value="")
        self.journal = tk.StringVar(value="")
        self.pages = tk.StringVar(value="")
        self.publisher = tk.StringVar(value="")

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Reference inserts at cursor position")
        label.grid(row=0, column=0, columnspan=2, sticky="ns")

        # Create frame to contain field entry widgets
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

        # Create labels and entry boxes for configurable parameters
        entry_type_label = ttk.Label(
            frame,
            text="Entry type: ",
            padding=(5, 0)
        )
        entry_type_label.grid(row=0, column=0, sticky="ns")

        entry_type_entry = ttk.Combobox(
            frame,
            textvariable=self.entry_type
        )
        entry_type_entry.grid(row=0, column=1, sticky="nesw", padx=(0, 5))
        # Add common entry types to combobox
        entry_type_entry.config(values=("@article", "@inproceedings", "@book", "@phdthesis", "@masterthesis", "@inbook",
                                       "@incollection", "@misc"))

        reference_label = ttk.Label(
            frame,
            text="Reference Label: ",
            padding=(5, 0)
        )
        reference_label.grid(row=1, column=0, sticky="ns", pady=5)

        reference_entry = ttk.Entry(
            frame,
            textvariable=self.reference,
            width=20
        )
        reference_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5))

        author_label = ttk.Label(
            frame,
            text="Author: ",
            padding=(5, 0)
        )
        author_label.grid(row=2, column=0, sticky="ns", pady=5)

        author_entry = ttk.Entry(
            frame,
            textvariable=self.author,
            width=20
        )
        author_entry.grid(row=2, column=1, sticky="ew", padx=(0, 5))

        title_label = ttk.Label(
            frame,
            text="Title: ",
            padding=(5, 0)
        )
        title_label.grid(row=3, column=0, sticky="ns", pady=5)

        title_entry = ttk.Entry(
            frame,
            textvariable=self.title,
            width=20
        )
        title_entry.grid(row=3, column=1, sticky="ew", padx=(0, 5))

        year_label = ttk.Label(
            frame,
            text="Year: ",
            padding=(5, 0)
        )
        year_label.grid(row=4, column=0, sticky="ns", pady=5)

        year_entry = ttk.Entry(
            frame,
            textvariable=self.year,
            width=20
        )
        year_entry.grid(row=4, column=1, sticky="ew", padx=(0, 5))

        journal_label = ttk.Label(
            frame,
            text="Journal: ",
            padding=(5, 0)
        )
        journal_label.grid(row=5, column=0, sticky="ns", pady=5)

        journal_entry = ttk.Entry(
            frame,
            textvariable=self.journal,
            width=20
        )
        journal_entry.grid(row=5, column=1, sticky="ew", padx=(0, 5))

        publisher_label = ttk.Label(
            frame,
            text="Publisher: ",
            padding=(5, 0)
        )
        publisher_label.grid(row=6, column=0, sticky="ns", pady=5)

        publisher_entry = ttk.Entry(
            frame,
            textvariable=self.publisher,
            width=20
        )
        publisher_entry.grid(row=6, column=1, sticky="ew", padx=(0, 5))

        pages_label = ttk.Label(
            frame,
            text="Pages: ",
            padding=(5, 0)
        )
        pages_label.grid(row=7, column=0, sticky="ns", pady=5)

        pages_entry = ttk.Entry(
            frame,
            textvariable=self.pages,
            width=20
        )
        pages_entry.grid(row=7, column=1, sticky="ew", padx=(0, 5))

        # Create create and close buttons
        create_button = ttk.Button(
            self,
            text="Create",
            command=self.create,
        )
        create_button.grid(row=2, column=0, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=2, column=1, sticky="ns")

    def create(self):
        """Inserts LaTeX code for bib entry in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Formats and
        inserts code for bib entry with parameters entered by user current cursor position
        """
        current_editor = self.controller.check_current_editor()
        # Create code with entered author, title and year
        insert = f"{self.entry_type.get()}{{{self.reference.get()},\n" \
                 f"  author = {{{self.author.get()}}},\n" \
                 f"  title = {{{self.title.get()}}},\n" \
                 f"  year = {{{self.year.get()}}}\n"

        # Add code for journal if entered
        if self.journal.get():
            insert += f"  journal = {{{self.journal.get()}}}, \n"

        # Add code for publisher if entered
        if self.publisher.get():
            insert += f"  publisher = {{{self.publisher.get()}}}, \n"

        # Add code for pages if entered
        if self.pages.get():
            insert += f"  pages = {{{self.pages.get()}}}, \n"

        # Add closing brace
        insert += "}"

        # Insert code at current cursor position
        current_editor.insert(tk.INSERT, insert)

    def close(self):
        """Destroy BibEntry toplevel window"""
        self.destroy()
