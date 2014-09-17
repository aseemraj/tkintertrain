from db import *
from outerline import *

'''
def getKey(train):
	return train["arrival_time"]

sortedTrain = sorted(trains.find(), key=getKey)

for platform in platforms:
	if platform["status"]=="ENABLED" and platform["occupancy"]=="Empty":
'''

class Scheduler():

	def __init__(self):

		self.trainSchedule = []
		for train in getTrainList().find():
			self.trainSchedule.append({"Code": train["code"],"Direction": train["direction"], "Type": train["type"], "Status": train["status"], "Scheduled_Arrival_Time": train["arrival_time"], "Platform_Arrival_Time": train["arrival_time"], "IsWaiting": False, "WaitLocation": 0 , "WaitTime": 0, "PlatformNumber": 0, "PlatformTime": 0})

		self.platformSchedule = []
		for platform in getPlatformList().find():
			self.platformSchedule.append({"Number": platform["number"], "Status": platform["status"], "Occupancy": platform["occupancy"], "Code": platform["code"]})

		self.sideLineSchedule = []
		for i in range (1,11):
			if i<6:
				self.sideLineSchedule.append({"Number": i, "Occupancy": "EMPTY", "Code": "0", "Location": "LEFT"})
			else:
				self.sideLineSchedule.append({"Number": i, "Occupancy": "EMPTY", "Code": "0", "Location": "RIGHT"})


		for train in self.trainSchedule:
			if train["Type"]=="Passing":
				train["PlatformTime"] = 5
			else:
				train["PlatformTime"] = 15


	#def drawOnPlatform(self,PlatformNumber,direction):


	# def drawOnSideline(self,sideLineNumber):
	# 	qp = QtGui.QPainter()
 #        qp.begin(self)
 #        SideLine = OuterLine(sideLineNumber,QtGui.QColor(255, 0, 0))
 #        SideLine.draw(qp)
 #        qp.end()

	def makeSchedule(self):

		for self.timer in range(0,60*24 + 1):

			self.schedulingPlatformTrains()
			self.schedulingWaitingTrains()
			self.schedulingIncomingTrains()


	def schedulingPlatformTrains(self):
		for train in self.trainSchedule:

			if train["Status"]=="ON_PLATFORM":
				currentTrain = self.getTrain(train["Code"])

				if train["PlatformTime"]==0:
					currentPlatform = self.getPlatform(train["PlatformNumber"])

					print ("Train " + str(currentTrain["Code"]) + " leaves Platform " + str(currentPlatform["Number"]))
					#DepartTrain(currentTrain["Number"],currentTrain["Direction"])

					currentTrain["Status"] = "DEPARTED"

					currentPlatform["Code"] = 0
					currentPlatform["Occupancy"] = "EMPTY"
				else:
					currentTrain["PlatformTime"] = currentTrain["PlatformTime"] - 1

	def schedulingWaitingTrains(self):
		waitingList = []
		for train in self.trainSchedule:

			if train["Status"]=="WAITING":
				waitingList.append(self.getTrain(train["Code"]))

		waitingList = sorted(waitingList, key=lambda k: self.timeToInt(k["Scheduled_Arrival_Time"]))
		waitCount = 0
		for platform in self.platformSchedule:
			if platform["Occupancy"]=="EMPTY" and platform["Status"]=="ENABLED" and waitCount<len(waitingList):
				currentTrain = self.getTrain(waitingList[waitCount]["Code"])
				currentPlatform = self.getPlatform(platform["Number"])
				currentSideLine = self.getSideLine(waitingList[waitCount]["WaitLocation"])
				

				if currentSideLine != None:
					print ("Train " + str(currentTrain["Code"]) + "left SideLine " + str(currentSideLine["Number"]) + " for Platform " + str(currentPlatform["Number"]))
					#changeLocation(sideLine["Number"],currentTrain["PlatformNumber"],currentTrain["Direction"])

					currentTrain["Status"] = "ON_PLATFORM"
					currentTrain["PlatformNumber"] = currentPlatform["Number"]
					currentTrain["Platform_Arrival_Time"] = self.intToTime(self.timer)

					currentPlatform["Occupancy"] = "OCCUPIED"
					currentPlatform["Code"] = currentTrain["Code"]

					currentSideLine["Occupancy"] = "EMPTY"
					currentSideLine["Code"] = 0

					waitCount = waitCount + 1

		
		while waitCount<len(waitingList):
			currentTrain = self.getTrain(waitingList[waitCount]["Code"])
			currentTrain["WaitTime"] = str(int(currentTrain["WaitTime"]) + 1)
			waitCount = waitCount + 1

	def schedulingIncomingTrains(self):
		incomingList = []
		for train in self.trainSchedule:
			if self.timeToInt(train["Scheduled_Arrival_Time"]) == self.timer:
				incomingList.append(self.getTrain(train["Code"]))

		platformList = getPlatformList()

		platformCount = 0
		sideLineCount = 0
		incomingCount = 0

		for platform in self.platformSchedule:
			if platform["Occupancy"]=="EMPTY" and platform["Status"]=="ENABLED" and incomingCount<len(incomingList):
				currentTrain = self.getTrain(incomingList[incomingCount]["Code"])
				currentPlatform = self.getPlatform(platform["Number"])

				currentTrain["Status"] = "ON_PLATFORM"
				currentTrain["PlatformNumber"] = currentPlatform["Number"]
				currentTrain["Platform_Arrival_Time"] = self.intToTime(self.timer)

				currentPlatform["Occupancy"] = "OCCUPIED"
				currentPlatform["Code"] = currentTrain["Code"]

				print (str(currentTrain["Code"]) + " arrived on platform " + str(currentTrain["PlatformNumber"]))

				#self.drawOnPlatform(PlatformNumber,currentTrain["Direction"])
				incomingCount = incomingCount + 1
				

		while incomingCount < len(incomingList) :

			currentTrain = self.getTrain(incomingList[incomingCount]["Code"])
			alloted = False

			for sideLine in self.sideLineSchedule:

				if alloted == False :
					if sideLine["Occupancy"]=="EMPTY" and sideLine["Number"] < 6 and currentTrain["Direction"] == "East" :
						
						currentSideLine = self.getSideLine(sideLine["Number"])
						alloted = True
						currentTrain["IsWaiting"] = True
						currentTrain["Status"] = "WAITING"
						currentTrain["WaitLocation"] = currentSideLine["Number"]
						# self.drawOnSideline(sideLine["Number"])

						print (str(currentTrain["Code"]) + " IS" + " WAITING" + " ON " + str(currentSideLine["Number"]) )

						currentSideLine["Occupancy"] = "OCCUPIED"
						currentSideLine["Code"] = currentTrain["Code"]

						incomingCount = incomingCount + 1

					elif sideLine["Occupancy"]=="EMPTY" and sideLine["Number"] >= 6 and currentTrain["Direction"] == "West" :
						alloted = True
						currentSideLine = self.getSideLine(sideLine["Number"])

						currentTrain["IsWaiting"] = True
						currentTrain["Status"] = "WAITING"
						currentTrain["WaitLocation"] = currentSideLine["Number"]
						# self.drawOnSideline(sideLine["Number"])

						print (str(currentTrain["Code"]) + " IS" + " WAITING" + " ON SideLine " + str(currentSideLine["Number"]) )

						currentSideLine["Occupancy"] = "OCCUPIED"
						currentSideLine["Code"] = currentTrain["Code"]

						incomingCount = incomingCount + 1

			if alloted == False:
				currentTrain["Scheduled_Arrival_Time"] = self.intToTime( self.timeToInt(currentTrain["Scheduled_Arrival_Time"]) + 1)
				incomingCount = incomingCount + 1

		while incomingCount < len(incomingList):
			currentTrain = self.getTrain(incomingList[incomingCount]["Code"])
			currentTrain["Scheduled_Arrival_Time"] = self.intToTime( self.timeToInt(currentTrain["Scheduled_Arrival_Time"]) + 1)
			incomingCount = incomingCount + 1


	def getTrain(self,code):
		for train in self.trainSchedule:
			if train["Code"]==code:
				return train

	def getPlatform(self,number):
		for platform in self.platformSchedule:
			if platform["Number"]==number:
				return platform

	def getSideLine(self,number):
		for sideLine in self.sideLineSchedule:
			if sideLine["Number"]==number:
				return sideLine

	def timeToInt(self,timeString):
		timeList = timeString.split(':')
		return(60*int(timeList[0]) + int(timeList[1]))

	def intToTime(self,timeInt):
		hour  = str(int(timeInt/60))
		if int(hour)<10:
			hour = "0" + hour

		minute = str(int(timeInt%60))
		if int(minute)<10:
			minute = "0" + minute

		return(hour + ":" + minute)

sch = Scheduler()
sch.makeSchedule()

print "from now"
print sch.trainSchedule



		
