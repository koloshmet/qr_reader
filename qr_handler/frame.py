import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

import typing as t

from .config import *


class LoopFrame(object):
    def __init__(self, root: tk.Tk):
        self._cur_picture: t.Optional[ImageTk.PhotoImage] = None

        self._frame = tk.Frame(root, relief=tk.FLAT)

        self._canvas = tk.Canvas(self._frame, height=480, width=860, relief=tk.FLAT)
        self._picture = self._canvas.create_image(430, 240, image=self._cur_picture)
        self._square = self._canvas.create_rectangle(330, 140, 530, 340, fill='', outline=COLOR_SQUARE)
        self._canvas.pack()

        self._reg_label = ttk.Label(self._frame, text='', font=FONT_BIG, foreground=COLOR_REG)
        self._name_label = ttk.Label(self._frame, text='', font=FONT_BIG, foreground=COLOR_TEXT)
        self._info_label = ttk.Label(self._frame, text='', font=FONT_BIG, foreground=COLOR_TEXT)
        self._comment_label = ttk.Label(self._frame, text='', font=FONT_BIG, foreground=COLOR_TEXT)
        self._reg_label.pack()
        self._name_label.pack()
        self._info_label.pack()
        self._comment_label.pack()

        self._frame.pack(fill=tk.BOTH, expand=True)

    def set_photo(self, photo: ImageTk.PhotoImage):
        self._cur_picture = photo
        self._canvas.itemconfig(self._picture, image=self._cur_picture)

    def not_found(self):
        self._reg_label.config(text=REG_ERR)
        self._name_label.config(text='')
        self._info_label.config(text='')
        self._comment_label.config(text='')

    def found(self, name: str, info: str, comment: str, checked: bool):
        self._reg_label.config(text=(REG_CHECKED if checked else ''))
        self._name_label.config(text=(name or ''))
        self._info_label.config(text=(info or ''))
        self._comment_label.config(text=(comment or ''))


class InitFrame(object):
    def __init__(self, root: tk.Tk, way: str, cmd: t.Callable):
        self._way = way or 'No file'

        self._frame = tk.Frame(root, relief=tk.FLAT)

        header = ttk.Label(self._frame, text=INIT_HEADER, foreground=COLOR_TEXT, font=FONT_BIG, padding=100)
        label = ttk.Label(self._frame, text=INIT_LABEL, foreground=COLOR_TEXT, font=FONT_STANDARD)
        filename = ttk.Label(self._frame, text=self._way, foreground=COLOR_TEXT, font=FONT_STANDARD, padding=20)
        button = ttk.Button(self._frame, text=INIT_BUTTON_CAPTURE, command=cmd)
        header.pack()
        label.pack()
        filename.pack()
        button.pack()

        self._frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        self._frame.pack_forget()
        self._frame.destroy()
