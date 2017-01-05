#!/usr/bin/env python
import Tkinter as tk
from solar_monitor import Solar, setupSolar

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)    
		self.createWidgets()

		self.plotData = None;

		self.leftPad = 40
		self.topPad = 10
		self.bottomPad = 30
		self.rightPad = 10
		self.currentParm = -1;
		self.currentFileIndex = 0;  # most recent
		

	def createWidgets(self):
		
		#
		# set up frames for the 4 sensors
		#
		top=self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1) 
		
		#
		# set up frames for the 4 sensors
		#

		self.sensor_LabelFrame = []
		for sensorIndex in xrange(4):
			self.sensor_LabelFrame.append( tk.LabelFrame(self, text="Sensor") )
			self.sensor_LabelFrame[sensorIndex].grid(column=sensorIndex, row=0)  

		self.canvas_LabelFrame = tk.LabelFrame(self, text="Waveform for None")
		self.canvas_LabelFrame.grid(column=0, row=1, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)  

		# make virtual 5th column take stretching. and row 1 (with canvas)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(4, weight=1)

		self.canvas_LabelFrame.rowconfigure(0, weight=1)
		self.canvas_LabelFrame.columnconfigure(1, weight=1)

		# add a bit of space left of the readings so that the field stays fixed width
		for sensorIndex in xrange(4):
			self.sensor_LabelFrame[sensorIndex].columnconfigure(1, minsize=120)


		#
		# set up IntVar variables for checkboxes
		#
		self.sensor_voltageIntVar = []
		self.sensor_currentIntVar = []
		self.sensor_powerIntVar = []
		for sensorIndex in xrange(4):
			self.sensor_voltageIntVar.append( tk.IntVar( ) )
			self.sensor_currentIntVar.append( tk.IntVar( ) )
			self.sensor_powerIntVar.append( tk.IntVar( ) )


		#
		# set up checkboxes for Sensors
		#

		self.sensor_voltageCheckbox = []
		self.sensor_currentCheckbox = []
		self.sensor_powerCheckbox = []
		for sensorIndex in xrange(4):
			self.sensor_voltageCheckbox.append( tk.Checkbutton(self.sensor_LabelFrame[sensorIndex], text="V", variable=self.sensor_voltageIntVar[sensorIndex], command=self.checkbuttonHandler) )
			self.sensor_voltageCheckbox[sensorIndex].grid(column=0, row=1, sticky=tk.W)   
					 
			self.sensor_currentCheckbox.append( tk.Checkbutton(self.sensor_LabelFrame[sensorIndex], text="mA", variable=self.sensor_currentIntVar[sensorIndex], command=self.checkbuttonHandler))
			self.sensor_currentCheckbox[sensorIndex].grid(column=0, row=2, sticky=tk.W)  
			
			self.sensor_powerCheckbox.append( tk.Checkbutton(self.sensor_LabelFrame[sensorIndex], text="mW", variable=self.sensor_powerIntVar[sensorIndex], command=self.checkbuttonHandler))
			self.sensor_powerCheckbox[sensorIndex].grid(column=0, row=3, sticky=tk.W)            
       
       
       
 		#
		# set up StringVar for data outputs
		#

		self.sensor_voltageStringVar = []
		self.sensor_currentStringVar = []
		self.sensor_powerStringVar = []
		for sensorIndex in xrange(4):
			self.sensor_voltageStringVar.append( tk.StringVar( ) )
			self.sensor_voltageStringVar[sensorIndex].set("xx.xxx Volts")
			
			self.sensor_currentStringVar.append( tk.StringVar( ) )
			self.sensor_currentStringVar[sensorIndex].set("y.yyy Amps")
			
			self.sensor_powerStringVar.append( tk.StringVar( ) )
			self.sensor_powerStringVar[sensorIndex].set("xx.xxx Watts")
		

		


 		#
		# set up Label widgets for data outputs
		#

		self.sensor_voltageLabel = []
		self.sensor_currentLabel = []
		self.sensor_powerLabel = []
		for sensorIndex in xrange(4):
			self.sensor_voltageLabel.append( tk.Label(self.sensor_LabelFrame[sensorIndex], textvariable=self.sensor_voltageStringVar[sensorIndex]) )
			self.sensor_voltageLabel[sensorIndex].grid(column=1, row=1, sticky=tk.E)  

			self.sensor_currentLabel.append( tk.Label(self.sensor_LabelFrame[sensorIndex], textvariable=self.sensor_currentStringVar[sensorIndex]) )
			self.sensor_currentLabel[sensorIndex].grid(column=1, row=2, sticky=tk.E)  

			self.sensor_powerLabel.append( tk.Label(self.sensor_LabelFrame[sensorIndex], textvariable=self.sensor_powerStringVar[sensorIndex]) )
			self.sensor_powerLabel[sensorIndex].grid(column=1, row=3, sticky=tk.E)  





		#
		# set up the left and right buttons
		#
		self.canvasLeftButton = tk.Button(self.canvas_LabelFrame, text='<', command=self.clickRight)            
		self.canvasLeftButton.grid(column=0,row=0)            

		self.canvasRightButton = tk.Button(self.canvas_LabelFrame, text='>', command=self.clickLeft)            
		self.canvasRightButton.grid(column=2,row=0)            


	
		#
		# set up the plot canvas widgets
		#
		self.canvas = tk.Canvas(self.canvas_LabelFrame, width=800, height=500)            
		self.canvas.grid(column=1,row=0, sticky=tk.E + tk.W + tk.N + tk.S )            

		#
		# add resize handler
		#
		self.canvas.bind("<Configure>", self.on_resize)

		#
		# add quit handler
		#
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)            
		self.quitButton.grid()            

	def checkbuttonHandler(self):
		self.currentParm = -1;
		self.chanList = [0,0,0,0]
		for index in xrange(4):
			if ( self.sensor_voltageIntVar[index].get() == 1 ):  # a voltage is checked. uncheck the rest.
				self.currentParm = 0;
				self.chanList[index] = 1
				print("voltage[%d] is 1" % index);
			elif ( self.sensor_currentIntVar[index].get() == 1 ):  # a voltage is checked. uncheck the rest.
				print("current[%d] is 1" % index);
				self.currentParm = 1;
				self.chanList[index] = 1
			elif ( self.sensor_powerIntVar[index].get() == 1 ):  # a voltage is checked. uncheck the rest.
				self.currentParm = 2;
				self.chanList[index] = 1
				print("Power[%d] is 1" % index);

			if self.currentParm == 0:
				for index in xrange(4):
					self.sensor_currentCheckbox[index].deselect();
					self.sensor_powerCheckbox[index].deselect();
					#~ self.sensor_currentIntVar[index].set(0);
					#~ self.sensor_powerIntVar[index].set(0);
			elif self.currentParm == 1:
				for index in xrange(4):
					self.sensor_powerCheckbox[index].deselect();
					#~ self.sensor_powerIntVar[index].set(0);			

			
		self.plotGraph()

	def updateGuiFields(self, solarData):
		for sensorIndex in xrange(4):
			self.sensor_LabelFrame[sensorIndex]["text"] = solarData["names"][sensorIndex];	
			self.sensor_voltageStringVar[sensorIndex].set("%2.3f Volts" % solarData["voltage"][sensorIndex])
			self.sensor_currentStringVar[sensorIndex].set("%2.3f Amps" % (solarData["current"][sensorIndex]/1000.0))
			self.sensor_powerStringVar[sensorIndex].set("%2.3f Watts" % (solarData["voltage"][sensorIndex]*solarData["current"][sensorIndex]/1000.0))

	def clickRight(self):
		self.currentFileIndex = self.currentFileIndex +1
		self.fetchAndPlot();
		
	def clickLeft(self):
		if self.currentFileIndex > 0:
			self.currentFileIndex = self.currentFileIndex -1
		self.fetchAndPlot();
		
	def fetchAndPlot(self):
