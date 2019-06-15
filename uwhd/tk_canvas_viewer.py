from .canvas_viewer import CanvasViewer

import tkinter as tk
#from tkinter import ttk

class TkCanvasViewer(CanvasViewer):
    def __init__(self, master, c, title, window=None):
        self.master = master

        if window is None:
            window = { 'w': c.w, 'h': c.h, 'x': 0, 'y': 0, 'invert': False }

        self.window = window
        self.invert = window['invert']

        self.px_w = 5
        self.px_h = 5
        self.cw = window['w']
        self.ch = window['h']
        self.canv_w = self.px_w * self.cw
        self.canv_h = self.px_h * self.ch
        f = tk.Frame(master, width=self.canv_w, height=self.canv_h)
        f.pack()
        w = tk.Canvas(f, width=self.canv_w, height=self.canv_h)
        w.pack()
        self.w = w;


    def show_px(self, x, y, color):
        if self.invert:
            x = self.cw - x
            y = self.ch - y

        self.w.create_rectangle((x + 0) * self.px_w, (y + 0) * self.px_h,
                                (x + 1) * self.px_w, (y + 1) * self.px_h,
                                fill=color.as_hex())

    def show(self, c):
        self.w.delete(tk.ALL)

        for y in range(self.ch):
            for x in range(self.cw):
                self.show_px(x, y,
                             c.get(self.window['x'] + x,
                                   self.window['y'] + y))
