"""Define TexToolButtonsFrame class.

Classes
-------
TexToolButtonsFrame
    Configures TexToolButtonsFrame frame.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
from .tex_editor_inner_frames import TexToolButtons
from .tex_error_container import TexErrorContainer
import shutil
from files import constants as cons


class TexToolButtonsFrame(ttk.Frame):
    """A class configuring TexToolButtonsFrame frame; also creates TexToolButtons frame

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    pdf_controller : widget object
        a reference to PDFViewer object in master widget object to provide access to its attributes/methods
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
    tex_tool_buttons : TexToolButtons()
        a frame to contain tool buttons

    Methods
    -------
    load_tex()
        Opens filedialog for user to select TeX file and loads content into scrolled text box
    save()
        Overwrites loaded TeX file with content of scrolled text box. Returns True if saved.
    save_as()
        Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text box.
        Returns True if saved.
    check_saved()
        Checks if TexEditorFrame has file name associated by returning result of self.save_as()
    compile_pdf(blank: bool = False)
        Compiles loaded TeX file using pdflatex and bibtex
    _load_compiled_pdf(self, blank: bool, pdf_file_name)
        Loads compiled PDF into PDF frame
    _move_log_file(self, log_file_name)
        Moves log file to log directory and returns file path
    _delete_temp_files()
        Deletes temporary files generated during compile
    close_tex()
        Clears scrolled text box and disassociates loaded Tex file with TexEditorFrame
    """

    def __init__(self, container, controller, pdf_controller, **kwargs):
        """Initialises TexToolButtonsFrame frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates frames.

        Parameters
        ----------
        self
            TexToolButtonsFrame object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        pdf_controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)
        # Create reference to TexEditor object to provide access to its attributes/methods
        self.controller = controller
        # Create reference to PDFViewer object to provide access to its attributes/methods
        self.pdf_controller = pdf_controller

        # Create references to directories
        self.tex_dir = cons.TEX_DIRECTORY
        self.pdf_dir = cons.PDF_DIRECTORY
        self.log_dir = cons.LOG_DIRECTORY
        self.pdflatex = cons.PDFLATEX_PATH
        self.bibtex = cons.BIBTEX_PATH

        # Make row 0 and column 0 fill all available space
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create TexToolButtons frame named tex_tool_buttons
        self.tex_tool_buttons = TexToolButtons(self, self)
        self.tex_tool_buttons.grid(row=0, column=0, sticky="ns")

    def load_tex(self):
        """Opens filedialog for user to select TeX file and loads content into scrolled text box"""
        # Open filedialog for user to select Tex file
        tex_file = filedialog.askopenfilename(
            title="Select a TeX file",
            initialdir=self.tex_dir,
            filetypes=(("TeX Files (*.tex)", "*.tex"), ("All Files", "*.*"))
        )
        # Check that tex file was selected
        if tex_file and ".tex" in tex_file:
            # Set tex file path
            self.controller.visible_tex_frame.tex_file = tex_file
            # Clear scrolled text box
            self.controller.visible_tex_frame.tex_editor.delete(1.0, "end")

            # Load content of tex vile into scrolled text box
            with open(self.controller.visible_tex_frame.tex_file, 'r') as read_content:
                tex_content = read_content.read()
            self.controller.visible_tex_frame.tex_editor.insert(1.0, tex_content)

            # Set tex file name
            tex_file_path, tex_file_name = os.path.split(self.controller.visible_tex_frame.tex_file)
            self.controller.visible_tex_frame.tex_file_name.set(
                tex_file_name.split(".")[0]
            )

    def save(self):
        """Overwrites loaded TeX file with content of scrolled text box. Returns True if saved.

        If not associated with a file calls self.save_as()

        Returns
        -------
        saved : bool
            True if file is saved
        """
        tex_content = self.controller.visible_tex_frame.tex_editor.get(1.0, "end-1c")
        try:
            with open(self.controller.visible_tex_frame.tex_file, 'w') as output:
                output.write(tex_content)
            return True
        except FileNotFoundError:
            saved = self.save_as()
            return saved

    def save_as(self):
        """Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text
        box

        Returns
        -------
        saved : bool
            True if file is saved
        """
        tex_file = tk.filedialog.asksaveasfilename(
            title="Save TeX file As",
            initialdir=self.tex_dir,
            initialfile="untitled_tex_file",
            filetypes=(("TeX documents (*.tex)", "*.tex"), ("All Files", "*.*")),
            defaultextension=".tex"
        )

        if tex_file:
            self.controller.visible_tex_frame.tex_file = tex_file
            tex_content = self.controller.visible_tex_frame.tex_editor.get(1.0, "end-1c")
            if self.controller.visible_tex_frame.tex_file:
                tex_file_path, tex_file_name = os.path.split(self.controller.visible_tex_frame.tex_file)
                self.controller.visible_tex_frame.tex_file_name.set(
                    tex_file_name.split(".")[0]
                )
                with open(self.controller.visible_tex_frame.tex_file, 'w') as output:
                    output.write(tex_content)
                return True

    def check_saved(self):
        """Checks if TexEditorFrame has file name associated"""
        return self.save()

    def compile_pdf(self, blank: bool = False):
        """Compiles loaded TeX file using pdflatex and bibtex

        If compile errors, creates TexErrorContainer and calls retrieve_error_message insided it. If succesful calls
        self._load_compiled_pdf

        Parameters
        ----------
        blank : bool
            Indicates if user selected to compile to a blank PDF viewer tab. If not specified defaults to False
        """
        if self.check_saved():
            # Check if a bib file is loaded or the bib editor is not empty
            if self.controller.visible_tex_frame.bib_file or not self.controller.visible_tex_frame.check_bib_empty():
                # Check that bib content is saved
                if not self.controller.visible_tex_frame.check_bib_saved():
                    return
            # Close error container if open
            if self.controller.error_container:
                self.controller.error_container.error_close()
            # Format tex file name
            tex_file_path, tex_file_name = os.path.split(self.controller.visible_tex_frame.tex_file)
            # Copy tex file to DoTeX root directory
            with open(self.controller.visible_tex_frame.tex_file, 'r') as output:
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
                # If compile successful run bibtex, then run pdflatex twice more
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
            # If pdflatex compile unsuccessful create TexErrorContainer and add to tex paned window, move log file to
            # log directory and retrieve error messages from log
            if exit_code != 0:
                log_file_name = f"{pdf_file_name}.log"
                log_file_path = self._move_log_file(log_file_name)

                self.controller.error_container = TexErrorContainer(
                        self.controller.tex_paned_window,
                        self.controller
                    )
                self.controller.tex_paned_window.add(self.controller.error_container)

                self.controller.error_container.retrieve_error_message(
                    log_file_name,
                    log_file_path,
                    self.controller.visible_tex_frame.tex_file,
                    tex_file_name
                )
            # If compile successful call self._load_compiled_pdf to load PDF into PDF viewer
            else:
                self._load_compiled_pdf(blank, pdf_file_name)

    def _load_compiled_pdf(self, blank: bool, pdf_file_name):
        """Loads compiled PDF into PDF frame

        Copies resultant PDF file to pdf directory. If user used Compile button, sets pdf path and loads pdf in visible
        PDF frame. If they used Compile (Blank Tab) checks if the currently visible PDF frame is empty and if so sets
        PDF path and loads PDF in it. If not, opens new PDF frame and sets PDF path and loads PDF there.

        Parameters
        ----------
        blank : bool
            Indicates if user selected to compile to a blank PDF viewer tab.
        pdf_file_name : str
            Name of resultant PDF file from compile
        """
        # Move resultant PDF file to pdf directory
        pdf_file = f"{pdf_file_name}.pdf"
        pdf_file_path = f"{self.pdf_dir}/{pdf_file}"
        shutil.move(pdf_file, pdf_file_path)

        if blank:
            if self.pdf_controller.visible_pdf_frame.pdf_image:
                self.pdf_controller.pdf_switch_buttons_frame.new_pdf_frame()
                self.pdf_controller.visible_pdf_frame.set_pdf_path(pdf_file_path)
                self.pdf_controller.visible_pdf_frame.load_pdf()
            else:
                self.pdf_controller.visible_pdf_frame.set_pdf_path(pdf_file_path)
                self.pdf_controller.visible_pdf_frame.load_pdf()
        else:
            self.pdf_controller.visible_pdf_frame.set_pdf_path(pdf_file_path)
            self.pdf_controller.visible_pdf_frame.load_pdf()

        self._delete_temp_files()

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

    def close_tex(self):
        """Clears scrolled text box and disassociates loaded Tex file with TexEditorFrame"""
        self.controller.visible_tex_frame.tex_editor.delete(1.0, "end")
        self.controller.visible_tex_frame.tex_file_name.set("Blank")
        self.controller.visible_tex_frame.tex_file = ""
