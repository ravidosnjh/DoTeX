"""Define DoTeX class. Create DoTeX application window object and run mainloop.

Classes
-------
DoTeX
    Configures DoTeX application window.
"""
import tkinter as tk
from tkinter import ttk
from frames import MainWindow, Toolbar


class DoTeX(tk.Tk):
    """A class configuring DoTeX application window; also creates MainWindow and Toolbar frames.

    Attributes
    ----------
    main_window : MainWindow(container)
        a MainWindow frame
    """

    def __init__(self, *args, **kwargs):
        """Initialises DoTeX application window

        Takes *args and **kwargs and passes them to parent tk.Tk class constructor. Initialises tk.Tk object.
        Configures DoTeX geometry, title, grid manager and ttk styles. Creates MainWindow and Toolbar frames.

        Parameters
        ----------
        self
            DoTeX object
        *args
            Arbitrary number of positional arguments
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(*args, **kwargs)

        # Set default window size to 1920x1080 and window title to DoTeX
        self.geometry("1920x1080")
        self.title("DoTeX")

        # Make row 1 and column 0 fill all available space
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Initialise ttk style database and configure custom styles
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TPanedwindow", background="black")
        style.configure("ZoomButtons.TButton", font=("Segoe UI", 14))
        style.configure("CloseButtons.TButton", foreground="red", padding=(-25, 0))
        style.configure("FindFrame.TFrame", background="white")
        style.configure("Bold.TButton", font=("Segoe UI", 9, "bold"), padding=(-25, 0))
        style.configure("Italic.TButton", font=("Segoe UI", 9, "italic"), padding=(-19, 0))
        style.configure("Underline.TButton", font=("Segoe UI", 9, "underline"), padding=(-19, 0))

        # Create MainWindow frame named main_window with DoTeX as master
        self.main_window = MainWindow(self)

        # Create and grid Toolbar frame named toolbar with DoTeX as master. Pass DoTeX and main_window as controllers to
        # toolbar
        toolbar = Toolbar(self, self, self.main_window)
        toolbar.grid(row=0, column=0, sticky="nesw")

        # Grid main_window
        self.main_window.grid(row=1, column=0, sticky="nesw")


# Check that this module is the one being run. Create DoTeX application window and run mainloop
if __name__ == "__main__":
    app = DoTeX()
    app.mainloop()
