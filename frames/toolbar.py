"""Define Toolbar class.

Classes
-------
Toolbar
    Configures Toolbar frame.
"""
from tkinter import ttk
from .toolbar_frames import Home, Format, Insert, Math, StudyTimer
from .toolbar_frames.toolbar_inner_frames import Settings


class Toolbar(ttk.Frame):
    """A class configuring Toolbar frame; also creates Home, File, Insert and Math frames.

    Attributes
    ----------
    dotex_controller : widget object
        a reference to DoTeX application window object to provide access to its attributes/methods
    main_window_controller : widget object
        a reference to main_window_frame frame from master widget to provide access to its attributes/methods
    settings_window : Settings()
        a Settings toplevel window
    toolbar_notebook : ttk.Notebook(master)
        a notebook widget
    home_tab : Home(container, controller, main_window_controller)
        a Home frame
    format_tab : Format(container, controller)
        a Format frame
    insert_tab : Insert(container, controller)
        an Insert frame
    math_tab : Math(container, controller)
        a Math frame
    study_timer : StudyTimer()
        a StudyTimer toplevel window

    Methods
    -------
    exit()
        Destroys application window
    launch_timer()
        Creates StudyTimer toplevel window
    launch_settings()
        Creates Settings toplevel window
    check_current_editor()
        Returns currently visible scrolled text box object
    """

    def __init__(self, container, dotex_controller, main_window_controller, **kwargs):
        """Initialises Toolbar frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates Home, Format, Insert and Math frames. Creates notebook widget to
        contain home, file, insert and math frames. Creates exit, settings and timer buttons.

        Parameters
        ----------
        self
            Toolbar object
        container : widget object
            Master widget
        dotex_controller : widget object
            A reference to DoTeX application window object to provide access to its attributes/methods
        main_window_controller : widget object
            A reference to main_window_frame frame from master widget to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create references to DoTeX object and DoTeX.main_window to provide access to their attributes/methods
        self.dotex_controller = dotex_controller
        self.main_window_controller = main_window_controller

        self.settings_window = None

        # Create and pack Notebook named toolbar_notebook with Toolbar as master, to contain Home, Format, Insert and
        # Math frames
        self.toolbar_notebook = ttk.Notebook(self)
        self.toolbar_notebook.pack(side="left", fill="both", expand=True)

        # Create Home, Format, Insert and Math frames as home_tab, format_tab, insert_tab and math_tab with
        # toolbar_notebook as masters. Pass Toolbar as controller to all and self.main_window_controller as
        # main_window_controller to home_tab
        self.home_tab = Home(self.toolbar_notebook, self, self.main_window_controller)
        self.format_tab = Format(self.toolbar_notebook, self)
        self.insert_tab = Insert(self.toolbar_notebook, self)
        self.math_tab = Math(self.toolbar_notebook, self)

        # Add frames to toolbar_notebook with corresponding tab names
        tab_names = ["Home", "Format", "Insert", "Math"]
        count = 0
        for widget in self.toolbar_notebook.winfo_children():
            self.toolbar_notebook.add(widget, text=tab_names[count])
            count += 1

        # Create and pack exit, settings and study timer buttons
        exit_button = ttk.Button(
            self,
            text="Exit",
            command=self.exit,
            padding=(0, 8)
        )
        exit_button.pack(side="right", fill="x", anchor="se")

        settings_button = ttk.Button(
            self,
            text="Settings",
            command=self.launch_settings,
            padding=(0, 8)
        )
        settings_button.pack(side="right", fill="x", anchor="se")

        self.study_timer = None

        study_timer_button = ttk.Button(
            self,
            text="Timer",
            command=self.launch_timer,
            padding=(0, 8)
        )
        study_timer_button.pack(side="right", fill="x", anchor="se")

    def exit(self):
        """Destroys DoTeX application window."""
        self.dotex_controller.destroy()

    def launch_timer(self):
        """If study_timer exists destroys it. Creates StudyTimer toplevel window named study_timer."""
        if self.study_timer:
            self.study_timer.close()
        self.study_timer = StudyTimer()

    def launch_settings(self):
        """If settings_window exists destroys it. Creates Settings toplevel window named settings_window."""
        if self.settings_window:
            self.settings_window.close()
        self.settings_window = Settings()

    def check_current_editor(self):
        """Returns currently visible scrolled text box object

        Calls check_current_editor() method from tex_editor_frame object from main_window_controller and assigns return
        to current_editor. This returns the scrolled text box widget in the currently selected tab in the currently
        visible tex editor frame. Returns current_editor.

        Returns
        -------
        current_editor : widget object
            currently visible scrolled text box object
        """
        current_editor = self.main_window_controller.tex_editor_frame.check_current_editor()
        return current_editor
