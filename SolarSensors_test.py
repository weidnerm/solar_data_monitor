
from unittest import TestCase, main, skip
from mock import patch, call, MagicMock

from SolarSensors import SolarSensors

import os


class SolarSensors_test(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_default_config(self):
        config = [
            {
                "address": "0x45",
                "name": "Panel",
                "scale": 2.0
            },
            {
                "address": "0x49",
                "name": "Batt 5",
                "scale": 1.0
            },
            {
                "address": "0x41",
                "name": "Batt 6",
                "scale": 1.0
            },
            {
                "address": "0x40",
                "name": "Load",
                "scale": 2.0
            },
            {
                "address": "0x42",
                "name": "Batt 7",
                "scale": 1.0
            },
            {
                "address": "0x43",
                "name": "Batt 8",
                "scale": 1.0
            },
            {
                "address": "0x48",
                "name": "Batt 4",
                "scale": 1.0
            },
            {
                "address": "0x47",
                "name": "Batt 3",
                "scale": 1.0
            },
            {
                "address": "0x4a",
                "name": "Batt 2",
                "scale": 1.0
            },
            {
                "address": "0x46",
                "name": "Batt 1",
                "scale": 1.0
            }
        ]

        return config

    def test_get_default_config(self):
        config = self.get_default_config()

        self.assertEqual( [
            {'scale': 2.0, 'name': 'Panel', 'address': '0x45'},
            {'scale': 1.0, 'name': 'Batt 5', 'address': '0x49'},
            {'scale': 1.0, 'name': 'Batt 6', 'address': '0x41'},
            {'scale': 2.0, 'name': 'Load', 'address': '0x40'},
            {'scale': 1.0, 'name': 'Batt 7', 'address': '0x42'},
            {'scale': 1.0, 'name': 'Batt 8', 'address': '0x43'},
            {'scale': 1.0, 'name': 'Batt 4', 'address': '0x48'},
            {'scale': 1.0, 'name': 'Batt 3', 'address': '0x47'},
            {'scale': 1.0, 'name': 'Batt 2', 'address': '0x4a'},
            {'scale': 1.0, 'name': 'Batt 1', 'address': '0x46'}], config)

    @patch('SolarSensors.INA219')
    def test_ctor(self, mockINA):
        mySolarSensors = SolarSensors( self.get_default_config() )

        self.assertEqual(['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1']
            , mySolarSensors.m_sensorNames)
        #self.assertEqual("" , mySolarSensors.m_sensors)
        self.assertEqual([2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] , mySolarSensors.m_scale_factors)


    @patch('SolarSensors.INA219')
    def test_getData(self, mockINA):
        mockINA.return_value.getBusVoltage_V.side_effect = [12.844 ,12.844 ,12.848 ,12.828 ,12.848 ,12.844 ,12.832 ,12.832 ,12.836 ,12.596]
        mockINA.return_value.getCurrent_mA.side_effect = [154 ,-17 ,-15 ,196 ,-21 ,-12 ,2 ,6 ,3 ,2346]

        mySolarSensors = SolarSensors( self.get_default_config() )
        data = mySolarSensors.getData()

        mySolarSensors
        self.assertEqual({
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }, data)

if __name__ == '__main__':
    main()

