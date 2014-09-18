from Tkinter import *
from train import *
from platform import *
from outerline import *
from db import *
import time

pltrains = []        # Trains that not on any platform yet
outertrains = []        # Trains that not on any platform yet
waitingtrains = []        # Trains that not on any platform yet
trainl = []             # List of all trains
platforml = []          # List of all platforms
outerl = []             # List of outerlines
startstate = False
fps = 100/6
counter = 11.8*60*60
timecnt = ''
mx = len(list(getTrainList().find()))
tablegrid = []


class addTrainDialog:

    def __init__(self, parent):


        self.top = Toplevel(parent)

        # TRAIN NAME
        Label(self.top, text="Train Number").grid(row=0, column=0)
        self.trainNumberEntered = StringVar(self.top)
        self.trainNumber = Entry(self.top, textvariable=self.trainNumberEntered).grid(row=0, column=1)

        # TRAIN NUMBER
        Label(self.top, text="Train Name").grid(row=1, column=0)
        self.trainNameEntered = StringVar(self.top)
        self.trainName = Entry(self.top, textvariable=self.trainNameEntered).grid(row=1, column=1)

        # TRAIN ARRIVAL TIME
        Label(self.top, text="Arrival Time").grid(row=2, column=0)
        self.arrivalTimeEntered = StringVar(self.top)
        self.arrivalTimeEntered.set("00:00")
        self.arrivalTime = Entry(self.top, textvariable=self.arrivalTimeEntered).grid(row=2, column=1)

        # TRAIN TYPE
        self.trainTypeOptions = ["Originating","Destination","Passing"]
        self.trainTypeSelected = StringVar(self.top)
        self.trainTypeSelected.set(self.trainTypeOptions[0])
        Label(self.top, text="Train Type").grid(row=3, column=0)
        self.trainType = OptionMenu(self.top, self.trainTypeSelected, *self.trainTypeOptions).grid(row=3, column=1)

        # TRAIN DIRECTIONS(S)
        self.trainDirectionOptions = ["<NA>","West","East"]
        self.trainFromDirectionSelected = StringVar(self.top)
        self.trainFromDirectionSelected.set(self.trainDirectionOptions[0])
        self.trainToDirectionSelected = StringVar(self.top)
        self.trainToDirectionSelected.set(self.trainDirectionOptions[0])
        Label(self.top, text="From Direction").grid(row=4, column=0)
        Label(self.top, text="To Direction").grid(row=5, column=0)
        self.trainType = OptionMenu(self.top, self.trainFromDirectionSelected, *self.trainDirectionOptions).grid(row=4, column=1)
        self.trainType = OptionMenu(self.top, self.trainToDirectionSelected, *self.trainDirectionOptions).grid(row=5, column=1)

        # SUBMIT/CANCEL BUTTONS
        self.submitButton = Button(self.top, text="Submit", command=self.submit).grid(row=6, column=0)
        self.cancelButton = Button(self.top, text="Cancel", command=self.cancel).grid(row=6, column=1)

    def submit(self):

        trainCode = self.trainNumberEntered.get()
        trainName = self.trainNameEntered.get()
        trainTime = self.arrivalTimeEntered.get()
        trainType = self.trainTypeSelected.get()
        trainDirection = self.trainFromDirectionSelected.get()

        addTrain(trainName, trainCode, trainTime, trainDirection, "NOT_ARRIVED", trainType)

        deptime = finddep(trainTime, trainType)
        tr = Train(app.w, trainCode, trainName, trainTime, deptime, trainType)
        trainl.append(tr)
        waitingtrains.append(tr)
        waitingtrains.sort(key=lambda x: x.arrival)
        trainl.sort(key=lambda x: x.arrival)

        currow = []
        i = len(trainl)
        label = Label(frame,text=trainCode,font = "Helvetica 10")
        label.grid(row=i,column=4)
        currow.append(label)
        label = Label(frame,text=trainName,font = "Helvetica 10")
        label.grid(row=i,column=8)
        currow.append(label)
        label = Label(frame,text=trainTime,font = "Helvetica 10")
        label.grid(row=i,column=12)
        currow.append(label)
        label = Label(frame,text=deptime,font = "Helvetica 10")
        label.grid(row=i,column=16)
        currow.append(label)
        label = Label(frame,text='0',font = "Helvetica 10")
        label.grid(row=i,column=20)
        currow.append(label)
        tablegrid.append(currow)

        dataupdate()

        self.top.destroy()

    def cancel(self):
        self.top.destroy()

