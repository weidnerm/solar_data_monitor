
from unittest import TestCase, main, skip
from mock import patch, call, MagicMock

from SolarDb import SolarDb

import os
import time

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
        self.assertEqual(mySolarDb.data['Panel'] , {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Load']  , {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 1'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 2'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 3'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 4'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 5'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 6'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 7'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 8'], {'10minute_mAsec': 0, 'today_minEnergy': 0, 'today_maxEnergy': 0, 'today_cumulativeEnergy': 0, 'prev_minEnergy': 999999999, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0})

    def test_addEntry(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        data = {
            'names': ['Panel', 'Batt 5', 'Batt 6', 'Load', 'Batt 7', 'Batt 8', 'Batt 4', 'Batt 3', 'Batt 2', 'Batt 1'],
            'current': [308, -17, -15, 392, -21, -12, 2, 6, 3, 2346],
            'voltage': [12.844, 12.844, 12.848, 12.828, 12.848, 12.844, 12.832, 12.832, 12.836, 12.596]
            }

        mySolarDb.addEntry(data)

        self.assertEqual(308, int(mySolarDb.data['Panel']['10minute_mAsec']))
        self.assertEqual(0, int(mySolarDb.data['Panel']['today_minEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['today_maxEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['today_cumulativeEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_minEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_maxEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_cumulativeEnergy']))

        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['10minute_mAsec']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['today_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['today_maxEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['today_cumulativeEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_minEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_maxEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_cumulativeEnergy']))

        mySolarDb.addEntry(data)

        self.assertEqual(616, int(mySolarDb.data['Panel']['10minute_mAsec']))
        self.assertEqual(0, int(mySolarDb.data['Panel']['today_minEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['today_maxEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['today_cumulativeEnergy']))
        self.assertEqual(308, int(mySolarDb.data['Panel']['prev_minEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['prev_maxEnergy']))
        self.assertEqual(616, int(mySolarDb.data['Panel']['prev_cumulativeEnergy']))

        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['10minute_mAsec']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['today_minEnergy']))
        self.assertEqual(0, int(mySolarDb.data['Batt 5']['today_maxEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['today_cumulativeEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['prev_minEnergy']))
        self.assertEqual(-17, int(mySolarDb.data['Batt 5']['prev_maxEnergy']))
        self.assertEqual(-34, int(mySolarDb.data['Batt 5']['prev_cumulativeEnergy']))



    def test__evaluate_rollovers__no_elapsed(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,21,8, 1,247, 1 )) )

        self.assertEqual((False, False), result)
        self.assertEqual((19*60+21)/10, mySolarDb.last_10_min_block)

    def test__evaluate_rollovers__lastSecondOfWindow(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,29,59, 1,247, 1 )) )

        self.assertEqual((False, False), result)
        self.assertEqual((19*60+29)/10, mySolarDb.last_10_min_block)

    def test__evaluate_rollovers__firstSecondOfNextWindow(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (19*60+21)/10

        print "mySolarDb.last_10_min_block=%d" %(mySolarDb.last_10_min_block)

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 19,30,00, 1,247, 1 )) )

        self.assertEqual((True, False), result)
        self.assertEqual((19*60+30)/10, mySolarDb.last_10_min_block)

    def test__evaluate_rollovers__dailyRolloverMidnight(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )
        mySolarDb.last_10_min_block = (23*60+55)/10

        print "mySolarDb.last_10_min_block=%d" %(mySolarDb.last_10_min_block)

        result = mySolarDb.evaluate_rollovers(
                    time.mktime((2018,9,4, 0,0,00, 1,247, 1 )) )

        self.assertEqual((True, True), result)
        self.assertEqual((0*60+0)/10, mySolarDb.last_10_min_block)

    def test__reset_todays_data(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        # make the data something other than the defaults
        mySolarDb.data['Load'  ]['10minute_mAsec'] = 100
        mySolarDb.data['Load'  ]['today_cumulativeEnergy'] = 100
        mySolarDb.data['Load'  ]['prev_maxEnergy'] = -100
        mySolarDb.data['Load'  ]['prev_cumulativeEnergy'] = 100
        mySolarDb.data['Load'  ]['today_maxEnergy'] = 100
        mySolarDb.data['Load'  ]['prev_minEnergy'] = 100
        mySolarDb.data['Load'  ]['today_minEnergy'] = 1000

        mySolarDb.reset_todays_data()

        self.assertEqual(mySolarDb.data['Load'  ], {'10minute_mAsec': 100, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 2'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 8'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 1'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 3'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Panel' ], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 5'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 4'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 7'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})
        self.assertEqual(mySolarDb.data['Batt 6'], {'10minute_mAsec': 0, 'today_cumulativeEnergy': 0, 'prev_maxEnergy': -999999999, 'prev_cumulativeEnergy': 0, 'today_maxEnergy': 0, 'prev_minEnergy': 999999999, 'today_minEnergy': 0})

    def test__reset_10_min_data(self):
        mySolarDb = SolarDb("myprefix", self.get_default_config() )

        mySolarDb.reset_todays_data()

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

