from OneFifo import OneFifo
import json
import socket
import select
import time

class SolarServer():
    def __init__(self):

        self.one_fifo = None

        self.one_fifo = OneFifo('/tmp/solar_data.fifo')
        self.one_fifo.__enter__()

        self.live_updates_addr = []
        self.getdata_info = []

        self.socket = socket.socket(socket.AF_INET, #internet,
                                    socket.SOCK_DGRAM) #UDP
        self.socket.setblocking(False)
        self.socket.bind( ('0.0.0.0', 29551) ) 

        self.live_updates_addr = []
        self.getdata_info = []

    #~ def sendToClients(self,msg):

    def sendUpdate(self,liveData, solarDb):


        #
        # Json Output
        #

        outputDict = {}
        outputDict["names"] = []
        outputDict["voltage"] = []
        outputDict["current"] = []
        outputDict["todayCumulativeEnergy"] = []
        outputDict["cumulativeEnergy"] = []
        outputDict["maxEnergy"] = []

        # add channel names and current values
        for index in xrange(len(liveData["names"])):
            name=liveData["names"][index]
            outputDict["names"].append( name )
            outputDict["voltage"].append( liveData["voltage"][index] )
            outputDict["current"].append( liveData["current"][index] )
            outputDict["todayCumulativeEnergy"].append( solarDb.data[name]["today_mAsec"] )
            outputDict["cumulativeEnergy"].append( solarDb.data[name]["prev_mAsec"] )
            outputDict["maxEnergy"].append( solarDb.data[name]["prev_mAsec_max"] )

        self.handleNewAttachments()

        # handle history requests
        self.sendHistoryToListeners(solarDb)

        # send live update to listeners
        jsonOutput = json.dumps(outputDict)
        self.sendLiveUpdateToListeners(jsonOutput)
        
        # send message through the pipe
        self.one_fifo.write(jsonOutput);
        
        return jsonOutput




    def handleNewAttachments(self):
        self.live_updates_addr = []
        self.getdata_info = []
        
        queue_empty = False
        while queue_empty == False:
            ready_to_read, ready_to_write, in_error = select.select( [self.socket], [], [], 0.001) # only wait 1 msec

            if len(ready_to_read) == 0:
                queue_empty = True
            else:
                data, address = ready_to_read[0].recvfrom(4096)
                if data == 'sub':
                    if not address in self.live_updates_addr:
                        self.live_updates_addr.append(address)
                        print('got %s msg from %s:%d' %(data, address[0], address[1]))
                elif data.startswith('getdata'):
                    req = {}
                    req['dayIndex'] = int(data.split()[1])
                    req['addr'] = address
                    self.getdata_info.append(req)
                    print('got %s msg from %s:%d' %(data, address[0], address[1]))

    def sendLiveUpdateToListeners(self, json):
        if self.live_updates_addr != None:
            for address in self.live_updates_addr:
                print('sending to %s:%s msg %s' % (address[0], address[1], json))
                self.socket.sendto(json, address)
                
    def sendHistoryToListeners(self, solarDb):
        for entry in self.getdata_info:
            address = entry['addr']
            dayIndex = entry['dayIndex']
            print('reading day %d:%s msg %s' % (dayIndex, address[0], address[1]))
            temp_data, filename = solarDb.readDayLog(dayIndex, startup=False)
            print('sending day %s:%s msg %s' % (filename, address[0], address[1]))
            
            sourceIndex = 0
            for source in temp_data:
                msgData = {}
                msgData['date'] = filename.replace('.csv', '').replace(solarDb.m_filenamePrefix, '')
                msgData['sourceName'] = source
                msgData['sourceIndex'] = sourceIndex
                msgData['sourceCount'] = len(temp_data)
                msgData['sourceData'] = temp_data[source]
                sourceIndex = sourceIndex + 1
            
                json_data = json.dumps(msgData)
                print('sending data for %s' % (source))

                time.sleep(0.02)
          
                self.socket.sendto(json_data, address)
                
                
                
                
