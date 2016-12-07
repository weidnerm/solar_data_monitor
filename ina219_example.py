#!/usr/bin/python

from Subfact_ina219 import INA219
import time

ina = INA219()
#result = ina.getBusVoltage_V()

time.sleep(3.0)

print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
print "Bus     : %.3f V" % ina.getBusVoltage_V()
print "Current : %.3f mA" % ina.getCurrent_mA()


#getShuntVoltage_raw 1
#getBusVoltage_raw 2
#getPower_raw  3
#getCurrent_raw  4
#  5

time.sleep(3.0)
voltageRaw = ina.getBusVoltage_raw()
print "Voltage Raw     : %d = %x V" % (voltageRaw, voltageRaw)
