from tkinter import *
import time
import real_time_graph
import Crypto_Hype_Convert
import clear_Crypto_Hype
import append_data
import Crypto_Hype
import threading
import os


def run_graph():
    lb.insert(END, "starting real-time graph...")
    real_time_graph.run()


def run_collection():
    lb.insert(END, "starting twitter collection...")
    threading.Thread(target=Crypto_Hype.run).start()


def run_export():
    lb.insert(END, "exporting collected data to excel...")
    Crypto_Hype_Convert.run()


def run_clear():
    lb.insert(END, "clearing all collected data...")
    clear_Crypto_Hype.run()


def run_append():
    lb.insert(END, "updating with market price...")
    append_data.run()


def update_clock(self):
    now = time.strftime("%H:%M:%S")
    self.label.configure(text=now)
    self.root.after(1000, self.update_clock)

root = Tk()
root.title("Crypto Shill Detector")
root.geometry("780x430")
root.resizable(0, 0)
app = Frame(root, background="black")
app.grid()

original_dir = os.getcwd()
path = original_dir + "\logos"
os.chdir(path)
title = PhotoImage(file="main_logo.png").subsample(2, 2)
rtg = PhotoImage(file="button_real-time-graph.png")
rdc = PhotoImage(file="button_run-main.png")
ecd = PhotoImage(file="button_export-data.png")
cdc = PhotoImage(file="button_clear-data.png")
ucp = PhotoImage(file="button_update.png")
os.chdir(original_dir)

label = Label(app, image=title, background='black')
lb = Listbox(app, height=22, width=40, font=("Courier", 9))
lb.insert(END, "action log...")
button1 = Button(app, image=rtg, command=run_graph, background='black')
button2 = Button(app, image=rdc, command=run_collection, background='black')
button3 = Button(app, image=ecd, command=run_export, background='black')
button5 = Button(app, image=cdc, command=run_clear, background='black')
button4 = Button(app, image=ucp, command=run_append, background='black')

lb.pack(side=RIGHT, padx=25)
label.pack(padx=20, pady=20)
button1.pack(pady=10)
button2.pack(pady=10)
button3.pack(pady=10)
button4.pack(pady=10)
button5.pack(pady=50)
now = time.strftime("%H:%M:%S")
lb.insert(END, now)

root.mainloop()
