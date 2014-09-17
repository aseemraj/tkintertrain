from db import *


deleteTrain("12501")
deleteTrain("12483")
deleteTrain("12481")
deleteTrain("13763")

addTrain("Mandore Exp.","12483","19:30","West","NOT_ARRIVED","Originating")
addTrain("Suryanagari Exp.","12481","17:30","East","NOT_ARRIVED","Destination")
addTrain("Howrah Exp.","12501","05:20","West","NOT_ARRIVED","Passing")
addTrain("Rajdhani Exp.","13763","12:00","East","NOT_ARRIVED","Originating")


#updateTrainArrivalTime("12483","21:45")


for train in trains.find():
	print train