
#!/usr/bin/python

from Subfact_ina219 import INA219
import time
import os

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
		returnValue.append( "%2.2f V              %2.2f V              %2.2f V              %2.2f V" % (results["voltage"][0],results["voltage"][1],results["voltage"][2],results["voltage"][3]));
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
		self.m_prev_hour = -1;
		for index in xrange(4):
			emptyList = []
			self.m_voltages.append(emptyList);
			emptyList = []
			self.m_currents.append(emptyList);
		self.m_filenamePrefix = filenamePrefix;
			
		
	def addEntry(self, date, time, data):
		
		# if rollover, flush the old data to the file.
		sampleHour = int(time[0:2])
		if ( self.m_prev_hour != sampleHour ) and (self.m_date != "0000_00_00"): # the hour rolled over.
			m_prev_hour = sampleHour;
			
			self.m_filename = self.m_filenamePrefix+self.m_date+".txt"
			
			# create the file if necessary
			if not os.path.exists(self.m_filename):
				f = open(self.m_filename, 'w')
				f.write("time,%s_voltage,%s_current,%s_voltage,%s_current,%s_voltage,%s_current,%s_voltage,%s_current\n" % (data["names"][0], data["names"][0], data["names"][1], data["names"][1], data["names"][2], data["names"][2], data["names"][3], data["names"][3]))
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
		self.m_prev_hour = sampleHour
		
		self.m_times.append(time);
		for index in xrange(len(data["voltage"])):
			self.m_voltages[index].append(data["voltage"][index]);
			self.m_currents[index].append(data["current"][index]);
			self.m_sensorNames.append(data["names"][index] );
		
		

def main():
	mySolarSensors = SolarSensors()

#	ina = INA219(0x40);
#	mySolarSensors.addSensor("Panel", ina ); # no jumpers.
#	mySolarSensors.addSensor("Battery1", ina ); # A0 jumper.
#	mySolarSensors.addSensor("Battery2", ina ); # A1 jumper.
#	mySolarSensors.addSensor("Load", ina ); # A0 and A1 jumpers.

	mySolarSensors.addSensor("Panel", INA219(0x45) ); # no jumpers.
	mySolarSensors.addSensor("Battery1", INA219(0x41) ); # A0 jumper.
	mySolarSensors.addSensor("Battery2", INA219(0x44) ); # A1 jumper.
	mySolarSensors.addSensor("Load", INA219(0x40) ); # A0 and A1 jumpers.
	
	mySolar = Solar(mySolarSensors, Timestamper() );
	while(True):
		data = mySolar.gatherData();
		mySolar.recordData(data);
		text = mySolar.printResults(data);
		# update gui
		time.sleep(1.0)

	
	

if __name__ == "__main__":
	main();
