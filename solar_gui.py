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

		self.sensor1_LabelFrame = tk.LabelFrame(self, text="Sensor 1 (40)")
		self.sensor1_LabelFrame.grid(column=0, row=0)  

		self.sensor2_LabelFrame = tk.LabelFrame(self, text="Sensor 2 (41)")
		self.sensor2_LabelFrame.grid(column=1, row=0)  

		self.sensor3_LabelFrame = tk.LabelFrame(self, text="Sensor 3 (45)")
		self.sensor3_LabelFrame.grid(column=2, row=0)  

		self.sensor4_LabelFrame = tk.LabelFrame(self, text="Sensor 4 (45)")
		self.sensor4_LabelFrame.grid(column=3, row=0)  


		self.canvas_LabelFrame = tk.LabelFrame(self, text="Waveform for 2016_10_11")
		self.canvas_LabelFrame.grid(column=0, row=1, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)  

		# make virtual 5th column take stretching. and row 1 (with canvas)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(4, weight=1)

		self.canvas_LabelFrame.rowconfigure(0, weight=1)
		self.canvas_LabelFrame.columnconfigure(1, weight=1)

		# add a bit of space left of the readings so that the field stays fixed width
		self.sensor1_LabelFrame.columnconfigure(1, minsize=120)
		self.sensor2_LabelFrame.columnconfigure(1, minsize=120)
		self.sensor3_LabelFrame.columnconfigure(1, minsize=120)
		self.sensor4_LabelFrame.columnconfigure(1, minsize=120)


		#
		# set up checkboxes for Sensor 1
		#

		self.sensor1_voltageCheckbox = tk.Checkbutton(self.sensor1_LabelFrame, text="V")
		self.sensor1_voltageCheckbox.grid(column=0, row=1, sticky=tk.W)   
		         
		self.sensor1_currentCheckbox = tk.Checkbutton(self.sensor1_LabelFrame, text="mA")
		self.sensor1_currentCheckbox.grid(column=0, row=2, sticky=tk.W)  
		
		self.sensor1_powerCheckbox = tk.Checkbutton(self.sensor1_LabelFrame, text="mW")
		self.sensor1_powerCheckbox.grid(column=0, row=3, sticky=tk.W)            
       
       
		self.sensor2_voltageCheckbox = tk.Checkbutton(self.sensor2_LabelFrame, text="V")
		self.sensor2_voltageCheckbox.grid(column=0, row=1, sticky=tk.W)   
		         
		self.sensor2_currentCheckbox = tk.Checkbutton(self.sensor2_LabelFrame, text="mA")
		self.sensor2_currentCheckbox.grid(column=0, row=2, sticky=tk.W)  
		
		self.sensor2_powerCheckbox = tk.Checkbutton(self.sensor2_LabelFrame, text="mW")
		self.sensor2_powerCheckbox.grid(column=0, row=3, sticky=tk.W)            
       
       
		self.sensor3_voltageCheckbox = tk.Checkbutton(self.sensor3_LabelFrame, text="V")
		self.sensor3_voltageCheckbox.grid(column=0, row=1, sticky=tk.W)   
		         
		self.sensor3_currentCheckbox = tk.Checkbutton(self.sensor3_LabelFrame, text="mA")
		self.sensor3_currentCheckbox.grid(column=0, row=2, sticky=tk.W)  
		
		self.sensor3_powerCheckbox = tk.Checkbutton(self.sensor3_LabelFrame, text="mW")
		self.sensor3_powerCheckbox.grid(column=0, row=3, sticky=tk.W)            
       
       
		self.sensor4_voltageCheckbox = tk.Checkbutton(self.sensor4_LabelFrame, text="V")
		self.sensor4_voltageCheckbox.grid(column=0, row=1, sticky=tk.W)   
		         
		self.sensor4_currentCheckbox = tk.Checkbutton(self.sensor4_LabelFrame, text="mA")
		self.sensor4_currentCheckbox.grid(column=0, row=2, sticky=tk.W)  
		
		self.sensor4_powerCheckbox = tk.Checkbutton(self.sensor4_LabelFrame, text="mW")
		self.sensor4_powerCheckbox.grid(column=0, row=3, sticky=tk.W)            
       
       
 		#
		# set up StringVar for data outputs
		#

		self.sensor1_voltageStringVar = tk.StringVar( )
		self.sensor1_voltageStringVar.set("xx.xxx Volts")
		
		self.sensor1_currentStringVar = tk.StringVar( )
		self.sensor1_currentStringVar.set("y.yyy Amps")
		
		self.sensor1_powerStringVar = tk.StringVar( )
		self.sensor1_powerStringVar.set("xx.xxx Watts")
		

		self.sensor2_voltageStringVar = tk.StringVar( )
		self.sensor2_voltageStringVar.set("xx.xxx Volts")
		
		self.sensor2_currentStringVar = tk.StringVar( )
		self.sensor2_currentStringVar.set("y.yyy Amps")
		
		self.sensor2_powerStringVar = tk.StringVar( )
		self.sensor2_powerStringVar.set("xx.xxx Watts")
		

		self.sensor3_voltageStringVar = tk.StringVar( )
		self.sensor3_voltageStringVar.set("xx.xxx Volts")
		
		self.sensor3_currentStringVar = tk.StringVar( )
		self.sensor3_currentStringVar.set("y.yyy Amps")
		
		self.sensor3_powerStringVar = tk.StringVar( )
		self.sensor3_powerStringVar.set("xx.xxx Watts")
		

		self.sensor4_voltageStringVar = tk.StringVar( )
		self.sensor4_voltageStringVar.set("xx.xxx Volts")
		
		self.sensor4_currentStringVar = tk.StringVar( )
		self.sensor4_currentStringVar.set("y.yyy Amps")
		
		self.sensor4_powerStringVar = tk.StringVar( )
		self.sensor4_powerStringVar.set("xx.xxx Watts")
		


 		#
		# set up Label widgets for data outputs
		#

		self.sensor1_voltageLabel = tk.Label(self.sensor1_LabelFrame, textvariable=self.sensor1_voltageStringVar)
		self.sensor1_voltageLabel.grid(column=1, row=1, sticky=tk.E)  

		self.sensor1_currentLabel = tk.Label(self.sensor1_LabelFrame, textvariable=self.sensor1_currentStringVar)
		self.sensor1_currentLabel.grid(column=1, row=2, sticky=tk.E)  

		self.sensor1_powerLabel = tk.Label(self.sensor1_LabelFrame, textvariable=self.sensor1_powerStringVar)
		self.sensor1_powerLabel.grid(column=1, row=3, sticky=tk.E)  


		self.sensor2_voltageLabel = tk.Label(self.sensor2_LabelFrame, textvariable=self.sensor2_voltageStringVar)
		self.sensor2_voltageLabel.grid(column=1, row=1, sticky=tk.E)  

		self.sensor2_currentLabel = tk.Label(self.sensor2_LabelFrame, textvariable=self.sensor2_currentStringVar)
		self.sensor2_currentLabel.grid(column=1, row=2, sticky=tk.E)  

		self.sensor2_powerLabel = tk.Label(self.sensor2_LabelFrame, textvariable=self.sensor2_powerStringVar)
		self.sensor2_powerLabel.grid(column=1, row=3, sticky=tk.E)  


		self.sensor3_voltageLabel = tk.Label(self.sensor3_LabelFrame, textvariable=self.sensor3_voltageStringVar)
		self.sensor3_voltageLabel.grid(column=1, row=1, sticky=tk.E)  

		self.sensor3_currentLabel = tk.Label(self.sensor3_LabelFrame, textvariable=self.sensor3_currentStringVar)
		self.sensor3_currentLabel.grid(column=1, row=2, sticky=tk.E)  

		self.sensor3_powerLabel = tk.Label(self.sensor3_LabelFrame, textvariable=self.sensor3_powerStringVar)
		self.sensor3_powerLabel.grid(column=1, row=3, sticky=tk.E)  


		self.sensor4_voltageLabel = tk.Label(self.sensor4_LabelFrame, textvariable=self.sensor4_voltageStringVar)
		self.sensor4_voltageLabel.grid(column=1, row=1, sticky=tk.E)  

		self.sensor4_currentLabel = tk.Label(self.sensor4_LabelFrame, textvariable=self.sensor4_currentStringVar)
		self.sensor4_currentLabel.grid(column=1, row=2, sticky=tk.E)  

		self.sensor4_powerLabel = tk.Label(self.sensor4_LabelFrame, textvariable=self.sensor4_powerStringVar)
		self.sensor4_powerLabel.grid(column=1, row=3, sticky=tk.E)  





		#
		# set up the left and right buttons
		#
		self.canvasLeftButton = tk.Button(self.canvas_LabelFrame, text='<', command=self.fetchAndPlot)            
		self.canvasLeftButton.grid(column=0,row=0)            

		self.canvasRightButton = tk.Button(self.canvas_LabelFrame, text='>', command=self.fetchAndPlot)            
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





 		#
		# set up the plot canvas widgets
		#
		self.canvas.create_line(0,0,800,500)

	def updateGuiFields(self, solarData):
		
		self.sensor1_LabelFrame["text"] = solarData["names"][0];
		self.sensor2_LabelFrame["text"] = solarData["names"][1];
		self.sensor3_LabelFrame["text"] = solarData["names"][2];
		self.sensor4_LabelFrame["text"] = solarData["names"][3];
		
		self.sensor1_voltageStringVar.set("%2.3f Volts" % solarData["voltage"][0])
		self.sensor2_voltageStringVar.set("%2.3f Volts" % solarData["voltage"][1])
		self.sensor3_voltageStringVar.set("%2.3f Volts" % solarData["voltage"][2])
		self.sensor4_voltageStringVar.set("%2.3f Volts" % solarData["voltage"][3])

		self.sensor1_currentStringVar.set("%2.3f Amps" % (solarData["current"][0]/1000.0))
		self.sensor2_currentStringVar.set("%2.3f Amps" % (solarData["current"][1]/1000.0))
		self.sensor3_currentStringVar.set("%2.3f Amps" % (solarData["current"][2]/1000.0))
		self.sensor4_currentStringVar.set("%2.3f Amps" % (solarData["current"][3]/1000.0))

		self.sensor1_powerStringVar.set("%2.3f Watts" % (solarData["voltage"][0]*solarData["current"][0]/1000.0))
		self.sensor2_powerStringVar.set("%2.3f Watts" % (solarData["voltage"][1]*solarData["current"][1]/1000.0))
		self.sensor3_powerStringVar.set("%2.3f Watts" % (solarData["voltage"][2]*solarData["current"][2]/1000.0))
		self.sensor4_powerStringVar.set("%2.3f Watts" % (solarData["voltage"][3]*solarData["current"][3]/1000.0))

	def fetchAndPlot(self):
		self.plotDate = self.mySolar.m_Timestamper.getDate()
