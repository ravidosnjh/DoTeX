"""Define Insert class.

Classes
-------
Insert
    Configures Insert frame.
"""
import tkinter as tk
from tkinter import ttk
from .toolbar_inner_frames import GreekLetters, Symbols, ReservedChars, List, Images, Table, Commands
from files import constants as cons


class Insert(ttk.Frame):
    """A class configuring Insert frame; also creates Commands menu.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    pictures_dir : str
        a reference to pictures directory from files/constants.py
    reserved_chars : ttk.tk.PhotoImage(file)
        a ReservedChars toplevel window
    greek_letters : tk.PhotoImage(file)
        a GreekLetters toplevel window
    symbols : tk.PhotoImage(file)
        a Symbols toplevel window
    list : tk.PhotoImage(file)
        a List toplevel window
    table : tk.PhotoImage(file)
        a Table toplevel window
    image : tk.PhotoImage(file)
        an Images toplevel window

    Methods
    -------
    bold()
        Inserts LaTeX command for bold format in currently visible scrolled text box
    italic()
        Inserts LaTeX command for italic format in currently visible scrolled text box
    underline()
        Inserts LaTeX command for underline format in currently visible scrolled text box
    justify(align)
        Inserts value of align in currently visible scrolled text box
    command(cmd)
        Inserts value of command in currently visible scrolled text box
    find_replace()
        Creates FindButtons frame in current visible_tex_frame
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises Math frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates toolbar buttons and Commands menu.

        Parameters
        ----------
        self
            Insert object
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
        # Set images directory to constant set in files/constants.py
        self.pictures_dir = cons.PICTURES_PATH

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create toolbar buttons
        images_button = ttk.Button(
            self,
            text="Use graphicx Package",
            command=self.insert_images
        )

        self.reserved_chars = None

        reserved_chars_keyboard = ttk.Button(
            self,
            text="Reserved Chars",
            command=self.launch_reserved_chars_keyboard
        )

        self.greek_letters = None

        greek_letter_keyboard = ttk.Button(
            self,
            text="Greek Letters",
            command=self.launch_greek_letter_keyboard
        )

        self.symbols = None

        symbols_keyboard = ttk.Button(
            self,
            text="Symbols",
            command=self.launch_symbols_keyboard
        )

        self.list = None

        list_button = ttk.Button(
            self,
            text="List",
            command=self.launch_list
        )

        self.table = None

        table_button = ttk.Button(
            self,
            text="Table",
            command=self.launch_table
        )

        self.image = None

        image_button = ttk.Button(
            self,
            text="Image",
            command=self.launch_image
        )

        cite = ttk.Button(
            self,
            text="Cite",
            command=self.insert_cite
        )

        label = ttk.Button(
            self,
            text="Label",
            command=self.insert_label
        )

        ref = ttk.Button(
            self,
            text="Ref",
            command=self.insert_ref
        )

        commands = ttk.Menubutton(
            self,
            text="All Commands"
        )
        # Create Commands menu and associate with commands menubutton
        commands_menu = Commands(commands, self.controller, tearoff=False)
        commands.config(menu=commands_menu)

        # Grid widgets in Insert
        count = 0
        for widget in self.winfo_children():
            widget.grid(row=0, column=count, sticky="nesw")
            count += 1

    def insert_images(self):
        """Inserts LaTeX command for graphicx package in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for graphicx package at second line of text box.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert("2.0", f"\n\\usepackage{{graphicx}}\n\\graphicspath{{ {{./{self.pictures_dir}/}} }}\n")

    def launch_reserved_chars_keyboard(self):
        """If reserved_chars exists destroys it. Creates ReservedChars toplevel window named reserved_chars."""
        if self.reserved_chars:
            self.reserved_chars.close()
        self.reserved_chars = ReservedChars(self.controller)

    def launch_greek_letter_keyboard(self):
        """If greek_letter exists destroys it. Creates GreekLetters toplevel window named greek_letter."""
        if self.greek_letters:
            self.greek_letters.close()
        self.greek_letters = GreekLetters(self.controller)

    def launch_symbols_keyboard(self):
        """If symbols exists destroys it. Creates Symbols toplevel window named symbols."""
        if self.symbols:
            self.symbols.close()
        self.symbols = Symbols(self.controller)

    def launch_list(self):
        """If list exists destroys it. Creates List toplevel window named list."""
        if self.list:
            self.list.close()
        self.list = List(self.controller)

    def launch_table(self):
        """If table exists destroys it. Creates Table toplevel window named table."""
        if self.table:
            self.table.close()
        self.table = Table(self.controller)

    def launch_image(self):
        """If image exists destroys it. Creates Images toplevel window named image."""
        if self.image:
            self.image.close()
        self.image = Images(self.controller)

    def insert_cite(self):
        """Inserts LaTeX command for cite in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for cite at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\cite{}")

    def insert_label(self):
        """Inserts LaTeX command for label in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for label at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\label{}")

    def insert_ref(self):
        """Inserts LaTeX command for reference in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for reference at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\ref{}")
