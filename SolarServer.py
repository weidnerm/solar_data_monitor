from OneFifo import OneFifo
import json
import socket
import select

class SolarServer():
    def __init__(self):

        self.one_fifo = None

        self.one_fifo = OneFifo('/tmp/solar_data.fifo')
        self.one_fifo.__enter__()

        self.listner_address = []

        self.socket = socket.socket(socket.AF_INET, #internet,
                                    socket.SOCK_DGRAM) #UDP
        self.socket.setblocking(False)
        self.socket.bind( ('0.0.0.0', 29551) ) 


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

        jsonOutput = json.dumps(outputDict)

        self.handleNewAttachments()
        self.sendUdpToListeners(jsonOutput)
        
        # send message through the pipe
        self.one_fifo.write(jsonOutput);
        
        return jsonOutput




    def handleNewAttachments(self):
        self.listner_address = []
        
        queue_empty = False
        while queue_empty == False:
            ready_to_read, ready_to_write, in_error = select.select( [self.socket], [], [], 0.001) # only wait 1 msec

            if len(ready_to_read) == 0:
                queue_empty = True
            else:
                data, address = ready_to_read[0].recvfrom(4096)
                if not address in self.listner_address:
                    self.listner_address.append(address)
                    print('got sub msg from')
                    print(self.listner_address)

    def sendUdpToListeners(self, json):
        if self.listner_address != None:
            for address in self.listner_address:
                print('sending to %s:%s msg %s' % (address[0], address[1], json))
                self.socket.sendto(json, address)