###############################################################################

class deleteTrainDialog:

    def __init__(self,parent):

        self.top = Toplevel(parent)

        # TRAIN NUMBER
        Label(self.top, text="Train Number").grid(row=0, column=0)
        self.trainNumberSelected = StringVar(self.top)

        self.trainNumberOptions = []
        for train in getTrainList().find():
            self.trainNumberOptions.append(train["code"])

        self.trainNumberSelected.set(self.trainNumberOptions[0])
        self.trainNumber = OptionMenu(self.top, self.trainNumberSelected, *self.trainNumberOptions).grid(row=0, column=1)

        # SUBMIT/CANCEL BUTTONS
        self.submitButton = Button(self.top, text="Submit", command=self.submit).grid(row=1, column=0)
        self.cancelButton = Button(self.top, text="Cancel", command=self.cancel).grid(row=1, column=1)

    def submit(self):

        trainCode = self.trainNumberSelected.get()
        deleteTrain(trainCode)

        for t in trainl:
            if t.code==trainCode:
                del trainl[trainl.index(t)]
                break
        for row in tablegrid:
            if row[0].cget("text")==trainCode:
                for label in row:
                    label.destroy()
                break

        dataupdate()

        self.top.destroy()

    def cancel(self):

        self.top.destroy()

##############################################################################

class editTrainDialog:

    def __init__(self,parent):

        self.top = Toplevel(parent)

        # TRAIN NUMBER
        Label(self.top, text="Train Number").grid(row=0, column=0)
        self.trainNumberSelected = StringVar(self.top)

        self.trainNumberOptions = []
        for train in getTrainList().find():
            self.trainNumberOptions.append(train["code"])

        self.trainNumber = OptionMenu(self.top, self.trainNumberSelected, *self.trainNumberOptions).grid(row=0, column=1)

        # TRAIN TIME
        Label(self.top, text="Train Time").grid(row=1, column=0)
        self.arrivalTimeEntered = StringVar(self.top)
        self.arrivalTime = Entry(self.top, textvariable=self.arrivalTimeEntered).grid(row=1, column=1)

        # SUBMIT/CANCEL BUTTONS
        self.submitButton = Button(self.top, text="Submit", command=self.submit).grid(row=2, column=0)
        self.cancelButton = Button(self.top, text="Cancel", command=self.cancel).grid(row=2, column=1)

        # CALLBACK for TRAIN TIME
        self.trainNumberSelected.trace('w', self.fillTrainTime)
        self.trainNumberSelected.set(self.trainNumberOptions[0])

    def fillTrainTime(self, *args):

        trainCode = self.trainNumberSelected.get()
        for train in getTrainList().find():
            if train["code"]==trainCode:
                self.arrivalTimeEntered.set(train["arrival_time"])
        

    def submit(self):

        trainCode = self.trainNumberSelected.get()
        trainTime = self.arrivalTimeEntered.get()
        updateTrainArrivalTime(trainCode, trainTime)

        for t in trainl:
            if t.code==trainCode:
                t.arrival = trainTime
                t.departure = finddep(trainTime, t.category)
                break

        waitingtrains.sort(key=lambda x: x.arrival)
        trainl.sort(key=lambda x: x.arrival)

        dataupdate()

        self.top.destroy()

    def cancel(self):

        self.top.destroy()

#####################################################################################################################

