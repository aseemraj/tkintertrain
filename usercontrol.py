from Tkinter import *
from train import *
from platform import *
from outerline import *
from db import *


#############################################################

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
        self.top.destroy()

    def cancel(self):

        print "CANCELLED!"
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
            else:
                updatePlatformStatus(i,"ENABLED")
            i=i+1

        self.top.destroy()

    def cancel(self):

        self.top.destroy()

        
