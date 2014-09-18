from db import *


deleteTrain("12501")
deleteTrain("12483")
deleteTrain("12481")
deleteTrain("13763")

addTrain("Mandore Express","12483","12:30","West","NOT_ARRIVED","Originating")
addTrain("Suryanagari Express","12481","12:25","East","NOT_ARRIVED","Destination")
addTrain("Howrah Express","12501","12:20","West","NOT_ARRIVED","Passing")
addTrain("Bangalore Rajdhani","13763","12:00","East","NOT_ARRIVED","Passing")
addTrain("KGP Rajdhani","45687","12:00","East","NOT_ARRIVED","Passing")
addTrain("Mumbai Rajdhani","13489","12:00","East","NOT_ARRIVED","Passing")
addTrain("BBS Rajdhani","64192","12:00","East","NOT_ARRIVED","Passing")
addTrain("Sealdah Rajdhani","18634","12:00","East","NOT_ARRIVED","Passing")
addTrain("EMU Ghaziabad","72641","12:00","East","NOT_ARRIVED","Originating")
addTrain("EMU Faridabad","31674","12:00","East","NOT_ARRIVED","Originating")
addTrain("Jaisalmer Intercity","10034","12:00","East","NOT_ARRIVED","Originating")
addTrain("Ranthambhore Express","72685","12:00","East","NOT_ARRIVED","Originating")
addTrain("Kathmandu Express","52846","12:00","East","NOT_ARRIVED","Originating")
addTrain("Lahore Express","52467","12:00","East","NOT_ARRIVED","Originating")
addTrain("Dhaka Mail","34252","12:00","East","NOT_ARRIVED","Originating")

# for n in range(6):
#     addPlatform(n+1, "ENABLED", "EMPTY", "0")

#updateTrainArrivalTime("12483","21:45")
