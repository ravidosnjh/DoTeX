"""Define Images class.

Classes
-------
Images
    Configures Images toplevel window.
"""
import tkinter as tk
from tkinter import ttk
import os
from files import constants as cons
from PIL import Image, ImageTk
from functools import partial
from tkinter import filedialog
import shutil


class Images(tk.Toplevel):
    """A class configuring Images toplevel window.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    pictures_dir : str
        a reference to pictures directory from files/constants.py
    images : dict
        dictionary containing references to images so they are not garbage collected
    chosen_image : str
        stringvar containing name of image chosen by user
    scale : int
        intvar containing scale entered by user
    width : int
        intvar containing width entered by user
    width_unit : str
        stringvar containing width_unit entered by user
    height : int
        intvar containing height entered by user
    height_unit : str
        stringvar containing height_unit entered by user
    angle : int
        intvar containing angle entered by user
    position : str
        stringvar containing position entered by user
    alignment : str
        stringvar containing alignment entered by user
    caption_check : int
        intvar indicating if caption checkbox has been ticked
    caption_position : str
        stringvar containing caption position entered by user
    entered_label : str
        stringvar containing label entered by user
    image_frame : ttk.Frame()
        frame to contain image gallery
    insert_button = ttk.Button()
        button inserting LaTeX code into currently visible tex editor

    Methods
    -------
    display_images()
        Loads image files from pictures directory and displays in gallery
    browse()
        Opens filedialog for user to select image file; copies selected file to pictures directory
    set_image(file_name)
        Sets chosen_image attribute to image file selected by user
    insert_image()
        Inserts LaTex code for image in currently visible scrolled text box
    reset_options()
        Resets entry field attributes to default values
    close()
        Destroys Images toplevel window
    """

    def __init__(self, controller):
        """Initialises Images toplevel window.

        Initialises tk.Toplevel object and sets window title. Creates necessary attributes and sets to default values.
        Displays images in gallery and creates buttons and entry boxes.

        Parameters
        ----------
        self
            Images object
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        """
        super().__init__()

        # Set window title, and make window not resizable
        self.title("Insert an Image")
        self.resizable(False, False)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller
        # Create reference to pictures directory
        self.pictures_dir = cons.PICTURES_PATH
        # Create dictionary to store image references so they are not garbage collected
        self.images = dict()

        # Create IntVar and StringVars and set default values
        self.chosen_image = tk.StringVar(value="")
        self.scale = tk.IntVar(value=0)
        self.width = tk.IntVar(value=0)
        self.width_unit = tk.StringVar(value="")
        self.height = tk.IntVar(value=0)
        self.height_unit = tk.StringVar(value="")
        self.angle = tk.IntVar(value=0)
        self.position = tk.StringVar(value="")
        self.alignment = tk.StringVar(value="")
        self.caption_check = tk.IntVar(value=0)
        self.caption_position = tk.StringVar(value="")
        self.entered_label = tk.StringVar(value="")

        # Make row 1 fill all available space
        self.rowconfigure(1, weight=1)

        # Create label indicating where code will be inserted
        label = tk.Label(self, text="Images insert at cursor position")
        label.grid(row=0, column=0, columnspan=5, sticky="ns")

        # Define image_frame attribute
        self.image_frame = None

        # Call self.display_images() method to create image gallery frame and display images from pictures directory in
        # it
        self.display_images()

        # Create frame to contain option fields user can configure
        options_frame = ttk.Frame(self)
        options_frame.grid(row=2, column=0, columnspan=5, sticky="nesw", pady="5")

        # Make options frame columns 1, 3, 6 and 9 fill all available space
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        options_frame.columnconfigure(6, weight=1)
        options_frame.columnconfigure(9, weight=1)

        # Create labels and entry boxes for image parameters user can configure
        entry = ttk.Entry(
            options_frame,
            textvariable=self.chosen_image,
            width=40,
            justify="center",
            state="disabled"
        )
        entry.grid(row=0, column=0, columnspan=10, sticky="ns", pady=5)

        scale_label = ttk.Label(
            options_frame,
            text="Scale: ",
            padding=(5, 0)
        )
        scale_label.grid(row=1, column=0, sticky="ns", pady=5)

        scale = ttk.Spinbox(
            options_frame,
            textvariable=self.scale,
            from_=0,
            to=100,
            justify="center"
        )
        scale.grid(row=1, column=1, sticky="nesw")

        width_label = ttk.Label(
            options_frame,
            text="Width: ",
            padding=(5, 0)
        )
        width_label.grid(row=1, column=2, sticky="ns")

        width = ttk.Spinbox(
            options_frame,
            textvariable=self.width,
            from_=0,
            to=1000,
            justify="center"
        )
        width.grid(row=1, column=3, sticky="nesw")

        width_unit = ttk.Combobox(
            options_frame,
            textvariable=self.width_unit,
            width=14,
            state="readonly"
        )
        # Add width unit options to combobox
        width_unit.config(values=("pt", "cm", "in", "ex", "m", "\\columnsep", "\\columnwidth", "\\linewidth",
                                  "\\paperwidth", "\\textwidth", "\\unitlength"))
        width_unit.grid(row=1, column=4, sticky="n")

        height_label = ttk.Label(
            options_frame,
            text="Height: ",
            padding=(5, 0)
        )
        height_label.grid(row=1, column=5, sticky="ns")

        height = ttk.Spinbox(
            options_frame,
            textvariable=self.height,
            from_=0,
            to=1000,
            justify="center"
        )
        height.grid(row=1, column=6, sticky="nesw")

        height_unit = ttk.Combobox(
            options_frame,
            textvariable=self.height_unit,
            width=10,
            state="readonly"
        )
        # Add height unit options to combobox
        height_unit.config(values=("pt", "cm", "in", "ex", "m", "\\paperheight", "\\textheight", "\\unitlength"))
        height_unit.grid(row=1, column=7, sticky="n")

        angle_label = ttk.Label(
            options_frame,
            text="Angle: ",
            padding=(5, 0)
        )
        angle_label.grid(row=1, column=8, sticky="nesw")

        angle = ttk.Spinbox(
            options_frame,
            textvariable=self.angle,
            from_=0,
            to=360,
            justify="center"
        )
        angle.grid(row=1, column=9, sticky="ns", padx=(0, 5))

        position_label = ttk.Label(
            options_frame,
            text="Position: ",
            padding=(5, 0)
        )
        position_label.grid(row=2, column=0, sticky="ns")

        position = ttk.Combobox(
            options_frame,
            textvariable=self.position,
            width=10,
            state="readonly"
        )
        # Add position options to combobox
        position.config(values=("Here", "Top of Page", "Bottom of Page", "Special Page"))
        position.grid(row=2, column=1, sticky="nesw")

        alignment_label = ttk.Label(
            options_frame,
            text="Alignment: ",
            padding=(5, 0),
        )
        alignment_label.grid(row=2, column=2, sticky="ns")

        alignment = ttk.Combobox(
            options_frame,
            textvariable=self.alignment,
            width=10,
            state="readonly"
        )
        # Add alignment options to combobox
        alignment.config(values=("\\centering", "None"))
        alignment.grid(row=2, column=3, sticky="nesw")

        caption_checkbox = ttk.Checkbutton(
            options_frame,
            text="Caption",
            variable=self.caption_check,
            onvalue=1,
            offvalue=0
        )
        caption_checkbox.grid(row=2, column=5, sticky="ns")

        caption_label = ttk.Label(
            options_frame,
            text="Above/Below Image: ",
            padding=(5, 0)
        )
        caption_label.grid(row=2, column=6, sticky="ns")

        caption_position = ttk.Combobox(
            options_frame,
            textvariable=self.caption_position,
            width=7,
            state="readonly"
        )
        # Add caption position options to combobox
        caption_position.config(values=("Above", "Below"))
        caption_position.grid(row=2, column=7, sticky="nesw")

        label_label = ttk.Label(
            options_frame,
            text="Label: ",
            padding=(5, 0)
        )
        label_label.grid(row=2, column=8, sticky="ns")

        label_entry = ttk.Entry(
            options_frame,
            textvariable=self.entered_label,
        )
        label_entry.grid(row=2, column=9, sticky="nesw", padx=(0, 5))

        packages_label = tk.Label(
            self,
            text="Suggested packages: floatrow, wrapfig, sidecap, epstopdf",
            justify="center"
        )
        packages_label.grid(row=3, column=0, columnspan=5, sticky="ns", pady=5)

        browse_button = ttk.Button(
            self,
            text="Browse",
            command=self.browse
        )
        browse_button.grid(row=4, column=0, sticky="ns")

        refresh_button = ttk.Button(
            self,
            text="Refresh Images",
            command=self.display_images
        )
        refresh_button.grid(row=4, column=1, sticky="ns")

        # Create insert, reset and close buttons
        self.insert_button = ttk.Button(
            self,
            text="Insert",
            command=self.insert_image,
            state="disabled"
        )
        self.insert_button.grid(row=4, column=2, sticky="ns")

        reset_options_button = ttk.Button(
            self,
            text="Reset Options",
            command=self.reset_options
        )
        reset_options_button.grid(row=4, column=3, sticky="ns")

        close_button = ttk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.grid(row=4, column=4, sticky="ns")

    def display_images(self):
        """Loads image files from pictures directory and displays in gallery

        Creates image frame. Reads image files from pictures directory. Creates Image objects and resizes them to
        150x100. Displays images as buttons in image frame,
        """
        # If image frame exists destroy it
        if self.image_frame:
            self.image_frame.destroy()

        # Create image frame to contain images
        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(row=1, column=0, columnspan=5, sticky="nesw")

        # Load files from pictures directory and create Image objects resized to 150x100. Create buttons with images in
        # images frame
        count, count1, count2, count3, count4, count5 = 0, 0, 0, 0, 0, 0
        # Load files form pictures directory
        for file in os.listdir(self.pictures_dir):
            file_name = file.split(".")[0]
            file_path = f"{self.pictures_dir}/{file}"
            # Create Image object and resize
            image = Image.open(file_path)
            r_image = image.resize((150, 100))
            image = ImageTk.PhotoImage(r_image)
            # Add image to images dictionary so it is not garbage collected
            self.images[file] = image

            # Created button to display image and set chosen_image to image name
            picture_p = partial(self.set_image, file_name)
            button = ttk.Button(
                self.image_frame,
                image=image,
                command=picture_p
            )
            # Grid 6 images per row
            if count <= 5:
                button.grid(row=0, column=count, sticky="nesw", padx=10, pady=10)
            elif count <= 11:
                button.grid(row=1, column=count1, sticky="nesw", padx=10, pady=10)
                count1 += 1
            elif count <= 17:
                button.grid(row=2, column=count2, sticky="nesw", padx=10, pady=10)
                count2 += 1
            elif count <= 23:
                button.grid(row=3, column=count3, sticky="nesw", padx=10, pady=10)
                count3 += 1
            elif count <= 29:
                button.grid(row=4, column=count4, sticky="nesw", padx=10, pady=10)
                count4 += 1
            elif count <= 35:
                button.grid(row=5, column=count5, sticky="nesw", padx=10, pady=10)
                count5 += 1
            else:
                break
            count += 1

    def browse(self):
        """Opens filedialog for user to select image file; copies selected file to pictures directory"""
        # Open filedialog for user to select image file
        file = tk.filedialog.askopenfilename(
            title="Select an Image",
            initialdir=self.pictures_dir,
            filetypes=(("JPEG (*.jpg)", "*.jpg"), ("PNG (*.png)", "*.png"), ("PDF (*.pdf)", "*.pdf"),
                       ("All Files", "*.*"))
        )
        # Copy image file to pictures directory if it is not already there
        try:
            shutil.copy(file, self.pictures_dir)
        except shutil.SameFileError:
            pass
        file_path, file_name = os.path.split(file)
        file_name = file_name.split(".")[0]
        # Call self.set_image to set chosen_image attribute to image file name
        self.set_image(file_name)
        # Make insert button active
        self.insert_button.config(state="normal")

    def set_image(self, file_name):
        """Sets chosen_image attribute to image file selected by user"""
        self.chosen_image.set(file_name)
        self.insert_button.config(state="normal")

    def insert_image(self):
        """Inserts LaTex code for image in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Formats code
        for image chosen by user with parameters entered, and inserts at current cursor position
        """
        current_editor = self.controller.check_current_editor()
        insert, scale, height, width, angle = "", "", "", "", ""
        # Format code for position entered if entered
        position = self.position.get()
        if position == "Here":
            position = "h"
        elif position == "Top of Page":
            position = "t"
        elif position == "Bottom of Page":
            position = "b"
        elif position == "Special Page":
            position = "p"

        # Format code for scale, width, height and angle entered if entered
        if self.scale.get():
            scale = f"scale={self.scale.get()},"
        if self.width.get():
            width = f"width={self.width.get()}{self.width_unit.get()},"
        if self.height.get():
            height = f"height={self.height.get()}{self.height_unit.get()},"
        if self.angle.get():
            angle = f"angle={self.angle.get()}"

        # Create code for image and position if entered
        if position:
            insert = f"\\begin{{figure}}[{position}]\n"
        else:
            insert = f"\\begin{{figure}}\n"

        # Add code for alignment if entered
        if self.alignment.get() and self.alignment.get() != "None":
            insert += f"    {self.alignment.get()}\n"

        # Add code for caption if selected and position is above
        if self.caption_check.get() and self.caption_position.get() == "Above":
            insert += f"    \\caption{{Type caption here}}\n"

        # Add code for image with scale, width, height or angle if entered
        if scale or width or height or angle:
            insert += f"    \\includegraphics[{scale}{width}{height}{angle}]{{{self.chosen_image.get()}}}\n"
        else:
            insert += f"    \\includegraphics{{{self.chosen_image.get()}}}\n"

        # Add code for caption if selected and position is below
        if self.caption_check.get() and self.caption_position.get() == "Below":
            insert += f"    \\caption{{Type caption here}}\n"

        # Add code for label if entered
        if self.entered_label.get():
            insert += f"    \\label{{{self.entered_label.get()}}}\n"

        # Add code to close figure environment
        insert += "\\end{figure}\n"

        # Insert code at current cursor position
        current_editor.insert(tk.INSERT, insert)

    def reset_options(self):
        """Resets entry field attributes to default values"""
        self.insert_button.config(state="disabled")
        self.chosen_image.set("")
        self.scale.set(0)
        self.width.set(0)
        self.width_unit.set("")
        self.height.set(0)
        self.height_unit.set("")
        self.angle.set(0)
        self.position.set("")
        self.alignment.set("")
        self.caption_check.set(0)
        self.caption_position.set("")
        self.entered_label.set("")

    def close(self):
        """Destroys Images toplevel window"""
        self.destroy()
