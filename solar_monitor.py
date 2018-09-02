
#!/usr/bin/python

from Subfact_ina219 import INA219
import time
import os
import glob
import Tkinter as tk
import math
import copy
from OneFifo import OneFifo
import json
import socket
import select

from SolarMonitor import SolarMonitor
from SolarSensors import SolarSensors
from SolarServer import SolarServer
from SolarDb import SolarDb

def orig_main():
    ina = INA219()
    result = ina.getBusVoltage_V()

    print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
    print "Bus     : %.3f V" % ina.getBusVoltage_V()
    print "Current : %.3f mA" % ina.getCurrent_mA()


class Solar:
    def __init__(self, sensors, timestamper, filenamePrefix="solarLog_"):
        self.m_SolarSensors = sensors;
        self.m_SolarDb = SolarDb(filenamePrefix);
        self.m_Timestamper = timestamper;

    def gatherData(self):
        data = self.m_SolarSensors.getData();
        return data;

    def formatPrintData(self, results):
        returnValue = []
        returnValue.append( "%-20s %-20s %-20s %-20s %-20s %-20s" % (results["names"][0],results["names"][1],results["names"][2],results["names"][4],results["names"][5],results["names"][3]));
        returnValue.append( "%2.3f V             %2.3f V             %2.3f V             %2.3f V             %2.3f V             %2.3f V" % (results["voltage"][0],results["voltage"][1],results["voltage"][2],results["voltage"][4],results["voltage"][5],results["voltage"][3]));
        returnValue.append( "%5.0f mA             %5.0f mA             %5.0f mA             %5.0f mA             %5.0f mA             %5.0f mA" % (results["current"][0],results["current"][1],results["current"][2],results["current"][4],results["current"][5],results["current"][3]));
        returnValue.append( "%5.0f mW             %5.0f mW             %5.0f mW             %5.0f mW             %5.0f mW             %5.0f mW" % (results["voltage"][0]*results["current"][0],results["voltage"][1]*results["current"][1],results["voltage"][2]*results["current"][2],results["voltage"][4]*results["current"][4],results["voltage"][5]*results["current"][5],results["voltage"][3]*results["current"][3]));
        return returnValue;

    def printResults(self, results):
        text = self.formatPrintData(results)
        print;
        for index in xrange(len(text)):
            print(text[index]);

    def recordData(self,data):
        rollOver = self.m_SolarDb.addEntry(self.m_Timestamper.getDate(), self.m_Timestamper.getTime(), data );
        return rollOver

    def getEmptyStatsDB(self):
        results = []
        for channelIndex in xrange(6):
            tempVal = {}
            tempVal["minEnergy"] = 0
            tempVal["maxEnergy"] = 0
            tempVal["cumulativeEnergy"] = 0
            results.append(tempVal);
        return results

    def computeNetPower(self, data, prevPwr=None):

        if prevPwr == None:
            results = self.getEmptyStatsDB()
        else:
            results = prevPwr

        for channelIndex in xrange(6):
            for index in xrange( len(data[channelIndex]["voltage"])-1 ):
                timeDelta = self.convertTimeString( data[channelIndex]["time"][index+1]) - self.convertTimeString(data[channelIndex]["time"][index])
                if (timeDelta <= 12 ):
#                   power=data[channelIndex]["voltage"][index] * data[channelIndex]["current"][index]
                    power=data[channelIndex]["current"][index]  # use mAHr for power.
                    energy = power*timeDelta
                    results[channelIndex]["cumulativeEnergy"] = results[channelIndex]["cumulativeEnergy"] + energy

                    if results[channelIndex]["cumulativeEnergy"] < results[channelIndex]["minEnergy"]:
                        results[channelIndex]["minEnergy"] = results[channelIndex]["cumulativeEnergy"];
                    elif results[channelIndex]["cumulativeEnergy"] > results[channelIndex]["maxEnergy"]:
                        results[channelIndex]["maxEnergy"] = results[channelIndex]["cumulativeEnergy"]


        for channelIndex in xrange(6):
            print("minEnergy=%.1f mAHr   maxEnergy=%.1f mAHr  cumulative=%.1f mAHr" % ( results[channelIndex]["minEnergy"]/3600.0, results[channelIndex]["maxEnergy"]/3600.0, results[channelIndex]["cumulativeEnergy"]/3600.0))
        print
        return results

    def convertTimeString(self, time):
        timeSec = 0;
        timeSec = timeSec + int(time[0:2])*60*60
        timeSec = timeSec + int(time[3:5])*60
        timeSec = timeSec + int(time[6:8])
        return timeSec

