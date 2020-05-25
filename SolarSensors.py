
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
            voltage = self.m_sensors[index].getBusVoltage_V()
            current = int(self.m_sensors[index].getCurrent_mA() * self.m_scale_factors[index])
            
            if self.m_sensorNames[index] in returnVal["names"]: # already found an entry for this. its got multiple  channels.  accumulate it.
                for search_index in range(len(returnVal["names"])):
                    if self.m_sensorNames[index] == returnVal["names"][search_index]:
                        #~ returnVal["voltage"][search_index] = returnVal["voltage"][search_index] + voltage
                        returnVal["current"][search_index] = returnVal["current"][search_index] + current
                        break
            else: # new entry
                returnVal["names"].append(self.m_sensorNames[index]);
                returnVal["voltage"].append( voltage );
                returnVal["current"].append( current );

        return returnVal;
