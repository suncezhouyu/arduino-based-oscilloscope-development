#Original code written by Sandro Tosi(Matplotlib for Python Developers, PACKT publishing, 2009).
#Slightly modified by Ji Li.

import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import serial
#import datetime
import time

TIMER_ID = wx.NewId()


class PlotFigure(wx.Frame):
    def __init__(self, portname, baudrate):###
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Arduino Monitor", size=(800,600))

        self.fig = Figure((8,6), 100)
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        self.ax = self.fig.add_subplot(1,1,1)

        self.ax.set_ylim([-0.1, 1.15])
        self.ax.set_xlim([0,300])
        self.ax.set_autoscale_on(False)

        self.xleft = 0
        self.xright = 300
        self.ax.set_xticks([])
        self.ax.set_yticks([0.0,0.5,1.0])
        self.ax.grid(True)

        self.data = [None] * 300    
        
        self.l_data,=self.ax.plot(range(300), self.data, label='Arduino Output')
        #',' means iteration
        self.l_x1 = self.ax.text(0,-0.05,'') 
        self.l_x5 = self.ax.text(290,-0.05,'')

        self.ax.legend(loc='upper center', ncol=1)

        self.canvas.draw()
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)

        self.ser = serial.Serial(portname, baudrate)###open serial port and assign a baudrate
        time.sleep(5)#this command is very important since the arduino board needs a short while to settle. 
        #without this settling time, the programme would got stuck!
        self.ser.flushInput()
        self.ser.flushOutput()
        self.counter = 0.0

        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)#binding

    def onTimer(self, evt):
        self.ser.write("?")#the py program might need to wait a bit till data arrives in buffer
        tmp = self.ser.read()#tmp is a string
        tmp = int(tmp)#tmp is an integer now
        self.canvas.restore_region(self.bg)
        self.data = self.data[1:] + [tmp]#keep self.data 300 elements long while forwarding the sequence
        
        self.xleft = self.xleft + 1
        self.xright = self.xright + 1
        #print self.xleft, self.xright

        self.l_data.set_ydata(self.data)
        self.counter = self.counter + 0.05
        tmp1 = str(int(self.counter + 0.5))
        tmp2 = str(int(self.counter + 0.5) - 15)# 15 = 300 pts / (1 sec / 50 msec)
        self.l_x1.set_text(tmp2)
        self.l_x5.set_text(tmp1)

        self.ax.draw_artist(self.l_data)
        
        self.ax.draw_artist(self.l_x1)##
        self.ax.draw_artist(self.l_x5)##

        self.canvas.blit(self.ax.bbox)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = PlotFigure("/dev/ttyACM0", 9600)###
    t = wx.Timer(frame, TIMER_ID)
    t.Start(50)

    frame.Show()
    app.MainLoop()
