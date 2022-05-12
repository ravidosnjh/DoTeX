"""Define Format class.

Classes
-------
Format
    Configures Format frame.
"""
import tkinter as tk
from tkinter import ttk
from .toolbar_inner_frames import Documentclass, Packages, Title, Environments, Bib, BibEntry
from functools import partial


class Format(ttk.Frame):
    """A class configuring Format frame; also creates Environments menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    documentclass : Documentclass()
        a Documentclass toplevel window
    packages : Packages()
        a Packages toplevel window
    title : Title()
        a Title toplevel window
    bib : Bib()
        a Bib toplevel window
    bib_entry : BibEntry()
        a BibEntry toplevel window

    Methods
    -------
    insert_documentclass()
        Create Documentclass toplevel window
    insert_package()
        Create Packages toplevel window
    insert_title()
        Create Title toplevel window
    insert_document()
        Inserts LaTeX commands for document environment in currently visible scrolled text box
    insert_abstract()
        Inserts LaTeX commands for abstract environment in currently visible scrolled text box
    insert_chapter()
        Inserts LaTeX command for chapter in currently visible scrolled text box
    create_section(numbered)
        Inserts LaTeX command for numbered or unnumbered section in currently visible scrolled text box
    create_subsection(numbered)
        Inserts LaTeX command for numbered or unnumbered subsection in currently visible scrolled text box
    insert_toc()
        Inserts LaTeX command for table of contents in currently visible scrolled text box
    launch_bib()
        Creates Bib toplevel window
    launch_bib_entry()
        Create BibEntry toplevel window
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises Format frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates toolbar buttons and Environments menu.

        Parameters
        ----------
        self
            Format object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        self.documentclass = None

        # Create toolbar buttons and menus
        self.documentclass_button = ttk.Button(
            self,
            text="Set Documentclass",
            command=self.insert_documentclass
        )

        self.packages = None

        self.packages_button = ttk.Button(
            self,
            text="Use Package",
            command=self.insert_package
        )

        self.title = None

        self.title_button = ttk.Button(
            self,
            text="Create Title",
            command=self.insert_title
        )

        document_button = ttk.Button(
            self,
            text="Create Document",
            command=self.insert_document
        )

        abstract_button = ttk.Button(
            self,
            text="Create Abstract",
            command=self.insert_abstract
        )

        chapter_button = ttk.Button(
            self,
            text="Create Chapter",
            command=self.insert_chapter
        )

        section_button = ttk.Menubutton(
            self,
            text="Create Section"
        )
        # Create section menu and associate with section menubutton
        section_button_menu = tk.Menu(section_button, tearoff=False)
        section_button.config(menu=section_button_menu)
        # Add commands to section menu
        numbered_p = partial(self.create_section, True)
        section_button_menu.add_command(
            label="Numbered Section",
            command=numbered_p
        )
        unnumbered_p = partial(self.create_section, False)
        section_button_menu.add_command(
            label="Unnumbered Section",
            command=unnumbered_p
        )

        subsection_button = ttk.Menubutton(
            self,
            text="Create Subsection"
        )
        # Create subsection menu and associate with subsection menubutton
        subsection_button_menu = tk.Menu(subsection_button, tearoff=False)
        subsection_button.config(menu=subsection_button_menu)
        # Add commands to subsection menu
        numbered_s_p = partial(self.create_subsection, True)
        subsection_button_menu.add_command(
            label="Numbered Subsection",
            command=numbered_s_p
        )
        unnumbered_s_p = partial(self.create_subsection, False)
        subsection_button_menu.add_command(
            label="Unnumbered Subsection",
            command=unnumbered_s_p
        )

        toc_button = ttk.Button(
            self,
            text="Create Table of Contents",
            command=self.insert_toc
        )

        self.bib = None

        bibliography = ttk.Button(
            self,
            text="Insert Bibliography",
            command=self.launch_bib
        )

        self.bib_entry = None

        bibliography_entry = ttk.Button(
            self,
            text="Create Bib Entry",
            command=self.launch_bib_entry
        )

        environments = ttk.Menubutton(
            self,
            text="All Environments"
        )
        # Create Environments menu as environments_menu and associate with environments menubutton
        environments_menu = Environments(environments, self.controller, tearoff=False)
        environments.config(menu=environments_menu)

        # Grid widgets in Format
        count = 0
        for widget in self.winfo_children():
            widget.grid(row=0, column=count, sticky="nesw")
            count += 1

    def insert_documentclass(self):
        """If documentclass exists destroys it. Creates Documentclass toplevel window named documentclass."""
        if self.documentclass:
            self.documentclass.close()
        self.documentclass = Documentclass(self.controller)

    def insert_package(self):
        """If packages exists destroys it. Creates Packages toplevel window named packages."""
        if self.packages:
            self.packages.close()
        self.packages = Packages(self.controller)

    def insert_title(self):
        """If title exists destroys it. Creates Title toplevel window named title."""
        if self.title:
            self.title.close()
        self.title = Title(self.controller)

    def insert_document(self):
        """Inserts LaTeX commands for document environment in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for document environment at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{document}\n\n\n\n\\end{document}\n")

    def insert_abstract(self):
        """Inserts LaTeX commands for abstract environment in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for abstract environment at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{abstract}\n\n\\end{abstract}\n")

    def insert_chapter(self):
        """Inserts LaTeX command for chapter in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for chapter at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\chapter{}\n")

    def create_section(self, numbered):
        """Inserts LaTeX command for numbered or unnumbered section in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If numbered
        = True inserts LaTeX code for numbered section at current cursor position. Else inserts code for unnumbered
        section. Value of numbered determined by which menu command selected.

        Parameters
        ----------
        numbered : bool
            value determining if numbered or unnumbered section selected
        """
        current_editor = self.controller.check_current_editor()
        if numbered:
            insert = "\\section{}\n"
        else:
            insert = "\\section*{}\n"
        current_editor.insert(tk.INSERT, insert)

    def create_subsection(self, numbered):
        """Inserts LaTeX command for numbered or unnumbered subsection in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If numbered
        = True inserts LaTeX code for numbered subsection at current cursor position. Else inserts code for unnumbered
        subsection. Value of numbered determined by which menu command selected.

        Parameters
        ----------
        numbered : bool
            value determining if numbered or unnumbered subsection selected
        """
        current_editor = self.controller.check_current_editor()
        if numbered:
            insert = "\\subsection{}\n"
        else:
            insert = "\\subsection*{}\n"
        current_editor.insert(tk.INSERT, insert)

    def insert_toc(self):
        """Inserts LaTeX command for table of contents in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for table of contents at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\tableofcontents\n")

    def launch_bib(self):
        """If bib exists destroys it. Creates Bib toplevel window named bib."""
        if self.bib:
            self.bib.close()
        self.bib = Bib(self.controller)

    def launch_bib_entry(self):
        """If bib_entry exists destroys it. Creates BibEntry toplevel window named bib_entry."""
        if self.bib_entry:
            self.bib_entry.close()
        self.bib_entry = BibEntry(self.controller)
