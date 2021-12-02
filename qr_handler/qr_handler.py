from .frame import InitFrame, LoopFrame
from .excel import Excel
from .camera import Camera


import zbarlight

import tkinter as tk
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk, ImageOps

import time
import os.path
import typing as t

from .config import *


class QrHandler(object):
    def __init__(self, camera: int, default_way: str):
        self._way: str = os.path.abspath(default_way) if os.path.exists(default_way) else ''
        self._state: int = 0

        self._root = tk.Tk()
        self._setup_window()
        self._init_frame = InitFrame(self._root, self._way, self._ask_filename)
        self._camera = Camera(camera)

        self._excel: t.Optional[Excel] = None
        self._frame: t.Optional[LoopFrame] = None

        self._cur_id: t.Optional[int] = None

    def run(self):
        self._start()
        print("Started")
        self._choose()
        self._loop()

    # private

    # setup
    def _setup_window(self):
        self._root.title(WINDOW_TITLE)
        self._root.protocol('WM_DELETE_WINDOW', self._window_closer)

    # callbacks
    def _ask_filename(self):
        filename = askopenfilename(filetypes=INIT_FILETYPES)
        if filename:
            self._way = filename
        print(f'File: {self._way}')
        if os.path.isfile(self._way):
            self._state = 2

    def _window_closer(self, *args):
        self._stop()
        print("Closed")
        self._root.destroy()

    # main routine
    def _start(self):
        self._state = 1

    def _stop(self):
        self._state = 0

    def _update(self):
        self._root.update()

    def _choose(self):
        while self._state == 1:
            self._update()
            time.sleep(FPS)

    def _loop(self):
        if self._state == 2:
            self._init_frame.destroy()
            self._excel = Excel(self._way)
            self._frame = LoopFrame(self._root)
        while self._state == 2:
            self._iteration()
            self._update()
            time.sleep(FPS)
        self._camera.close()

    # loop implementation
    def _iteration(self):
        image = self._read_image()

        self._frame.set_photo(self._convert_image(image))

        for img in self._scanning_images(image):
            codes = zbarlight.scan_codes(['qrcode'], img)
            if codes is not None:
                print(f"Detected: {codes}")
                self._find(codes)
                print("Scanned")
                break

    def _read_image(self) -> Image.Image:
        return self._camera.get_image()

    @staticmethod
    def _scanning_images(image: Image.Image) -> t.List[Image.Image]:
        grey = image.convert('L')
        neg = ImageOps.invert(grey)
        grey.load()
        neg.load()
        return [grey, neg]

    @staticmethod
    def _convert_image(image: Image.Image) -> ImageTk.PhotoImage:
        new_size = (int(image.size[0] * (480 / image.size[1])), 480)
        transformed_image = image.resize(new_size).transpose(Image.FLIP_LEFT_RIGHT)
        return ImageTk.PhotoImage(transformed_image)

    def _find(self, codes: t.List[str]):
        try:
            search_id = int(codes[0])
            if self._cur_id is not None and search_id == self._cur_id:
                return
            else:
                self._cur_id = search_id

            user = self._excel.find(search_id)
            if user is not None:
                self._frame.found(*user)
            else:
                self._frame.not_found()
        except ValueError:
            self._frame.not_found()
            print(f"Qr is incorrect: {codes[0]}")
