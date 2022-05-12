"""Define MainWindow class.

Classes
-------
MainWindow
    Configures MainWindow frame.
"""
import tkinter as tk
from tkinter import ttk
from .main_window_frames import TexEditor, PDFViewer


class MainWindow(ttk.Frame):
    """A class configuring MainWindow frame; also creates PDFViewer and TexEditor frames.

    Attributes
    ----------
    pdf_viewer_frame : PDFViewer(container)
        a PDFViewer frame
    tex_editor_frame : TexEditor(container)
        a TexEditor frame
    """

    def __init__(self, container, **kwargs):
        """Initialises MainWindow frame.

        Takes *args and **kwargs and passes them to parent tk.Tk class constructor. Initialises tk.Tk object.
        Configures DoTeX geometry, title and grid manager, and ttk styles. Creates MainWindow and Toolbar frames.

        Parameters
        ----------
        self
            MainWindow object
        container : widget object
            Master widget
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create and pack PanedWindow named paned_window with MainWindow as master, to contain PDFViewer and TexEditor
        # frames. Orient horizontal so child frame are arranged side by side
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(side="left", fill="both", expand=True)

        # Create PDFViewer frame named pdf_viewer_frame and TexEditor frame named tex_editor_frame, with paned_window as
        # masters. Pass pdf_viewer_frame as controller to tex_editor_frame
        self.pdf_viewer_frame = PDFViewer(paned_window)
        self.tex_editor_frame = TexEditor(paned_window, self.pdf_viewer_frame)

        # Add tex_editor_frame and pdf_viewer_frame to paned_window with equal weight
        paned_window.add(self.tex_editor_frame, weight=1)
        paned_window.add(self.pdf_viewer_frame, weight=1)
