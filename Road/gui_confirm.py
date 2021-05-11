from tkinter import *
from tkinter import simpledialog
import tkinter
import sys
import os
class My_gui():
    def __init__(self,init_window_name):
        self.init_window_name=init_window_name
    def set_init_window(self):
        self.init_window_name.title=("运行结束")
        self.init_window_name.geometry('200x80+200+200')
        self.init_label=Label(self.init_window_name,text='ss')
        self.init_label.grid(row=1, column=1)
        self.confirmbutton=Button(self.init_window_name,text='运行结束',width=10,command=self.init_window_name.quit)
        self.confirmbutton.grid(row=2, column=10)
        pass
    # def funexit(self):
    #     os.popen()
    #     sys.exit
def gui_start():
    init_window=Tk()
    ZMJ_PORTAL=My_gui(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()


def gui_input(title):
    root = tkinter.Tk()
    root.withdraw()
    res = simpledialog.askstring(title, title)
    return res

# gui_start()