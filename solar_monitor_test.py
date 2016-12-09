
import unittest
import os

from solar_monitor import SolarSensors;
from solar_monitor import Solar;
from solar_monitor import SolarDb;
from solar_monitor import TimestamperInterface;



class INA219_Dummy:
	def __init__(self, address=0x40, debug=False):
		self.m_voltage = 12.0000;
		self.m_current = 100.0;
		self.m_address = address;
		
		self.m_voltageDelta = 0.1;
		self.m_currentDelta = 100.0;
		
	def getBusVoltage_V(self):
		self.m_voltage = self.m_voltage + self.m_voltageDelta
		if (self.m_voltage > 20.0):
			self.m_voltageDelta = -0.1;
		if (self.m_voltage < 10.0):
			self.m_voltageDelta = 0.2;
		return self.m_voltage
		
	def getCurrent_mA(self):
		self.m_current = self.m_current + self.m_currentDelta
		if (self.m_current > 2000.0):
			self.m_currentDelta = -200.0;
		if (self.m_current < -2000.0):
			self.m_currentDelta = 100.0;
		return self.m_current
		
	def getPower_mW(self):
		return self.m_current*self.m_voltageDelta
		
	def getAddr(self):
		return self.m_address;
		
	
	
class TimestamperMock(TimestamperInterface):
	def __init__(self):
		self.m_year = 2016
		self.m_month = 11
		self.m_day = 30
		self.m_hours = 01
		self.m_mins = 5
		self.m_secs = 10

	def getDate(self):
		return ("%02d_%02d_%02d" % (self.m_year, self.m_month, self.m_day) )
		
	def getTime(self):
#		self.m_secs = self.m_secs +1;
		return ("%02d:%02d:%02d" % (self.m_hours, self.m_mins, self.m_secs) )
		
	def setDateTime(self, year, month, day, hour, mins, secs):
		self.m_year = year
		self.m_month = month
		self.m_day = day
		self.m_hours = hour
		self.m_mins = mins
		self.m_secs = secs
		
	def advanceOneSec(self):
		self.m_secs = self.m_secs + 1
		if ( self.m_secs == 60 ):
			self.m_secs = 0
			self.m_mins = self.m_mins + 1
		if ( self.m_mins == 60 ):
			self.m_mins = 0
			self.m_hours = self.m_hours + 1
		if ( self.m_hours == 24 ):
			self.m_hours = 0
			self.m_day = self.m_day + 1
		if ( self.m_day == 32 ):
			self.m_day = 1
			self.m_month = self.m_month + 1
		if ( self.m_month == 13 ):
			self.m_month = 1
			self.m_year = self.m_year + 1

		




def getSensors():
	m_SolarSensors = SolarSensors();
	m_SolarSensors.addSensor("Panel",INA219_Dummy(0x40));
	m_SolarSensors.addSensor("Battery1",INA219_Dummy(0x41));
	m_SolarSensors.addSensor("Load",INA219_Dummy(0x42));
	m_SolarSensors.addSensor("Battery2",INA219_Dummy(0x43));
	
	m_SolarSensors.m_sensors[0].m_voltage = 12.0;
	m_SolarSensors.m_sensors[1].m_voltage = 13.0;
	m_SolarSensors.m_sensors[2].m_voltage = 14.0;
	m_SolarSensors.m_sensors[3].m_voltage = 15.0;
			
	m_SolarSensors.m_sensors[0].m_current = 400.0;
	m_SolarSensors.m_sensors[1].m_current = 300.0;
	m_SolarSensors.m_sensors[2].m_current = 200.0;
	m_SolarSensors.m_sensors[3].m_current = 100.0;
	return m_SolarSensors;
	
