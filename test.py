from Tkinter import *
from train import *
from platform import *
from outerline import *
from db import *
from usercontrol import *
import time

pltrains = []        # Trains that not on any platform yet
outertrains = []        # Trains that not on any platform yet
waitingtrains = []        # Trains that not on any platform yet
trainl = []             # List of all trains
platforml = []          # List of all platforms
outerl = []             # List of outerlines
startstate = False
fps = 100/6
counter = 19*60*60
timecnt = ''

class App:

    def __init__(self, master):
        global w, trainl, platforml, outerl, table

        self.w = Canvas(master, width=1300, height=400)
        self.w.pack(side=TOP)
        
        self.f = Frame(master, width=1300, height=300)
        self.f.pack(side=TOP, fill=X)
        

        for p in getPlatformList().find():
            pl = Platform(self.w, p['number'])
            platforml.append(pl)

        for i in range(10):
            outerl.append(Outerline(self.w, i+1))

        # self.maketable(self.f)
        self.makebuttons(self.f)

    def makebuttons(self, arena):
        self.start = Button(arena, text="Start Simulation", command=self.sim)
        self.start.pack(side=LEFT)
        
        self.stop = Button(arena, text="Stop Simulation", command=self.stop, state=DISABLED)
        self.stop.pack(side=LEFT)
        
        self.addt = Button(arena, text="Add Train", command=lambda: self.addTrainClicked(master))
        self.addt.pack(side=LEFT)

        self.delt = Button(arena, text="Delete Train", command=lambda: self.deleteTrainClicked(master))
        self.delt.pack(side=LEFT)

        self.edt = Button(arena, text="Edit Train", command=lambda: self.editTrainClicked(master))
        self.edt.pack(side=LEFT)

        self.addp = Button(arena, text="Add Platform", command=lambda: self.addPlatformClicked(master))
        self.addp.pack(side=LEFT)

        self.edp = Button(arena, text="Edit Platform", command=lambda: self.editPlatformClicked(master))
        self.edp.pack(side=LEFT)

        self.qbutt = Button(arena, text="Exit", fg="red", command=arena.quit)
        self.qbutt.pack(side=LEFT)


    def sim(self):
        global startstate
        startstate = True
        counter_label(timer)
        master.after(10, simulate)
        self.start.config(state=DISABLED)
        self.stop.config(state=NORMAL)
        data()
    
    def stop(self):
        global startstate
        startstate = False
        self.start.config(state=NORMAL)
        self.stop.config(state=DISABLED)

    def addTrainClicked(self,master):
        dialog = addTrainDialog(master)
        master.wait_window(dialog.top)

    def deleteTrainClicked(self,master):
        dialog = deleteTrainDialog(master)
        master.wait_window(dialog.top)

    def editTrainClicked(self,master):
        dialog = editTrainDialog(master)
        master.wait_window(dialog.top)

    def addPlatformClicked(self,master):
        dialog = addPlatformDialog(master)
        master.wait_window(dialog.top)

    def editPlatformClicked(self,master):
        dialog = editPlatformDialog(master)
        master.wait_window(dialog.top)

def schedule():
    global waitingtrains, pltrains, outertrains

    for t in getTrainList().find().sort([('arrival_time',pymongo.ASCENDING)]):
        deptime = finddep(t['arrival_time'], t['type'])
        tr = Train(app.w, t['code'], t['name'], t['arrival_time'], deptime)
        trainl.append(tr)
        waitingtrains.append(tr)


def finddep(arrival, category):
    [hour, mint] = arrival.split(':')
    if category=="Passing":
        if int(mint)>=45:
            hour = str((int(hour)+1)%24)
        mint=str((int(mint)+15)%60)
    else:
        if int(mint)>=55:
            hour = str((int(hour)+1)%24)
        mint=str((int(mint)+5)%60)
    if len(hour)<2:
        hour = '0'+hour
    if len(mint)<2:
        mint = '0'+mint
    return hour+':'+mint


