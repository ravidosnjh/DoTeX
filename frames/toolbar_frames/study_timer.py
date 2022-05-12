"""Define StudyTimer class.

Classes
-------
TimerWindow
    Configures StudyTimer toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from collections import deque
from .toolbar_inner_frames import Timer, TimerSettings


class StudyTimer(tk.Toplevel):
    """A class configuring StudyTimer toplevel window; also creates Timer and TimerSettings frames.

    Attributes
    ----------
    study : str
        stringvar containing length of study periods
    short_break : str
        stringvar containing length of short breaks
    long_break : str
        stringvar containing length of long breaks
    timer_order : list
        list containing order of stages
    timer_schedule : deque
        deque of timer_order
    frames : dict
        dictionary containing Timer and TimerSettings frames

    Methods
    -------
    show_frame()
        Raises currently hidden frame to top
    close()
        Destroys StudyTimer toplevel window
    """

    def __init__(self):
        """Initialises StudyTimer frame.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and Timer and TimerSettings frames.

        Parameters
        ----------
        self
            StudyTimer object
        """
        super().__init__()

        # Set window title
        self.title("Study Timer")
        # Make row 0 and column 0 fill available space
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create StringVars to store lengths of different periods, and default values
        self.study = tk.StringVar(value=25)
        self.long_break = tk.StringVar(value=15)
        self.short_break = tk.StringVar(value=5)
        # Create list with starting order of periods and deque
        self.timer_order = ["Study", "Short Break", "Study", "Short Break", "Study", "Long Break"]
        self.timer_schedule = deque(self.timer_order)

        # Create and grid container frame for Timer and Settings frames. Make column 0 fill all available space
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nesw")
        container.columnconfigure(0, weight=1)

        # Create frames dictionary
        self.frames = dict()

        # Create and grid Timer and TimerSettings frames named timer_frame and settings_frame
        timer_frame = Timer(container, self, lambda: self.show_frame(TimerSettings))
        timer_frame.grid(row=0, column=0, sticky="nesw")
        settings_frame = TimerSettings(container, self, lambda: self.show_frame(Timer))
        settings_frame.grid(row=0, column=0, sticky="nesw")

        # Create frame for close button and close button
        close_frame = ttk.Frame(self)
        close_frame.grid(row=1, column=0, sticky="nesw")
        close_frame.columnconfigure(0, weight=1)

        close_button = ttk.Button(
            close_frame,
            text="Close",
            command=self.close
        )
        close_button.grid(row=0, column=0, sticky="ns", pady=(0, 10))

        # Add frames to frame dictionary
        self.frames[Timer] = timer_frame
        self.frames[TimerSettings] = settings_frame

        # Call self.show_frame to raise timer_frame to top so it is visible
        self.show_frame(Timer)

    def show_frame(self, container):
        """Raises currently hidden frame to top.

        Calls tkraise() on frame passed as container to raise it to the top and make it visible.

        Parameters
        ----------
        container : frame object
            Frame to be raised
        """
        frame = self.frames[container]
        frame.tkraise()

    def close(self):
        """Destroys StudyTimer toplevel window."""
        self.destroy()
