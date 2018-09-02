
from SolarSensors import SolarSensors
from SolarServer import SolarServer
from SolarDb import SolarDb
import time

class SolarMonitor():
    def __init__(self, config):
        self.config = config
        
        self.currentBatPwrList = []


        self.solarSensors = SolarSensors(config)
        self.solarServer = SolarServer()
        self.solarDb = SolarDb("solarLog_", config)

    def run(self):
        while True:
            live_data = self.solarSensors.getData()
            self.solarDb.addEntry(live_data)
            self.solarServer.sendUpdate(live_data, self.solarDb)
            
            print(live_data)
            time.sleep(1.0)
            #~ break  # delete me

