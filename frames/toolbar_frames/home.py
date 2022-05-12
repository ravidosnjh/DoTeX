"""Define Home class.

Classes
-------
Home
    Configures Home frame.
"""
import tkinter as tk
from tkinter import ttk
from functools import partial


class Home(ttk.Frame):
    """A class configuring Home frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    main_window_controller : widget object
        a reference to main_window_controller attribute of master widget to provide access to its attributes/methods
    l_align : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    c_align : ttk.tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    r_align : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected

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

    def __init__(self, container, controller, main_window_controller, **kwargs):
        """Initialises Home frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates image objects and toolbar buttons.

        Parameters
        ----------
        self
            Home object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        main_window_controller : widget object
            A reference to main_window_frame frame from master widget to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create references to Toolbar object and DoTeX.main_window to provide access to their attributes/methods
        self.controller = controller
        self.main_window_controller = main_window_controller

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create references to images, so they aren't garbage collected. To be used as icons on buttons
        self.l_align = tk.PhotoImage(file=r"assets/left_align.png")
        self.c_align = tk.PhotoImage(file=r"assets/centre_align.png")
        self.r_align = tk.PhotoImage(file=r"assets/right_align.png")

        # Create toolbar buttons
        bold_button = ttk.Button(
            self,
            text="B",
            style="Bold.TButton",
            command=self.bold
        )

        italic_button = ttk.Button(
            self,
            text="I",
            style="Italic.TButton",
            command=self.italic
        )

        underline_button = ttk.Button(
            self,
            text="U",
            style="Underline.TButton",
            command=self.underline
        )

        # Create partials to pass corresponding LaTeX commands to self.justify(align) when button is pressed
        left_p = partial(self.justify, "flushleft")
        left_button = ttk.Button(
            self,
            image=self.l_align,
            command=left_p,
            padding=(0, 0)
        )

        centre_p = partial(self.justify, "center")
        centre_button = ttk.Button(
            self,
            image=self.c_align,
            command=centre_p,
            padding=(0, 0)
        )

        right_p = partial(self.justify, "flushright")
        right_button = ttk.Button(
            self,
            image=self.r_align,
            command=right_p,
            padding=(0, 0)
        )

        # Create partials to pass corresponding LaTeX events to self.command(cmd) when button is pressed
        undo_p = partial(self.command, "<<Undo>>")
        undo_button = ttk.Button(
            self,
            text="Undo",
            command=undo_p,
            padding=(-5, 0)
        )

        redo_p = partial(self.command, "<<Redo>>")
        redo_button = ttk.Button(
            self,
            text="Redo",
            command=redo_p,
            padding=(-5, 0)
        )

        cut_p = partial(self.command, "<<Cut>>")
        cut_button = ttk.Button(
            self,
            text="Cut",
            command=cut_p,
            padding=(-5, 0)
        )

        copy_p = partial(self.command, "<<Copy>>")
        copy_button = ttk.Button(
            self,
            text="Copy",
            command=copy_p,
            padding=(-5, 0)
        )

        paste_p = partial(self.command, "<<Paste>>")
        paste_button = ttk.Button(
            self,
            text="Paste",
            command=paste_p,
            padding=(-5, 0)
        )

        find_replace_button = ttk.Button(
            self,
            text="Find/Replace",
            command=self.find_replace,
        )

        count = 0
        for widget in self.winfo_children():
            widget.grid(row=0, column=count, sticky="nesw")
            count += 1

    def bold(self):
        """Inserts LaTeX command for bold format in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If the "sel"
        tag exists in the widget, inserts LaTeX code for bold formatting around the selected text. Else inserts it at
        the current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        if current_editor.tag_ranges("sel"):
            current_editor.insert(tk.SEL_FIRST, "\\textbf{")
            current_editor.insert(tk.SEL_LAST, "}")
        else:
            current_editor.insert(tk.INSERT, "\\textbf{}")

    def italic(self):
        """Inserts LaTeX command for bold format in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If the "sel"
        tag exists in the widget, inserts LaTeX code for italic formatting around the selected text. Else inserts it at
        the current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        if current_editor.tag_ranges("sel"):
            current_editor.insert(tk.SEL_FIRST, "\\textit{")
            current_editor.insert(tk.SEL_LAST, "}")
        else:
            current_editor.insert(tk.INSERT, "\\textit{}")

    def underline(self):
        """Inserts LaTeX command for bold format in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If the "sel"
        tag exists in the widget, inserts LaTeX code for underline formatting around the selected text. Else inserts it
        at the current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        if current_editor.tag_ranges("sel"):
            current_editor.insert(tk.SEL_FIRST, "\\textunderline{")
            current_editor.insert(tk.SEL_LAST, "}")
        else:
            current_editor.insert(tk.INSERT, "\\textunderline{}")

    def justify(self, align):
        """Inserts value of align in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts the
        value of align, determined by which button is pressed, at current cursor position.

        Parameters
        ----------
        align : str
            LaTeX command to insert
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, f"\\begin{{{align}}}\n\n\\end{{{align}}}")

    def command(self, cmd):
        """Inserts value of align in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Generates
        event determined by value of cmd which is determined by which button is pressed.

        Parameters
        ----------
        cmd : str
            LaTeX event to generate
        """
        current_editor = self.controller.check_current_editor()
        current_editor.event_generate(f"{cmd}")

    def find_replace(self):
        """Creates FindButtons frame in current visible_tex_frame

        Calls create_find_frame() method from visible_tex_frame form tex_editor_frame from main_window_controller.
        This creates a FindButtons frame in the currently visible tex frame.
        """
        self.main_window_controller.tex_editor_frame.visible_tex_frame.create_find_frame()
