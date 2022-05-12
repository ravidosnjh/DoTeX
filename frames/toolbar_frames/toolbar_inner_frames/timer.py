"""Define Timer class.

Classes
-------
Timer
    Configures Timer frame.
"""
import tkinter as tk
from tkinter import ttk
from collections import deque


class Timer(ttk.Frame):
    """A class configuring TimerSettings frame.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    current_time : str
        stringvar containing length of study periods
    current_timer_label : str
        stringvar containing length of study periods
    timer_running : bool
        bool indicating if the timer is currently decrementing
    _timer_decrement_job : after(time, function)
        variable storing queued after calls
    start_button : ttk.Button()
        button widget to make timer start decrementing
    stop_button : ttk.Button()
        button widget to make timer stop decrementing

    Methods
    -------
    start_timer()
        Makes timer start decrementing
    stop_timer()
        Makes timer stop decrementing
    reset_timer()
        Resets timer to initial length of initial stage
    decrement_time()
        Decrements time
    """

    def __init__(self, container, controller, show_settings):
        """Initialises Timer frame.

        Takes container and passes it to parent ttk.Frame class constructor. Initialises ttk.Frame object. Creates label
        to display timer stage and time, and control buttons.

        Parameters
        ----------
        self
            Timer object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        show_settings : lambda function
            Passes show_frame(container) method with TimerSettings frame to be used in button
        """
        super().__init__(container)

        # Create reference to StudyTimer object to provide access to its attributes/methods
        self.controller = controller

        # Make column 0 and 1 fill all available space
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # Create StringVars to time and timer stage
        self.current_time = tk.StringVar(value=f"{controller.study.get()}:00")
        self.current_timer_label = tk.StringVar(value=self.controller.timer_schedule[0])
        # Create vars to indicate if timer running and store after jobs
        self.timer_running = False
        self._timer_decrement_job = None

        # Create label to display timer stage and time, and button to raise TimerSettings frame
        timer_description = ttk.Label(
            self,
            textvariable=self.current_timer_label
        )
        timer_description.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(10, 0))

        settings_button = ttk.Button(
            self,
            text="Settings",
            command=show_settings
        )
        settings_button.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 0))

        timer_frame = ttk.Frame(self, height="100")
        timer_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="nesw")

        timer_counter = ttk.Label(
            timer_frame,
            textvariable=self.current_time,
            font=("Segoe UI", 32)
        )
        timer_counter.place(relx=0.5, rely=0.5, anchor="center")

        # Create frame to contain buttons
        button_container = ttk.Frame(self, padding=10)
        button_container.grid(row=2, column=0, columnspan=2, sticky="ew")
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)
        button_container.columnconfigure(2, weight=1)

        # Create start button, stop button and reset button
        self.start_button = ttk.Button(
            button_container,
            text="Start",
            command=self.start_timer
        )
        self.start_button.grid(row=0, column=0, sticky="ew")

        self.stop_button = ttk.Button(
            button_container,
            text="Stop",
            state="disabled",
            command=self.stop_timer
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=5)

        reset_button = ttk.Button(
            button_container,
            text="Reset",
            command=self.reset_timer
        )
        reset_button.grid(row=0, column=2, sticky="ew")

    def start_timer(self):
        """Makes timer start decrementing

        Sets timer_running bool to True. Enables stop button and disables start button. Calls self.decrement_time() to
        start decrementing time
        """
        self.timer_running = True
        self.stop_button["state"] = "enabled"
        self.start_button["state"] = "disabled"
        self.decrement_time()

    def stop_timer(self):
        """Makes timer stop decrementing

        Sets timer_running bool to False. Disables stop button and enables start button. If pending after jobs exist,
        cancels them and sets _timer_decrement_job to None
        """
        self.timer_running = False
        self.stop_button["state"] = "disabled"
        self.start_button["state"] = "enabled"

        if self._timer_decrement_job:
            self.after_cancel(self._timer_decrement_job)
            self._timer_decrement_job = None

    def reset_timer(self):
        """Resets timer to initial length of initial stage

        Calls self.stop_timer() to make timer stop decrementing. Sets current_time to value of controller.study to reset
        to initial length of study period. Resets controller.timer_schedule list to initial order and sets
        current_time_label to index 0 of this list to reset timer stage to Study
        """
        self.stop_timer()
        study_time = self.controller.study.get()
        self.current_time.set(f"{int(study_time):02d}:00")
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.current_timer_label.set(self.controller.timer_schedule[0])

    def decrement_time(self):
        """Decrements time

        Gets value of current_time. If the timer is running and the current time has not reached 00:00 decrements the
        minutes of the current time by 1 and sets seconds to 59 if a full minute has passed, else seconds by 1. Else
        timer stage to the next stage and sets the current time to the initial length of the corresponding stage. In
        either case queues an after job to set the current_time to the decremented time after 1 second.
        """
        current_time = self.current_time.get()

        if self.timer_running and current_time != "00:00":
            minutes, seconds = current_time.split(":")

            if int(seconds) > 0:
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1

            self.current_time.set(f"{minutes:02d}:{seconds:02d}")
            self._timer_decrement_job = self.after(1000, self.decrement_time)
        elif self.timer_running and current_time == "00:00":
            self.controller.timer_schedule.rotate(-1)
            next_up = self.controller.timer_schedule[0]
            self.current_timer_label.set(next_up)

            if next_up == "study":
                study_time = int(self.controller.study.get())
                self.current_time.set(f"{study_time:02d}:00")
            elif next_up == "Short Break":
                short_break_time = int(self.controller.short_break.get())
                self.current_time.set(f"{short_break_time:02d}:00")
            elif next_up == "Long Break":
                long_break_time = int(self.controller.long_break.get())
                self.current_time.set(f"{long_break_time:02d}:00")

            self._timer_decrement_job = self.after(1000, self.decrement_time)
        