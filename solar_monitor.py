
#!/usr/bin/python

from Subfact_ina219 import INA219
import time
import os
import glob
import Tkinter as tk
import math
import copy

def orig_main():
	ina = INA219()
	result = ina.getBusVoltage_V()

	print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
	print "Bus     : %.3f V" % ina.getBusVoltage_V()
	print "Current : %.3f mA" % ina.getCurrent_mA()

class SolarSensors:
	def __init__(self):
		self.m_sensors = [];
		self.m_sensorNames = [];

	def addSensor(self,name,sensor):
		self.m_sensors.append(sensor);
		self.m_sensorNames.append(name);

	def getData(self):
		returnVal = {};

		returnVal["names"] = [];
		returnVal["voltage"] = [];
		returnVal["current"] = [];

		for index in xrange(len(self.m_sensors)):
			returnVal["names"].append(self.m_sensorNames[index]);

			voltage = self.m_sensors[index].getBusVoltage_V()
			current = self.m_sensors[index].getCurrent_mA()
			returnVal["voltage"].append( voltage );
			returnVal["current"].append( current );

		return returnVal;

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
		self.m_SolarDb.addEntry(self.m_Timestamper.getDate(), self.m_Timestamper.getTime(), data );

	def computeNetPower(self, data, prevPwr=None):
		
		if prevPwr == None:
			results = []
			for channelIndex in xrange(6):
				tempVal = {}
				tempVal["minEnergy"] = 0
				tempVal["maxEnergy"] = 0
				tempVal["cumulativeEnergy"] = 0
				results.append(tempVal);
		else:
			results = prevPwr

		for channelIndex in xrange(6):
			for index in xrange( len(data[channelIndex]["voltage"])-1 ):
				timeDelta = self.convertTimeString( data[channelIndex]["time"][index+1]) - self.convertTimeString(data[channelIndex]["time"][index])
				if (timeDelta <= 12 ):
#					power=data[channelIndex]["voltage"][index] * data[channelIndex]["current"][index]
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

class SolarDb:
	def __init__(self, filenamePrefix):
		self.totalEnergy = 0.0;
		self.m_sensorNames = [];
		self.m_voltages = [];
		self.m_currents = [];
		self.m_times = [];
		self.m_date = "0000_00_00";
		self.m_filename = "unknown"
		self.m_prev_sampleWindow = -1;
		for index in xrange(6):
			emptyList = []
			self.m_voltages.append(emptyList);
			emptyList = []
			self.m_currents.append(emptyList);
		self.m_filenamePrefix = filenamePrefix;

		averages = {}
		averages["voltage"] = [];
		averages["current"] = [];

		for index in xrange(6):
			averages["voltage"].append( 0.0 );
			averages["current"].append( 0 );
		self.averages = averages
		self.averages_dataPoints = 0


	def addEntry(self, date, time, data):

		# figure the new point into the averages.
		for index in xrange(len(data["voltage"])):
			self.averages["voltage"][index] = self.averages["voltage"][index] + data["voltage"][index];
			self.averages["current"][index] = self.averages["current"][index] + data["current"][index];
		self.averages_dataPoints = self.averages_dataPoints +1;

		if ( self.averages_dataPoints == 10):
			# if rollover, flush the old data to the file.
			sampleWindow = int(time[3:5])/10
			if ( self.m_prev_sampleWindow != sampleWindow ) and (self.m_date != "0000_00_00"): # the hour rolled over.
				m_prev_sampleWindow = sampleWindow;

				self.m_filename = self.m_filenamePrefix+self.m_date+".csv"

				# create the file if necessary
				if not os.path.exists(self.m_filename):
					f = open(self.m_filename, 'w')
					headerLineText = "time"
					for index in xrange(6):
						newSection = ",%s voltage,%s current" % (data["names"][index], data["names"][index])
						headerLineText = headerLineText+newSection
					f.write(headerLineText)
					#~ f.write("time,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current\n" % (data["names"][0], data["names"][0], data["names"][1], data["names"][1], data["names"][2], data["names"][2], data["names"][3], data["names"][3]))
					f.close();

				# append the current data
				f = open(self.m_filename, 'a')
				print("length=%d" % (len(self.m_voltages[0])))
				for index in xrange(len(self.m_voltages[0])):
					f.write(self.m_times[index]);
					f.write(",");
					for sensorIndex in xrange(6):
						f.write("%s,%s" % (self.m_voltages[sensorIndex][index],self.m_currents[sensorIndex][index] ))
						if (sensorIndex != 5):
							f.write(",");
					f.write("\n");
				f.close()


				# clear the cached data for the next hour
				self.m_voltages = [];
				self.m_currents = [];
				self.m_times = [];
				for index in xrange(6):
					emptyList = []
					self.m_voltages.append(emptyList);
					emptyList = []
					self.m_currents.append(emptyList);

			self.m_date = date;
			self.m_prev_sampleWindow = sampleWindow

			self.m_times.append(time);
			for index in xrange(len(data["voltage"])):
				voltageAvg = self.averages["voltage"][index] / self.averages_dataPoints;
				currentAvg = self.averages["current"][index] / self.averages_dataPoints;

				self.m_voltages[index].append(voltageAvg);
				self.m_currents[index].append(currentAvg);
				self.m_sensorNames.append(data["names"][index] );
