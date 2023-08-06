from tkinter import *
from tkinter.font import Font
import tkinter.ttk as ttk
from TuneCoach.python_bridge.pitch_utilities import *
from math import sin, cos, radians
import time
from TuneCoach.gui.IndicatorLight import *
from TuneCoach.gui.constants import *
from TuneCoach.gui.RoundedLabel import *


class PitchDisplay:
    def __init__(self, mainWindow, threshold=10):
        self.frame = mainWindow.right_frame
        self.mainWindow = mainWindow

        self.threshold = threshold

        self.font = Font(size=20)
        self.pitchOffset = self.font.metrics('linespace')*0.75

        self._pitchValue = '---'  # default display
        self._centsValue = -50
        self._hertzValue = 0
        self._octaveValue = ''

        self._span = 75  # Size of tuner arc in degrees, starting at vertical

        self.canvas = Canvas(self.frame, bg=Colors.background, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Configure>", self.configure)

        self.top_frame = Frame(self.canvas, height=35, bg=Colors.background, bd=0, highlightthickness=0)
        #self.top_frame.pack_propagate(0)
        self.top_frame.pack(side='top', fill=tk.X, anchor=tk.N)

        self.rec_frame = Frame(self.top_frame, width=80, height=35, bg=Colors.background, bd=0, highlightthickness=0)
        self.rec_frame.pack_propagate(0)
        self.rec_frame.pack(anchor='w', side=tk.LEFT)

        self.light = IndicatorLight(self.rec_frame, 35)
        self.light.pack(anchor='w', side='left')

        self.time_label = Label(self.rec_frame, text='00:00', anchor='e', justify=RIGHT, fg=Colors.text, bg=Colors.background)
        self.time_label.pack(side='right')

        self.score_label = RoundedLabel(self.top_frame, "Score: 0%", Colors.score_label, Colors.background, height=35, width=110)
        self.score_label.pack(side='right')
        #self.score_label.set_text("adfasdf")

        self.showsHertz = BooleanVar()

        style = ttk.Style()
        style.configure("Pitch.TCheckbutton", background=Colors.background, foreground=Colors.text)
        style.map('Pitch.TCheckbutton',

        foreground=[('active', Colors.text)],
        background=[('pressed', '!focus', '#232323'),
                    ('active', Colors.aux)])

        c = ttk.Checkbutton(self.canvas, text="Show Hertz", variable=self.showsHertz, takefocus=False, command=self.display_default_gui, style="Pitch.TCheckbutton")
        c.pack(anchor='e', side='bottom')

        self._last_time = 0
        self._clearing = False

        self.display_default_gui()

    def pause(self):
        self.light.stop()
        self.canvas.itemconfig(self.help_text, text='Press \'space\' to accept audio input')
        self._clearing = True

    def resume(self):
        self.light.start_flashing()
        self.canvas.itemconfig(self.help_text, text='Press \'space\' to pause audio input')

    def cents_to_angle(self, cents):
        return cents/50 * self._span

    def configure(self, event):
        self.display_default_gui()

    def display_score(self, score):
        self.score_label.set_text(f"Score: {round(score)}%")

    def display_current_gui(self):
        pitch_and_octave = self._pitchValue + self._octaveValue
        self.canvas.itemconfig(self.current_pitch_display, text=pitch_and_octave)
        if self.showsHertz.get():
            self.canvas.itemconfig(self.hertzDisplay, text=self._hertzValue)
        self.update_line(self._centsValue)
        if not self._clearing and abs(self._centsValue) <= self.threshold:
            self.canvas.itemconfig(self.green_arc, fill=Colors.green)
        else:
            self.canvas.itemconfig(self.green_arc, fill="#ccffbf")

    def display_default_gui(self):
        self.canvas.delete("all")
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()
        min_dimension = min(self.width, self.height)
        self.radius = 0.4 * min_dimension
        self.centerX = self.width/2
        self.centerY = self.height/2 + 15

        self.current_pitch_display = self.canvas.create_text(self.centerX, self.centerY + self.pitchOffset, font=self.font, text='---', fill=Colors.text)
        if self.showsHertz.get():
            self.hertzDisplay = self.canvas.create_text(self.centerX, self.centerY + 2*self.pitchOffset, font="Ubuntu 14", text='', fill=Colors.text)

        self.help_text = self.canvas.create_text(self.width/2, self.height-35, text='Press \'space\' to accept audio input', fill=Colors.text)

        x0 = self.centerX - self.radius
        y0 = self.centerY - self.radius
        x1 = self.centerX + self.radius
        y1 = self.centerY + self.radius

        # rect = self.canvas.create_rectangle(x0, y0, x1, y1)

        rStart = 90 - self._span
        rSpan = 2 * self._span
        yStart = 90 - self.cents_to_angle(self.mainWindow.controller.yellow_threshold)
        ySpan = 2 * (90 - yStart)
        gStart = 90 - self.cents_to_angle(self.threshold)
        gSpan = 2 * self.cents_to_angle(self.threshold)

        self.red_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.red_arc, start=rStart, fill="#ffbfbf", extent=rSpan, outline='')

        self.yellow_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.yellow_arc,  start=yStart, fill="#fffeb0", extent=ySpan, outline='')

        self.green_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.green_arc, start=gStart, fill="#ccffbf", extent=gSpan, outline='')

        self.line = self.canvas.create_line(0, 0, 0, 0, fill=Colors.tuner_needle, width=4, 
                                            arrow=FIRST, arrowshape=(self.radius, 10, 5))
        self.update_line(-50)

    def update_line(self, cents):
        deg = self.cents_to_angle(cents)
        theta = radians(deg)
        dx = self.radius * sin(theta)
        dy = self.radius * cos(theta)
        self.canvas.coords(self.line, self.centerX, self.centerY, self.centerX + dx, self.centerY - dy)

    def set_threshold(self, thresh):
        self.threshold = thresh
        self.display_default_gui()

    def update_pitch(self, value):  # event as parameter
        self._pitchValue = value

    def update_hertz(self, value):
        self._hertzValue = value

    def update_cents(self, value):
        self._centsValue = value

    def update_octave(self, value):
        self._octaveValue = value

    def set_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        display_string = '{:02}:{:02}'.format(minutes, seconds)
        self.time_label.config(text=display_string)

    def update_data(self, hz, data): #TODO: remove data parameter?
        if hz != 0:
            self._clearing = False
            midi = hz_to_midi(hz)
            if data.midi_range[0] <= midi <= data.midi_range[1]:
                pitch_class = midi_to_pitch_class(midi)
                desired_hz = closest_in_tune_frequency(hz)
                cent = cents(desired_hz, hz)
                name = data.key_signature.get_display_for(pitch_class)
                self.update_cents(cent)
                self.update_hertz(f"{round(hz)} Hz")
                self.update_octave(f"{get_octave(midi)}")
                self.update_pitch(name)
                self.display_current_gui()
                self._last_time = time.time()
        else:
            self.clear()

        self.set_time(data.timer.get()) # TODO move timer

    def clear(self):
        self._clearing = True
        if self._centsValue != -50 and time.time() - self._last_time > 1.5:
            self.update_cents(max(-50, self._centsValue - 3))
            self.update_pitch('---')
            self.update_hertz('')
            self.update_octave('')
            self.display_current_gui()
        elif self._centsValue == -50: # clearing animation has finished
            self._clearing = False

    def needs_update(self):
        return self._clearing