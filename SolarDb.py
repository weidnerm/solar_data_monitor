import time
import os


class SolarDb:
    def __init__(self, filenamePrefix, config):
        self.config = config
        self.m_filenamePrefix = filenamePrefix;

        # self.data = {} [<name>] = {}
        #                              ["10minute_mAsec"] = int
        #                              ["today_minEnergy"] = int
        #                              ["today_maxEnergy"] = int
        #                              ["today_cumulativeEnergy"] = int
        #                              ["prev_minEnergy"] = int
        #                              ["prev_maxEnergy"] = int
        #                              ["prev_cumulativeEnergy"] = int
        self.data = {}
        for entry in self.config:
            tempVal = {}
            tempVal["10minute_mAsec"] = 0;
            tempVal["today_minEnergy"] = 0  # mA*Sec
            tempVal["today_maxEnergy"] = 0
            tempVal["today_cumulativeEnergy"] = 0
            tempVal["prev_minEnergy"] = 999999999
            tempVal["prev_maxEnergy"] = -999999999
            tempVal["prev_cumulativeEnergy"] = 0
            self.data[entry["name"]] = tempVal
        self.reset_todays_data()

        self.fileUpdateInterval = 10 # minutes

        cur_time_full = time.time()
        cur_time_full_struct = time.localtime(cur_time_full)
        cur_10_min_block = int((cur_time_full_struct.tm_hour*60 + cur_time_full_struct.tm_min)/self.fileUpdateInterval)
        self.last_10_min_block = cur_10_min_block



        # original config stuff
        self.totalEnergy = 0.0;
        self.m_sensorNames = [];
        self.m_voltages = [];
        self.m_currents = [];
        self.m_times = [];
        self.m_date = "0000_00_00";
        self.m_filename = "unknown"
        self.m_prev_sampleWindow = -1;
        for index in xrange(6):
            emptyList = []
            self.m_voltages.append(emptyList);
            emptyList = []
            self.m_currents.append(emptyList);

        averages = {}
        averages["voltage"] = [];
        averages["current"] = [];

        for index in xrange(6):
            averages["voltage"].append( 0.0 );
            averages["current"].append( 0 );
        self.averages = averages
        self.averages_dataPoints = 0


    #~ def accumulateEnergy(self, solarData):  # probably belongs in SolarDb fixme.
        #~ # 0-panel;  1-bat 1;  2-bat 2;  3-load;  4-bat 3;  5-bat 4



        #~ powerInts = []
        #~ for index in range(len(solarData)):
            #~ value = int(solarData["current"][index])
            #~ powerInts.append(value)



        #~ panelPwr = powerInts[0]
        #~ loadPwr  = powerInts[3]

        #~ self.currentPanelPwr = int( panelPwr )
        #~ self.currentLoadPwr  = int( loadPwr )

        #~ # add new readings to totals;  assume 1 second integration window
        #~ for index in range(solarData):
            #~ self.todayStats[index]["cumulativeEnergy"] = self.todayStats[index]["cumulativeEnergy"] + int(solarData["current"][index])
            #~ self.prevStats[index]["cumulativeEnergy"] = self.prevStats[index]["cumulativeEnergy"] + int(solarData["current"][index])

            #~ if self.prevStats[index]["cumulativeEnergy"] < self.prevStats[index]["minEnergy"]:
                #~ self.prevStats[index]["minEnergy"] = self.prevStats[index]["cumulativeEnergy"];
            #~ elif self.prevStats[index]["cumulativeEnergy"] > self.prevStats[index]["maxEnergy"]:
                #~ self.prevStats[index]["maxEnergy"] = self.prevStats[index]["cumulativeEnergy"]









    def addEntry(self, data):
        # solarData = {} ['names'] = [index] = strings
        #                ['voltage'] = [index] = float
        #                ['current'] = [index] = int

        cur_time_secs = time.time()
        cur_date_str = time.strftime("%Y_%m_%d", time.localtime(cur_time_secs))
        cur_time_str = time.strftime("%H:%M:%S", time.localtime(cur_time_secs))

        for index in xrange(len(data["voltage"])):
            name = data['names'][index]

            power_mA = data['current'][index]

            # accumulate mA hours
            entry = self.data[name]
            entry['10minute_mAsec'] = entry['10minute_mAsec'] + power_mA
            entry['today_cumulativeEnergy'] = entry['today_cumulativeEnergy'] + power_mA
            entry['prev_cumulativeEnergy'] = entry['prev_cumulativeEnergy'] + power_mA

            # update min/max values
            if entry['today_minEnergy'] > entry['today_cumulativeEnergy']: # if tracked min is too big
                entry['today_minEnergy'] = entry['today_cumulativeEnergy']
            if entry['today_maxEnergy'] < entry['today_cumulativeEnergy']: # if tracked max is too small
                entry['today_maxEnergy'] = entry['today_cumulativeEnergy']

            if entry['prev_minEnergy'] > entry['prev_cumulativeEnergy']:
                entry['prev_minEnergy'] = entry['prev_cumulativeEnergy']
            if entry['prev_maxEnergy'] < entry['prev_cumulativeEnergy']:
                entry['prev_maxEnergy'] = entry['prev_cumulativeEnergy']

            # update file if needed
            reset_10min, reset_day = self.evaluate_rollovers(cur_time_secs)

            if reset_10min:
                self.write_data_to_file(cur_time_secs)
                #~ self.reset_10_min_data()
                pass

            if reset_day:
                self.reset_todays_data()

    # entry = {} ["time"] = seconds from time.time()
    #            ["data"] = {}
    #                          [<sourceName>] = {} ['mAsec']

    def write_data_to_file(self, time):
        data = {}
        # data['time'] = time
        # data['data'] = {}
        # for entry in self.config:
        #     tempVal = {}
        #     tempVal["mAsec"] = 0  # mA*Sec
        #     tempVal["today_maxEnergy"] = 0
        #     tempVal["today_cumulativeEnergy"] = 0
        #     tempVal["prev_minEnergy"] = 999999999
        #     tempVal["prev_maxEnergy"] = -999999999
        #     tempVal["prev_cumulativeEnergy"] = 0
        #     self.data[entry["name"]] = tempVal



    def evaluate_rollovers(self, cur_time_secs):
        write_needed = False
        new_file_needed = False

        cur_time_full_struct = time.localtime(cur_time_secs)
        cur_10_min_block = int((cur_time_full_struct.tm_hour*60 + cur_time_full_struct.tm_min)/self.fileUpdateInterval)

        # print "cur_10_min_block=%d" %(cur_10_min_block)

        # write data to a file if its time
        if cur_10_min_block != self.last_10_min_block:

            self.last_10_min_block = cur_10_min_block
            write_needed = True

            if cur_10_min_block == 0:
                new_file_needed = True

        return write_needed, new_file_needed


    def reset_todays_data(self):
        for index in range(len(self.config)):
            name = self.config[index]["name"]

            self.data[name]["today_minEnergy"] = 0  # mA*Sec
            self.data[name]["today_maxEnergy"] = 0
            self.data[name]["today_cumulativeEnergy"] = 0
            self.data[name]["prev_minEnergy"] = 999999999
            self.data[name]["prev_maxEnergy"] = -999999999
            self.data[name]["prev_cumulativeEnergy"] = 0

    def reset_10_min_data(self):
        for entry in self.config:
            self.data[entry["name"]]["10minute_mAsec"] = 0



    def formerly_addEntry_stuff(self):


        rolledOverToNewDay = False
        # figure the new point into the averages.
        for index in xrange(len(data["voltage"])):
            self.averages["voltage"][index] = self.averages["voltage"][index] + data["voltage"][index];
            self.averages["current"][index] = self.averages["current"][index] + data["current"][index];
        self.averages_dataPoints = self.averages_dataPoints +1;

        if ( self.averages_dataPoints == 10):
            # if rollover, flush the old data to the file.
            sampleWindow = int(time[3:5])/10
            if ( self.m_prev_sampleWindow != sampleWindow ) and (self.m_date != "0000_00_00"): # the hour rolled over.
                m_prev_sampleWindow = sampleWindow;

                self.m_filename = self.m_filenamePrefix+self.m_date+".csv"

                # create the file if necessary
                if not os.path.exists(self.m_filename):
                    f = open(self.m_filename, 'w')
                    headerLineText = "time"
                    for index in xrange(6):
                        newSection = ",%s voltage,%s current" % (data["names"][index], data["names"][index])
                        headerLineText = headerLineText+newSection
                    f.write(headerLineText)
                    #~ f.write("time,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current,%s voltage,%s current\n" % (data["names"][0], data["names"][0], data["names"][1], data["names"][1], data["names"][2], data["names"][2], data["names"][3], data["names"][3]))
                    f.close();
                    rolledOverToNewDay = True

                # append the current data
                f = open(self.m_filename, 'a')
                print("length=%d" % (len(self.m_voltages[0])))
                for index in xrange(len(self.m_voltages[0])):
                    f.write(self.m_times[index]);
                    f.write(",");
                    for sensorIndex in xrange(6):
                        f.write("%s,%s" % (self.m_voltages[sensorIndex][index],self.m_currents[sensorIndex][index] ))
                        if (sensorIndex != 5):
                            f.write(",");
                    f.write("\n");
                f.close()


                # clear the cached data for the next hour
                self.m_voltages = [];
                self.m_currents = [];
                self.m_times = [];
                for index in xrange(6):
                    emptyList = []
                    self.m_voltages.append(emptyList);
                    emptyList = []
                    self.m_currents.append(emptyList);

            self.m_date = date;
            self.m_prev_sampleWindow = sampleWindow

            self.m_times.append(time);
            for index in xrange(len(data["voltage"])):
                voltageAvg = self.averages["voltage"][index] / self.averages_dataPoints;
                currentAvg = self.averages["current"][index] / self.averages_dataPoints;

                self.m_voltages[index].append(voltageAvg);
                self.m_currents[index].append(currentAvg);
                self.m_sensorNames.append(data["names"][index] );
