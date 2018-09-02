
from unittest import TestCase, main, skip
from mock import patch, call, MagicMock

from SolarDb import SolarDb

import os


class SolarDb_test(TestCase):

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

    def test_ctor(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        self.assertEqual("myprefix", mySolarDb.m_filenamePrefix)
        self.assertEqual({
            'Panel':  {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Load':   {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 1': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 2': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 3': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 4': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 5': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 6': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 7': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            'Batt 8': {'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 0, 'prev_maxEnergy': 0, 'prev_cumulativeEnergy': 0},
            }, mySolarDb.data)

    def test_addEntry(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }

        mySolarDb.addEntry(data)

        self.assertEqual(0, int(mySolarDb.data['Panel']['today_minEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['today_maxEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['today_cumulativeEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Panel']['prev_minEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_maxEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_cumulativeEnergy']))

        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['today_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['today_maxEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['today_cumulativeEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['prev_maxEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_cumulativeEnergy']))

        mySolarDb.addEntry(data)

        self.assertEqual(0, int(mySolarDb.data['Panel']['today_minEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['today_maxEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['today_cumulativeEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Panel']['prev_minEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['prev_maxEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['prev_cumulativeEnergy']))

        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['today_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['today_maxEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['today_cumulativeEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['prev_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['prev_maxEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['prev_cumulativeEnergy']))


if __name__ == '__main__':
    main()

