
from Subfact_ina219 import INA219

class SolarSensors:
    def __init__(self, config):
        self.config = config

        self.m_sensors = [];
        self.m_sensorNames = [];
        self.m_scale_factors = []
        
        for index in range(len(config)):
            addr = int(config[index]['address'], 16)
            self.m_sensors.append( INA219(addr) );
            self.m_sensorNames.append(config[index]['name']);
            self.m_scale_factors.append(config[index]['scale'])

    def getData(self):
        returnVal = {};

        returnVal["names"] = [];
        returnVal["voltage"] = [];
        returnVal["current"] = [];

        for index in range(len(self.m_sensors)):
            returnVal["names"].append(self.m_sensorNames[index]);

            voltage = self.m_sensors[index].getBusVoltage_V()
            current = int(self.m_sensors[index].getCurrent_mA() * self.m_scale_factors[index])
            returnVal["voltage"].append( voltage );
            returnVal["current"].append( current );

        return returnVal;
