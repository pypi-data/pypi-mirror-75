# main gui for TuneCoach. Made by the group, Jamm Hostetler, James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui
from TuneCoach.gui.PitchDisplay import *
from TuneCoach.gui.SessionHistory import *
from TuneCoach.gui.SessionDiagnostics import *
from TuneCoach.gui.TunerSettingsWindow import *
from TuneCoach.gui.FAQWindow import *
from TuneCoach.gui.TutorialWindow import *
from TuneCoach.gui.IntroWindow import *
from TuneCoach.gui.Timer import *

from TuneCoach.gui.MainController import MainController

import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk
from ttkthemes import ThemedStyle


def invalid_path(path):
    # print(path)
    return path == '' or path == () or path == None


# Main GUI
class MainWindow:
    def __init__(self, master):
        style = ThemedStyle(master)
        style.set_theme("yaru")

        self.controller = MainController(self)
        self.master = master

        master.attributes('-fullscreen', True)
        master.state('iconic')
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        master.attributes('-fullscreen', False)
        master.deiconify()
        master.title("TuneCoach")
        master.geometry(f'{self.screen_width}x{self.screen_height}')
        master.minsize(width=int(self.screen_width * 0.6), height=int(self.screen_height*0.7))
        master.maxsize(width=self.screen_width, height=self.screen_height)

        master.bind('<space>', lambda ev: self.controller.toggle_pause())
        master.bind('<Control-Key-o>', lambda ev: self.controller.load_from())
        master.bind('<Control-Key-t>', lambda ev: TunerSettingsWindow(self))
        master.bind('<Control-Key-n>', lambda ev: self.controller.new_session())
        master.bind('<F1>', lambda ev: TutorialWindow(self))
        master.bind('<F2>', lambda ev: FAQWindow(self))
        master.bind('<F12>', lambda ev: self.controller.save_as())
        master.bind('<Control-Shift-Key-S>', lambda ev: self.controller.save_as())
        if self.controller.save:
            master.bind('<Control-Key-s>', lambda ev: self.controller.save())
        else:
            master.bind('<Control-Key-s>', lambda ev: self.controller.save_as())
        
        self.enable()
        self.create_menubar()
        self.layout_frames(self.screen_width, self.screen_height)
        IntroWindow(self)
    
    def cleanup(self):
        self.disable()
        if not self.controller.cleanup():
            self.enable()
            return # do not close if we're saving and then we cancel

        self.master.destroy() 
        
    # Creating frames to organize the screen.
    def layout_frames(self, screen_width, screen_height):
        frames_style = ttk.Style()
        frames_style.configure('MainFrames.TFrame', background=Colors.background)
        self.bottom_frame = ttk.Frame(self.master, style='MainFrames.TFrame')
        self.left_frame = ttk.Frame(self.master, style='MainFrames.TFrame')
        self.right_frame = ttk.Frame(self.master, style='MainFrames.TFrame')

        # Putting the frames into a grid layout
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # setting up grid weights.
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1, minsize=250)
        self.master.grid_columnconfigure(0, weight=1, uniform="halfwidth")
        self.master.grid_columnconfigure(1, weight=1, uniform="halfwidth")

        # Here we can work on creating the functionality for each frame, ex: tuner, pitch history, information
        self.history = SessionHistory(self, self.bottom_frame)
        self.diagnostics = SessionDiagnostics(self)
        self.pitch_display = PitchDisplay(self, self.controller.threshold)
    
    def perform_save_as(self, newSession = False):
        if newSession:
            path = tk.filedialog.asksaveasfilename(initialdir='./', title="Would you like to save your current session?", filetypes=[('session files', '*.session')])
        else:
            path = tk.filedialog.asksaveasfilename(initialdir='./', title="Save session as...", filetypes=[('session files', '*.session')])
        if invalid_path(path): # if the user cancels the dialog, don't do anything
            return (None, True) # this tuple means the user canceled

        return (path, False) # we did save

    def perform_load(self):
        path = tk.filedialog.askopenfilename(initialdir='./', title="Select a session", filetypes=[('session files', '*.session')])
        if invalid_path(path): # if the user cancels the dialog, don't do anything
            return (None, True) # cancel
        return (path, False)

    # Adding menu options to the top of the screen.
    # returns False ONLY IF THE USER CANCELS
    
    def disable(self):
        self.master.protocol("WM_DELETE_WINDOW", lambda: ...)
        self.controller.pause()

    def enable(self):
        self.master.protocol("WM_DELETE_WINDOW", self.cleanup)
    
    def create_menubar(self):
        def session_menu_item(fn):
            def command_function():
                self.disable()
                fn()
                self.enable()
            return command_function
        
        menubar = tk.Menu(self.master, bg='white')
        self.master.config(menu=menubar)
        file_menu = tk.Menu(menubar)

        # File menubar
        menubar.add_cascade(label="File", menu=file_menu)
        commands = ( 
            ("New Practice Session (CTRL-N)", self.controller.new_session),
            ("Save Current Session (CTRL-S)", self.controller.save),
            ("Save Current Session As... (CTRL-SHIFT-S)", self.controller.save_as),
            ("Load Existing Session (CTRL-O)", self.controller.load_from))
        
        for label, fn in commands:
            file_menu.add_command(label=label, command=session_menu_item(fn), background='white')

        # Settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Tuner Settings (CTRL-T)", command=lambda: TunerSettingsWindow(self), background='white')

        # Help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Tutorial (F1)", command=lambda: TutorialWindow(self), background='white')
        help_menu.add_command(label="FAQ (F2)", command=lambda: FAQWindow(self), background='white')

   ### METHODS IMPLEMENTED FOR CONTROLLER ### 

    def update_diagnostics(self, data):
        self.diagnostics.update_plot(data)
        self.pitch_display.display_score(data.get_overall())

    def update_history(self, data):
        self.history.update(data)

    def refresh_timer(self, data):
        self.pitch_display.update_data(0, data)

    def update_threshold(self, threshold):
        self.pitch_display.set_threshold(threshold)

    def update_pitch(self, hz, data):
        self.pitch_display.update_data(hz, data)
    
    def update_session_name(self, name):
        self.diagnostics.session_name.configure(text=name)
    
    def clear(self):
        self.history.reset()
        self.diagnostics.clear_plot()
        self.pitch_display.clear()

    def pause(self):
        self.pitch_display.pause()
        self.history.pause_scrollbar()

    def resume(self):
        self.pitch_display.resume()
        self.history.resume_scrollbar()

    def error(self, msg, title="Error!"):
        tk.messagebox.showerror(title, msg)
    
    def success(self, msg, title="Success!"):
        tk.messagebox.showinfo(title, msg)

    def ask_should_save(self):
        return tk.messagebox.askyesnocancel("", "Save current session?")

    def after(self, ms, fn): self.master.after(ms, fn)
