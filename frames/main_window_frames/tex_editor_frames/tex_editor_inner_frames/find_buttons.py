"""Define FindButtons class.

Classes
-------
FindButtons
    Configures FindButtons frame.
"""
import tkinter as tk
from tkinter import ttk


class FindButtons(ttk.Frame):
    """A class configuring FindButtons frame.

    Attributes
    ----------
    controller : widget object
        a reference to scrolled text object to provide access to its methods
    frame_controller : widget object
        a reference to TexEditor object to provide access to its attributes/methods
    word : StringVar()
        stringvar to store string to search for
    word_replace : StringVar()
        stringvar to store string to replace with
    current_word : int
        indicates what match out of matches found is selected
    step_started : bool
        indicates whether iteration through matches has begun
    words : StringVar()
        stringvar storing number of results
    resuls_label : tk.Label
        label displaying value of words

    Methods
    -------
    find(event=None)
        Finds matches in controller for entered word
    find_next(event=None)
        Highlights next match in controller for entered word
    find_prev(event=None)
        Highlights previous match in controller for entered word
    replace()
        Replaces selected match with word_replace
    replace_all()
        Replaces all matches with word_replace
    close_find()
        Destroys FindButtons frame
    """

    def __init__(self, container, controller, frame_controller, **kwargs):
        """Initialises FindButtons.

        Takes container and **kwargs and passes them to parent ttk.Frame class constructor. Initialises ttk.Frame
        object. Creates necessary attributes. Creates entry boxes and buttons.

        Parameters
        ----------
        self
            FindButtons object
        container : widget object
            Master widget
        controller : widget object
            A reference to master widget object to provide access to its attributes/methods
        frame_controller : widget object
            A reference to TexEditor object to provide access to its attributes/methods
        **kwargs
            Arbitrary number of key word arguments
        """
        super().__init__(container, **kwargs)

        # Create references to controller objects
        self.controller = controller
        self.frame_controller = frame_controller

        # Create attributes and variables
        self.word = tk.StringVar()
        self.word_replace = tk.StringVar()
        self.words_found = 0
        self.current_word = 0
        self.step_started = False
        self.words = tk.StringVar()
        # Create configurations for tags
        self.controller.tag_config("found", background="#90EE90")
        self.controller.tag_config("found_individual", background="#30C5FF")
        self.controller.tag_config("replaced", background="yellow")

        # Create labels, entry boxes and buttons
        self.results_label = tk.Label(
            self,
            textvariable=self.words,
            background="white"
        )

        find_entry = ttk.Entry(
            self,
            takefocus=True,
            textvariable=self.word
        )
        find_entry.grid(row=0, column=1)
        find_entry.focus_set()

        search_button = ttk.Button(
            self,
            text="Find",
            command=self.find,
            padding=(-10, 0),
            cursor="arrow"
        )
        search_button.grid(row=0, column=2)
        find_entry.bind("<Return>", self.find)

        find_prev = ttk.Button(
            self,
            text="<",
            command=self.find_prev,
            padding=(-25, 0),
            cursor="arrow"
        )
        find_prev.grid(row=0, column=3)
        self.bind("<Left>", self.find_prev)

        find_next = ttk.Button(
            self,
            text=">",
            command=self.find_next,
            padding=(-25, 0),
            cursor="arrow"
        )
        find_next.grid(row=0, column=4)
        self.bind("<Right>", self.find_next)

        replace_entry = ttk.Entry(
            self,
            textvariable=self.word_replace
        )
        replace_entry.grid(row=0, column=5)

        replace_button = ttk.Button(
            self,
            text="Replace",
            command=self.replace,
            padding=(-10, 0),
            cursor="arrow"
        )
        replace_button.grid(row=0, column=6)

        replace_all_button = ttk.Button(
            self,
            text="Replace All",
            command=self.replace_all,
            padding=(0, 0),
            cursor="arrow"
        )
        replace_all_button.grid(row=0, column=7)

        find_close = tk.Button(
            self,
            text="X",
            foreground="red",
            command=self.frame_controller.close_find_frame,
            bg="white",
            highlightthickness=0,
            relief="flat",
            padx=-25,
            cursor="arrow"
        )
        find_close.grid(row=0, column=8)

        # Bind Escape key to close frame for all widgets in frame
        self.controller.bind("<Escape>", self.frame_controller.close_find_frame)
        for widget in self.winfo_children():
            widget.bind("<Escape>", self.frame_controller.close_find_frame)

    def find(self, event=None):
        """Finds matches in controller for entered word.

        Parameters
        ----------
        event
            tkinter event to handle bind. Defaults to None
        """
        # Reset attributes and variables
        self.words_found = 0
        self.current_word = 0
        self.step_started = False
        self.results_label.grid_forget()
        # Remove tags from text box
        self.controller.tag_remove("found", "1.0", "end")
        self.controller.tag_remove("found_individual", "1.0", "end")
        self.controller.tag_remove("replaced", "1.0", "end")
        # Search for string in text box content and add found tag to matches
        search_string = self.word.get()
        if search_string:
            index = "1.0"
            while True:
                # Start search from index of end of previous match
                index = self.controller.search(search_string, index, nocase=True, stopindex="end")
                if not index:
                    break
                # Set index to be used in next run and add found tag
                last_index = f"{index} + {len(search_string)}c"
                self.controller.tag_add("found", index, last_index)
                index = last_index
            if len(self.controller.tag_ranges("found")) > 0:
                # Set words found and format results string
                self.words_found = len(self.controller.tag_ranges("found")) - 1
                self.words.set(f"{int((self.words_found + 1)/2)}/{int((self.words_found + 1)/2)} matches")
            else:
                # Format result string for 0 matches
                self.words.set("0 matches")
            # Grid results label
            self.results_label.grid(row=0, column=0)

    def find_next(self, event=None):
        """Highlights next match in controller for entered word.

        Parameters
        ----------
        event
            tkinter event to handle bind. Defaults to None
        """
        if self.words_found > 0:
            self.controller.tag_remove("replaced", "1.0", "end")
            # If this is the first instance of either find_next or find_prev
            if not self.step_started:
                self.step_started = True
                # Add found_individual tag to first result
                self.controller.tag_add(
                    "found_individual",
                    self.controller.tag_ranges("found")[self.current_word],
                    self.controller.tag_ranges("found")[self.current_word + 1]
                    )
            else:
                # Remove found_individual from current result
                self.controller.tag_remove("found_individual", "1.0", "end")
                # Increment by 2 if there is a next result. Else set back to the first result.
                if self.current_word + 2 < self.words_found:
                    self.current_word += 2
                else:
                    self.current_word = 0
                # Add found_individual tag to result
                self.controller.tag_add(
                    "found_individual",
                    self.controller.tag_ranges("found")[self.current_word],
                    self.controller.tag_ranges("found")[self.current_word + 1]
                )
            # Format words to show which result is highlighted
            self.words.set(f"{int((self.current_word/2) + 1)}/{int((self.words_found + 1)/2)} matches")

    def find_prev(self, event=None):
        """Highlights previous match in controller for entered word.

        Parameters
        ----------
        event
            tkinter event to handle bind. Defaults to None
        """
        if self.words_found > 0:
            self.controller.tag_remove("replaced", "1.0", "end")
            # If this is the first instance of either find_next or find_prev
            if not self.step_started:
                self.step_started = True
                # Add found_individual tag to last result
                self.controller.tag_add(
                    "found_individual",
                    self.controller.tag_ranges("found")[self.words_found - 1],
                    self.controller.tag_ranges("found")[self.words_found]
                )
                self.current_word = self.words_found - 1
            else:
                # Remove found_individual from current result
                self.controller.tag_remove("found_individual", "1.0", "end")
                # Decrement by 2 if there is a previous result. Else set back to the last result.
                if self.current_word - 2 >= 0:
                    self.current_word -= 2
                else:
                    self.current_word = self.words_found - 1
                # Add found_individual tag to result
                self.controller.tag_add(
                    "found_individual",
                    self.controller.tag_ranges("found")[self.current_word],
                    self.controller.tag_ranges("found")[self.current_word + 1]
                )
            # Format words to show which result is highlighted
            self.words.set(f"{int((self.current_word/2) + 1)}/{int((self.words_found + 1)/2)} matches")

    def replace(self):
        """Replaces selected match with word_replace"""
        if self.controller.tag_ranges("found_individual"):
            start_index = self.controller.tag_ranges("found_individual")[0]
            end_index = self.controller.tag_ranges("found_individual")[1]
            self.controller.delete(start_index, end_index)
            self.controller.insert(start_index, self.word_replace.get(), "replaced")
            self.current_word = 0
            self.words_found -= 2
            self.step_started = False

    def replace_all(self):
        """Replaces all matches with word_replace

        Also produces toplevel window displaying what changes were made
        """
        self.find()
        if self.controller.tag_ranges("found"):
            words = int((self.words_found + 1)/2)
            for word in range(0, words):
                start_index = self.controller.tag_ranges("found")[0]
                end_index = self.controller.tag_ranges("found")[1]
                self.controller.delete(start_index, end_index)
                self.controller.insert(
                    start_index,
                    self.word_replace.get(),
                    "replaced"
                )
            popup = tk.Toplevel()
            popup.title("Replace All Completed")
            popup.resizable(False, False)
            popup_label = ttk.Label(
                popup,
                text=f"{words} instances of \"{self.word.get()}\" "
                     f"have been replaced with \"{self.word_replace.get()}\"",
                padding=(25, 25)
            )
            popup_label.pack(side="left", anchor="center")

            self.current_word = 0
            self.words_found = 0
            self.step_started = False

    def close_find(self):
        """Destroys FindButtons frame"""
        self.controller.tag_remove("found", "1.0", "end")
        self.controller.tag_remove("found_individual", "1.0", "end")
        self.controller.tag_remove("replaced", "1.0", "end")
        self.controller.unbind("<Escape>")
        self.controller.focus_set()
        self.pack_forget()
        self.destroy()