#		self.plotDate = "2016_12_09"
		
		self.plotData = self.mySolar.m_SolarDb.readDayLog(self.plotDate);
		

		
		self.plotGraph()
		
		print(self.plotDate)
		
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
		
		# plot the data traces
		if not self.plotData == None:
			self.channelIndex = 2
			parm = 2

			tempMinMax = self.getMinMaxForParm(parm)
			gridScaleMax = tempMinMax[1];
			gridScaleMin = tempMinMax[0];
			gridLeft = self.leftPad
			gridRight = self.plotwidth-self.rightPad
			gridBottom = self.plotheight-self.bottomPad
			gridTop = self.topPad
			gridWidth = gridRight-gridLeft
			gridHeight = gridBottom-gridTop
			gridScaleSpan = gridScaleMax-gridScaleMin
			

			valueCount = len(self.plotData[self.channelIndex]["voltage"])  # assume length of each array is the same.
			skipCount = valueCount/(self.plotwidth-self.leftPad-self.rightPad) # how many data points get put into each horizontal pixel of the plot
			print("voltage count=%d   plotWidth=%d   skipcount=%d" % (valueCount,self.plotwidth-self.leftPad-self.rightPad,skipCount))
			if skipCount <= 0:
				skipCount = 1
			plotXBase = self.leftPad
			plotYBase = self.plotheight-self.bottomPad
