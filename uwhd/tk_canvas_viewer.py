from .canvas_viewer import CanvasViewer

import tkinter as tk
#from tkinter import ttk

class TkCanvasViewer(CanvasViewer):
    def __init__(self, master, c, title):
        self.px_w = 5
        self.px_h = 5
        self.canv_w = self.px_w * c.w
        self.canv_h = self.px_h * c.h
        f = tk.Frame(master, width=self.canv_w, height=self.canv_h)
        f.pack()
        w = tk.Canvas(f, width=self.canv_w, height=self.canv_h)
        w.pack()
        self.w = w;
        self.master = master


    def show_px(self, x, y, color):
        self.w.create_rectangle((x + 0) * self.px_w, (y + 0) * self.px_h,
                                (x + 1) * self.px_w, (y + 1) * self.px_h,
                                fill=color.as_hex())

    def show(self, c):
        self.w.delete(tk.ALL)

        for y in range(c.h):
            for x in range(c.w):
                self.show_px(x, y, c.get(x, y))