class addPlatformDialog:

    def __init__(self,parent):

        self.top = Toplevel(parent)

        Label(self.top, text="Number of platforms").grid(row=0, column=0)
        self.platformNumberEntered = StringVar(self.top)
        self.platformNumber = Entry(self.top, textvariable=self.platformNumberEntered).grid(row=0, column=1)

        # SUBMIT/CANCEL BUTTONS
        self.submitButton = Button(self.top, text="Submit", command=self.submit).grid(row=1, column=0)
        self.cancelButton = Button(self.top, text="Cancel", command=self.cancel).grid(row=1, column=1)

    def submit(self):

        platformNumber = self.platformNumberEntered.get()

        platformCount = 0
        for platform in platforms.find():
            platformCount = platformCount + 1

        for i in range(1,int(platformNumber)+1):
            addPlatform(i+platformCount,"ENABLED","EMPTY","0")
            pl = Platform(app.w, i+platformCount)
            platforml.append(pl)

        self.top.destroy()

    def cancel(self):

        self.top.destroy()

#####################################################################################################################

class editPlatformDialog:

    def __init__(self,parent):

        self.top = Toplevel(parent)

        platformCount = 0
        for platform in platforms.find():
            platformCount = platformCount + 1

        self.platformList = []
        self.platformStatus = []

        for i in range(0,platformCount):
            self.platformStatus.append(IntVar(self.top))
            self.platformStatus[i].set(1)
        
        for i in range(1,platformCount+1):
            Label(self.top, text=("Platform "+str(i))).grid(row=i-1,column=0)
            self.platformList.append(Checkbutton(self.top, variable=self.platformStatus[i-1]))
            self.platformList[i-1].grid(row=i-1, column=1)
            self.platformList[i-1].deselect()

        for platform in platforms.find():
            if platform["status"]=="DISABLED":
                self.platformList[int(platform["number"]-1)].select()

        # SUBMIT/CANCEL BUTTONS
        self.submitButton = Button(self.top, text="Submit", command=self.submit).grid(row=platformCount, column=0)
        self.cancelButton = Button(self.top, text="Cancel", command=self.cancel).grid(row=platformCount, column=1)

    def submit(self):

        i=1
        for status in self.platformStatus:
            if status.get()==1:
                updatePlatformStatus(i,"DISABLED")
                for p in platforml:
                    if p.platformNo==i:
                        p.status=False
                        break
            else:
                updatePlatformStatus(i,"ENABLED")
                for p in platforml:
                    if p.platformNo==i:
                        p.status=True
                        break
            i=i+1


        self.top.destroy()

    def cancel(self):

        self.top.destroy()


class App:

    def __init__(self, master):
        global w, trainl, platforml, outerl, table

        self.w = Canvas(master, width=1300, height=400)
        self.w.pack(side=TOP)
        
        self.f = Frame(master, width=1300, height=300)
        self.f.pack(side=TOP, fill=X)
        

        for p in getPlatformList().find():
            pl = Platform(self.w, p['number'])
            if p['status']=='DISABLED':
                pl.status = False
            platforml.append(pl)

        for i in range(6):
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
        dataupdate()
    
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
        tr = Train(app.w, t['code'], t['name'], t['arrival_time'], deptime, t['type'])
        trainl.append(tr)
        waitingtrains.append(tr)


def finddep(arrival, category):
    [hour, mint] = arrival.split(':')
    if category=="Passing":
        if int(mint)>=55:
            hour = str((int(hour)+1)%24)
        mint=str((int(mint)+5)%60)
    else:
        if int(mint)>=45:
            hour = str((int(hour)+1)%24)
        mint=str((int(mint)+15)%60)
    if len(hour)<2:
        hour = '0'+hour
    if len(mint)<2:
        mint = '0'+mint
    return hour+':'+mint


