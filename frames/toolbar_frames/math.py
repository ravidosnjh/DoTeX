"""Define Math class.

Classes
-------
Math
    Configures Math frame.
"""
import tkinter as tk
from tkinter import ttk
from .toolbar_inner_frames import Fraction, Matrix, OperatorsMenu, Brackets, SaveEquation
from functools import partial
from files import saved_equations


class Math(ttk.Frame):
    """A class configuring Math frame; also creates Brackets and OperatorsMenu menus.

    Attributes
    ----------
    controller : widget object
        a reference to master widget object to provide access to its attributes/methods
    frac : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    integral : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    cyclic_integral : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    binomial : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    sum : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    product : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    coproduct : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    limit : tk.PhotoImage(file)
        a reference to Image object so image is not garbage collected
    fraction : Fraction()
        a Fraction toplevel window
    matrix : Matrix()
        a Matrix toplevel window
    save_equation : SaveEquation()
        a SaveEquation toplevel window

    Methods
    -------
    insert_amsmath()
        Inserts LaTeX command for amsmath package in currently visible scrolled text box
    insert_inline()
        Inserts LaTeX commands for inline mode in currently visible scrolled text box
    insert_display()
        Inserts LaTeX commands for display mode in currently visible scrolled text box
    superscript()
        Inserts LaTeX command for supersript in currently visible scrolled text box
    subscript()
        Inserts LaTeX command for subscript in currently visible scrolled text box
    insert_frac()
        Inserts LaTeX command for fraction in currently visible scrolled text box
    launch_fraction()
        Creates Fraction toplevel window
    insert_binomial()
        Inserts LaTeX command for binomial in currently visible scrolled text box
    launch_matrix()
        Creates Matrix toplevel window
    insert_integral()
        Inserts LaTeX command for integral in currently visible scrolled text box
    insert_cylic_integral()
        Inserts LaTeX command for cylic integral in currently visible scrolled text box
    insert_sum()
        Inserts LaTeX command for sum in currently visible scrolled text box
    insert_product()
        Inserts LaTeX command for product in currently visible scrolled text box
    insert_coproduct()
        Inserts LaTeX command for coproduct in currently visible scrolled text box
    insert_limit()
        Inserts LaTeX command for limit in currently visible scrolled text box
    create_equation(numbered)
        Inserts LaTeX commands for equation environment in currently visible scrolled text box
    label()
        Inserts LaTeX command for label in currently visible scrolled text box
    align()
        Inserts LaTeX commands for align environment in currently visible scrolled text box
    gather()
        Inserts LaTeX commands for gather environment in currently visible scrolled text box
    multiline()
        Inserts LaTeX commands for multiline environment in currently visible scrolled text box
    launch_save_equation()
        Creates SaveEquation toplevel window
    load_saved_equations()
        Reads saved equations from saved_equations.py and adds as commands to saved_equations_button_menu
    insert_equation(equation)
        Inserts value of equation in currently visible scrolled text box
    delete_equation(equation)
        Deletes equation from saved_equations.py and saved_equations_button_menu
    """

    def __init__(self, container, controller, **kwargs):
        """Initialises Math frame.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates toolbar buttons, and Brackets and OperatorsMenu menus.

        Parameters
        ----------
        self
            Math object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create reference to Toolbar object to provide access to its attributes/methods
        self.controller = controller

        # Create references to images, so they aren't garbage collected. To be used as icons on buttons
        self.frac = tk.PhotoImage(file=r"assets/fraction.png")
        self.integral = tk.PhotoImage(file=r"assets/integral.png")
        self.cyclic_integral = tk.PhotoImage(file=r"assets/cyclic_integral.png")
        self.binomial = tk.PhotoImage(file=r"assets/binomial.png")
        self.sum = tk.PhotoImage(file=r"assets/sum.png")
        self.product = tk.PhotoImage(file=r"assets/product.png")
        self.coproduct = tk.PhotoImage(file=r"assets/coproduct.png")
        self.limit = tk.PhotoImage(file=r"assets/limit.png")

        # Make row 0 fill all available space
        self.rowconfigure(0, weight=1)

        # Create toolbar buttons
        amsmath_button = ttk.Button(
            self,
            text="Use amsmath Package",
            command=self.insert_amsmath
        )

        inline_button = ttk.Button(
            self,
            text="Inline Mode",
            command=self.insert_inline
        )

        display_button = ttk.Button(
            self,
            text="Display Mode",
            command=self.insert_display
        )

        brackets_button = ttk.Menubutton(
            self,
            text="Brackets",
            width=8
        )
        # Create Brackets menu and associate with brackets menubutton
        brackets_button_menu = Brackets(brackets_button, self.controller, tearoff=False)
        brackets_button.config(menu=brackets_button_menu)

        superscript = ttk.Button(
            self,
            text="x\N{SUPERSCRIPT TWO}",
            command=self.superscript,
            padding=(-18, 0)
        )

        subscript = ttk.Button(
            self,
            text="x\N{SUBSCRIPT TWO}",
            command=self.subscript,
            padding=(-18, 0)
        )

        frac = ttk.Button(
            self,
            image=self.frac,
            command=self.insert_frac,
            padding=(0, 0)
        )

        self.fraction = None

        launch_fraction = ttk.Button(
            self,
            text="Fraction",
            command=self.launch_fraction
        )

        binomial = ttk.Button(
            self,
            image=self.binomial,
            command=self.insert_binomial,
            padding=(0, 0)
        )

        self.matrix = None

        matrix_button = ttk.Button(
            self,
            text="Matrix",
            command=self.launch_matrix
        )

        integral = ttk.Button(
            self,
            image=self.integral,
            command=self.insert_integral,
            padding=(0, 0)
        )

        cylic_integral = ttk.Button(
            self,
            image=self.cyclic_integral,
            command=self.insert_cyclic_integral,
            padding=(0, 0)
        )

        sum = ttk.Button(
            self,
            image=self.sum,
            command=self.insert_sum,
            padding=(0, 0)
        )

        product = ttk.Button(
            self,
            image=self.product,
            command=self.insert_product,
            padding=(0, 0)
        )

        coproduct = ttk.Button(
            self,
            image=self.coproduct,
            command=self.insert_coproduct,
            padding=(0, 0)
        )

        limit = ttk.Button(
            self,
            image=self.limit,
            command=self.insert_limit,
            padding=(0, 0)
        )

        equation_button = ttk.Menubutton(
            self,
            text="Create Equation"
        )
        # Create equation menu and associate with equation menubutton
        equation_button_menu = tk.Menu(equation_button, tearoff=False)
        equation_button.config(menu=equation_button_menu)
        # Add commands to equation menu
        numbered_p = partial(self.create_equation, True)
        equation_button_menu.add_command(
            label="Numbered Equation",
            command=numbered_p
        )
        unnumbered_p = partial(self.create_equation, False)
        equation_button_menu.add_command(
            label="Unnumbered Equation",
            command=unnumbered_p
        )
        equation_button_menu.add_command(
            label="Label",
            command=self.label
        )
        equation_button_menu.add_command(
            label="Align",
            command=self.align
        )
        equation_button_menu.add_command(
            label="Gather",
            command=self.gather
        )
        equation_button_menu.add_command(
            label="Multiline",
            command=self.multiline
        )

        self.save_equation = None

        save_equation = ttk.Button(
            self,
            text="Save Equation",
            command=self.launch_save_equation
        )

        saved_equations_button = ttk.Menubutton(
            self,
            text="Saved Equations"
        )
        # Create saved equations menu and associate with saved equations menubutton
        self.saved_equations_button_menu = tk.Menu(saved_equations_button, tearoff=False)
        saved_equations_button.config(menu=self.saved_equations_button_menu)

        # Populate saved equations menu
        self.load_saved_equations()

        operators_button = ttk.Menubutton(
            self,
            text="All Operators"
        )
        # Create OperatorsMenu menu and associate with section menubutton
        operators_button_menu = OperatorsMenu(operators_button, self.controller, tearoff=False)
        operators_button.config(menu=operators_button_menu)

        # Grid widgets in Math
        count = 0
        for widget in self.winfo_children():
            widget.grid(row=0, column=count, sticky="nesw")
            count += 1

    def insert_amsmath(self):
        """Inserts LaTeX command for amsmath package in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for amsmath package at second line of text box.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert("2.0", "\n\\usepackage{amsmath}\n")

    def insert_inline(self):
        """Inserts LaTeX commands for inline mode in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for inline mode at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\( \\)")

    def insert_display(self):
        """Inserts LaTeX commands for display mode in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for display mode at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\[ \\]")

    def superscript(self):
        """Inserts LaTeX command for superscript in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for superscript at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "^")

    def subscript(self):
        """Inserts LaTeX command for subscript in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for subscript at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "_")

    def insert_frac(self):
        """Inserts LaTeX command for fraction in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for fraction at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\frac{num}{denom}")

    def launch_fraction(self):
        """If fraction exists destroys it. Creates Fraction toplevel window named fraction."""
        if self.fraction:
            self.fraction.close()
        self.fraction = Fraction(self.controller)

    def insert_binomial(self):
        """Inserts LaTeX command for binomial in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for binomial at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\binom{num}{denom}")

    def launch_matrix(self):
        """If matrix exists destroys it. Creates Matrix toplevel window named matrix."""
        if self.matrix:
            self.matrix.close()
        self.matrix = Matrix(self.controller)

    def insert_integral(self):
        """Inserts LaTeX command for integral in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for integral at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\int_{lower}^{upper}")

    def insert_cyclic_integral(self):
        """Inserts LaTeX command for cylic integral in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for cylic integral at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\oint_{lower}")

    def insert_sum(self):
        """Inserts LaTeX command for sum in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for sum at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\sum_{lower}^{upper}")

    def insert_product(self):
        """Inserts LaTeX command for product in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for product at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\prod_{lower}^{upper}")

    def insert_coproduct(self):
        """Inserts LaTeX command for coproduct in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for coproduct at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\coprod_{lower}^{upper}")

    def insert_limit(self):
        """Inserts LaTeX command for limit in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for limit at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\lim_{lower}")

    def create_equation(self, numbered):
        """Inserts LaTeX commands for numbered or unnumbered equation in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. If numbered
        = True inserts LaTeX code for numbered section at current cursor position. Else inserts code for unnumbered
        equation. Value of numbered determined by which menu command selected.

        Parameters
        ----------
        numbered : bool
            value determining if numbered or unnumbered equation selected
        """
        current_editor = self.controller.check_current_editor()
        if numbered:
            insert = "\\begin{equation}\n\n\\end{equation}\n"
        else:
            insert = "\\begin{equation*}\n\n\\end{equation*}\n"
        current_editor.insert(tk.INSERT, insert)

    def label(self):
        """Inserts LaTeX command for label in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for label at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\label{}")

    def align(self):
        """Inserts LaTeX commands for align environment in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for align environment at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{align*}\n\n\\end{align*}\n")

    def gather(self):
        """Inserts LaTeX command for gather environment in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for gather environment at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{gather*}\n\n\\end{gather*}\n")

    def multiline(self):
        """Inserts LaTeX command for multiline environment in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts LaTeX
        code for multiline environment at current cursor position.
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, "\\begin{multiline*}\n\n\\end{multiline*}\n")

    def launch_save_equation(self):
        """If save_equation exists destroys it. Creates SaveEquation toplevel window named save_equation."""
        if self.save_equation:
            self.save_equation.close()
        self.save_equation = SaveEquation(self)

    def load_saved_equations(self):
        """Reads saved equations from saved_equations.py and adds as commands to saved_equations_button_menu

        For each key:value pair in the equations dictionary inside the file files/saved_equations.py, adds a menu with
        commands to insert the equation code into the currently visible editor or delete the key:value pair from the
        dictionary
        """
        try:
            for name, equation in saved_equations.equations.items():
                # Create menu inside saved equations menu for name:equation entry in dictionary
                equation_sub_menu = tk.Menu(self.saved_equations_button_menu, tearoff=0)
                self.saved_equations_button_menu.add_cascade(
                    label=name,
                    menu=equation_sub_menu
                )

                equation_p = partial(self.insert_equation, equation)
                equation_delete_p = partial(self.delete_equation, name)
                equation_sub_menu.add_command(
                    label="Insert",
                    command=equation_p
                )
                equation_sub_menu.add_command(
                    label="Delete",
                    command=equation_delete_p
                )
        except FileNotFoundError:
            pass
        except AttributeError:
            pass

    def insert_equation(self, equation):
        """Inserts value of equation in currently visible scrolled text box

        Calls check_current_editor() method from controller and assigns return to current editor. This returns the
        scrolled text box widget in the currently selected tab in the currently visible tex editor frame. Inserts value
        of equation, determined by which saved equation is chosen, at current cursor position.

        Parameters
        ----------
        equation : str
            LaTeX code to insert
        """
        current_editor = self.controller.check_current_editor()
        current_editor.insert(tk.INSERT, equation)

    def delete_equation(self, equation):
        """Deletes equation from saved_equations.py and saved_equations_button_menu

        Removes the entry from the equations dictionary inside the file files/saved_equations.py with key equal to the
        value of equation argument. Opens the saved_equations.py file and overwrites its contents with the updated
        dictionary. Deletes the menu with name equal to the value of equation from the saved equations menu

        Parameters
        ----------
        equation : str
            LaTeX code to insert
        """
        equations = saved_equations.equations
        equations.pop(equation)
        file = open("files/saved_equations.py", "w")
        file.write(f"equations = {equations}")
        file.close()
        self.saved_equations_button_menu.delete(equation)