#				print("avgV=%2.3f  avgC=%d" % (voltageAvg,currentAvg))

			for index in xrange(len(data["voltage"])): # clear out the averages for next time.
				self.averages["voltage"][index] = 0.0;
				self.averages["current"][index] = 0;
			self.averages_dataPoints = 0;

	#
	# retval = [0-3] = {} "name"       = [0-3] = string "panel", "load", etc."
	#                     "voltage"    = [0-n] = float Volts
	#                     "current"    = [0-n] = int  mAmps
	#                     "time"       = [0-n] = string "hh:mm:ss"
	#                     "maxVoltage" = float
	#                     "maxCurrent" = float

	def readDayLog(self,fileIndex):
		returnVal = [];

		filename = self.getFilenameFromIndex(fileIndex)

		for index in xrange(6):
			tempVal = {}  # put an empty dictionary for each array entry.
			tempVal["name"]    = []
			tempVal["voltage"] = []
			tempVal["current"] = []
			tempVal["time"]    = []

			returnVal.append(tempVal);

		fileHandle = open(filename,"r");
		rawLines = fileHandle.readlines();
		firstLineFields = rawLines[0].split(",");

		for chanIndex in xrange(6):
			returnVal[chanIndex]["name"] = firstLineFields[1+chanIndex*2][:-8];  # strip off " voltage" from the end for the base name.

		#~ returnVal[0]["name"] = firstLineFields[1][:-8];  # strip off " voltage" from the end for the base name.
		#~ returnVal[1]["name"] = firstLineFields[3][:-8];  # strip off " voltage" from the end for the base name.
		#~ returnVal[2]["name"] = firstLineFields[5][:-8];  # strip off " voltage" from the end for the base name.
		#~ returnVal[3]["name"] = firstLineFields[7][:-8];  # strip off " voltage" from the end for the base name.

		for chanIndex in xrange(6):
			returnVal[chanIndex]["maxVoltage"] = -99999999.0 # very small.
			returnVal[chanIndex]["minVoltage"] =  99999999.0 # very big.
			returnVal[chanIndex]["maxCurrent"] = -99999999 # very small.
			returnVal[chanIndex]["minCurrent"] =  99999999 # very big.
			returnVal[chanIndex]["maxPower"] = -99999999 # very small.
			returnVal[chanIndex]["minPower"] =  99999999 # very big.

		for index in xrange(1,len(rawLines)):
			fields = rawLines[index].split(",");

			for chanIndex in xrange(6):
				returnVal[chanIndex]["voltage"].append(float(fields[1+chanIndex*2]))
				returnVal[chanIndex]["current"].append(int(fields[2+chanIndex*2]))
				returnVal[chanIndex]["time"].append(fields[0])

				if (returnVal[chanIndex]["maxVoltage"] < float(fields[1+chanIndex*2])):
					returnVal[chanIndex]["maxVoltage"] = float(fields[1+chanIndex*2])
				if (returnVal[chanIndex]["minVoltage"] > float(fields[1+chanIndex*2])):
					returnVal[chanIndex]["minVoltage"] = float(fields[1+chanIndex*2])
				if (returnVal[chanIndex]["maxCurrent"] < int(fields[2+chanIndex*2])):
					returnVal[chanIndex]["maxCurrent"] = int(fields[2+chanIndex*2])
				if (returnVal[chanIndex]["minCurrent"] > int(fields[2+chanIndex*2])):
					returnVal[chanIndex]["minCurrent"] = int(fields[2+chanIndex*2])
				if (returnVal[chanIndex]["maxPower"] < float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])):
					returnVal[chanIndex]["maxPower"] = float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])
				if (returnVal[chanIndex]["minPower"] > float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])):
					returnVal[chanIndex]["minPower"] = float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])

		fileHandle.close()
		return (returnVal, filename);

	def getFilenameFromIndex(self, index):
		fileList = []
		pattern = self.m_filenamePrefix + "*.csv"
