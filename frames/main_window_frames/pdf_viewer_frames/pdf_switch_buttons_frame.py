"""Define PDFSwitchButtonsFrame class.

Classes
-------
PDFSwitchButtonsFrame
    Configures PDFSwitchButtonsFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from functools import partial
from .pdf_frame import PDFFrame


class PDFSwitchButtonsFrame(ttk.Frame):
    """A class configuring PDFSwitchButtonsFrame frame; also creates TexToolButtons frame

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    pdf_frames : dict
        a dictionary storing PDFFrames
    _switch_buttons : dict
        a dictionary storing switch buttons
    _next_frame : int
        int variable indicating what number to give next frame

    Methods
    -------
    new_pdf_frame()
        Creates new PDFFrame and corresponding switch button
    _close_pdf_frame(frame_number)
        Destroys PDFFrame and corresponding switch button
    check_visible_pdf_frame(frame)
        Checks what PDFFrame is currently visible
    show_frame(frame)
        Raises PDFFrame to be visible
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises PDFSwitchButtonsFrame frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates button.

        Parameters
        ----------
        self
            PDFFrame object
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

        # Create dictionaries to store PDFFrames and switch buttons
        self.pdf_frames = dict()
        self._switch_buttons = dict()
        # Create int to control what number next frame is given
        self._next_frame = 1

        # Create new tab button
        new_pdf_frame_button = ttk.Button(
            self,
            text="New Tab",
            command=self.new_pdf_frame
        )
        new_pdf_frame_button.pack(side="right")

    def new_pdf_frame(self):
        """Creates new PDFFrame and corresponding switch button

        Increments frame number, creates new PDFFrame and adds to pdf frames dictionary with frame number key and
        object value. Creates switch button and adds to switch buttons dictionary with button number key and button
        value. Calls self.show_frame on new PDFFrame
        """
        # Increment _next_frame so new frame is given next number
        self._next_frame += 1
        frame_number = self._next_frame

        # Create new PDFFrame and add to tex frames dictionary with frame number
        pdf_frame = PDFFrame(self.controller.pdf_container_frame)
        pdf_frame.grid(row=1, sticky="nesw")
        self.pdf_frames[f"frame{frame_number}"] = pdf_frame

        # Remove welcome label
        pdf_frame.buttons_frame.welcome_label.place_forget()

        # Create new switch button frame and add to switch buttons dictionary with button number
        switch_button_frame = ttk.Frame(self)
        switch_button_frame.pack(side="left")
        self._switch_buttons[f"button{frame_number}"] = switch_button_frame

        # Create switch button
        raise_p = partial(self.show_frame, self.pdf_frames[f"frame{frame_number}"])
        switch_button = ttk.Button(
            switch_button_frame,
            textvariable=pdf_frame.pdf_file_name,
            command=raise_p
        )
        switch_button.pack(side="left")

        # Create close button
        close_p = partial(self._close_pdf_frame, frame_number)
        close_frame_button = tk.Button(
            switch_button_frame,
            text="X",
            foreground="red",
            command=close_p,
            bg="#dcdad5",
            highlightthickness=0,
            relief="flat"
        )
        close_frame_button.pack(side="left", fill="both")

        # Call self.show_frame to set as visible frame
        self.show_frame(pdf_frame)

    def _close_pdf_frame(self, frame_number):
        """Destroys PDFFrame and corresponding switch button.

        Destroys and removes switch button with passed number from switch buttons. Destroys and removes PDFFrame
        with passed number from pdf frames dictionary. Updates visible pdf frame attribute and sets focus to it.

        Parameters
        ----------
        frame_number : int
            frame number to give new frame
        """
        switch_button = self._switch_buttons[f"button{frame_number}"]
        switch_button.pack_forget()
        switch_button.destroy()
        del self._switch_buttons[f"button{frame_number}"]

        pdf_frame = self.pdf_frames[f"frame{frame_number}"]
        pdf_frame.grid_forget()
        self.controller.pdf_frames_list.remove(pdf_frame)
        pdf_frame.destroy()
        del self.pdf_frames[f"frame{frame_number}"]

        self.controller.visible_pdf_frame = self.controller.pdf_frames_list[-1]

    def check_visible_pdf_frame(self, frame):
        """Checks what PDFFrame is currently visible.

        If the frame passed is in the pdf frames list, removes it and readds it to the end of the list. Then sets
        visible pdf frame to the end of the pdf frames list (i.e. the frame passed)

        Parameters
        ----------
        frame : PDFFrame()
            frame to set as visible
        """
        if frame in self.controller.pdf_frames_list:
            self.controller.pdf_frames_list.remove(frame)
        self.controller.pdf_frames_list.append(frame)
        self.controller.visible_pdf_frame = self.controller.pdf_frames_list[-1]

    def show_frame(self, frame):
        """Raises PDFFrame to be visible.

        Raises frame passed to be visible and calls self.check_visible_pdf_frame to set frame as visible.

        Parameters
        ----------
        frame : PDFFrame()
            frame to be raised
        """
        frame.tkraise()
        self.check_visible_pdf_frame(frame)