#               print("avgV=%2.3f  avgC=%d" % (voltageAvg,currentAvg))

            for index in xrange(len(data["voltage"])): # clear out the averages for next time.
                self.averages["voltage"][index] = 0.0;
                self.averages["current"][index] = 0;
            self.averages_dataPoints = 0;

        return rolledOverToNewDay;


    def readDayLog(self,fileIndex):
        returnVal = [];

        filename = self.getFilenameFromIndex(fileIndex)

        for index in xrange(6):
            tempVal = {}  # put an empty dictionary for each array entry.
            tempVal["name"]    = []
            tempVal["voltage"] = []
            tempVal["current"] = []
            tempVal["time"]    = []

            returnVal.append(tempVal);

        fileHandle = open(filename,"r");
        rawLines = fileHandle.readlines();
        firstLineFields = rawLines[0].split(",");

        for chanIndex in xrange(6):
            returnVal[chanIndex]["name"] = firstLineFields[1+chanIndex*2][:-8];  # strip off " voltage" from the end for the base name.

        #~ returnVal[0]["name"] = firstLineFields[1][:-8];  # strip off " voltage" from the end for the base name.
        #~ returnVal[1]["name"] = firstLineFields[3][:-8];  # strip off " voltage" from the end for the base name.
        #~ returnVal[2]["name"] = firstLineFields[5][:-8];  # strip off " voltage" from the end for the base name.
        #~ returnVal[3]["name"] = firstLineFields[7][:-8];  # strip off " voltage" from the end for the base name.

        for chanIndex in xrange(6):
            returnVal[chanIndex]["maxVoltage"] = -99999999.0 # very small.
            returnVal[chanIndex]["minVoltage"] =  99999999.0 # very big.
            returnVal[chanIndex]["maxCurrent"] = -99999999 # very small.
            returnVal[chanIndex]["minCurrent"] =  99999999 # very big.
            returnVal[chanIndex]["maxPower"] = -99999999 # very small.
            returnVal[chanIndex]["minPower"] =  99999999 # very big.

        for index in xrange(1,len(rawLines)):
            fields = rawLines[index].split(",");

            for chanIndex in xrange(6):
                returnVal[chanIndex]["voltage"].append(float(fields[1+chanIndex*2]))
                returnVal[chanIndex]["current"].append(int(fields[2+chanIndex*2]))
                returnVal[chanIndex]["time"].append(fields[0])

                if (returnVal[chanIndex]["maxVoltage"] < float(fields[1+chanIndex*2])):
                    returnVal[chanIndex]["maxVoltage"] = float(fields[1+chanIndex*2])
                if (returnVal[chanIndex]["minVoltage"] > float(fields[1+chanIndex*2])):
                    returnVal[chanIndex]["minVoltage"] = float(fields[1+chanIndex*2])
                if (returnVal[chanIndex]["maxCurrent"] < int(fields[2+chanIndex*2])):
                    returnVal[chanIndex]["maxCurrent"] = int(fields[2+chanIndex*2])
                if (returnVal[chanIndex]["minCurrent"] > int(fields[2+chanIndex*2])):
                    returnVal[chanIndex]["minCurrent"] = int(fields[2+chanIndex*2])
                if (returnVal[chanIndex]["maxPower"] < float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])):
                    returnVal[chanIndex]["maxPower"] = float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])
                if (returnVal[chanIndex]["minPower"] > float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])):
                    returnVal[chanIndex]["minPower"] = float(fields[1+chanIndex*2])*int(fields[2+chanIndex*2])

        fileHandle.close()
        return (returnVal, filename);

    def getFilenameFromIndex(self, index):
        fileList = []
        pattern = self.m_filenamePrefix + "*.csv"
