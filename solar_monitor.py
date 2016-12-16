
#!/usr/bin/python

from Subfact_ina219 import INA219
import time
import os
import glob

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
		returnValue.append( "%-20s %-20s %-20s %-20s" % (results["names"][0],results["names"][1],results["names"][2],results["names"][3]));
		returnValue.append( "%2.3f V              %2.3f V              %2.3f V              %2.3f V" % (results["voltage"][0],results["voltage"][1],results["voltage"][2],results["voltage"][3]));
		returnValue.append( "%5.0f mA             %5.0f mA             %5.0f mA             %5.0f mA" % (results["current"][0],results["current"][1],results["current"][2],results["current"][3]));
		returnValue.append( "%5.0f mW             %5.0f mW             %5.0f mW             %5.0f mW" % (results["voltage"][0]*results["current"][0],results["voltage"][1]*results["current"][1],results["voltage"][2]*results["current"][2],results["voltage"][3]*results["current"][3]));
		return returnValue;

	def printResults(self, results):
		text = self.formatPrintData(results)
		print;
		for index in xrange(len(text)):
			print(text[index]);

	def recordData(self,data):
		self.m_SolarDb.addEntry(self.m_Timestamper.getDate(), self.m_Timestamper.getTime(), data );

	def computeNetPower(self, data):
		results = []
		for channelIndex in xrange(4):
			tempVal = {}
			tempVal["minEnergy"] = 0
			tempVal["maxEnergy"] = 0
			tempVal["cumulativeEnergy"] = 0
			
			
			minEnergy = 0
			maxEnergy = 0
			cumulativeEnergy = 0
			for index in xrange( len(data[channelIndex]["voltage"])-1 ):
				timeDelta = self.convertTimeString( data[channelIndex]["time"][index+1]) - self.convertTimeString(data[channelIndex]["time"][index])
				if (timeDelta <= 12 ):
#					power=data[channelIndex]["voltage"][index] * data[channelIndex]["current"][index]
					power=data[channelIndex]["current"][index]
					energy = power*timeDelta
					cumulativeEnergy = cumulativeEnergy + energy
					
					if cumulativeEnergy < minEnergy:
						minEnergy = cumulativeEnergy;
					elif cumulativeEnergy > maxEnergy:
						maxEnergy = cumulativeEnergy

			tempVal["minEnergy"] = minEnergy
			tempVal["maxEnergy"] = maxEnergy
			tempVal["cumulativeEnergy"] = cumulativeEnergy
			
			results.append(tempVal);
			
		for channelIndex in xrange(4):
			print("minEnergy=%.1f mAHr   maxEnergy=%.1f mAHr  cumulative=%.1f mAHr" % ( results[channelIndex]["minEnergy"]/3600.0, results[channelIndex]["maxEnergy"]/3600.0, results[channelIndex]["cumulativeEnergy"]/3600.0))
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
		for index in xrange(4):
			emptyList = []
			self.m_voltages.append(emptyList);
			emptyList = []
			self.m_currents.append(emptyList);
		self.m_filenamePrefix = filenamePrefix;

		averages = {}
		averages["voltage"] = [];
		averages["current"] = [];

		for index in xrange(4):
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
					f.write("time,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current\n" % (data["names"][0], data["names"][0], data["names"][1], data["names"][1], data["names"][2], data["names"][2], data["names"][3], data["names"][3]))
					f.close();

				# append the current data
				f = open(self.m_filename, 'a')
				print("length=%d" % (len(self.m_voltages[0])))
				for index in xrange(len(self.m_voltages[0])):
					f.write(self.m_times[index]);
					f.write(",");
					for sensorIndex in xrange(4):
						f.write("%s,%s" % (self.m_voltages[sensorIndex][index],self.m_currents[sensorIndex][index] ))
						if (sensorIndex != 3):
							f.write(",");
					f.write("\n");
				f.close()


				# clear the cached data for the next hour
				self.m_voltages = [];
				self.m_currents = [];
				self.m_times = [];
				for index in xrange(4):
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

		for index in xrange(4):
			tempVal = {}  # put an empty dictionary for each array entry.
			tempVal["name"]    = []
			tempVal["voltage"] = []
			tempVal["current"] = []
			tempVal["time"]    = []
			
			returnVal.append(tempVal);

		fileHandle = open(filename,"r");
		rawLines = fileHandle.readlines();
		firstLineFields = rawLines[0].split(",");
		
		returnVal[0]["name"] = firstLineFields[1][:-8];  # strip off " voltage" from the end for the base name.
		returnVal[1]["name"] = firstLineFields[3][:-8];  # strip off " voltage" from the end for the base name.
		returnVal[2]["name"] = firstLineFields[5][:-8];  # strip off " voltage" from the end for the base name.
		returnVal[3]["name"] = firstLineFields[7][:-8];  # strip off " voltage" from the end for the base name.
		
		for chanIndex in xrange(4):
			returnVal[chanIndex]["maxVoltage"] = -99999999.0 # very small.
			returnVal[chanIndex]["minVoltage"] =  99999999.0 # very big.
			returnVal[chanIndex]["maxCurrent"] = -99999999 # very small.
			returnVal[chanIndex]["minCurrent"] =  99999999 # very big.
			returnVal[chanIndex]["maxPower"] = -99999999 # very small.
			returnVal[chanIndex]["minPower"] =  99999999 # very big.

		for index in xrange(1,len(rawLines)):
			fields = rawLines[index].split(",");
				
			for chanIndex in xrange(4):
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

	mySolar = Solar(mySolarSensors, Timestamper() );
	return mySolar;


def main():
	mySolar = setupSolar()
	while(True):
		data = mySolar.gatherData();
		mySolar.recordData(data);
		mySolar.printResults(data);
		# update gui
		time.sleep(1.0)




if __name__ == "__main__":
	main();
