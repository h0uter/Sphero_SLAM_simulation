from tkinter import *

master = Tk()

wc = Canvas(master, width=400, height=300)
wc.pack()


#w.create_line(Start_X, Start_Y, Einde_X, EINDE,Y)
wc.create_line(300, 100, 200, 100)
wc.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

wc.create_rectangle(50, 25, 150, 75, fill="blue")

mainloop()