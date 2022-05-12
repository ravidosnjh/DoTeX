"""Define TexEditorFrame class.

Classes
-------
TexEditorFrame
    Configures TexEditorFrame frame.
"""
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolled_text
from .tex_editor_inner_frames import BibButtonsFrame, FindButtons


class TexEditorFrame(ttk.Frame):
    """A class configuring TexEditorFrame frame; also creates BibButtonsFrame frame

    Attributes
    ----------
    tex_file : str
        tex file path
    tex_file_name : str
        stringvar containing loaded tex file name
    bib_file : str
        bib file path
    tex_editor_find_frame : FindButtons()
        frame containing find replace controls
    bib_editor_find_frame : FindButtons()
        frame containing find replace controls
    right_clicked : ScrolledText()
        indicates which editor was right clicked
    tex_notebook : ttk.Notebook()
        notebook to contain tex and bib scrolled text boxes
    tex_editor : ScrolledText()
        scrolled text box for editing tex files
    bib_frame : ttk.Frame()
        frame to contain bib editor and bib buttons
    bib_editor : ScrolledText()()
        scrolled text box for editing bib files
    bib_buttons : BibButtonsFrame()
        frame to contain bib tool buttons
    context_menu : tk.Menu()
        menu to appear when user right clicks

    Methods
    -------
    popup(event, editor)
        Creates context menu at cursor position when user right clicks
    cut()
        Cuts selected text
    copy()
        Copies selected text
    paste()
        Pastes clipboard text
    create_find_frame(event)
        Creates FindButtons frame
    close_find_frame(event)
        Closes FindButtons frame
    check_bib_saved()
        Returns True if bib file is saved
    check_bib_empty()
        Returns True if bib editor is empty
    """

    def __init__(self, container, **kwargs):
        """Initialises TexEditorFrame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            TexEditorFrame object
        container : widget object
            Master widget
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create variables to store tex file path and name
        self.tex_file = ""
        self.tex_file_name = tk.StringVar(value="Blank")

        # Create variable to store bib file path
        self.bib_file = ""

        # Create variables to be assigned to tex editor and bib editor FindButtons frames
        self.tex_editor_find_frame = None
        self.bib_editor_find_frame = None

        # Create variable to store which editor was right clicked
        self.right_clicked = None

        # Create notebook to store tex and bib editors
        self.tex_notebook = ttk.Notebook(self)
        self.tex_notebook.enable_traversal()
        self.tex_notebook.pack(side="left", fill="both", expand=True)

        # Create scrolled text named tex_editor and set focus
        self.tex_editor = scrolled_text.ScrolledText(self.tex_notebook, width=110, undo=True)
        self.tex_editor.focus_set()

        # Create bib frame to store bib editor and bib tool buttons
        self.bib_frame = ttk.Frame(self.tex_notebook)
        self.bib_frame.pack(side="left", fill="both", expand=True)
        # Make bib frame row 0 and column 0 fill all available space
        self.bib_frame.rowconfigure(0, weight=1)
        self.bib_frame.columnconfigure(0, weight=1)

        # Add tex editor and bib frame to notebook
        self.tex_notebook.add(self.tex_editor, text="TeX")
        self.tex_notebook.add(self.bib_frame, text="Bib")

        # Create scrolled text named bib_editor
        self.bib_editor = scrolled_text.ScrolledText(self.bib_frame, undo=True)
        self.bib_editor.grid(row=0, column=0, sticky="nesw")

        # Create BibButtonsFrame named bib_buttons containg tool buttons
        self.bib_buttons = BibButtonsFrame(self.bib_frame, self)
        self.bib_buttons.grid(row=1, column=0, sticky="ns")

        # Create right click context menu and add commands
        self.context_menu = tk.Menu(self.tex_editor, tearoff=0)
        self.context_menu.add_command(
            label="Cut",
            command=self.cut,
            accelerator="Ctrl+X"
        )
        self.context_menu.add_command(
            label="Copy",
            command=self.copy,
            accelerator="Ctrl+C"
        )
        self.context_menu.add_command(
            label="Paste",
            command=self.paste,
            accelerator="Ctrl+V"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Find/Replace",
            command=self.create_find_frame,
            accelerator="Ctrl+F"
        )

        # Create binds
        self.tex_editor.bind("<Button-3>", lambda event: self.popup(event, self.tex_editor))
        self.bib_editor.bind("<Button-3>", lambda event: self.popup(event, self.bib_editor))
        self.tex_editor.bind("<Control-f>", self.create_find_frame)
        self.tex_editor.bind("<Control-F>", self.create_find_frame)
        self.bib_editor.bind("<Control-F>", self.create_find_frame)
        self.bib_editor.bind("<Control-f>", self.create_find_frame)

    def popup(self, event, editor):
        """Creates context menu at cursor position when user right clicks.

        Parameters
        ----------
        event
            tkinter event to handle bind
        editor : scrolled text object
            editor that was right clicked
        """
        self.right_clicked = editor
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    def cut(self):
        """Cuts selected text."""
        self.right_clicked.event_generate("<<Cut>>")

    def copy(self):
        """Copies selected text."""
        self.right_clicked.event_generate("<<Copy>>")

    def paste(self):
        """Pastes clipboard text."""
        self.right_clicked.event_generate("<<Paste>>")

    def create_find_frame(self, event=None):
        """Creates FindButtons frame.

        Checks which editor is visible and creates FindButtons frame in it.

        Parameters
        ----------
        event
            tkinter event to handle bind. If not provided defaults to None
        """
        # If index of selected tab is 0 create FindButtons frame in bib editor. Else in tex editor
        if self.tex_notebook.index("current"):
            # If a find and replace frame is already in bib editor open close it
            if self.bib_editor_find_frame:
                self.bib_editor_find_frame.close_find()
            self.bib_editor_find_frame = FindButtons(
                self.bib_editor,
                self.bib_editor,
                self,
                style="FindFrame.TFrame"
            )
            self.bib_editor_find_frame.pack(side="top", anchor="ne")
        else:
            # If a find and replace frame is already open in tex editor close it
            if self.tex_editor_find_frame:
                self.tex_editor_find_frame.close_find()
            self.tex_editor_find_frame = FindButtons(
                self.tex_editor,
                self.tex_editor,
                self,
                style="FindFrame.TFrame"
            )
            self.tex_editor_find_frame.pack(side="top", anchor="ne")

    def close_find_frame(self, event=None):
        """Closes FindButtons frame.

        Checks which editor is visible and closes FindButtons frame in it.

        Parameters
        ----------
        event
            tkinter event to handle bind. If not provided defaults to None
        """
        if self.tex_notebook.index("current"):
            self.bib_editor_find_frame.close_find()
            self.bib_editor_find_frame = None
        else:
            self.tex_editor_find_frame.close_find()
            self.tex_editor_find_frame = None

    def check_bib_saved(self):
        """Returns True if bib file is saved

        Calls save_bib method inside BibButtons object and returns result
        """
        return self.bib_buttons.save_bib()

    def check_bib_empty(self):
        """Returns True if bib editor is empty"""
        # Get content of bib editor and check if there is any non whitespaces
        bib_content = self.bib_editor.get(1.0, "end")
        if len(bib_content.strip()) == 0:
            return True
