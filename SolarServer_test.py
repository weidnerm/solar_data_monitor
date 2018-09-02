
from unittest import TestCase, main, skip
from mock import patch, call, MagicMock

from SolarServer import SolarServer
from SolarDb import SolarDb

import os


class SolarServer_test(TestCase):

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


    def config_mocks(self, mockSelect, mockSocket, mockOneFifo):
        mockSocket.AF_INET=123
        mockSocket.SOCK_DGRAM=765
        
        mockSelect.select.return_value = ([], [], [])
        
    @patch('SolarServer.OneFifo')
    @patch('SolarServer.socket')
    @patch('SolarServer.select')
    def test_ctor(self, mockSelect, mockSocket, mockOneFifo):
        self.config_mocks(mockSelect, mockSocket, mockOneFifo)
        
        mySolarServer = SolarServer()
        
        self.assertEqual([call(123, 765)], 
            mockSocket.socket.call_args_list)
        self.assertEqual([call(('127.0.0.1', 29551))], mockSocket.socket.return_value.bind.call_args_list)
        self.assertEqual([call(False)], mockSocket.socket.return_value.setblocking.call_args_list)

        self.assertEqual([call('/tmp/solar_data.fifo')], mockOneFifo.call_args_list)
        self.assertEqual([call()], mockOneFifo.return_value.__enter__.call_args_list)

    @patch('SolarServer.OneFifo')
    @patch('SolarServer.socket')
    @patch('SolarServer.select')
    def test_sendUpdate(self, mockSelect, mockSocket, mockOneFifo):
        self.config_mocks(mockSelect, mockSocket, mockOneFifo)
        mySolarDb = SolarDb('filename', self.get_default_config())
        live_data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }
        
        mySolarServer = SolarServer()
        mySolarServer.listner_address = ('127.0.0.1', 29552)
        mySolarServer.sendUpdate(live_data, mySolarDb)
        
        self.assertEqual([call('{"cumulativeEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"maxEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"current": [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346], '
            '"names": ["Panel", "Batt 5", "Batt 6", "Load", "Batt 7", "Batt 8", "Batt 4", "Batt 3", "Batt 2", "Batt 1"], '
            '"todayCumulativeEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"voltage": [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]}'
                , ('127.0.0.1', 29552))]
            , mockSocket.socket.return_value.sendto.call_args_list)

        self.assertEqual([call('{"cumulativeEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"maxEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"current": [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346], '
            '"names": ["Panel", "Batt 5", "Batt 6", "Load", "Batt 7", "Batt 8", "Batt 4", "Batt 3", "Batt 2", "Batt 1"], '
            '"todayCumulativeEnergy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '
            '"voltage": [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]}')]
            , mockOneFifo.return_value.write.call_args_list)

if __name__ == '__main__':
    main()

 
