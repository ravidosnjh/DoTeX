"""Define TimerSettings class.

Classes
-------
TimerSettings
    Configures TimerSettings frame.
"""
import tkinter as tk
from tkinter import ttk


class TimerSettings(ttk.Frame):
    """A class configuring TimerSettings frame."""

    def __init__(self, container, controller, show_timer):
        """Initialises TimerSettings frame.

        Takes container and passes it to parent ttk.Frame class constructor. Initialises ttk.Frame object. Creates label
        and spinboxes to set timer period lengths, and button to raise Timer frame.

        Parameters
        ----------
        self
            TimerSettings object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        show_timer : lambda function
            Passes show_frame(container) method with Timer frame to be used in button
        """
        super().__init__(container)

        # Make column 0 and row 2 fill all available space
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Create frame to contain settings fields and raise timer button
        settings_container = ttk.Frame(
            self,
            padding="30 15 30 15"
        )

        settings_container.grid(column=0, row=0, sticky="ew", padx=10, pady=10)

        # Make row 0 and 1 of settings container frame fill all available spce
        settings_container.columnconfigure(0, weight=1)
        settings_container.rowconfigure(1, weight=1)

        # Create labels and spinboxes for settings fields
        study_label = ttk.Label(
            settings_container,
            text="Study: ",
        )
        study_label.grid(column=0, row=0, sticky="w")

        study_input = tk.Spinbox(
            settings_container,
            from_=0,
            to=120,
            increment=1,
            justify="center",
            textvariable=controller.study,
            width=10
        )
        study_input.grid(row=0, column=1, sticky="ew")
        study_input.focus()

        long_break_label = ttk.Label(
            settings_container,
            text="Long Break: "
        )
        long_break_label.grid(column=0, row=1, sticky="w")

        long_break_input = tk.Spinbox(
            settings_container,
            from_=0,
            to=60,
            increment=1,
            justify="center",
            textvariable=controller.long_break,
            width=10
        )
        long_break_input.grid(row=1, column=1, sticky="ew")

        short_break_label = ttk.Label(
            settings_container,
            text="Short Break: "
        )
        short_break_label.grid(column=0, row=2, sticky="w")

        short_break_input = tk.Spinbox(
            settings_container,
            from_=0,
            to=30,
            increment=1,
            justify="center",
            textvariable=controller.short_break,
            width=10
        )
        short_break_input.grid(row=2, column=1, sticky="ew")

        # Grid widgets in settings frame
        for widget in settings_container.winfo_children():
            widget.grid_configure(padx=5, pady=5)

        # Create frame to contain button that raises Timer frame and create button
        button_container = ttk.Frame(self)
        button_container.grid(sticky="ew", padx=10)
        button_container.columnconfigure(0, weight=1)

        timer_button = ttk.Button(
            button_container,
            text="<- Back",
            command=show_timer
        )
        timer_button.grid(column=0, row=0, sticky="ew", padx=2)