#       print(pattern)
        for file in glob.glob( pattern ):
            fileList.append(file)

        fileList.sort()
        fileList.reverse()
        filteredIndex = index;
        if filteredIndex < 0:
            filteredIndex = 0
        elif filteredIndex >= len(fileList):
            filteredIndex = len(fileList)-1
        return fileList[filteredIndex]

#~ def setupSolar():
    #~ mySolarSensors = SolarSensors()

#~ #   ina = INA219(0x40);
#~ #   mySolarSensors.addSensor("Panel", ina ); # no jumpers.
#~ #   mySolarSensors.addSensor("Battery1", ina ); # A0 jumper.
#~ #   mySolarSensors.addSensor("Battery2", ina ); # A1 jumper.
#~ #   mySolarSensors.addSensor("Load", ina ); # A0 and A1 jumpers.

    #~ mySolarSensors.addSensor("Panel",  INA219(0x45), scale=2.0 ); # A0 and A1 jumpers.
    #~ # mySolarSensors.addSensor("Dead",   INA219(0x43) );
    #~ mySolarSensors.addSensor("Batt 5", INA219(0x49) );
    #~ mySolarSensors.addSensor("Batt 6", INA219(0x41) );
    #~ mySolarSensors.addSensor("Load",   INA219(0x40), scale=2.0);
    #~ mySolarSensors.addSensor("Batt 7", INA219(0x42) );
    #~ mySolarSensors.addSensor("Batt 8", INA219(0x43) );

    #~ mySolarSensors.addSensor("Batt 4", INA219(0x48) );
    #~ mySolarSensors.addSensor("Batt 3", INA219(0x47) );
    #~ mySolarSensors.addSensor("Batt 2", INA219(0x4a) );
    #~ mySolarSensors.addSensor("Batt 1", INA219(0x46) );

    #~ mySolar = Solar(mySolarSensors, Timestamper() );
    #~ return mySolar;


