"""Define PDFViewer class.

Classes
-------
PDFViewer
    Configures PDFViewer frame.
"""
import tkinter as tk
from tkinter import ttk
from .pdf_viewer_frames import PDFFrame, PDFSwitchButtonsFrame
from functools import partial


class PDFViewer(ttk.Frame):
    """A class configuring PDFViewer frame; also creates PDFSwitchButtonsFrame and PDFFrame.

    Attributes
    ----------
    pdf_frames_list : list
        a list to store existing pdf frames
    pdf_container_frame : ttk.Frame()
        a frame to contain pdf switch buttons frame and pdf frames
    pdf_switch_buttons_frame : PDFSwitchButtonsFrame()
        a frame to contain switch buttons
    initial_pdf_frame : PDFFrame()
        default pdf frame loaded on application launch
    visible_pdf_frame : PDFFrame()
        a variable indicating which PDFFrame is currently visible in the application
    """

    def __init__(self, container, **kwargs):
        """Initialises PDFViewer frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            PDFViewer object
        container : widget object
            Master widget
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create list to store PDFFrames
        self.pdf_frames_list = []

        # Create frame named pdf_container_frame to contain switch buttons frame and pdf frames
        self.pdf_container_frame = ttk.Frame(self)
        self.pdf_container_frame.pack(side="left", fill="both", expand=True)

        # Make pdf container frame row 1 and column 0 fill all available space
        self.pdf_container_frame.rowconfigure(1, weight=1)
        self.pdf_container_frame.columnconfigure(0, weight=1)

        # Create PDFSwitchButtons frame named pdf_switch_buttons_frame
        self.pdf_switch_buttons_frame = PDFSwitchButtonsFrame(self.pdf_container_frame, self)
        self.pdf_switch_buttons_frame.grid(row=0, sticky="nesw")

        # Create default PDFFrame named initial_pdf_frame
        self.initial_pdf_frame = PDFFrame(self.pdf_container_frame, initial_frame=True)
        self.initial_pdf_frame.grid(row=1, sticky="nesw")

        # Add initial_pdf_frame to list of PDFFrames and set as visible pdf frame. Add to pdf_frames dictionary inside
        # pdf_switch_buttons_frame
        self.pdf_frames_list.append(self.initial_pdf_frame)
        self.visible_pdf_frame = self.pdf_frames_list[-1]
        self.pdf_switch_buttons_frame.pdf_frames["frame1"] = self.initial_pdf_frame

        # Create switch button initial_pdf_frame
        raise_p = partial(self.pdf_switch_buttons_frame.show_frame, self.initial_pdf_frame)
        switch_initial_pdf = ttk.Button(
            self.pdf_switch_buttons_frame,
            textvariable=self.initial_pdf_frame.pdf_file_name,
            command=raise_p,
        )
        switch_initial_pdf.pack(side="left")
