# Import required libraries
from tkinter import *
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Use TkAgg in the backend of tkinter application
matplotlib.use('TkAgg')

# Create an instance of tkinter frame
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Set the title of the window
win.title("LaTex Viewer")

# Define a function to get the figure output
def graph(text):
   # Get the Entry Input
   tmptext = entry.get()
   tmptext = "$"+tmptext+"$"
   # Clear any previous Syntax from the figure
   wx.clear()
   wx.text(0.2, 0.6, tmptext, fontsize = 20)
   canvas.draw()
# Create a Frame object
frame = Frame(win)
frame.pack()
# Create an Entry widget
var = StringVar()
entry = Entry(frame, width=70, textvariable=var)
entry.pack()

# Add a label widget in the frame
label = Label(frame)
label.pack()

# Define the figure size and plot the figure
fig = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
wx = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=label)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

# Set the visibility of the Canvas figure
wx.get_xaxis().set_visible(False)
wx.get_yaxis().set_visible(False)

win.bind('<Return>', graph)
win.mainloop()
