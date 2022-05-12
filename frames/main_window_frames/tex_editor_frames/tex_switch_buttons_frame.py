"""Define TexSwitchButtonsFrame class.

Classes
-------
TexSwitchButtonsFrame
    Configures TexSwitchButtonsFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from .tex_editor_frame import TexEditorFrame
from functools import partial


class TexSwitchButtonsFrame(ttk.Frame):
    """A class configuring TexSwitchButtonsFrame frame; also creates TexToolButtons frame

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    tex_frames : dict
        a dictionary storing TexEditorFrames
    _switch_buttons : dict
        a dictionary storing switch buttons
    _next_frame : int
        int variable indicating what number to give next frame

    Methods
    -------
    new_tex_frame()
        Creates new TexEditorFrame frame and corresponding switch button
    _close_tex_frame(frame_number)
        Destroys TexEditorFrame frame and corresponding switch button
    check_visible_tex_frame(frame)
        Checks what TexEditorFrame frame is currently visible
    show_frame(frame)
        Raises TexEditorFrame frame to be visible
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises TexSwitchButtonsFrame frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates button.

        Parameters
        ----------
        self
            TexSwitchButtonsFrame object
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

        # Create dictionaries to store TexEditorFrames and switch buttons
        self.tex_frames = dict()
        self._switch_buttons = dict()
        # Create int to control what number next frame is given
        self._next_frame = 1

        # Create new tab button
        new_tex_frame_button = ttk.Button(
            self,
            text="New Tab",
            command=self.new_tex_frame
        )
        new_tex_frame_button.pack(side="right")

    def new_tex_frame(self):
        """Creates new TexEditorFrame frame and corresponding switch button

        Increments frame number, creates new TexEditorFrame and adds to tex frames dictionary with frame number key and
        object value. Creates switch button and adds to switch buttons dictionary with button number key and button
        value. Calls self.show_frame on new TexEditorFrame
        """
        # Increment _next_frame so new frame is given next number
        self._next_frame += 1
        frame_number = self._next_frame

        # Create new TexEditorFrame and add to tex frames dictionary with frame number
        tex_frame = TexEditorFrame(self.controller.tex_editor_container)
        tex_frame.grid(row=0, column=0, sticky="nsew")
        self.tex_frames[f"frame{frame_number}"] = tex_frame

        # Create new switch button frame and add to switch buttons dictionary with button number
        switch_button_frame = ttk.Frame(self)
        switch_button_frame.pack(side="left")
        self._switch_buttons[f"button{frame_number}"] = switch_button_frame

        # Create switch button
        raise_p = partial(self.show_frame, self.tex_frames[f"frame{frame_number}"])
        switch_button = ttk.Button(
            switch_button_frame,
            textvariable=tex_frame.tex_file_name,
            command=raise_p
        )
        switch_button.pack(side="left")

        # Create close button
        close_p = partial(self._close_tex_frame, frame_number)
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
        self.show_frame(tex_frame)

    def _close_tex_frame(self, frame_number):
        """Destroys TexEditorFrame frame and corresponding switch button

        Destroys and removes switch button with passed number from switch buttons. Destroys and removes TexEditorFrame
        with passed number from tex frames dictionary. Updates visible tex frame attribute and sets focus to it

        Parameters
        ----------
        frame_number : int
            frame number to give new frame
        """
        switch_button = self._switch_buttons[f"button{frame_number}"]
        switch_button.pack_forget()
        switch_button.destroy()
        del self._switch_buttons[f"button{frame_number}"]

        tex_frame = self.tex_frames[f"frame{frame_number}"]
        tex_frame.grid_forget()
        self.controller.tex_frames_list.remove(tex_frame)
        tex_frame.destroy()
        del self.tex_frames[f"frame{frame_number}"]

        self.controller.visible_tex_frame = self.controller.tex_frames_list[-1]
        if self.controller.visible_tex_frame.tex_notebook.index("current"):
            self.controller.visible_tex_frame.bib_editor.focus_set()
        else:
            self.controller.visible_tex_frame.tex_editor.focus_set()

    def check_visible_tex_frame(self, frame):
        """Checks what TexEditorFrame frame is currently visible

        If the frame passed is in the tex frames list, removes it and readds it to the end of the list. Then sets
        visible tex frame to the end of the tex frames list (i.e. the frame passed)

        Parameters
        ----------
        frame : TexEditorFrame()
            frame to set as visible
        """
        if frame in self.controller.tex_frames_list:
            self.controller.tex_frames_list.remove(frame)
        self.controller.tex_frames_list.append(frame)
        self.controller.visible_tex_frame = self.controller.tex_frames_list[-1]

    def show_frame(self, frame):
        """Raises TexEditorFrame frame to be visible

        Raises frame passed to be visible. Sets focus to visible text box and calls self.check_visible_tex_frame to set
        frame as visible

        Parameters
        ----------
        frame : TexEditorFrame()
            frame to be raised
        """
        frame.tkraise()
        self.check_visible_tex_frame(frame)
        if self.controller.visible_tex_frame.tex_notebook.index("current"):
            self.controller.visible_tex_frame.bib_editor.focus_set()
        else:
            self.controller.visible_tex_frame.tex_editor.focus_set()
