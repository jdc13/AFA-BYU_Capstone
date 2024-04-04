'''This file contains a class to generate the UI for the sensor array'''
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

#Colors:
active = "lime green"
inactive = "firebrick3"

class GUI:
    '''A graphical interface to allow for switching between raw and processed outputs'''
    def __init__(self):
        #Control Variables:

        #Lists of things to plot
        self.walls = []
        self.raw = []
        
        #Generate window
        self.root = Tk() 
        self.root.configure(bg = "white")
        self.root.title("USAFA/BYU Robotics")
        
        #Generate figure to display the resutls
        self.fig = Figure(figsize = (5,5), dpi = 100)
        self.plot = self.fig.add_subplot(111)

        #Create the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        #Format the figure:
        self.plot.axis("off")

        #Create buttons:
        buttonFrame = Frame(self.root, bg = "white")
        buttonFrame.pack()
        self.b_raw = Button(buttonFrame, text="Show Raw", command=self.raw_press)
        self.b_walls = Button(buttonFrame, text = "Hide Walls", command=self.wall_press)

        #Position buttons
        gap = 40
        self.b_raw.grid(column=0, row = 0, padx=(0, gap/2))
        self.b_raw.config(bg=inactive)
        self.b_walls.grid(column=1, row=0, padx=(gap/2, 0))
        self.b_walls.configure(bg=active)
        self.b_walls.widgetName


        self.root.update()
    
    def raw_press(self):
        #Toggle Raw visibility
        if self.b_raw.cget('bg') == active:
            self.b_raw.configure(bg = inactive, text= "Show Raw")
        else:
            self.b_raw.configure(bg = active, text="Hide Raw")
        
    
    def wall_press(self):
        #Toggle wall visibility
        if self.b_walls.cget('bg') == active:
            self.b_walls.configure(bg = inactive, text = "Show Walls")
        else:
            self.b_walls.configure(bg = active, text = "Hide Walls")


    def update(self, segments = [], raw = []):
        self.walls = self.walls + segments
        self.raw = self.raw + raw

        for w in self.walls:
            self.plot_segment(w)
        self.root.update()

    def plot_segment(self, segment):
        '''Function to plot the line segments'''
        #Switched x and y from testing to make it more intuitive
        self.fig.plot(segment.T[1], segment.T[0], color = "k") 

if __name__ == "__main__":
    '''Code that will run if this is the root file (debuging)'''
    interface = GUI()
    for i in range(2000):
        time.sleep(.001)
        interface.update()




