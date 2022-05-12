"""Define PDFFrame class.

Classes
-------
PDFFrame
    Configures PDFFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from show_pdf import show_pdf as pdf
from tkinter import filedialog
from .pdf_frame_inner_frames import PDFButtonsFrame, PDFErrorContainer
import os
import subprocess
import shutil
from files import constants as cons


class PDFFrame(ttk.Frame):
    """A class configuring PDFFrame frame; also creates PDFButtonsFrame frame

    Attributes
    ----------
    initial_frame : bool
        indicates if this is the initial frame created on application launch
    tex_dir : str
        a reference to tex directory from files/constants.py
    pdf_dir : str
        a reference to pdf directory from files/constants.py
    log_dir : str
        a reference to log directory from files/constants.py
    pdflatex : str
        a reference to file path of pdflatex.exe from files/constants.py
    bibtex : str
        a reference to file path of bibtex.exe from files/constants.py
    zoom_dpi : int
        intvar containing current zoom dpi
    pdf_object : pdf.ShowPDF()
        object to create PDF image
    pdf_image : Image object
        image of pdf file
    pdf_file : str
        pdf file path
    pdf_file_name : str
        stringvar containing loaded pdf file name
    pdf_frame : ttk.Frame()
        frame to contain pdf object frame and PDFErrorContainer
    pdf_object_frame : ttk.Frame()
        frame to contain pdf object
    error_container : PDFErrorContainer()
        frame to display compile errors
    buttons_frame : PDFButtonsFrame()
        frame to contain pdf tool buttons

    Methods
    -------
    browse_pdf()
        Opens filedialog for user to select PDF file and loads PDF into viewer
    compile_from_browse()
        Opens filedialog for user to select TeX file and compiles selected TeX file using pdflatex and bibtex
    set_pdf_path(path: str)
        Sets pdf_pile to passed file path
    load_pdf(zoom_dpi: int = cons.ZOOM_DPI_DEFAULT)
        Loads PDF into PDF frame
    close_pdf()
        Removes pdf image and disassociates loaded PDF file with PDFFrame
    zoom(option: str)
        Zooms PDF in, out or to default depending on option
    handle_scale_change(event)
        Zooms PDF to dpi chosen by sliding zoom scale
    _move_log_file(self, log_file_name)
        Moves log file to log directory and returns file path
    _delete_temp_files()
        Deletes temporary files generated during compile
    """

    def __init__(self, container, initial_frame=False, **kwargs):
        """Initialises PDFFrame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            PDFFrame object
        container : widget object
            Master widget
        initial_frame : bool
            Indicates if this is the initial frame created on application launch. If not specified defaults to False
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Set whether this is initial frame created on application launch
        self.initial_frame = initial_frame

        # Set file paths from files/constants.py
        self.tex_dir = cons.TEX_DIRECTORY
        self.pdf_dir = cons.PDF_DIRECTORY
        self.log_dir = cons.LOG_DIRECTORY
        self.pdflatex = cons.PDFLATEX_PATH
        self.bibtex = cons.BIBTEX_PATH

        # Create IntVar storing PDF zoom dpi
        self.zoom_dpi = tk.IntVar(value=cons.ZOOM_DPI_DEFAULT)
        # Define pdf object and image object
        self.pdf_object = None
        self.pdf_image = None
        # Create variables for pdf file path and name
        self.pdf_file = ""
        self.pdf_file_name = tk.StringVar(value="Blank")

        # Create frame to store pdf object and error container
        self.pdf_frame = ttk.Frame(self)
        self.pdf_frame.pack(side="left", fill="both", expand=True)
        # Make PDFFrame row 0 and column 0 fill all available space
        self.pdf_frame.rowconfigure(0, weight=1)
        self.pdf_frame.columnconfigure(0, weight=1)

        # Create pdf object frame to display pdf image
        self.pdf_object_frame = ttk.Frame(self.pdf_frame)
        self.pdf_object_frame.grid(row=0, sticky="nesw")

        # Define error container
        self.error_container = None

        # Create PDFButtonsFrame named buttons_frame to contain tool buttons
        self.buttons_frame = PDFButtonsFrame(self.pdf_frame, self, self.initial_frame)
        self.buttons_frame.grid(row=1, sticky="nesw")

    def browse_pdf(self):
        """Opens filedialog for user to select PDF file and loads PDF into viewer.

        Opens filedialog for user to select PDF file and sets pdf_file to selected file path. If PDF file is selected
        calls self.load_pdf.
        """
        self.pdf_file = filedialog.askopenfilename(
            title="Select a PDF file",
            initialdir=self.pdf_dir,
            filetypes=(("PDF Files (*.pdf)", "*.pdf"), ("All Files", "*.*"))
        )
        if self.pdf_file and ".pdf" in self.pdf_file:
            self.load_pdf()

    def compile_from_browse(self):
        """Opens filedialog for user to select TeX file and compiles selected TeX file using pdflatex and bibtex."""
        # Open filedialog for user to select tex file
        tex_file = filedialog.askopenfilename(
            title="Select a TeX file",
            initialdir=self.tex_dir,
            filetypes=(("TeX Files (*.tex)", "*.tex"), ("All Files", "*.*"))
        )
        # Proceed if tex file selected
        if tex_file and ".tex" in tex_file:
            # Close error container if open
            if self.error_container:
                self.error_container.error_close()

            # Copy tex file to DoTeX root directory
            tex_file_path, tex_file_name = os.path.split(tex_file)
            with open(tex_file, 'r') as output:
                tex_content = output.read()
                with open(f"{tex_file_name}", 'w') as write_to:
                    write_to.write(tex_content)
            file = tex_file_name.split(".")[0]
            # Run pdflatex
            try:
                exit_code = subprocess.call(
                    f"{self.pdflatex} -file-line-error -interaction=nonstopmode "
                    f"\"{file}\""
                )
                # If compile successful, run bibtex and then pdflatex twice more
                if exit_code == 0:
                    subprocess.call(
                        f"{self.bibtex} \"{file}\"",
                    )
                    subprocess.call(
                        f"{self.pdflatex} -file-line-error -interaction=nonstopmode "
                        f"\"{file}\""
                    )
                    exit_code = subprocess.call(
                        f"{self.pdflatex} -file-line-error -interaction=nonstopmode "
                        f"\"{file}\""
                    )
            # Delete temp files and stop if pdflatex or bibtex not found
            except FileNotFoundError:
                self._delete_temp_files()
                return

            pdf_file_name = file
            # If compile unsuccessful create error container, move log file to log directory and retrieve error messages
            # from log
            if exit_code != 0:
                log_file_name = f"{pdf_file_name}.log"
                log_file_path = self._move_log_file(log_file_name)

                if self.initial_frame:
                    self.buttons_frame.welcome_label.place_forget()

                self.error_container = PDFErrorContainer(self.pdf_frame, self)
                self.error_container.grid(row=0, sticky="nesw")

                self.error_container.retrieve_error_message(log_file_name, log_file_path, tex_file, tex_file_name)
            # If compile successful move resultant PDF file to pdf directory, set pdf path to correct file path, load
            # the PDF and delete temporary files
            else:
                pdf_file = f"{pdf_file_name}.pdf"
                pdf_file_path = f"{self.pdf_dir}/{pdf_file}"
                shutil.move(pdf_file, pdf_file_path)
                self.set_pdf_path(pdf_file_path)
                self.load_pdf()
                self._delete_temp_files()

    def set_pdf_path(self, path: str):
        """Sets pdf_pile to passed file path.

        Parameters
        ----------
        path : str
            pdf file path
        """
        if ".pdf" in path:
            self.pdf_file = path

    def load_pdf(self, zoom_dpi: int = cons.ZOOM_DPI_DEFAULT):
        """Loads PDF into PDF frame,

        Creates pdf object and pdf image and

        Parameters
        ----------
        zoom_dpi : int
            zoom dpi to load PDF image with. If not specified defaults to default dpi from files/constants.py
        """
        # If there is a PDF loaded in the frame destroy it
        if self.pdf_image:
            self.pdf_image.destroy()

        # If there is an error container in the frame close it
        if self.error_container:
            self.error_container.error_close()

        pdf_file_path, pdf_file_name = os.path.split(self.pdf_file)
        self.pdf_file_name.set(pdf_file_name.split(".")[0])

        # If this is the default frame remove the welcome label
        if self.initial_frame:
            self.buttons_frame.welcome_label.place_forget()

        # Set button states
        self.buttons_frame.button_states_on_load()
        self.buttons_frame.button_states_on_zoom(zoom_dpi)

        # Create pdf image
        self.pdf_object = pdf.ShowPDF()
        self.pdf_object.img_object_li.clear()

        # Add pdf image to frame
        self.pdf_image = self.pdf_object.pdf_view(
            self.pdf_object_frame,
            pdf_location=self.pdf_file,
            zoom_dpi=zoom_dpi
        )
        self.pdf_image.pack(side="left", fill="both", expand=True)

    def close_pdf(self):
        """Removes pdf image and disassociates loaded PDF file with PDFFrame

        Destroys pdf image and sets to None. Sets button states and replaces welcome label if initial frame
        """
        self.pdf_image.destroy()
        self.pdf_image = None
        self.buttons_frame.button_states_on_close()
        self.pdf_file_name.set("Blank")

        if self.initial_frame:
            self.buttons_frame.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    def zoom(self, option: str):
        """Zooms PDF in, out or to default depending on option.

        Sets zoom dpi to new value based on option input and reloads pdf image with new dpi.

        Parameters
        ----------
        option : str
            indicates whether to inrease, decrease or reset zoom dpi
        """
        if option == "in":
            self.zoom_dpi.set(self.zoom_dpi.get() + 10)
        elif option == "default":
            self.zoom_dpi.set(cons.ZOOM_DPI_DEFAULT)
        elif option == "out":
            self.zoom_dpi.set(self.zoom_dpi.get() - 10)

        self.load_pdf(self.zoom_dpi.get())

    def handle_scale_change(self, event):
        """Zooms PDF to dpi chosen by sliding zoom scale"""
        self.load_pdf(self.zoom_dpi.get())

    def _move_log_file(self, log_file_name):
        """Moves log file to log directory

        Parameters
        ----------
        log_file_name : str
            Name of log file from compile

        Returns
        -------
        log_file_path : str
            New log file path after move
        """
        log_file_path = self.log_dir + "/" + log_file_name
        shutil.move(log_file_name, log_file_path)
        self._delete_temp_files()
        return log_file_path

    @staticmethod
    def _delete_temp_files():
        """Deletes temporary files generated during compile"""
        for file in os.listdir("."):
            if \
                file.endswith(".aux") \
                    or file.endswith(".bbl") \
                    or file.endswith(".blg") \
                    or file.endswith(".out") \
                    or file.endswith(".tex") \
                    or file.endswith(".log") \
                    or file.endswith(".pdf"):
                os.remove(file)
