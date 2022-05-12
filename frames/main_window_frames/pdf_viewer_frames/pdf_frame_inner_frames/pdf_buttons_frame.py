"""Define PDFButtonsFrame class.

Classes
-------
PDFButtonsFrame
    Configures PDFButtonsFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from functools import partial


class PDFButtonsFrame(ttk.Frame):
    """A class configuring PDFButtonsFrame frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    initial_frame : bool
        indicates if this is the initial frame created on application launch
    zoom_default_button : ttk.Button()
        button to reset zoom to default
    zoom_in_button : ttk.Button()
        button to increase zoom
    scale : tk.Scale()
        scale to set zoom dpi
    zoom_out_button : ttk.Button()
        button to decrease zoom
    welcome_label : ttk.Label()
        label displaying welcome message
    load_pdf_button : ttk.Button()
        button to load pdf into viewer
    compile_from_browse : ttk.Button()
        button to compile pdf from tex file
    close_pdf_button : ttk.Button()
        button to close loaded pdf

    Methods
    -------
    button_states_on_load()
        Sets button states for when PDF is loaded
    button_states_on_close()
        Sets button states for when no PDF is loaded
    button_states_on_zoom(zoom_dpi: int)
        Sets button states depending on zoom_dpi
    """

    def __init__(self, container, controller, initial_frame, **kwargs):
        """Initialises PDFButtonsFrame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates buttons and scale

        Parameters
        ----------
        self
            PDFButtonsFrame object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        initial_frame : bool
            Indicates if this is the initial frame created on application launch
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to PDFFrame object to provide access to its attributes/methods
        self.controller = controller
        # Set whether this is initial frame created on application launch
        self.initial_frame = initial_frame

        # Create partials to pass zoom type to self.controller.zoom
        _zoom_default_p = partial(self.controller.zoom, "default")
        _zoom_in_p = partial(self.controller.zoom, "in")
        _zoom_out_p = partial(self.controller.zoom, "out")

        # Create tool buttons, scale and welcome label
        self.zoom_default_button = ttk.Button(
            self,
            state="disabled",
            text="/",
            command=_zoom_default_p,
            style="ZoomButtons.TButton",
            padding=(-40, 0)
        )
        self.zoom_default_button.pack(side='right', fill="y")

        self.zoom_in_button = ttk.Button(
            self,
            state="disabled",
            text="+",
            command=_zoom_in_p,
            style="ZoomButtons.TButton",
            padding=(-40, 0)
        )
        self.zoom_in_button.pack(side='right', fill="y")

        self.scale = tk.Scale(
            self,
            state="disabled",
            orient="horizontal",
            from_=10,
            to=300,
            variable=controller.zoom_dpi,
            cursor="hand2",
            bg="#dcdad5",
            highlightbackground="#9e9a91",
            highlightthickness=1,
            length=200
        )
        self.scale.pack(side="right", fill="y")

        self.zoom_out_button = ttk.Button(
            self,
            state="disabled",
            text="-",
            command=_zoom_out_p,
            style="ZoomButtons.TButton",
            padding=(-40, 0)
        )
        self.zoom_out_button.pack(side='right', fill="y")

        self.welcome_label = ttk.Label(
            self.controller,
            text="Welcome to DoTeX. Compiled PDFs will appear here",
            font=("Segoe UI", 22)
        )

        self.load_pdf_button = ttk.Button(
            self,
            text="Load PDF",
            command=self.controller.browse_pdf,
        )
        self.load_pdf_button.pack(side="left", fill="y")

        self.compile_from_browse = ttk.Button(
            self,
            text="Compile (Browse)",
            command=self.controller.compile_from_browse
        )
        self.compile_from_browse.pack(side="left", fill="y")

        self.close_pdf_button = ttk.Button(
            self,
            state="disabled",
            text="Close PDF",
            command=self.controller.close_pdf,
        )
        self.close_pdf_button.pack(side="left", fill="y")

        # If this is the initial frame place the welcome message
        if self.initial_frame:
            self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    def button_states_on_load(self):
        """Sets button states for when PDF is loaded"""
        self.load_pdf_button.config(state="disabled")
        self.compile_from_browse.config(state="disabled")
        self.close_pdf_button.config(state="normal")
        self.scale.config(state="active")
        self.scale.bind("<ButtonRelease-1>", self.controller.handle_scale_change)

    def button_states_on_close(self):
        """Sets button states for when no PDF is loaded"""
        self.load_pdf_button.config(state="active")
        self.compile_from_browse.config(state="active")
        self.close_pdf_button.config(state="disabled")
        self.zoom_in_button.config(state="disabled")
        self.zoom_default_button.config(state="disabled")
        self.zoom_out_button.config(state="disabled")
        self.scale.config(state="disabled")
        self.scale.unbind("<ButtonRelease-1>")

    def button_states_on_zoom(self, zoom_dpi: int):
        """Sets button states depending on zoom_dpi"""
        # If zoom is at max disable zoom in button
        if zoom_dpi < 300:
            self.zoom_in_button.config(state="active")
        else:
            self.zoom_in_button.config(state="disabled")

        self.zoom_default_button.config(state="active")

        # If zoom is at min disable zoom out button
        if zoom_dpi > 10:
            self.zoom_out_button.config(state="active")
        else:
            self.zoom_out_button.config(state="disabled")
