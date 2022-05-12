"""Define Settings class.

Classes
-------
Settings
    Configures Settings toplevel window.
"""
import tkinter as tk
from tkinter import ttk
from files import constants as cons


class Settings(tk.Toplevel):
    """A class configuring Settings toplevel window.

    Attributes
    ----------
    zoom : str
        stringvar containing default zoom value from files/constants.py
    tex : str
        stringvar containing tex file directory from files/constants.py
    pdf : str
        stringvar containing pdf file directory from files/constants.py
    log : str
        stringvar containing log file directory from files/constants.py
    filtered_log : int
        stringvar containing filtered log file directory from files/constants.py
    pictures : str
        stringvar containing pictures file directory from files/constants.py

    Methods
    -------
    submit()
        Writes values entered by user to files/constants.py
    reset()
        Writes default values to files/constants.py
    close()
        Destroys Settings toplevel window
    """

    def __init__(self):
        """Initialises Settings toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Creates buttons and entry boxes.

        Parameters
        ----------
        self
            Settings object
        """
        super().__init__()

        # Set window title and make window not resizable
        self.title("Change Settings")
        self.resizable(False, False)

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create frame to contain settings configurable by user
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, columnspan=3)

        # Create IntVar and StringVars and set default values
        self.zoom = tk.IntVar(value=cons.ZOOM_DPI_DEFAULT)
        self.tex = tk.StringVar(value=cons.TEX_DIRECTORY)
        self.pdf = tk.StringVar(value=cons.PDF_DIRECTORY)
        self.log = tk.StringVar(value=cons.LOG_DIRECTORY)
        self.filtered_log = tk.StringVar(value=cons.FILTERED_LOG_DIRECTORY)
        self.pictures = tk.StringVar(value=cons.PICTURES_PATH)

        # Create labels and entry boxes for configurable settings
        zoom_label = ttk.Label(
            frame,
            text="Default PDF Zoom (10-300)",
            padding=(5, 5)
        )
        tex_label = ttk.Label(
            frame,
            text="Default TeX Directory: ",
            padding=(5, 5)
        )
        pdf_label = ttk.Label(
            frame,
            text="Default PDF Directory: ",
            padding=(5, 5)
        )
        log_label = ttk.Label(
            frame,
            text="Default Log Directory: ",
            padding=(5, 5)
        )
        filtered_log_label = ttk.Label(
            frame,
            text="Default Filtered Log Directory: ",
            padding=(5, 5)
        )
        pictures_label = ttk.Label(
            frame,
            text="Default Pictures Directory: ",
            padding=(5, 5)
        )
        zoom_entry = tk.Spinbox(
            frame,
            from_=10,
            to=300,
            textvariable=self.zoom
        )
        tex_entry = tk.Entry(
            frame,
            textvariable=self.tex
        )
        pdf_entry = tk.Entry(
            frame,
            textvariable=self.pdf
        )
        log_entry = tk.Entry(
            frame,
            textvariable=self.log
        )
        filtered_log_entry = tk.Entry(
            frame,
            textvariable=self.filtered_log
        )
        pictures_entry = tk.Entry(
            frame,
            textvariable=self.pictures
        )

        # Grid widgets in frame
        count, count1 = 1, 1
        for widget in frame.winfo_children():
            if count < 7:
                widget.grid(row=count, column=0, sticky="ns")
            else:
                widget.grid(row=count1, column=1, columnspan=2, sticky="nesw")
                count1 += 1
            count += 1

        # Create restart required label
        heading_label = ttk.Label(
            frame,
            text="Change Default Settings (Restart Required)",
            padding=(5, 5)
        )
        heading_label.grid(row=0, column=0, columnspan=3, sticky="ns")

        # Create reset, submit and close buttons
        reset_button = ttk.Button(
            self,
            text="Reset to Default",
            command=self.reset
        )
        reset_button.grid(row=1, column=0, sticky="ns")

        submit_button = ttk.Button(
            self,
            text="Submit",
            command=self.submit
        )
        submit_button.grid(row=1, column=1, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=1, column=2, sticky="ns")

    def submit(self):
        """Writes values entered by user to files/constants.py"""
        new_defaults = f"ZOOM_DPI_DEFAULT = {self.zoom.get()}\n" \
                       f"TEX_DIRECTORY = \"{self.tex.get()}\"\n" \
                       f"PDF_DIRECTORY = \"{self.pdf.get()}\"\n" \
                       f"LOG_DIRECTORY = \"{self.log.get()}\"\n" \
                       f"FILTERED_LOG_DIRECTORY = \"{self.filtered_log.get()}\"\n" \
                       f"PICTURES_PATH = \"{self.pictures.get()}\"\n" \
                       f"PDFLATEX_PATH = \"texlive/2021/bin/win32/pdflatex.exe\"\n" \
                       f"BIBTEX_PATH = \"texlive/2021/bin/win32/bibtex.exe\"\n"
        constants_file = open("files/constants.py", "r+")
        constants_file.truncate(0)
        constants_file.write(new_defaults)
        constants_file.close()

    def reset(self):
        """Writes default values to files/constants.py"""
        self.zoom.set(90)
        self.tex.set("TeX_Documents")
        self.pdf.set("PDFs")
        self.log.set("Logs")
        self.filtered_log.set("Logs/Filtered_Logs")
        self.pictures.set("Pictures")
        defaults = f"ZOOM_DPI_DEFAULT = \"{self.zoom.get()}\"\n" \
                   f"TEX_DIRECTORY = \"{self.tex.get()}\"\n" \
                   f"PDF_DIRECTORY = \"{self.pdf.get()}\"\n" \
                   f"LOG_DIRECTORY = \"{self.log.get()}\"\n" \
                   f"FILTERED_LOG_DIRECTORY = \"{self.filtered_log.get()}\"\n" \
                   f"PICTURES_PATH = \"{self.pictures.get()}\"\n" \
                   f"PDFLATEX_PATH = \"texlive/2021/bin/win32/pdflatex.exe\"\n" \
                   f"BIBTEX_PATH = \"texlive/2021/bin/win32/bibtex.exe\"\n"
        constants_file = open("files/constants.py", "r+")
        constants_file.truncate(0)
        constants_file.write(defaults)
        constants_file.close()

    def close(self):
        """Destroys Settings toplevel window"""
        self.destroy()
