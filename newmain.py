#!/usb/bin/py
# Ticket Bucket
import tkinter as tk # NEED TO CHANGE THIS TO IMPORT TKINTER AS TK OR SOMETHING
# IT HELPS AVOID 'GLOBAL NAMESPACE POLLUTION'
# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import pyperclip
import os

def main():
    def style_normal_button(button):
        # set bg and fg
        button.background = "#00467f"
        button.foreground = "#ffffff"
        button.font = "Roboto 16 bold"
        # set the hovering actions
        set_hover_normal(button)

    def set_hover_normal(button):
        button.bind("<Enter>", func=lambda e: button.config(background="#ffffff", fg="#00467f"))
        button.bind("<Leave>", func=lambda e: button.config(background="#00467f", fg="#ffffff"))
    
    # erase text inside a Text widget when its clicked on, then unbind the erase function from the mouse click
    def erase_text(widget):
        widget.delete('1.0', tk.END)
        widget.bind("<Button-1>", func=lambda e: None)

    def change_window(tohide, toshow):
        tohide.withdraw()
        # tohide.withdraw()
        toshow.deiconify()
        # toshow.deiconify()
    def return_home(hide, show, windows):
        # hide both view / add windows:
        windows["view"].withdraw()
        windows["add"].withdraw()
        hide.withdraw()
        # tohide.withdraw()
        show.deiconify()
    
    # function below will show the program docs / readme file (right now its just a txt file, maybe make an actual tkinter Window at some point)
    def show_readme():
        # startfile opens the file with the system's default text editor (windows / linux / mac) according to stack overflow
        # https://stackoverflow.com/questions/43007196/python-open-a-textnotepad-document
        os.startfile("res\\readme.txt")

    def focus_next_widget(event):
        # if event.widget == title_entry:
        #     erase_text(content_entry)
        event.widget.tk_focusNext().focus()
        return("break")
    def create_menu(window, windows_dict):
            # separate out the windows_dict:
            main_win = windows_dict["main"]
            add_win = windows_dict["add"]
            view_win = windows_dict["view"]
            settings_win = windows_dict["settings"]
            # create outer menubar
            menubar = tk.Menu(window)
            # create File cascade:
            filemenu = tk.Menu(menubar, tearoff=0)

            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(label="Create new response", command=lambda: add_win.change_window(window, add_win))
            filemenu.add_command(label="View stored responses", command=lambda: view_win.view_stored_responses())

            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=window.quit)

            menubar.add_cascade(label="File", menu=filemenu)

            # create Edit cascade
            editmenu = tk.Menu(menubar, tearoff=0)
            editmenu.add_command(label="Settings", command=lambda: settings_win.deiconify())
            menubar.add_cascade(label="Edit", menu=editmenu)

            # create Help cascade:

            helpmenu = tk.Menu(menubar, tearoff=0)
            helpmenu.add_command(label="About / Readme", command=CustomWidget.show_readme)
            helpmenu.add_separator()

            menubar.add_cascade(label="Help", menu=helpmenu)

            window.config(menu=menubar)
    # when windows are closed - withdraw them instead of destroying them:
    # assign this funciton to close event with: widget.protocol("WM_DELETE_WINDOW", _on_closing)
    def _on_closing(win_master):
        close_window = tk.Toplevel()
        close_window.title("Exit program?")

        question = tk.Label(close_window, text="Are you sure you'd like to exit?")

        button_frame = tk.Frame(close_window)
        # this will be interesting if the below arguments to command work
        home_button = tk.Button(button_frame, text="return home", command=lambda: change_window(close_window, win_master))
        style_normal_button(home_button)
        exit_button = tk.Button(button_frame, text="exit program", command=win_master.quit)
        style_normal_button(exit_button)

        home_button.pack(side=tk.LEFT, padx=(10,15))
        exit_button.pack(side=tk.LEFT, padx=(15,10))
        button_frame.pack(side=tk.BOTTOM, pady=(15,10))

        question.pack(side=tk.TOP, pady=5)

        # present a window with options to either 1. exit app or 2. go back to main window
        withdraw()

    # WINDOW DIMENSIONS (will be able to modify in the settings..eventually):
    widths = {}
    heights = {}
    widths["main"] = 700
    heights["main"] = 225
    widths["view"] = 325
    heights["view"] = 800
    widths["add"] = 450
    heights["add"] = 600

    # make windows
    windows = {}
    windows["main"] = tk.Tk(title="Ticket Bucket")

    windows["view"] = tk.Toplevel()
    windows["view"].geometry
    windows["add"] = tk.Toplevel()
    screen_width = windows["main"].winfo_screenwidth()
    screen_height = windows["main"].winfo_screenheight()
    # find the top left point
    left_x = int(screen_width/4 - width / 2)
    top_y = int(screen_height/5 - height / 2)
    windows["main"].geometry(f'{widths["main"]}x{heights["main"]}+{left_x}+{top_y}')