def simulate():
    global startstate, pltrains, outertrains, waitingtrains
    global trainl, platforml, outerl
    for t in pltrains:
        if timecnt>=t.departure:
            t.vel = 3
            t.platform = 0
            t.status = "departed"
            dataupdate()
            for p in platforml:
                if p.train==t and t.x>=400:
                    p.train = None
                    p.occupied = False
                    del pltrains[pltrains.index(t)]
                    break

    for t in outertrains:
        flag = 0
        for p in platforml:
            if not p.occupied and p.status:
                flag = 1
                outer = t.outerline
                t.vel = 3
                app.w.move(t.body, 0, p.trainy-t.y)
                app.w.move(t.label, 0, p.trainy-t.y)
                t.platform = p.platformNo
                t.status = "arrived"
                t.departure = finddep(timecnt, t.category)
                p.occupied = True
                p.train = t
                del outertrains[outertrains.index(t)]
                dataupdate()
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
                if (not p.occupied) and p.status:
                    flag = 1
                    t.vel = 3
                    t.platform = p.platformNo
                    app.w.move(t.body, 0, p.trainy-t.y)
                    app.w.move(t.label, 0, p.trainy-t.y)
                    t.status = "arrived"
                    t.departure = finddep(timecnt, t.category)
                    p.occupied = True
                    p.train = t
                    del waitingtrains[waitingtrains.index(t)]
                    dataupdate()
                    pltrains.append(t)
                    break
            if flag==0:
                for ol in outerl:
                    if not ol.occupied:
                        ol.occupied = True
                        ol.train = t
                        del waitingtrains[waitingtrains.index(t)]
                        outertrains.append(t)
                        ol.update(app.w)
                        break
                break

    for t in trainl:
        if (t.x<400 and t.status=='arrived') or t.status=='departed':
            t.update(app.w)
    for o in outerl:
        o.update(app.w)

    if startstate:
        master.after(5, simulate)

def counter_label(label):
    def count():
        global counter, startstate, timecnt
        counter += 1
        timecnt = time.strftime("%H:%M", time.gmtime(counter))
        label.config(text="Time: "+time.strftime("%H:%M", time.gmtime(counter)))
        if(startstate):
            label.after(fps, count)
    count()

def data():
    global tablegrid
    Label(frame).grid(row=0,column=0,padx=100)
    currow = []
    label = Label(frame, text="Train Code",font = "Helvetica 14 bold")
    label.grid(row=0,column=4,padx=30)
    currow.append(label)
    label = Label(frame,text="Train Name",font = "Helvetica 14 bold")
    label.grid(row=0,column=8,padx=30)
    currow.append(label)
    label = Label(frame,text="Arrival Time",font = "Helvetica 14 bold")
    label.grid(row=0,column=12,padx=30)
    currow.append(label)
    label = Label(frame,text="Departure Time",font = "Helvetica 14 bold")
    label.grid(row=0,column=16,padx=30)
    currow.append(label)
    label = Label(frame,text="Platform Number",font = "Helvetica 14 bold")
    label.grid(row=0,column=20,padx=30)
    currow.append(label)
    tablegrid.append(currow)
    i = 0
    for trains in waitingtrains:
        currow = []
        label = Label(frame,text=trains.code,font = "Helvetica 10")
        label.grid(row=i+1,column=4)
        currow.append(label)
        label = Label(frame,text=trains.name,font = "Helvetica 10")
        label.grid(row=i+1,column=8)
        currow.append(label)
        label = Label(frame,text=trains.arrival,font = "Helvetica 10")
        label.grid(row=i+1,column=12)
        currow.append(label)
        label = Label(frame,text=trains.departure,font = "Helvetica 10")
        label.grid(row=i+1,column=16)
        currow.append(label)
        label = Label(frame,text=trains.platform,font = "Helvetica 10")
        label.grid(row=i+1,column=20)
        currow.append(label)
        tablegrid.append(currow)
        i+=1

def dataupdate():
    global tablegrid
    i = 1
    for t in trainl:
        tablegrid[i][0].configure(text=t.code)
        tablegrid[i][1].configure(text=t.name)
        tablegrid[i][2].configure(text=t.arrival)
        tablegrid[i][3].configure(text=t.departure)
        if str(t.platform)=='0':
            tablegrid[i][4].configure(text='---')
        else:
            tablegrid[i][4].configure(text=t.platform)
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
# things related to train timetable over

schedule()
data()
master.mainloop()