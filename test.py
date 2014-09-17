from Tkinter import *
from train import *
from platform import *
from outerline import *
from db import *
import time

waitinglist = []        # Trains that not on any platform yet
trainl = []             # List of all trains
platforml = []          # List of all platforms
outerl = []             # List of outerlines
startstate = False

class schtable(Frame):
    def __init__(self, parent, rows, columns):
        global trainl
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = Label(self, text="", borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    def fill(self):
        r = 1
        for train in trainl:
            self.set(r, 0, train.code)
            self.set(r, 1, train.name)
            self.set(r, 2, train.arrival)
            self.set(r, 3, train.departure)
            self.set(r, 4, train.platform)
            r+=1

    def removerow(self, code):
        for i in range(len(self._widgets)):
            if self._widgets[i][0].cget('text')==code:
                del self._widgets[i]
                break


class App:

    def __init__(self, master):
        global w, trainl, platforml, outerl, table

        w = Canvas(master, width=1300, height=400)
        w.pack(side=TOP)
        


        platforml = [Platform(w, 1), Platform(w, 2)]

        for i in range(10):
            outerl.append(Outerline(w, i+1))

        for t in getTrainList().find():
            tr = Train(w, t['code'], t['name'], t['arrival_time'], '00:00', 1)
            trainl.append(tr)

        self.maketable(master)
        self.makebuttons(master)

    def maketable(self, arena):
        global table
        table = schtable(arena, len(trainl)+1, 5)
        table.pack(side=TOP, fill=BOTH)
        table.set(0, 0, "Train Code")
        table.set(0, 1, "Train Name")
        table.set(0, 2, "Arrival Time")
        table.set(0, 3, "Departure Time")
        table.set(0, 4, "On Platform")
        table.fill()

    def makebuttons(self, arena):
        self.start = Button(arena, text="Start Simulation", command=self.sim)
        self.start.pack(side=LEFT)
        
        self.stop = Button(arena, text="Stop Simulation", command=self.stop, state=DISABLED)
        self.stop.pack(side=LEFT)
        
        self.addt = Button(arena, text="Add Train", command=None)
        self.addt.pack(side=LEFT)

        self.qbutt = Button(arena, text="Exit", fg="red", command=arena.quit)
        self.qbutt.pack(side=LEFT)


    def sim(self):
        global startstate
        startstate = True
        counter_label(timer)
        master.after(10, simulate)
        self.start.config(state=DISABLED)
        self.stop.config(state=NORMAL)
    
    def stop(self):
        global startstate
        startstate = False
        self.start.config(state=NORMAL)
        self.stop.config(state=DISABLED)


def schedule():
    for t in getTrainList().find():
        print t['code'], t['name']

def simulate():
    global startstate
    for t in trainl:
        if(t.x<400):
            t.update(w)
    for o in outerl:
        o.update(w)

    if startstate:
        master.after(10, simulate)

counter = 0 
def counter_label(label):
    def count():
        global counter
        global startstate
        counter += 1
        label.config(text="Timer: "+time.strftime("%H:%M", time.gmtime(counter)))
        if(startstate):
            label.after(1, count)
    count()

master = Tk()
Label(master, text="Welcome To NDLS Railway Station",fg = "black",font = "Helvetica 18 bold").pack()
timer = Label(master, fg="black", font = "Helvetica 18 bold")
timer.pack()
app = App(master)
schedule()
master.mainloop()