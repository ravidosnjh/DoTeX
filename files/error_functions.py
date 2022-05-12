# Functions used in error containers
import tkinter as tk
from tkinter import filedialog
from files import constants as cons

# Strings in log file to be replaced
error_strings = ["If you have\nmisspelled it (e.g., `\hobx'), type `I' and the correct\nspelling (e.g., `I\hbox')."
                 " Otherwise just continue,\nand I'll forget about whatever was undefined.",
                 "Such booboos are generally harmless, so keep going.",
                 "How can we recover?\nMy plan is to forget the whole thing and hope for the best.",
                 "*** (cannot \\read from terminal in nonstop modes)"
                 ]


def retrieve_error_message(self, log_file_name, log_file_path, tex_file, tex_file_name):
    """ Retrieve error messages from log file and return log file name and line numbers where error occurred.

    Parameters
    ----------
    self : object
        object that called function
    log_file_name : str
        log file name
    log_file_path: str
        log file path
    tex_file: str
        tex file path
    tex_file_name:
        tex file name

    Returns
    -------
    log_file_name[0:-4] : str
        log file name without file extension
    line_numbers : list
        list of line numbers where errors occurred
    """
    # Create variables
    error_start_indices = []
    error_end_indices = []
    errors = dict()
    error_number = 0

    # Create header message
    error_frame_heading = \
        f"Compile failed for {tex_file_name}!\n" \
        f"The following errors were retrieved from {log_file_name}.\n" \
        f"The complete log can be found in the Logs Folder\n"

    self.error_frame.insert(1.0, error_frame_heading)

    # Read lines from log into list
    with open(log_file_path, 'r') as log_content:
        lines = log_content.readlines()

    # Create string for how tex file path is displayed in log
    tex_file_in_log = f"./{tex_file_name}"
    # If string is less than 79 characters (max line length in log) add a colon. Else take the first 79 characters. Take
    # result as string to search for in log file
    if len(tex_file_in_log) < 79:
        tex_file_search = [f"{tex_file_in_log}:"]
    else:
        tex_file_search = [f"{tex_file_in_log[0:78]}"]

    # Find occurrences of search string in log file and compile into list
    error_start = [line for line in lines if all((words in line) for words in tex_file_search)]

    # Create list of indices where search string occurred in log file, and where next blank line is for each. These are
    # the errors
    prev_index = 0
    for line in error_start:
        try:
            error_start_index = lines.index(line, prev_index)
            if error_start_index not in error_start_indices:
                error_start_indices.append(error_start_index)
                error_end_indices.append(lines.index("\n", error_start_indices[-1]))
            prev_index = error_end_indices[-1]
        except ValueError:
            error_start_indices.pop()

    # For each start and end index pair, add corresponding lines from log file into error string. AAdd error string to
    # errors dictionary
    for x in range(len(error_start_indices)):
        error = ""
        error_number += 1
        for y in range(error_start_indices[x], error_end_indices[x]):
            error += lines[y]
        error = f"\n\nError {error_number}: {error}"
        errors[f"error{error_number}"] = error

    # Format error strings
    line_numbers = self._format_error_message(errors)
    self.error_frame.config(state="disabled")
    return log_file_name[0:-4], line_numbers


def format_error_message(self, errors):
    """Formats error strings and returns line numbers where errors occurred.

    Parameters
    ----------
    errors : dict
        dictionary of errors

    Returns
    -------
    line_numbers : list
        list of line numbers where errors occurred
    """
    line_numbers = []
    for error in errors.values():
        # Change "l.linenumber" to "At line linenumber"
        try:
            line_number_index = error.index("l.") + 2
            line_number_end_index = error.index(" ", line_number_index)
            line_numbers.append(f"{error[line_number_index:line_number_end_index]}")
            error = f"{error[:line_number_end_index]}: {error[line_number_end_index:]}"
            error = error.replace("l.", "At line ")
        except ValueError:
            pass
        # Remove unwanted strings from error string
        for error_string in error_strings:
            error = error.replace(error_string, "")
        # Clarify ^^M in error
        if "^^M" in error:
            error = error.replace("^^M", " Cannot find package in the previous line")

        # Insert errors into text box
        self.error_frame.insert("end", error)
    return line_numbers


def save_log_as(self):
    """Opens filedialog for user to select file (name) and overwrites selected file with content of scrolled text
    box.
    """
    log_file = tk.filedialog.asksaveasfilename(
        initialdir=cons.FILTERED_LOG_DIRECTORY,
        initialfile=f"{self.log_file_name}_filtered",
        filetypes=(("Log files (*.log)", "*.log"), ("All Files", "*.*")),
        defaultextension=".log"
    )
    if log_file:
        log_content = self.error_frame.get(1.0, "end-1c")
        with open(log_file, 'w') as output:
            output.write(log_content)
