
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


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

        self.createWidgets()

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
        for index in xrange(4,-1,-1):
            (plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex+index);
            print("processing %s" % filename)
            self.prevStats = self.mySolar.computeNetPower(plotData, prevPwr=self.prevStats)

    def on_resize(self, event):
        self.plotheight = event.height;
        self.plotwidth = event.width;
        print("resized to %d %d" %(self.plotwidth,self.plotheight))
        self.plotGraph(self.parsedData);

    def plotGraph(self, data):

        #~ data["names"] = []
        #~ data["voltage"] = []
        #~ data["current"] = []
        #~ data["todayCumulativeEnergy"] = []
        #~ data["cumulativeEnergy"] = []
        #~ data["maxEnergy"] = []

        graphPad = 3
        graphTop = graphPad
        graphBottom = self.plotheight - graphPad
        graphLeft = graphPad
        graphRight = self.plotwidth - graphPad
        graphHeight = graphBottom-graphTop
        graphWidth = self.plotwidth - graphPad*2

        #
        # plot batteries
        #


        for sensorIndex in xrange(4):
            batActualIndex = self.batmap[sensorIndex]

            relBatLevel = (data["maxEnergy"][batActualIndex] -
                           data["cumulativeEnergy"][batActualIndex])

            maxBatDrainAmount = 2000*3600   # 2000 mAHr max usable amp hours for now.  computed in mA*Seconds

            actualBatFracMaxDrainRelative = 1.0 - float(relBatLevel)/float(maxBatDrainAmount)

            if relBatLevel > maxBatDrainAmount:
                relBatLevel = maxBatDrainAmount
            bar_1_frac = float(relBatLevel)/float(maxBatDrainAmount)
            bar_2_frac = 1 - bar_1_frac


            bar_1_color = "#777"
            if data["current"][batActualIndex] < -10:
                bar_2_color = "#f00"
            elif data["current"][batActualIndex] > 10:
                bar_2_color = "#0f0"
            else:
                bar_2_color = "#ff0"

            bar_2_top = graphHeight - int(bar_2_frac*graphHeight)
            bar_1_top = bar_2_top - int(bar_1_frac*graphHeight)

            self.energy_Col_graph_canvas[sensorIndex].delete("all");
            self.energy_Col_graph_canvas[sensorIndex].create_rectangle(graphLeft,bar_1_top, graphRight,bar_2_top, fill=bar_1_color)
            self.energy_Col_graph_canvas[sensorIndex].create_rectangle(graphLeft,bar_2_top, graphRight,graphBottom, fill=bar_2_color)

            # set up the battery rate of flow stuff
            self.energy_Col_text[sensorIndex].set( "%d mA" % (data["current"][batActualIndex]) )
            # set up the battery rate of flow stuff
            self.voltage_Col_text[sensorIndex].set( "%2.3f V" % (data["voltage"][batActualIndex]) )
            # set up the battery rate of flow stuff
            self.wattage_Col_text[sensorIndex].set( "%2.3f W" % (data["voltage"][batActualIndex]*data["current"][batActualIndex]/1000) )
            # display percentage
            self.percent_Col_text[sensorIndex].set( "%.1f %%" % (actualBatFracMaxDrainRelative*100.0) )

        # show the panel current and load current values
        self.energy_Col_text[4].set( "%d mA" % (data["current"][0]) )
        self.energy_Col_text[5].set( "%d mA" % (data["current"][3]) )
        # show the panel current and load voltage values
        self.voltage_Col_text[4].set( "%2.3f V" % (data["voltage"][0]) )
        self.voltage_Col_text[5].set( "%2.3f V" % (data["voltage"][3]) )
        # show the panel current and load wattage values
        self.wattage_Col_text[4].set( "%2.3f W" % (data["voltage"][0]*data["current"][0]/1000) )
        self.wattage_Col_text[5].set( "%2.3f W" % (data["voltage"][3]*data["current"][3]/1000) )

        #
        # plot load/panel stuff
        #
        for sensorIndex in xrange(4,6):
            if sensorIndex == 4:
                bar_1_color = "#0f0"
                bar_2_color = "#ff0"
                bar_3_color = "#ff0"

                bar_1_frac = data["todayCumulativeEnergy"][0]/3600.0/ 12000.0 # /3600 convert sec to hr;  /12000 to set max scale to 12000mAHr

                bar_2_frac = 0
                for index in xrange(4):
                    batActualIndex = self.batmap[index]
                    bar_2_frac = bar_2_frac + data["todayCumulativeEnergy"][batActualIndex]
                bar_2_frac = bar_2_frac /3600.0/ 12000.0 # /3600 convert sec to hr;  /12000 to set max scale
                bar_3_frac = data["todayCumulativeEnergy"][3]/3600.0/ 12000.0 # /3600 convert sec to hr;  /12000 to set max scale

                if bar_2_frac < 0:
                    bar_2_frac = abs(bar_2_frac)
                    bar_2_color = "#f00"
                else:
                    bar_2_color = "#0f0"



            else:
                batCurrent = 0
                for index in xrange(4):
                    batActualIndex = self.batmap[index]
                    batCurrent = batCurrent + data["current"][batActualIndex]

                bar_1_color = "#0f0"  # yellow for transfer power bar
                if batCurrent < 0:
                    bar_2_color = "#f00"  # red for discharge
                else:
                    bar_2_color = "#0f0"  # green for charge
                bar_3_color = "#ff0"  # yellow for transfer power bar

                bar_1_frac = float(abs(data["current"][0]))/3200.0  # 3.2A max
                bar_2_frac = float(abs(batCurrent))/3200.0
                bar_3_frac = float(abs(data["current"][3]))/3200.0

                #~ self.energy_Col_text[sensorIndex].set("")

            bar_3_top = graphHeight - int(bar_3_frac*graphHeight)
            bar_2_top = graphHeight - int(bar_2_frac*graphHeight)
            bar_1_top = graphHeight - int(bar_1_frac*graphHeight)

            self.energy_Col_graph_canvas[sensorIndex].delete("all");
            self.energy_Col_graph_canvas[sensorIndex].create_rectangle(
                           graphLeft+((graphWidth*0)/3), bar_1_top,
                           graphLeft+((graphWidth*1)/3), graphHeight,  fill=bar_1_color)
            self.energy_Col_graph_canvas[sensorIndex].create_rectangle(
                           graphLeft+((graphWidth*1)/3), bar_2_top,
                           graphLeft+((graphWidth*2)/3), graphHeight,  fill=bar_2_color)
            self.energy_Col_graph_canvas[sensorIndex].create_rectangle(
                           graphLeft+((graphWidth*2)/3), bar_3_top,
                           graphLeft+((graphWidth*3)/3), graphHeight,  fill=bar_3_color)
        print("plotGraph done")

    def createWidgets(self):
        #
        # set up frames for the 6 sensors
        #
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        #
        # set up overall window frame
        #

        self.energy_LabelFrame = tk.LabelFrame(top, text="System Summary")
        self.energy_LabelFrame.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)


        #
        # set up frames for the 6 sensors
        #
        self.energy_Col_LabelFrame = []
        labels = ["Batt 1","Batt 2","Batt 3","Batt 4","Today","Now"]
        for sensorIndex in xrange(6):
            myField = tk.LabelFrame(self.energy_LabelFrame, text=labels[sensorIndex] )
            myField.grid(column=sensorIndex, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
            myField.rowconfigure(0, weight=1)
            myField.rowconfigure(1, weight=0)
            myField.columnconfigure(0, weight=1)
            self.energy_LabelFrame.rowconfigure(0, weight=1, minsize=100)
            self.energy_LabelFrame.columnconfigure(sensorIndex, weight=1, minsize=70)
            self.energy_Col_LabelFrame.append( myField )

        #
        # set canvas for each bar graph
        #

        self.energy_Col_graph_canvas = []
        for sensorIndex in xrange(6):
            myField = tk.Canvas(self.energy_Col_LabelFrame[sensorIndex], width=70, height=200)
            myField.grid(column=0,row=1, sticky=tk.E + tk.W + tk.N + tk.S )
            self.energy_Col_graph_canvas.append( myField )

            #~ myTextField = myField.create_text(anchor=tk.SW)

        #
        # add resize handler
        #
        self.energy_Col_graph_canvas[0].bind("<Configure>", self.on_resize)

        #
        # set text fields for each bottom
        #

        self.voltage_Col_Label = []
        self.voltage_Col_text = []
        for sensorIndex in xrange(6):
            myStringVar = tk.StringVar()
            myStringVar.set("0 V")
            myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
            myField.grid(column=0,row=2, sticky=tk.E + tk.W + tk.N + tk.S )
            self.voltage_Col_Label.append( myField )
            self.voltage_Col_text.append( myStringVar )

        self.energy_Col_Label = []
        self.energy_Col_text = []
        for sensorIndex in xrange(6):
            myStringVar = tk.StringVar()
            myStringVar.set("0 mA")
            myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
            myField.grid(column=0,row=3, sticky=tk.E + tk.W + tk.N + tk.S )
            self.energy_Col_Label.append( myField )
            self.energy_Col_text.append( myStringVar )

        self.wattage_Col_Label = []
        self.wattage_Col_text = []
        for sensorIndex in xrange(6):
            myStringVar = tk.StringVar()
            myStringVar.set("0 W")
            myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
            myField.grid(column=0,row=4, sticky=tk.E + tk.W + tk.N + tk.S )
            self.wattage_Col_Label.append( myField )
            self.wattage_Col_text.append( myStringVar )

        self.percent_Col_Label = []
        self.percent_Col_text = []
        for sensorIndex in xrange(6):
            myStringVar = tk.StringVar()
            myStringVar.set("")
            myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
            myField.grid(column=0,row=0, sticky=tk.E + tk.W + tk.N + tk.S )
            self.percent_Col_Label.append( myField )
            self.percent_Col_text.append( myStringVar )


    def updateGuiFields(self, solarData):
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

        #~ textData = self.mySolarClient.retrieveData()
        #~ self.parsedData = self.mySolarClient.parseResult(textData)

        newData = self.mySolarClient.retrieveDataUdp()
        if newData != None:
            #~ print(newData)
            self.plotGraph(newData)

        self.after(900,self.periodicEventHandler);
        #~ self.plotGraph(self.parsedData)


class SolarClient():
    def __init__(self):
        self.one_fifo = OneFifo('/tmp/solar_data.fifo')
        self.one_fifo.__enter__()


        self.socket = socket.socket(socket.AF_INET, #internet,
                                    socket.SOCK_DGRAM) #UDP
        self.socket.setblocking(False)
        #~ self.socket.bind( ('127.0.0.1', 29551) )  # port = 's'*256 + 'o'
        self.socket.sendto( 'sub', ('127.0.0.1', 29551))

    def retrieveData(self):
        result = self.one_fifo.read()
        if result is not None:
            print result

        return result

    def retrieveDataUdp(self):
        queue_empty = False
        returnData = None
        while queue_empty == False:
            ready_to_read, ready_to_write, in_error = select.select( [self.socket], [], [], 0.001) # only wait 1 msec

            if len(ready_to_read) == 0:
                queue_empty = True
            else:
                data, address = ready_to_read[0].recvfrom(4096)
                self.listner_address = address
                print('got data msg from %s:%s = %s' % (self.listner_address[0], self.listner_address[1], data))

                returnData = json.loads(data)

        return returnData




    def parseResult(self,dataLine):
        fields = dataLine.split(',')

        parsedData = {}
        parsedData["names"] = []
        parsedData["voltage"] = []
        parsedData["current"] = []
        parsedData["todayCumulativeEnergy"] = []
        parsedData["cumulativeEnergy"] = []
        parsedData["maxEnergy"] = []

        if len(fields) < 6*6+1:
            print("Too few fields (%d) in input line" % (len(fields)) )
        else:

            numChannels = fields[0]

            for index in xrange(int(numChannels)):
                inputFieldIndexBase = 1 + index*6

                parsedData["names"].append(fields[inputFieldIndexBase+0])
                parsedData["voltage"].append(float(fields[inputFieldIndexBase+1]))
                parsedData["current"].append(int(fields[inputFieldIndexBase+2]))
                parsedData["todayCumulativeEnergy"].append(float(fields[inputFieldIndexBase+3]))
                parsedData["cumulativeEnergy"].append(float(fields[inputFieldIndexBase+4]))
                parsedData["maxEnergy"].append(float(fields[inputFieldIndexBase+5]))

            #print(parsedData)
        return parsedData


def main():
    app = Application()
    app.master.title('Solar Panel Monitor')

    app.mySolarClient = SolarClient()

    app.after(0,app.periodicEventHandler);
    app.mainloop() ;







if __name__ == "__main__":
    main();
