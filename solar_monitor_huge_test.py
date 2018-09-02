

from unittest import TestCase, main, skip
from mock import patch, call, MagicMock
from Subfact_ina219 import INA219

import os
from solar_monitor import SolarSensors
import time

class TestSolar(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_SolarSensors(self):
        mySolarSensors = SolarSensors()

        mySolarSensors.addSensor("Panel",  INA219(0x45), scale=2.0 ); # A0 and A1 jumpers.
        # mySolarSensors.addSensor("Dead",   INA219(0x43) );
        mySolarSensors.addSensor("Batt 5", INA219(0x49) );
        mySolarSensors.addSensor("Batt 6", INA219(0x41) );
        mySolarSensors.addSensor("Load",   INA219(0x40), scale=2.0);
        mySolarSensors.addSensor("Batt 7", INA219(0x42) );
        mySolarSensors.addSensor("Batt 8", INA219(0x43) );

        mySolarSensors.addSensor("Batt 4", INA219(0x48) );
        mySolarSensors.addSensor("Batt 3", INA219(0x47) );
        mySolarSensors.addSensor("Batt 2", INA219(0x4a) );
        mySolarSensors.addSensor("Batt 1", INA219(0x46) );

        for index in range(10):
            data = mySolarSensors.getData();
            
            time.sleep(1.0)
        
            print data
        
if __name__ == '__main__':
    main()