def simulate():
    global startstate
    for t in pltrains:
        if timecnt>=t.departure:
            t.vel = 2
            t.platform = 0
            t.status = "departed"
            del pltrains[pltrains.index(t)]
            # remove this train from schedule table

    for t in outertrains:
        flag = 0
        for p in platforml:
            if not p.occupied and p.status:
                flag = 1
                outer = t.outerline
                t.vel = 2
                t.platform = p.platformNo
                t.status = "arrived"
                p.occupied = True
                p.train = t
                del outertrains[outertrains.index(t)]
                pltrains.append(t)
                for ol in outerl:
                    if ol.train==t:
                        ol.train = None
                        ol.occupied = False
                        break
                break
        if flag==0:
            break

    for t in waitingtrains:
        flag = 0
        if timecnt>=t.arrival:
            for p in platforml:
                if not p.occupied and p.status:
                    flag = 1
                    t.vel = 2
                    t.platform = p.platformNo
                    t.status = "arrived"
                    p.occupied = True
                    p.train = t
                    del waitingtrains[waitingtrains.index(t)]
                    data()
                    pltrains.append(t)
                    break
        if flag==0:
            break

    for t in trainl:
        if (t.x<400 and t.status=='arrived') or t.status=='departed':
            t.update(app.w)
    for o in outerl:
        o.update(app.w)

    if startstate:
        master.after(10, simulate)

def counter_label(label):
    def count():
        global counter, startstate, timecnt
        counter += 1
        timecnt = time.strftime("%H:%M", time.gmtime(counter))
        label.config(text="Timer: "+time.strftime("%H:%M", time.gmtime(counter)))
        if(startstate):
            label.after(fps, count)
    count()

def data():
    #Label(frame,text="Train Code                    "+"Train Name                  "+ "Arrival Time               "+"Departure Time             "+"Arrival Platform Number               ").grid(row=0,column=1)
    Label(frame).grid(row=0,column=0,padx=100)
    Label(frame,text="Train Code",font = "Helvetica 14 bold").grid(row=0,column=4,padx=30)
    Label(frame,text="Train Name",font = "Helvetica 14 bold").grid(row=0,column=8,padx=30)
    Label(frame,text="Arrival Time",font = "Helvetica 14 bold").grid(row=0,column=12,padx=30)
    Label(frame,text="Departure Time",font = "Helvetica 14 bold").grid(row=0,column=16,padx=30)
    Label(frame,text="Platform Number",font = "Helvetica 14 bold").grid(row=0,column=20,padx=30)
    i = 0
    for trains in waitingtrains:
       Label(frame,text=trains.code,font = "Helvetica 10").grid(row=i+1,column=4)
       Label(frame,text=trains.name,font = "Helvetica 10").grid(row=i+1,column=8)
       Label(frame,text=trains.arrival,font = "Helvetica 10").grid(row=i+1,column=12)
       Label(frame,text=trains.departure,font = "Helvetica 10").grid(row=i+1,column=16)
       Label(frame,text=trains.platform,font = "Helvetica 10").grid(row=i+1,column=20)
       i = i+1

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=master.winfo_screenwidth()-100,height=200)

master = Tk()

posx = 0
posy = 0
screenWidth = master.winfo_screenwidth()
screenHeight = master.winfo_screenheight()
master.wm_geometry("%dx%d+%d+%d" % (screenWidth, screenHeight, posx, posy))

Label(master, text="Welcome To NDLS Railway Station",fg = "black",font = "Helvetica 18 bold").pack()
timer = Label(master, fg="black", font = "Helvetica 18 bold")
timer.pack()
app = App(master)

# All things realted to train time table
myframe=Frame(master,relief=GROOVE,width=50,height=100,bd=1)
myframe.place(x=10,y=master.winfo_screenheight()-230)

canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data()
# things related to train timetable over

schedule()
master.mainloop()