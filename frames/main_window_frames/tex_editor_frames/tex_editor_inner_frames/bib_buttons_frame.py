"""Define BibButtonsFrame class.

Classes
-------
BibButtonsFrame
    Configures BibButtonsFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class BibButtonsFrame(ttk.Frame):
    """A class configuring BibButtonsFrame frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods

    Methods
    -------
    _load_bib()
        Opens filedialog for user to select bib file and loads content into scrolled text box
    _close_bib()
        Clears scrolled text box and disassociates loaded bib file with TexEditorFrame
    save_bib()
        Overwrites loaded bib file with content of scrolled text box. Returns True if saved.
    _save_bib_as()
        Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text box.
        Returns True if saved.
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises BibButtonsFrame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates buttons.

        Parameters
        ----------
        self
            BibButtonsFrame object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create reference to TexEditor object to provide access to its attributes/methods
        self.controller = controller

        # Create tool buttons
        bib_load = ttk.Button(
            self,
            text="Load Bib",
            command=self._load_bib,
            padding=(0, 0)
        )
        bib_load.grid(row=0, column=0, sticky="ns")

        bib_close = ttk.Button(
            self,
            text="Close Bib",
            command=self._close_bib,
            padding=(0, 0)
        )
        bib_close.grid(row=0, column=1, sticky="ns")

        bib_save = ttk.Button(
            self,
            text="Save Bib",
            command=self.save_bib,
            padding=(0, 0)
        )
        bib_save.grid(row=0, column=2, sticky="ns")

        bib_save_as = ttk.Button(
            self,
            text="Save Bib As",
            command=self._save_bib_as,
            padding=(0, 0)
        )
        bib_save_as.grid(row=0, column=3, sticky="ns")

    def _load_bib(self):
        """Opens filedialog for user to select bib file and loads content into scrolled text box"""
        bib_file = tk.filedialog.askopenfilename(
            title="Select a Bib file",
            initialdir=".",
            filetypes=(("Bib Files (*.bib)", "*.bib"), ("All Files", "*.*"))
        )

        if bib_file and ".bib" in bib_file:
            self.controller.bib_file = bib_file

            self.controller.bib_editor.delete(1.0, "end")

            with open(self.controller.bib_file, 'r') as read_content:
                bib_content = read_content.read()
            self.controller.bib_editor.insert(1.0, bib_content)

    def _close_bib(self):
        """Clears scrolled text box and disassociates loaded bib file with TexEditorFrame"""
        self.controller.bib_editor.delete(1.0, "end")
        self.controller.bib_file = ""

    def save_bib(self):
        """Overwrites loaded bib file with content of scrolled text box. Returns True if saved.

        If not associated with a file calls self.save_bib_as().

        Returns
        -------
        saved : bool
            True if file is saved
        """
        bib_content = self.controller.bib_editor.get(1.0, "end-1c")
        try:
            with open(self.controller.bib_file, 'w') as output:
                output.write(bib_content)
            return True
        except FileNotFoundError:
            saved = self._save_bib_as()
            return saved

    def _save_bib_as(self):
        """Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text
        box.

        Returns
        -------
        saved : bool
            True if file is saved
        """
        bib_file = tk.filedialog.asksaveasfilename(
            title="Save Bib file As",
            initialdir=".",
            initialfile="untitled_bib_file",
            filetypes=(("Bib documents (*.bib)", "*.bib"), ("All Files", "*.*")),
            defaultextension=".bib"
        )
        if bib_file:
            self.bib_file = bib_file
            bib_content = self.controller.bib_editor.get(1.0, "end-1c")
            if self.bib_file:
                with open(self.bib_file, 'w') as output:
                    output.write(bib_content)
                return True
