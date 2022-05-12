"""Define TexToolButtons class.

Classes
-------
TexToolButtons
    Configures TexToolButtons frame.
"""
from tkinter import ttk
from functools import partial


class TexToolButtons(ttk.Frame):
    """A class configuring TexToolButtons frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises TexToolButtons.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates buttons.

        Parameters
        ----------
        self
            TexToolButtons object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to TexEditor object to provide access to its attributes/methods
        self.controller = controller
        self.error_frame = None

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create tool buttons
        load_tex_button = ttk.Button(
            self,
            text="Load TeX",
            command=self.controller.load_tex
        )

        close_tex_button = ttk.Button(
            self,
            text="Close TeX",
            command=self.controller.close_tex
        )

        save_button = ttk.Button(
            self,
            text="Save Tex",
            command=self.controller.save
        )

        save_as_button = ttk.Button(
            self,
            text="Save TeX As",
            command=self.controller.save_as
        )

        compile_button = ttk.Button(
            self,
            text="Compile",
            command=self.controller.compile_pdf
        )

        compile_p = partial(self.controller.compile_pdf, blank=True)
        compile_blank_button = ttk.Button(
            self,
            text="Compile (Blank Tab)",
            command=compile_p,
        )

        # Grid tool buttons
        count = 0
        for widget in self.winfo_children():
            widget.grid(row=0, column=count, sticky="ns")
            count += 1
