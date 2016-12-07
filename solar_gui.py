#!/usr/bin/env python
import Tkinter as tk

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)    
		self.createWidgets()

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
		# set up the plot canvas widgets
		#


		self.canvasLeftButton = tk.Button(self.canvas_LabelFrame, text='<', command=self.quit)            
		self.canvasLeftButton.grid(column=0,row=0)            

		self.canvasRightButton = tk.Button(self.canvas_LabelFrame, text='>', command=self.quit)            
		self.canvasRightButton.grid(column=2,row=0)            

		self.canvas = tk.Canvas(self.canvas_LabelFrame, width=800, height=500)            
		self.canvas.grid(column=1,row=0)            




		self.quitButton = tk.Button(self, text='Quit', command=self.quit)            
		self.quitButton.grid()            





 		#
		# set up the plot canvas widgets
		#
		self.canvas.create_line(0,0,800,500)










def main():
	app = Application()                       
	app.master.title('Solar Panel Monitor')    
	app.mainloop()              


	
	

if __name__ == "__main__":
	main();