#		print(pattern)
		for file in glob.glob( pattern ):
			fileList.append(file)

		fileList.sort()
		fileList.reverse()
		filteredIndex = index;
		if filteredIndex < 0:
			filteredIndex = 0
		elif filteredIndex >= len(fileList):
			filteredIndex = len(fileList)-1
		return fileList[filteredIndex]

def setupSolar():
	mySolarSensors = SolarSensors()

#   ina = INA219(0x40);
#   mySolarSensors.addSensor("Panel", ina ); # no jumpers.
#   mySolarSensors.addSensor("Battery1", ina ); # A0 jumper.
#   mySolarSensors.addSensor("Battery2", ina ); # A1 jumper.
#   mySolarSensors.addSensor("Load", ina ); # A0 and A1 jumpers.

	mySolarSensors.addSensor("Solar Panel (45)", INA219(0x45) ); # A0 and A1 jumpers.
	mySolarSensors.addSensor("Battery 1 (44)", INA219(0x44) ); # A1 jumper.
	mySolarSensors.addSensor("Battery 2 (41)", INA219(0x41) ); # A0 jumper.
	mySolarSensors.addSensor("Load (40)", INA219(0x40) ); # no jumpers.
	mySolarSensors.addSensor("Battery 3 (42)", INA219(0x42) ); # A0->SDA  A1=0
	mySolarSensors.addSensor("Battery 4 (43)", INA219(0x43) ); # A0->SCL  A1=0

	mySolar = Solar(mySolarSensors, Timestamper() );
	return mySolar;





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

		self.currentXferPwr = 0
		self.currentBatPwr = 0
		self.currentPanelPwr = 0
		self.currentLoadPwr = 0
		self.currentBatPwrList = []
		for index in xrange(4):
			self.currentBatPwrList.append(0)

		self.plotheight = 1; # dummy values.
		self.plotwidth = 1; # dummy values.
		self.todayStats = None


	def setSolar(self, solar):
		self.mySolar = solar
		(plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex);
		self.todayStats = self.mySolar.computeNetPower(plotData)

		self.prevStats = copy.deepcopy(self.todayStats)
		for index in xrange(1,5):
			(plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex+index);
			self.prevStats = self.mySolar.computeNetPower(plotData, prevPwr=self.prevStats)

	def on_resize(self, event):
		self.plotheight = event.height;
		self.plotwidth = event.width;
		print("resized to %d %d" %(self.plotwidth,self.plotheight))
		self.plotGraph();

	def plotGraph(self):

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

			fraction = 0.1 + sensorIndex*0.1
			boundary = graphTop + int(graphHeight*fraction)

			if sensorIndex <= 3:
				bar_1_color = "#777"
				if self.currentBatPwrList[sensorIndex] < 0:
					bar_2_color = "#f00"
				else:
					bar_2_color = "#0f0"
				bar_2_frac = 0.6 - sensorIndex*0.1
				bar_1_frac = 1 - bar_2_frac

			bar_2_top = graphHeight - int(bar_2_frac*graphHeight)
			bar_1_top = bar_2_top - int(bar_1_frac*graphHeight)

			self.energy_Col_graph_canvas[sensorIndex].delete("all");
			self.energy_Col_graph_canvas[sensorIndex].create_rectangle(graphLeft,bar_1_top, graphRight,bar_2_top, fill=bar_1_color)
			self.energy_Col_graph_canvas[sensorIndex].create_rectangle(graphLeft,bar_2_top, graphRight,graphBottom, fill=bar_2_color)

		#
		# plot load/panel stuff
		#
		for sensorIndex in xrange(4,6):
			if sensorIndex == 4:
				bar_1_color = "#0f0"
				bar_2_color = "#ff0"
				bar_3_color = "#ff0"

				if self.todayStats == None:
					bar_1_frac = 0.1
					bar_2_frac = 0.6 - sensorIndex*0.1
					bar_3_frac = 0.1
				else:
					bar_1_frac = self.todayStats[0]["cumulativeEnergy"]/3600.0/ 12000.0 # /3600 convert sec to hr;  /12000 to set max scale to 12000mAHr
					bar_2_frac = ((self.todayStats[1]["cumulativeEnergy"] +
					               self.todayStats[2]["cumulativeEnergy"] +
					               self.todayStats[4]["cumulativeEnergy"] +
					               self.todayStats[5]["cumulativeEnergy"] )
					                     /3600.0/ 12000.0) # /3600 convert sec to hr;  /12000 to set max scale
					bar_3_frac = self.todayStats[3]["cumulativeEnergy"]/3600.0/ 12000.0 # /3600 convert sec to hr;  /12000 to set max scale

					if bar_2_frac < 0:
						bar_2_frac = abs(bar_2_frac)
						bar_2_color = "#f00"
					else:
						bar_2_color = "#0f0"
						

			else:
				bar_1_color = "#0f0"  # yellow for transfer power bar
				if self.currentBatPwr < 0:
					bar_2_color = "#f00"  # red for discharge
				else:
					bar_2_color = "#0f0"  # green for charge
				bar_3_color = "#ff0"  # yellow for transfer power bar

				bar_1_frac = float(abs(self.currentPanelPwr))/3200.0  # 3.2A max
				bar_2_frac = float(abs(self.currentBatPwr))/3200.0
				bar_3_frac = float(abs(self.currentLoadPwr))/3200.0

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
			myField.grid(column=0,row=0, sticky=tk.E + tk.W + tk.N + tk.S )
			self.energy_Col_graph_canvas.append( myField )

			#~ myTextField = myField.create_text(anchor=tk.SW)

		#
		# add resize handler
		#
		self.energy_Col_graph_canvas[0].bind("<Configure>", self.on_resize)

		#
		# set text fields for each
		#

		self.energy_Col_Label = []
		self.energy_Col_text = []
		for sensorIndex in xrange(6):
			myStringVar = tk.StringVar()
			myStringVar.set("12345 mAHr")
			myField = tk.Label(self.energy_Col_LabelFrame[sensorIndex], textvariable=myStringVar)
			myField.grid(column=0,row=1, sticky=tk.E + tk.W + tk.N + tk.S )
			self.energy_Col_Label.append( myField )
			self.energy_Col_text.append( myStringVar )



	def updateGuiFields(self, solarData):
		# 0-panel;  1-bat 1;  2-bat 2;  3-load;  4-bat 3;  5-bat 4
		self.currentBatPwrList = []
		bat_1_pwr = int(solarData["current"][1])
		bat_2_pwr = int(solarData["current"][2])
		bat_3_pwr = int(solarData["current"][4])
		bat_4_pwr = int(solarData["current"][5])

		self.currentBatPwrList.append( bat_1_pwr )
		self.currentBatPwrList.append( bat_2_pwr )
		self.currentBatPwrList.append( bat_3_pwr )
		self.currentBatPwrList.append( bat_4_pwr )

		self.currentBatPwr = 0;
		for index in xrange(4):
			self.currentBatPwr = self.currentBatPwr + self.currentBatPwrList[index]

		panelPwr = int(solarData["current"][0]) # use load voltage to try to ignore losses in regulator.
		loadPwr  = int(solarData["current"][3])

		self.currentPanelPwr = int( panelPwr )
		self.currentLoadPwr  = int( loadPwr )

		self.currentXferPwr = self.currentPanelPwr - self.currentBatPwr

		# add new readings to totals;  assume 1 second integration window
		self.todayStats[0]["cumulativeEnergy"] = self.todayStats[0]["cumulativeEnergy"] + panelPwr
		self.todayStats[1]["cumulativeEnergy"] = self.todayStats[1]["cumulativeEnergy"] + bat_1_pwr
		self.todayStats[2]["cumulativeEnergy"] = self.todayStats[2]["cumulativeEnergy"] + bat_2_pwr
		self.todayStats[3]["cumulativeEnergy"] = self.todayStats[3]["cumulativeEnergy"] + loadPwr
		self.todayStats[4]["cumulativeEnergy"] = self.todayStats[4]["cumulativeEnergy"] + bat_3_pwr
		self.todayStats[5]["cumulativeEnergy"] = self.todayStats[5]["cumulativeEnergy"] + bat_4_pwr



	def periodicEventHandler(self):
		self.after(1000,self.periodicEventHandler);

		data = self.mySolar.gatherData();
		self.updateGuiFields(data);
		self.plotGraph()
		self.mySolar.recordData(data);
		self.mySolar.printResults(data)

def main():
	app = Application()
	app.master.title('Solar Panel Monitor')
	app.setSolar( setupSolar() )
	app.after(0,app.periodicEventHandler);
	app.mainloop() ;


	#~ mySolar = setupSolar()
	#~ while(True):
		#~ data = mySolar.gatherData();
		#~ mySolar.recordData(data);
		#~ mySolar.printResults(data);
		#~ # update gui
		#~ time.sleep(1.0)




if __name__ == "__main__":
	main();
