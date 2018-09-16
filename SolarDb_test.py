
from unittest import TestCase, main, skip
from mock import patch, call, MagicMock

from SolarDb import SolarDb

import os
import time
import json
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

    @patch('SolarDb.open')
    def test_get_default_config(self, mock_open):
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

    @patch('SolarDb.open')
    def test_ctor(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        self.assertEqual("myprefix", mySolarDb.m_filenamePrefix)

        self.assertEqual(mySolarDb.data['Panel']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['today_count'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['prev_count'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec_max'], -999999999 )

        self.assertEqual(mySolarDb.data['Panel']['10minute_count'], 0 )  # spot check at least one field from each input
        self.assertEqual(mySolarDb.data['Load'  ]['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 1']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 2']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 3']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 4']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 5']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 6']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 7']['10minute_count'], 0 )
        self.assertEqual(mySolarDb.data['Batt 8']['10minute_count'], 0 )

        # self.assertEqual(mySolarDb.data['Panel'] , {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Load'  ], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 1'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 2'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 3'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 4'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 5'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 6'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 7'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})
        # self.assertEqual(mySolarDb.data['Batt 8'], {'today_count': 0, '10minute_count': 0, 'prev_count': 0, '10minute_mAsec': 0, '10minute_mAsec_min': 999999999, '10minute_mAsec_max': -999999999, 'today_mAsec_min': 999999999, 'today_mAsec_max': -999999999, 'today_mAsec': 0, 'prev_mAsec_min': 999999999, 'prev_mAsec_max': -999999999, 'prev_mAsec': 0})

    @patch('SolarDb.open')
    def test_addEntry(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }

        mySolarDb.addEntry(data)

        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mAsec_min']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Panel']['10minute_count']))
        self.assertAlmostEqual(12.844,     mySolarDb.data['Panel']['10minute_v'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Panel']['10minute_v_min'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Panel']['10minute_v_max'])
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mA']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mA_min']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mA_max']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['today_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['today_mAsec_min']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['today_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Panel']['today_count']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['prev_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['prev_mAsec_min']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['prev_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Panel']['prev_count']))

        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mAsec']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Batt 5']['10minute_count']))
        self.assertAlmostEqual(12.844,     mySolarDb.data['Batt 5']['10minute_v'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Batt 5']['10minute_v_min'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Batt 5']['10minute_v_max'])
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mA']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mA_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mA_max']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['today_mAsec']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['today_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['today_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Batt 5']['today_count']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['prev_mAsec']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['prev_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['prev_mAsec_max']))
        self.assertEqual(1           , int(mySolarDb.data['Batt 5']['prev_count']))

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [309, -18, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [13.844, 13.844, 13.848, 13.828, 13.848, 13.844, 13.832, 13.832, 13.836, 13.596]
            }
        mySolarDb.addEntry(data)

        self.assertEqual(617         , int(mySolarDb.data['Panel']['10minute_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mAsec_min']))
        self.assertEqual(617         , int(mySolarDb.data['Panel']['10minute_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Panel']['10minute_count']))
        self.assertAlmostEqual(26.688,     mySolarDb.data['Panel']['10minute_v'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Panel']['10minute_v_min'])
        self.assertAlmostEqual(13.844,     mySolarDb.data['Panel']['10minute_v_max'])
        self.assertEqual(617         , int(mySolarDb.data['Panel']['10minute_mA']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['10minute_mA_min']))
        self.assertEqual(309         , int(mySolarDb.data['Panel']['10minute_mA_max']))
        self.assertEqual(617         , int(mySolarDb.data['Panel']['today_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['today_mAsec_min']))
        self.assertEqual(617         , int(mySolarDb.data['Panel']['today_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Panel']['today_count']))
        self.assertEqual(617         , int(mySolarDb.data['Panel']['prev_mAsec']))
        self.assertEqual(308         , int(mySolarDb.data['Panel']['prev_mAsec_min']))
        self.assertEqual(617         , int(mySolarDb.data['Panel']['prev_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Panel']['prev_count']))

        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['10minute_mAsec']))
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['10minute_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Batt 5']['10minute_count']))
        self.assertAlmostEqual(26.688,     mySolarDb.data['Batt 5']['10minute_v'])
        self.assertAlmostEqual(12.844,     mySolarDb.data['Batt 5']['10minute_v_min'])
        self.assertAlmostEqual(13.844,     mySolarDb.data['Batt 5']['10minute_v_max'])
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['10minute_mA']))
        self.assertEqual(-18         , int(mySolarDb.data['Batt 5']['10minute_mA_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['10minute_mA_max']))
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['today_mAsec']))
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['today_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['today_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Batt 5']['today_count']))
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['prev_mAsec']))
        self.assertEqual(-35         , int(mySolarDb.data['Batt 5']['prev_mAsec_min']))
        self.assertEqual(-17         , int(mySolarDb.data['Batt 5']['prev_mAsec_max']))
        self.assertEqual(2           , int(mySolarDb.data['Batt 5']['prev_count']))



    @patch('SolarDb.open')
    def test__evaluate_rollovers__no_elapsed(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,21,8, 1,247, 1 )) )

        self.assertEqual((False, False), result)
        self.assertEqual((19*60+21)/10, mySolarDb.last_10_min_block)

    @patch('SolarDb.open')
    def test__evaluate_rollovers__lastSecondOfWindow(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,29,59, 1,247, 1 )) )

        self.assertEqual((False, False), result)
        self.assertEqual((19*60+29)/10, mySolarDb.last_10_min_block)

    @patch('SolarDb.open')
    def test__evaluate_rollovers__firstSecondOfNextWindow(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        print "mySolarDb.last_10_min_block=%d" %(mySolarDb.last_10_min_block)

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,30,00, 1,247, 1 )) )

        self.assertEqual((True, False), result)
        self.assertEqual((19*60+30)/10, mySolarDb.last_10_min_block)

    @patch('SolarDb.open')
    def test__evaluate_rollovers__dailyRolloverMidnight(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (23*60+55)/10

        print "mySolarDb.last_10_min_block=%d" %(mySolarDb.last_10_min_block)

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 0,0,00, 1,247, 1 )) )

        self.assertEqual((True, True), result)
        self.assertEqual((0*60+0)/10, mySolarDb.last_10_min_block)

    @patch('SolarDb.open')
    def test__reset_todays_data(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        # make the data something other than the defaults
        mySolarDb.data['Load'  ]['10minute_mAsec'] = 100
        mySolarDb.data['Load'  ]['10minute_mAsec_max'] = 100
        mySolarDb.data['Load'  ]['10minute_mAsec_min'] = 100
        mySolarDb.data['Load'  ]['10minute_count'] = 1
        mySolarDb.data['Load'  ]['today_mAsec'] = 100
        mySolarDb.data['Load'  ]['today_mAsec_min'] = 1000
        mySolarDb.data['Load'  ]['today_mAsec_max'] = 100
        mySolarDb.data['Load'  ]['today_count'] = 1
        mySolarDb.data['Load'  ]['prev_mAsec'] = 100
        mySolarDb.data['Load'  ]['prev_mAsec_min'] = 100
        mySolarDb.data['Load'  ]['prev_mAsec_max'] = -100
        mySolarDb.data['Load'  ]['prev_count'] = -1

        mySolarDb.reset_todays_data()

        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec'], 100)
        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec_min'], 100)
        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec_max'], 100)
        self.assertEqual(mySolarDb.data['Load']['10minute_count'], 1)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec'], 0)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec_min'], 999999999)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec_max'], -999999999)
        self.assertEqual(mySolarDb.data['Load']['today_count'], 0)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec'], 100)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec_min'], 100)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec_max'], -100)
        self.assertEqual(mySolarDb.data['Load']['prev_count'], -1)


    @patch('SolarDb.open')
    def test__reset_10_min_data(self, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        # make the data something other than the defaults
        mySolarDb.data['Load'  ]['10minute_mAsec'] = 100
        mySolarDb.data['Load'  ]['10minute_mAsec_max'] = 100
        mySolarDb.data['Load'  ]['10minute_mAsec_min'] = 100
        mySolarDb.data['Load'  ]['10minute_v'] = 100
        mySolarDb.data['Load'  ]['10minute_v_max'] = 100
        mySolarDb.data['Load'  ]['10minute_v_min'] = 100
        mySolarDb.data['Load'  ]['10minute_mA'] = 100
        mySolarDb.data['Load'  ]['10minute_mA_max'] = 100
        mySolarDb.data['Load'  ]['10minute_mA_min'] = 100
        mySolarDb.data['Load'  ]['10minute_count'] = 1
        mySolarDb.data['Load'  ]['today_mAsec'] = 100
        mySolarDb.data['Load'  ]['today_mAsec_min'] = 1000
        mySolarDb.data['Load'  ]['today_mAsec_max'] = 100
        mySolarDb.data['Load'  ]['today_count'] = 1
        mySolarDb.data['Load'  ]['prev_mAsec'] = 100
        mySolarDb.data['Load'  ]['prev_mAsec_min'] = 100
        mySolarDb.data['Load'  ]['prev_mAsec_max'] = -100
        mySolarDb.data['Load'  ]['prev_count'] = -1

        mySolarDb.reset_10_min_data()

        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec'], 0)
        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec_min'], 999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_mAsec_max'], -999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_v'], 0)
        self.assertEqual(mySolarDb.data['Load']['10minute_v_min'], 999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_v_max'], -999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_mA'], 0)
        self.assertEqual(mySolarDb.data['Load']['10minute_mA_min'], 999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_mA_max'], -999999999)
        self.assertEqual(mySolarDb.data['Load']['10minute_count'], 0)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec'], 100)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec_min'], 1000)
        self.assertEqual(mySolarDb.data['Load']['today_mAsec_max'], 100)
        self.assertEqual(mySolarDb.data['Load']['today_count'], 1)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec'], 100)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec_min'], 100)
        self.assertEqual(mySolarDb.data['Load']['prev_mAsec_max'], -100)
        self.assertEqual(mySolarDb.data['Load']['prev_count'], -1)

    @patch('SolarDb.open')
    @patch('SolarDb.time.time')
    def tests_get_10min_entry(self, mock_time, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }
        mock_time.side_effect = [time.mktime((2018,9,4, 19,21,8, 1,247, 1 )),
                                 time.mktime((2018,9,4, 19,21,9, 1,247, 1 )),
                                 time.mktime((2018,9,4, 19,21,10, 1,247, 1 )),
                                 time.mktime((2018,9,4, 19,30,0, 1,247, 1 ))]

        mySolarDb.addEntry(data)
        mySolarDb.addEntry(data)
        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [318, -27, -25, 402, -31, -22, 12, 16, 13, 2356],
            'voltage': [13.844, 13.844, 13.848, 13.828, 13.848, 13.844, 13.832, 13.832, 13.836, 13.596]
            }
        mySolarDb.addEntry(data)
        result_dict = mySolarDb.get_10min_entry(123.4)

        mySolarDb.addEntry(data)  # force a file write

        self.assertEqual(3              , result_dict['samples'])
        self.assertEqual('19:21:10'     , result_dict['time'])
        self.assertEqual(123.4          , result_dict['time_sec'])
        self.assertEqual([1186, 13.161333333333332, 12.828, 13.828, 395, 392, 402]  , result_dict['inputs']['Load'])
        self.assertEqual([934, 13.177333333333332, 12.844, 13.844, 311, 308, 318]   , result_dict['inputs']['Panel'])

        self.assertEqual([call('myprefix2018_09_04.csv', 'a+')], mock_open.call_args_list)
        self.assertEqual([call()], mock_open.return_value.close.call_args_list)
        # self.assertEqual([call('{"time_sec": 1536103800.0, "inputs": {"Load": [1176, 392, 1176], "Batt 2": [9, 3, 9], "Batt 8": [-36, -36, -12], "Batt 1": [7038, 2346, 7038], "Batt 3": [18, 6, 18], "Panel": [924, 308, 924], "Batt 5": [-51, -51, -17], "Batt 4": [6, 2, 6], "Batt 7": [-63, -63, -21], "Batt 6": [-45, -45, -15]}, "samples": 3, "time": "19:21:10"}\n')], mock_open.return_value.write.call_args_list)
        self.assertEqual(1, len(mock_open.return_value.write.call_args_list))


    @patch('SolarDb.open')
    @patch('SolarDb.time.time')
    def test_midnight_rollover(self, mock_time, mock_open):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }
        mock_time.side_effect = [time.mktime((2018,9,4, 23,51,8, 1,247, 1 )),
                                 time.mktime((2018,9,4, 23,51,9, 1,247, 1 )),
                                 time.mktime((2018,9,4, 23,51,10, 1,247, 1 )),
                                 time.mktime((2018,9,5, 0,0,0, 1,247, 1 )), # triggers first write
                                 time.mktime((2018,9,5, 0,10,0, 1,247, 1 )), # triggers second write
                                 ]

        mySolarDb.addEntry(data)
        mySolarDb.addEntry(data)
        mySolarDb.addEntry(data)
        result_dict = mySolarDb.get_10min_entry(123.4)

        mySolarDb.addEntry(data)  # force a file write
        mySolarDb.addEntry(data)  # force a file write
        # expected = {
        #     'inputs':
        #             {'Load': [1176, 392, 1176],
        #             'Panel': [924, 308, 924],
        #             'Batt 1': [7038, 2346, 7038],
        #             'Batt 2': [9, 3, 9],
        #             'Batt 3': [18, 6, 18],
        #             'Batt 4': [6, 2, 6],
        #             'Batt 5': [-51, -51, -17],
        #             'Batt 6': [-45, -45, -15],
        #             'Batt 7': [-63, -63, -21],
        #             'Batt 8': [-36, -36, -12] },
        #     'samples': 3,
        #     'time': '23:51:10',
        #     'time_sec': 123.4}

        # self.assertEqual(expected, result_dict)
        self.assertEqual([call('myprefix2018_09_04.csv', 'a+'),
                          call('myprefix2018_09_05.csv', 'a+')], mock_open.call_args_list)
        self.assertEqual([call(), call()], mock_open.return_value.close.call_args_list)
        # self.assertEqual([call('{"time_sec": 1536120000.0, "inputs": {"Load": [1176, 392, 1176], "Batt 2": [9, 3, 9], "Batt 8": [-36, -36, -12], "Batt 1": [7038, 2346, 7038], "Batt 3": [18, 6, 18], "Panel": [924, 308, 924], "Batt 5": [-51, -51, -17], "Batt 4": [6, 2, 6], "Batt 7": [-63, -63, -21], "Batt 6": [-45, -45, -15]}, "samples": 3, "time": "23:51:10"}\n'),
        #                   call('{"time_sec": 1536120600.0, "inputs": {"Load": [392, 392, 392], "Batt 2": [3, 3, 3], "Batt 8": [-12, -12, -12], "Batt 1": [2346, 2346, 2346], "Batt 3": [6, 6, 6], "Panel": [308, 308, 308], "Batt 5": [-17, -17, -17], "Batt 4": [2, 2, 2], "Batt 7": [-21, -21, -21], "Batt 6": [-15, -15, -15]}, "samples": 1, "time": "00:00:00"}\n')], mock_open.return_value.write.call_args_list)
        self.assertEqual(2 , len(mock_open.return_value.write.call_args_list))



    @patch('SolarDb.open')
    @patch('SolarDb.time.time')
    @patch('SolarDb.glob')
    def test_readDayLog__one_day(self, mock_glob, mock_time, mock_open):
        mock_glob.glob.return_value = ['solarLog_2018_09_06.csv', 'solarLog_2018_09_05.csv']
        mock_open.return_value.readlines.return_value = [
            '{"time_sec": 1536353400.18906, "inputs": {"Load": [1041246, 2080, 1041246], "Batt 8": [-120477, -120477, -304], "Batt 1": [-73203, -73203, -187], "Batt 3": [-69663, -69663, -177], "Panel": [265766, 152, 265766], "Batt 5": [-137945, -137945, -347], "Batt 4": [-86528, -86528, -217], "Batt 7": [-145348, -145348, -343], "Batt 6": [-158404, -158404, -395]}, "samples": 574, "time": "16:49:59"}',
            '{"time_sec": 1536354000.675743, "inputs": {"Load": [818830, 1576, 818830], "Batt 8": [-89837, -89837, -180], "Batt 1": [-56725, -56725, -111], "Batt 3": [-54431, -54431, -106], "Panel": [232100, 408, 232100], "Batt 5": [-102850, -102850, -205], "Batt 4": [-67678, -67678, -132], "Batt 7": [-114046, -114046, -223], "Batt 6": [-118699, -118699, -238]}, "samples": 575, "time": "16:59:59"}']

        mySolarDb = SolarDb("myprefix", self.get_default_config() )

            # 'Panel': {'today_count': 2, 'prev_mAsec_min': , '10minute_mAsec_min': 999999999, '10minute_count': 0, 
            # '10minute_mAsec_max': -999999999, 'today_mAsec_max': , 'prev_count': 4,
            #  'prev_mAsec_max': , 'today_mAsec': , '10minute_mAsec': 0,
            #  'today_mAsec_min': , 'prev_mAsec': },

        self.assertEqual(mySolarDb.data['Panel']['10minute_count'], 0 )  # spot check at least one source
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mAsec_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_v_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA'], 0 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA_min'], 999999999 )
        self.assertEqual(mySolarDb.data['Panel']['10minute_mA_max'], -999999999 )
        self.assertEqual(mySolarDb.data['Panel']['today_count'], 2 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec'], 497866 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec_min'], 265766 )
        self.assertEqual(mySolarDb.data['Panel']['today_mAsec_max'], 497866 )
        self.assertEqual(mySolarDb.data['Panel']['prev_count'], 4 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec'], 995732 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec_min'], 265766 )
        self.assertEqual(mySolarDb.data['Panel']['prev_mAsec_max'], 995732 )

        result,filename = mySolarDb.readDayLog(0)

        self.assertEqual('solarLog_2018_09_06.csv', filename)

        # self.assertEqual(
        #     {'Load': {'today_count': 2, 'prev_mAsec_min': 1041246, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': 1860076, 'prev_count': 4, 'prev_mAsec_max': 3720152, 'today_mAsec': 1860076, '10minute_mAsec': 0, 'today_mAsec_min': 1041246, 'prev_mAsec': 3720152},
        #     'Batt 2': {'today_count': 0, 'prev_mAsec_min': 999999999, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -999999999, 'prev_count': 0, 'prev_mAsec_max': -999999999, 'today_mAsec': 0, '10minute_mAsec': 0, 'today_mAsec_min': 999999999, 'prev_mAsec': 0},
        #     'Batt 8': {'today_count': 2, 'prev_mAsec_min': -420628, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -120477, 'prev_count': 4, 'prev_mAsec_max': -120477, 'today_mAsec': -210314, '10minute_mAsec': 0, 'today_mAsec_min': -210314, 'prev_mAsec': -420628},
        #     'Batt 1': {'today_count': 2, 'prev_mAsec_min': -259856, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -73203, 'prev_count': 4, 'prev_mAsec_max': -73203, 'today_mAsec': -129928, '10minute_mAsec': 0, 'today_mAsec_min': -129928, 'prev_mAsec': -259856},
        #     'Batt 3': {'today_count': 2, 'prev_mAsec_min': -248188, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -69663, 'prev_count': 4, 'prev_mAsec_max': -69663, 'today_mAsec': -124094, '10minute_mAsec': 0, 'today_mAsec_min': -124094, 'prev_mAsec': -248188},
        #     'Panel': {'today_count': 2, 'prev_mAsec_min': 265766, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': 497866, 'prev_count': 4, 'prev_mAsec_max': 995732, 'today_mAsec': 497866, '10minute_mAsec': 0, 'today_mAsec_min': 265766, 'prev_mAsec': 995732},
        #     'Batt 5': {'today_count': 2, 'prev_mAsec_min': -481590, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -137945, 'prev_count': 4, 'prev_mAsec_max': -137945, 'today_mAsec': -240795, '10minute_mAsec': 0, 'today_mAsec_min': -240795, 'prev_mAsec': -481590},
        #     'Batt 4': {'today_count': 2, 'prev_mAsec_min': -308412, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -86528, 'prev_count': 4, 'prev_mAsec_max': -86528, 'today_mAsec': -154206, '10minute_mAsec': 0, 'today_mAsec_min': -154206, 'prev_mAsec': -308412},
        #     'Batt 7': {'today_count': 2, 'prev_mAsec_min': -518788, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -145348, 'prev_count': 4, 'prev_mAsec_max': -145348, 'today_mAsec': -259394, '10minute_mAsec': 0, 'today_mAsec_min': -259394, 'prev_mAsec': -518788},
        #     'Batt 6': {'today_count': 2, 'prev_mAsec_min': -554206, '10minute_mAsec_min': 999999999, '10minute_count': 0, '10minute_mAsec_max': -999999999, 'today_mAsec_max': -158404, 'prev_count': 4, 'prev_mAsec_max': -158404, 'today_mAsec': -277103, '10minute_mAsec': 0, 'today_mAsec_min': -277103, 'prev_mAsec': -554206}}, mySolarDb.data)


    @patch('SolarDb.glob')
    @patch('SolarDb.open')
    def test_getFilenameFromIndex(self, mock_open, mock_glob):
        mock_glob.glob.return_value = ['solarLog_2018_09_06.csv', 'solarLog_2018_09_07.csv']

        mySolarDb = SolarDb("solarLog_", self.get_default_config() )

        self.assertEquals('solarLog_2018_09_07.csv', mySolarDb.getFilenameFromIndex(0))
        self.assertEquals('solarLog_2018_09_06.csv', mySolarDb.getFilenameFromIndex(1))
        self.assertEquals(None,                      mySolarDb.getFilenameFromIndex(2))
        self.assertEquals(None,                      mySolarDb.getFilenameFromIndex(3))
        self.assertEquals(None,                      mySolarDb.getFilenameFromIndex(4))



    #~ def test_time_formatting(self):

        #~ cur_time_full = time.time()
        #~ cur_date = time.strftime("%Y_%m_%d", time.localtime(cur_time_full))
        #~ cur_time = time.strftime("%H:%M:%S", time.localtime(cur_time_full))

        #~ print(cur_time_full)
        #~ print(cur_date)
        #~ print(cur_time)
        #~ print(time.localtime(cur_time_full))
        #~ print(time.localtime(cur_time_full).tm_hour)
        #~ print(time.localtime(cur_time_full).tm_min)
        #~ print(time.localtime(cur_time_full).tm_sec)


if __name__ == '__main__':
    main()

