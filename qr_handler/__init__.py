import cv2
import zbarlight

import openpyxl
from tkinter import *
from PIL import Image, ImageTk

from time import sleep


class QrHandler:
    def __init__(self, camera, way=''):
        self.way = way
        self.cap = cv2.VideoCapture(camera)
        self.running = False
        self.wb = openpyxl.load_workbook(filename=self.way + 'info.xlsx')

        self.root = Tk()
        self.root.title(u'HSE Party Qr Reader')
        self.root.protocol('WM_DELETE_WINDOW', self._window_closer)
        self.root.bind('<Key>', self._window_closer)

        self.frame = Frame(self.root, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.frame, height=800, width=860)
        self.canvas_pic = self.canvas.create_image(420, 240)

        self.reg_label = self.canvas.create_text(420, 520, text='', fill='red', font='arial 50')
        self.label1 = self.canvas.create_text(420, 570, text='', fill='black', font='arial 50')
        self.label2 = self.canvas.create_text(420, 620, text='', fill='black', font='arial 50')
        self.label3 = self.canvas.create_text(420, 670, text='', fill='black', font='arial 50')

        self.square = self.canvas.create_rectangle(320, 140, 520, 340, fill='', outline='green')

        self.canvas.pack(expand=YES, fill=BOTH)

        self.cur_id = None

    def run(self):
        self.running = True
        while self.running:
            sleep(0.01)
            self._iteration()

    def stop(self):
        self.running = False

    def finish(self):
        self.cap.release()

    # private

    def _iteration(self):
        ret, frame = self.cap.read()
        cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(cv2_im)

        new_size = (int(image.size[0] * (480.0 / image.size[1])), 480)

        photo = ImageTk.PhotoImage(image.resize(new_size).transpose(Image.FLIP_LEFT_RIGHT))
        self.canvas.itemconfig(self.canvas_pic, image=photo)
        self.root.update()

        image.load()

        codes = zbarlight.scan_codes(['qrcode'], image)
        if codes is not None:
            self._excel(codes)
            print("Scanned")

    def _window_closer(self):
        self.stop()
        print(u'Окно закрыто')
        self.root.destroy()

    def _excel(self, codes):
        sheet = self.wb['Лист1']

        search_id = int(codes[0])
        if self.cur_id is not None and search_id == self.cur_id:
            return
        else:
            self.cur_id = search_id

        i = 1
        while sheet['A' + str(i)].value is not None:
            if sheet['A' + str(i)].value == search_id:
                if sheet['E' + str(i)].value != '*':
                    sheet['E' + str(i)] = '*'
                    self.wb.save(self.way + 'info.xlsx')

                    self.canvas.itemconfig(self.reg_label, text='')
                else:
                    self.canvas.itemconfig(self.reg_label, text='Уже зарегистрирован')

                self.canvas.itemconfig(self.label1, text=sheet['B' + str(i)].value)
                self.canvas.itemconfig(self.label2, text=sheet['C' + str(i)].value)
                self.canvas.itemconfig(self.label3, text=sheet['D' + str(i)].value)
                break

            i += 1

        if sheet['A' + str(i)].value is None:
            self.canvas.itemconfig(self.reg_label, text='В базе нет такого qr кода')
            self.canvas.itemconfig(self.label1, text='')
            self.canvas.itemconfig(self.label2, text='')
            self.canvas.itemconfig(self.label3, text='')