class TimestamperInterface:
    def getDate(self):
        pass;

    def getTime(self):
        pass

class Timestamper(TimestamperInterface):
    def getDate(self):
        return (time.strftime("%Y_%m_%d"))

    def getTime(self):
        return (time.strftime("%H:%M:%S"))


    


#class Application(tk.Frame):
class Application():
    def __init__(self, master=None):
        #tk.Frame.__init__(self, master)
        #self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        #self.createWidgets()

        self.plotData = None;

        self.leftPad = 40
        self.topPad = 10
        self.bottomPad = 30
        self.rightPad = 10
        self.currentParm = -1;
        self.currentFileIndex = 0;  # most recent
        self.firstPoint = 0
        self.lastPoint = 0;

        self.currentBatPwr = 0
        self.currentPanelPwr = 0
        self.currentLoadPwr = 0
        self.currentBatPwrList = []
        for index in xrange(4):
            self.currentBatPwrList.append(0)

        self.plotheight = 1; # dummy values.
        self.plotwidth = 1; # dummy values.
        self.todayStats = None

        self.batmap = [1,2,4,5] # list of channels that are batteries


    def setSolar(self, solar):
        self.mySolar = solar
        (plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex);
        self.todayStats = self.mySolar.computeNetPower(plotData)

        self.prevStats = None
        for index in xrange(1,-1,-1): # fixme put back to 4,-1,-1
            (plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex+index);
            print("processing %s" % filename)
            self.prevStats = self.mySolar.computeNetPower(plotData, prevPwr=self.prevStats)



    #~ def createWidgets(self):
        #~ #
        #~ # set up frames for the 6 sensors
        #~ #
        #~ top=self.winfo_toplevel()
        #~ top.rowconfigure(0, weight=1)
        #~ top.columnconfigure(0, weight=1)

        #~ #
        #~ # set up overall window frame
        #~ #

        #~ self.energy_LabelFrame = tk.LabelFrame(top, text="System Summary")
        #~ self.energy_LabelFrame.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)


        #~ #
        #~ # set up frames for the 6 sensors
        #~ #
        #~ self.energy_Col_LabelFrame = []
        #~ labels = ["Batt 1","Batt 2","Batt 3","Batt 4","Today","Now"]
        #~ for sensorIndex in xrange(6):
            #~ myField = tk.LabelFrame(self.energy_LabelFrame, text=labels[sensorIndex] )
            #~ myField.grid(column=sensorIndex, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
            #~ myField.rowconfigure(0, weight=1)
            #~ myField.rowconfigure(1, weight=0)
            #~ myField.columnconfigure(0, weight=1)
            #~ self.energy_LabelFrame.rowconfigure(0, weight=1, minsize=100)
            #~ self.energy_LabelFrame.columnconfigure(sensorIndex, weight=1, minsize=70)
            #~ self.energy_Col_LabelFrame.append( myField )

        #~ #
        #~ # set canvas for each bar graph
        #~ #

        #~ self.energy_Col_graph_canvas = []
        #~ for sensorIndex in xrange(6):
            #~ myField = tk.Canvas(self.energy_Col_LabelFrame[sensorIndex], width=70, height=200)
            #~ myField.grid(column=0,row=0, sticky=tk.E + tk.W + tk.N + tk.S )
            #~ self.energy_Col_graph_canvas.append( myField )

           #~ # myTextField = myField.create_text(anchor=tk.SW)

        #~ #
        #~ # add resize handler
        #~ #
        #~ #self.energy_Col_graph_canvas[0].bind("<Configure>", self.on_resize)

        #~ #
        #~ # set text fields for each bottom
        #~ #

        #~ self.energy_Col_Label = []
        #~ self.energy_Col_text = []
        #~ for sensorIndex in xrange(6):
            #~ myStringVar = tk.StringVar()
            #~ myStringVar.set("0 mA")
            #~ myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
            #~ myField.grid(column=0,row=1, sticky=tk.E + tk.W + tk.N + tk.S )
            #~ self.energy_Col_Label.append( myField )
            #~ self.energy_Col_text.append( myStringVar )



    def accumulateEnergy(self, solarData):
        # 0-panel;  1-bat 1;  2-bat 2;  3-load;  4-bat 3;  5-bat 4

        powerInts = []
        for index in xrange(6):
            value = int(solarData["current"][index])
            powerInts.append(value)

        #~ bat_1_pwr = int(solarData["current"][1])
        #~ bat_2_pwr = int(solarData["current"][2])
        #~ bat_3_pwr = int(solarData["current"][4])
        #~ bat_4_pwr = int(solarData["current"][5])

        #~ self.currentBatPwrList.append( bat_1_pwr )
        #~ self.currentBatPwrList.append( bat_2_pwr )
        #~ self.currentBatPwrList.append( bat_3_pwr )
        #~ self.currentBatPwrList.append( bat_4_pwr )

        self.currentBatPwr = 0;
        #~ self.currentBatPwrList = []
        for index in xrange(4):
            self.currentBatPwrList[index] = powerInts[self.batmap[index]]
            self.currentBatPwr = self.currentBatPwr + self.currentBatPwrList[index]

        panelPwr = powerInts[0]
        loadPwr  = powerInts[3]

        self.currentPanelPwr = int( panelPwr )
        self.currentLoadPwr  = int( loadPwr )

        # add new readings to totals;  assume 1 second integration window
        for index in xrange(6):
            self.todayStats[index]["cumulativeEnergy"] = self.todayStats[index]["cumulativeEnergy"] + powerInts[index]
            self.prevStats[index]["cumulativeEnergy"] = self.prevStats[index]["cumulativeEnergy"] + powerInts[index]

            if self.prevStats[index]["cumulativeEnergy"] < self.prevStats[index]["minEnergy"]:
                self.prevStats[index]["minEnergy"] = self.prevStats[index]["cumulativeEnergy"];
            elif self.prevStats[index]["cumulativeEnergy"] > self.prevStats[index]["maxEnergy"]:
                self.prevStats[index]["maxEnergy"] = self.prevStats[index]["cumulativeEnergy"]

    def periodicEventHandler(self):
        #self.after(1000,self.periodicEventHandler);

        data = self.mySolar.gatherData();
        self.accumulateEnergy(data);
        #~ self.plotGraph()
        rollOver = self.mySolar.recordData(data);
        if rollOver:
            self.todayStats = self.mySolar.getEmptyStatsDB()  # we had a day rollover. reset the daily stats
        self.mySolar.printResults(data)

        self.mySolarServer.sendUpdate(data, self)



def main(config):
    #~ app = Application()
    #~ app.setSolar( setupSolar() )

    #~ app.mySolarServer = SolarServer()

    #~ mySolarSensors = SolarSensors(config)
    #~ mySolarServer = SolarServer()
    mySolarMonitor = SolarMonitor(config)
    
    mySolarMonitor.run()

    #~ while True:
        #~ # app.periodicEventHandler()
        #~ live_data = mySolarSensors.getData()
        #~ mySolarServer.sendUpdate(live_data, cumulative_data)
        
        #~ print(live_data)
        #~ time.sleep(1.0)

#    {
#        "address": "0x46", 
#        "name": "Batt 2", 
#        "scale": 1.0
#    },




if __name__ == "__main__":
    fp = open("config.json", "r")
    config_string = fp.read()
    fp.close()
    config = json.loads(config_string)

    main(config)
