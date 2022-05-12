"""Define TexEditor class.

Classes
-------
TexEditor
    Configures TexEditor frame.
"""
from tkinter import ttk
from .tex_editor_frames import TexToolButtonsFrame, TexSwitchButtonsFrame, TexEditorFrame, TexErrorContainer
from functools import partial


class TexEditor(ttk.Frame):
    """A class configuring TexEditor frame; also creates TexSwitchButtonsFrame and TexEditorFrame.

    Attributes
    ----------
    pdf_controller : widget object
        a reference to PDFViewer object in master widget object to provide access to its attributes/methods
    tex_frames_list : list
        a list to store existing tex frames
    tex_switch_buttons_frame : TexSwitchButtonsFrame()
        a frame to contain switch buttons
    tex_paned_window : ttk.PanedWindow()
        a paned window to contain tex editor containers and tex error containers
    tex_editor_container : ttk.Frame()
        a frame to contain TexEditorFrames
    error_container : ttk.Frame()
        a frame to contain TexErrorContainers
    initial_tex_editor_frame : PDFFrame()
        default tex editor frame loaded on application launch
    visible_tex_frame : PDFFrame()
        a variable indicating which TexEditorFrame is currently visible in the application

    Methods
    -------
    check_current_editor()
        Returns the scrolled text box widget in the currently selected tab in the currently visible tex editor frame
    """

    def __init__(self, container, pdf_controller, **kwargs):
        """Initialises TexEditor frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            TexEditor object
        container : widget object
            Master widget
        pdf_controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to PDFViewer object to provide access to its attributes/methods
        self.pdf_controller = pdf_controller

        # Create list to store TexEditorFrames
        self.tex_frames_list = []

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Create TexSwitchButtons frame named tex_switch_buttons_frame
        self.tex_switch_buttons_frame = TexSwitchButtonsFrame(self, self)
        self.tex_switch_buttons_frame.grid(row=0, sticky="nesw")

        # Create paned window named tex_paned_window to contain tex editor containers and tex error containers
        self.tex_paned_window = ttk.PanedWindow(self)
        self.tex_paned_window.grid(row=1, column=0, sticky="nesw")

        # Create frame named tex_editor_container to contain TexEditorFrames
        self.tex_editor_container = ttk.Frame(self.tex_paned_window)
        self.tex_editor_container.pack(fill="both", expand=True)

        # Make tex editor container row 0 and column 0 fill all available space
        self.tex_editor_container.rowconfigure(0, weight=1)
        self.tex_editor_container.columnconfigure(0, weight=1)

        # Define error_container attribute
        self.error_container = None

        # Add tex editor container to tex paned window
        self.tex_paned_window.add(self.tex_editor_container, weight=1)

        # Create default TexEditorFrame named initial_tex_editor_frame that loads on application launch
        self.initial_tex_editor_frame = TexEditorFrame(self.tex_editor_container)
        self.initial_tex_editor_frame.grid(row=0, column=0, sticky="nsew")

        # Add initial_tex_editor_frame to list of TexFrames and set as visible tex frame. Add to tex_frames dictionary
        # inside tex_switch_buttons_frame
        self.tex_frames_list.append(self.initial_tex_editor_frame)
        self.visible_tex_frame = self.tex_frames_list[-1]
        self.tex_switch_buttons_frame.tex_frames["frame1"] = self.initial_tex_editor_frame

        # Create TexToolButtonsFrame named buttons_frame
        buttons_frame = TexToolButtonsFrame(
            self,
            self,
            self.pdf_controller
        )
        buttons_frame.grid(row=2, sticky="nsew")

        # Create switch button initial_tex_editor_frame
        raise_p = partial(self.tex_switch_buttons_frame.show_frame, self.initial_tex_editor_frame)
        switch_initial_tex = ttk.Button(
            self.tex_switch_buttons_frame,
            textvariable=self.visible_tex_frame.tex_file_name,
            command=raise_p,
        )
        switch_initial_tex.pack(side="left")

    def check_current_editor(self):
        """Returns the scrolled text box widget in the currently selected tab in the currently visible tex editor frame.

        Returns
        -------
        current_editor : scrolled text box object
            scrolled text box in currently selected tab of currently visible TexEditorFrame
        """
        # Check if tab 0 or 1 is selected in currently visible TexEditorFrame
        if self.visible_tex_frame.tex_notebook.index("current"):
            # Visible text box is Bib
            current_editor = self.visible_tex_frame.bib_editor
        else:
            # Visible text box is Tex
            current_editor = self.visible_tex_frame.tex_editor
        return current_editor