#		self.plotDate = self.mySolar.m_Timestamper.getDate()
#		self.plotDate = "2016_12_09"
		
		(self.plotData, filename) = self.mySolar.m_SolarDb.readDayLog(self.currentFileIndex);
		
		self.filename = filename
		self.mySolar.computeNetPower(self.plotData)
		
		self.plotGraph()
		
#		print(self.plotDate)
		
	def on_resize(self, event):
		self.plotheight = event.height;
		self.plotwidth = event.width;
		print("resized to %d %d" %(self.plotwidth,self.plotheight))
		self.plotGraph();

	def plotGraph(self):
		
		self.canvas.delete("all");
		# draw left y axis
		self.canvas.create_line(self.leftPad,self.topPad,self.leftPad,self.plotheight-self.bottomPad)
		# draw left y axis
		self.canvas.create_line(self.plotwidth-self.rightPad,self.topPad,self.plotwidth-self.rightPad,self.plotheight-self.bottomPad)
		# draw x axis only if there is no data to plot.
		if self.plotData == None:
			self.canvas.create_line(self.leftPad, self.plotheight-self.bottomPad, self.plotwidth-self.rightPad,self.plotheight-self.bottomPad)

#		self.canvas.create_line(0,0,self.plotwidth,self.plotheight)
		
		self.canvas_LabelFrame["text"] = "Waveform for " + self.filename
		
		# plot the data traces
		if (not self.plotData == None) and (self.currentParm != -1 ):
			for channelIndex in xrange(4):
				if self.chanList[channelIndex] == 1:
					
					parm = self.currentParm

					tempMinMax = self.getMinMaxForParm(parm, channelIndex)
					gridScaleMax = tempMinMax[1];
					gridScaleMin = tempMinMax[0];
					gridLeft = self.leftPad
					gridRight = self.plotwidth-self.rightPad
					gridBottom = self.plotheight-self.bottomPad
					gridTop = self.topPad
					gridWidth = gridRight-gridLeft
					gridHeight = gridBottom-gridTop
					gridScaleSpan = gridScaleMax-gridScaleMin
					

					valueCount = len(self.plotData[channelIndex]["voltage"])  # assume length of each array is the same.
					skipCount = valueCount/(self.plotwidth-self.leftPad-self.rightPad) # how many data points get put into each horizontal pixel of the plot
					print("voltage count=%d   plotWidth=%d   skipcount=%d" % (valueCount,self.plotwidth-self.leftPad-self.rightPad,skipCount))
					if skipCount <= 0:
						skipCount = 1
					plotXBase = self.leftPad
					plotYBase = self.plotheight-self.bottomPad
					if ( gridScaleMax == gridScaleMin):
						verticalScale = 1
					else:
						verticalScale = float(self.plotheight-self.topPad-self.bottomPad)/(gridScaleMax - gridScaleMin)
					horizontalScale = float(self.plotwidth-self.rightPad-self.leftPad)/float(valueCount )
					vertMin = gridScaleMin

					# plot the data
					leftValue=self.getDataValueForParm(parm,channelIndex,0)
					for index in xrange(skipCount,valueCount-skipCount,skipCount):
						rightValue = self.getDataValueForParm(parm,channelIndex,index);
						self.canvas.create_line(plotXBase+horizontalScale*(index),plotYBase-verticalScale*(leftValue-vertMin),plotXBase+horizontalScale*(index+skipCount),plotYBase-verticalScale*(rightValue-vertMin))
						leftValue = rightValue;
					
					# draw "0" x axis line
					if (gridScaleMin < 0) and (gridScaleMax > 0): # max is below 0 and min is above, so draw "0" line.
						self.canvas.create_line(gridLeft,plotYBase-verticalScale*(0-vertMin),gridRight,plotYBase-verticalScale*(0-vertMin))


					#
					# put the scale info
					#
					
					# axis numbers
					# x-axis numbers - left
					self.canvas.create_text(gridLeft, gridBottom + 2, text=self.plotData[channelIndex]["time"][0], anchor=tk.NW)
					# x-axis numbers - middle-left
					self.canvas.create_text( gridLeft+gridWidth/4 , gridBottom + 2, text=self.plotData[channelIndex]["time"][valueCount/4], anchor=tk.N)
					# x-axis numbers - middle
					self.canvas.create_text( gridLeft+gridWidth/2 , gridBottom + 2, text=self.plotData[channelIndex]["time"][valueCount/2], anchor=tk.N)
					# x-axis numbers - middle-right
					self.canvas.create_text( gridLeft+gridWidth*3/4 , gridBottom + 2, text=self.plotData[channelIndex]["time"][valueCount*3/4], anchor=tk.N)
					# x-axis numbers - right
					self.canvas.create_text(gridRight, gridBottom + 2, text=self.plotData[channelIndex]["time"][valueCount-1], anchor=tk.NE)

					# y-axis numbers - top
					self.canvas.create_text(0, gridTop + 2, text=("%2.2f" % (gridScaleMin+gridScaleSpan)), anchor=tk.NW)
					# y-axis numbers - middle-top
					self.canvas.create_text( 0 , gridTop+gridHeight/4, text=("%2.2f" % (gridScaleMin+gridScaleSpan*3/4)), anchor=tk.W)
					# y-axis numbers - middle
					self.canvas.create_text( 0 , gridTop+gridHeight/2, text=("%2.2f" % (gridScaleMin+gridScaleSpan/2)), anchor=tk.W)
					# y-axis numbers - middle-bottom
					self.canvas.create_text( 0 , gridTop+gridHeight*3/4, text=("%2.2f" % (gridScaleMin+gridScaleSpan/4)), anchor=tk.W)
					# y-axis numbers - bottom
					self.canvas.create_text(0, gridBottom - 2, text=("%2.2f" % (gridScaleMin)), anchor=tk.SW)
		
	def getDataValueForParm(self,parm,channelIndex,index):
		returnVal = 0;
		if parm == 0:  # voltage
			returnVal = self.plotData[channelIndex]["voltage"][index];
		elif parm == 1: # current
			returnVal = self.plotData[channelIndex]["current"][index];
		elif parm == 2: # power
			returnVal = self.plotData[channelIndex]["voltage"][index] * self.plotData[channelIndex]["current"][index];
		return returnVal
		
	def getMinMaxForParm(self,parm,channelIndex):
		returnVal = [999999999.0, -999999999.0] # baseline extreme opposite numbers for min and max
		channelMax = 0; channelMin = 0
		for channelIndex in xrange(4):
			if self.chanList[channelIndex] == 1:# is channel enabled. FIXME when clickers working
				if parm == 0: # voltage
					channelMax = self.plotData[channelIndex]["maxVoltage"];
					channelMin = self.plotData[channelIndex]["minVoltage"];
				elif parm == 1: # current
					channelMax = self.plotData[channelIndex]["maxCurrent"];
					channelMin = self.plotData[channelIndex]["minCurrent"];
				elif parm == 2: # power
					channelMax = self.plotData[channelIndex]["maxPower"];
					channelMin = self.plotData[channelIndex]["minPower"];

				if channelMax > returnVal[1]: # find new max
					returnVal[1] = channelMax;
				if channelMin < returnVal[0]: # find new min
					returnVal[0] = channelMin;
		return returnVal
				
	def periodicEventHandler(self):
#		self.after(1000,self.periodicEventHandler);
		
		data = self.mySolar.gatherData();
		self.updateGuiFields(data);
		self.mySolar.recordData(data);
		self.mySolar.printResults(data);





def main():
	app = Application()                       
	app.master.title('Solar Panel Monitor')    
	
#	app.after(0,app.periodicEventHandler);
	
	app.mySolar = setupSolar()
	app.mainloop() ;
	 


	
	

if __name__ == "__main__":
	main();