class TestSolar(unittest.TestCase):
	
	def setUp(self):
		self.m_SolarSensors = getSensors();
		self.m_TimestamperMock = TimestamperMock()
		self.m_solar = Solar( self.m_SolarSensors, self.m_TimestamperMock ,filenamePrefix="test_solarLog_")
		self.purge();
				
	def tearDown(self):
		self.m_SolarSensors = None;
		self.m_TimestamperMock = None;
		self.m_solar = None;
		self.purge();
		
	def purge(self):
		dir = "."
		for f in os.listdir(dir):
			if ( "test_solarLog_" == f[:14]) and (".txt" == f[-4:]):
				os.remove(os.path.join(dir, f))
	
	def checkNames(self, results):
		if not "names" in results:
			self.fail();
		if not "voltage" in results:
			self.fail();
		if not "current" in results:
			self.fail();
		self.assertEqual(results["names"][0], "Panel")
		self.assertEqual(results["names"][1], "Battery1")
		self.assertEqual(results["names"][2], "Load")
		self.assertEqual(results["names"][3], "Battery2")
		
	def checkParameter(self, results, parameter, expected):
		self.assertAlmostEqual(results[parameter][0], expected[0], places=7)
		self.assertAlmostEqual(results[parameter][1], expected[1], places=7)
		self.assertAlmostEqual(results[parameter][2], expected[2], places=7)
		self.assertAlmostEqual(results[parameter][3], expected[3], places=7)

	
	def test_SolarSensors_ctor(self):
		self.assertEqual(self.m_SolarSensors.m_sensors[0].getAddr(), 0x40)
		self.assertEqual(self.m_SolarSensors.m_sensors[1].getAddr(), 0x41)
		self.assertEqual(self.m_SolarSensors.m_sensors[2].getAddr(), 0x42)
		self.assertEqual(self.m_SolarSensors.m_sensors[3].getAddr(), 0x43)
		
		self.assertEqual(self.m_SolarSensors.m_sensorNames[0], "Panel")
		self.assertEqual(self.m_SolarSensors.m_sensorNames[1], "Battery1")
		self.assertEqual(self.m_SolarSensors.m_sensorNames[2], "Load")
		self.assertEqual(self.m_SolarSensors.m_sensorNames[3], "Battery2")
		
	def test_SolarSensors_getData_1(self):
		results = self.m_SolarSensors.getData();
		
		self.checkNames(results);
		self.checkParameter(results, "voltage", (12.1, 13.1, 14.1, 15.1) )
		self.checkParameter(results, "current", (500.0, 400.0, 300.0, 200.0) )


	def test_SolarSensors_getData_2(self):
		results = self.m_SolarSensors.getData();
		results = self.m_SolarSensors.getData();
		
		self.checkNames(results);
		self.checkParameter(results, "voltage", (12.2, 13.2, 14.2, 15.2) )
		self.checkParameter(results, "current", (600.0, 500.0, 400.0, 300.0) )








	def test_Solar_gatherData_1(self):
		results = self.m_solar.gatherData();
		self.checkNames(results);
		self.checkParameter(results, "voltage", (12.1, 13.1, 14.1, 15.1) )
		self.checkParameter(results, "current", (500.0, 400.0, 300.0, 200.0) )
		self.m_solar.printResults(results)
		
		results = self.m_solar.gatherData();
		self.checkNames(results);
		self.checkParameter(results, "voltage", (12.2, 13.2, 14.2, 15.2) )
		self.checkParameter(results, "current", (600.0, 500.0, 400.0, 300.0) )

		results = self.m_solar.gatherData();
		self.checkNames(results);
		self.checkParameter(results, "voltage", (12.3, 13.3, 14.3, 15.3) )
		self.checkParameter(results, "current", (700.0, 600.0, 500.0, 400.0) )




	def test_TimestamperMock_getTime(self):
		
		self.assertEqual("2016_11_30", self.m_TimestamperMock.getDate() );
		self.assertEqual("01:05:10", self.m_TimestamperMock.getTime() );

		self.m_TimestamperMock.setDateTime(2015,10,29,0,4,9);

		self.assertEqual("2015_10_29", self.m_TimestamperMock.getDate() );
		self.assertEqual("00:04:09", self.m_TimestamperMock.getTime() );

	def test_TimestamperMock_advanceOneSec(self):
		
		self.m_TimestamperMock.setDateTime(2015,12,31,23,59,59);
		self.m_TimestamperMock.advanceOneSec();

		self.assertEqual("2016_01_01", self.m_TimestamperMock.getDate() );
		self.assertEqual("00:00:00", self.m_TimestamperMock.getTime() );



	def test_SolarDb_recordData_1(self):
		self.m_TimestamperMock.setDateTime(2016,11,30,01,05,10);
		results = self.m_solar.gatherData();
		self.m_solar.recordData(results);

		self.m_TimestamperMock.setDateTime(2016,11,30,01,05,11);
		results = self.m_solar.gatherData();
		self.m_solar.recordData(results);
		
		self.assertEqual("Panel", self.m_solar.m_SolarDb.m_sensorNames[0] )
		self.assertEqual("Battery1", self.m_solar.m_SolarDb.m_sensorNames[1] )
		self.assertEqual("Load", self.m_solar.m_SolarDb.m_sensorNames[2] )
		self.assertEqual("Battery2", self.m_solar.m_SolarDb.m_sensorNames[3] )
		
		self.assertEqual(12.1, self.m_solar.m_SolarDb.m_voltages[0][0] )
		self.assertEqual(13.1, self.m_solar.m_SolarDb.m_voltages[1][0] )
		self.assertEqual(14.1, self.m_solar.m_SolarDb.m_voltages[2][0] )
		self.assertEqual(15.1, self.m_solar.m_SolarDb.m_voltages[3][0] )
		
		self.assertEqual(500.0, self.m_solar.m_SolarDb.m_currents[0][0] )
		self.assertEqual(400.0, self.m_solar.m_SolarDb.m_currents[1][0] )
		self.assertEqual(300.0, self.m_solar.m_SolarDb.m_currents[2][0] )
		self.assertEqual(200.0, self.m_solar.m_SolarDb.m_currents[3][0] )

		


		self.assertEqual(12.2, self.m_solar.m_SolarDb.m_voltages[0][1] )
		self.assertEqual(13.2, self.m_solar.m_SolarDb.m_voltages[1][1] )
		self.assertEqual(14.2, self.m_solar.m_SolarDb.m_voltages[2][1] )
		self.assertEqual(15.2, self.m_solar.m_SolarDb.m_voltages[3][1] )
		
		self.assertEqual(600.0, self.m_solar.m_SolarDb.m_currents[0][1] )
		self.assertEqual(500.0, self.m_solar.m_SolarDb.m_currents[1][1] )
		self.assertEqual(400.0, self.m_solar.m_SolarDb.m_currents[2][1] )
		self.assertEqual(300.0, self.m_solar.m_SolarDb.m_currents[3][1] )


		self.assertEqual("01:05:10", self.m_solar.m_SolarDb.m_times[0] )
		self.assertEqual("01:05:11", self.m_solar.m_SolarDb.m_times[1] )

	def getFileSize(self, filename):
		statinfo = os.stat(filename)
		return statinfo.st_size;

		
	def test_SolarDb_recordData_fileWrite_notTimeToWriteYet(self):
		
		self.m_TimestamperMock.setDateTime(2016,11,30,01,0,0);
		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(False, os.path.exists("test_solarLog_2016_11_30.txt"));
		
		for index in xrange(600-1):
			self.m_TimestamperMock.advanceOneSec();
			self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(False, os.path.exists("test_solarLog_2016_11_30.txt"));

		self.assertEqual("01:09:59", self.m_TimestamperMock.getTime());

		# advance so that the hour rolls over.  will trigger a file creation and write.
		self.m_TimestamperMock.advanceOneSec();
		self.assertEqual("01:10:00", self.m_TimestamperMock.getTime());

		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(True, os.path.exists("test_solarLog_2016_11_30.txt"));
		size_after_3600 = self.getFileSize("test_solarLog_2016_11_30.txt");

		# advance to right before the next rollover. make sure no writes in between.
		for index in xrange(600-1):
			self.m_TimestamperMock.advanceOneSec();
			self.m_solar.recordData( self.m_solar.gatherData() );
			size_after_7199 = self.getFileSize("test_solarLog_2016_11_30.txt");
			self.assertEqual(size_after_3600, size_after_7199);

		self.assertEqual("01:19:59", self.m_TimestamperMock.getTime());

		
		# advance so that the hour rolls over.  will trigger a file write.
		self.m_TimestamperMock.advanceOneSec();
		self.assertEqual("01:20:00", self.m_TimestamperMock.getTime());

		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(True, os.path.exists("test_solarLog_2016_11_30.txt"));
		size_after_7200 = self.getFileSize("test_solarLog_2016_11_30.txt");
		self.assertNotEqual(size_after_7199, size_after_7200);

	def test_SolarDb_recordData_fileWrite_midnight_rollover(self):
		
		self.m_TimestamperMock.setDateTime(2016,11,30,23,59,50);
		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(False, os.path.exists("test_solarLog_2016_11_30.txt"));
		
		for index in xrange(9):
			self.m_TimestamperMock.advanceOneSec();
			self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(False, os.path.exists("test_solarLog_2016_11_30.txt"));

		self.assertEqual("23:59:59", self.m_TimestamperMock.getTime());

		# advance so that the window rolls over.  will trigger a file creation and write.
		self.m_TimestamperMock.advanceOneSec();
		self.assertEqual("00:00:00", self.m_TimestamperMock.getTime());
		self.assertEqual("2016_11_31", self.m_TimestamperMock.getDate());

		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(False, os.path.exists("test_solarLog_2016_11_31.txt"));

		# advance to right before the next rollover. make sure no writes in between.
		for index in xrange(600-1):
			self.m_TimestamperMock.advanceOneSec();
			self.m_solar.recordData( self.m_solar.gatherData() );

		self.assertEqual("00:09:59", self.m_TimestamperMock.getTime());

		
		# advance so that the window rolls over.  will trigger a file write.
		self.m_TimestamperMock.advanceOneSec();
		self.assertEqual("00:10:00", self.m_TimestamperMock.getTime());

		self.m_solar.recordData( self.m_solar.gatherData() );
		self.assertEqual(True, os.path.exists("test_solarLog_2016_11_31.txt"));
		
		

if __name__ == '__main__':
	unittest.main()
	
	