#			print("maxVoltage=%2.3f  minVoltage=%2.3f" % (self.plotData[self.channelIndex]["maxVoltage"],self.plotData[self.channelIndex]["minVoltage"]))
			verticalScale = float(self.plotheight-self.topPad-self.bottomPad)/(gridScaleMax - gridScaleMin)
			horizontalScale = float(self.plotwidth-self.rightPad-self.leftPad)/float(valueCount )
			vertMin = gridScaleMin

			# plot the data
			leftValue=self.getDataValueForParm(parm,0)
			for index in xrange(skipCount,valueCount-skipCount,skipCount):
				rightValue = self.getDataValueForParm(parm,index);
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
			self.canvas.create_text(gridLeft, gridBottom + 2, text=self.plotData[self.channelIndex]["time"][0], anchor=tk.NW)
			# x-axis numbers - middle-left
			self.canvas.create_text( gridLeft+gridWidth/4 , gridBottom + 2, text=self.plotData[self.channelIndex]["time"][valueCount/4], anchor=tk.N)
			# x-axis numbers - middle
			self.canvas.create_text( gridLeft+gridWidth/2 , gridBottom + 2, text=self.plotData[self.channelIndex]["time"][valueCount/2], anchor=tk.N)
			# x-axis numbers - middle-right
			self.canvas.create_text( gridLeft+gridWidth*3/4 , gridBottom + 2, text=self.plotData[self.channelIndex]["time"][valueCount*3/4], anchor=tk.N)
			# x-axis numbers - right
			self.canvas.create_text(gridRight, gridBottom + 2, text=self.plotData[self.channelIndex]["time"][valueCount-1], anchor=tk.NE)

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
		
	def getDataValueForParm(self,parm,index):
		returnVal = 0;
		if parm == 0:  # voltage
			returnVal = self.plotData[self.channelIndex]["voltage"][index];
		elif parm == 1: # current
			returnVal = self.plotData[self.channelIndex]["current"][index];
		elif parm == 2: # power
			returnVal = self.plotData[self.channelIndex]["voltage"][index] * self.plotData[self.channelIndex]["current"][index];
		return returnVal
		
	def getMinMaxForParm(self,parm):
		returnVal = [999999999.0, -999999999.0] # baseline extreme opposite numbers for min and max
		channelMax = 0; channelMin = 0
		for channelIndex in xrange(4):
			if ( channelIndex == self.channelIndex ):  # is channel enabled. FIXME when clickers working
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
		self.after(1000,self.periodicEventHandler);
		
		data = self.mySolar.gatherData();
		self.updateGuiFields(data);
		self.mySolar.recordData(data);
		self.mySolar.printResults(data);





def main():
	app = Application()                       
	app.master.title('Solar Panel Monitor')    
	
	app.after(0,app.periodicEventHandler);
	
	app.mySolar = setupSolar()
	app.mainloop() ;
	 


	
	

if __name__ == "__main__":
	main();

