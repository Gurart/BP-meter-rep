import serial
comport = 6
portname = "COM{}".format(comport)
try:
    ser = serial.Serial(portname)
    ser.baudrate = 115200
    ser.timeout = 0.1
except serial.SerialException:
    print("error of serial")
    exit(1)

import matplotlib
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
miss=3

class Scope:
    def __init__(self, ax, maxt=6, dt=0.01):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata, color="red")
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1, 1024)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt: # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

def emitter():
    global miss
    if miss>0:
        miss=miss-1
        yield 0
    else:
        ser.flushInput()
        ser.readline()
        yield int(ser.readline()[:-2])

fig = plt.figure()
ax = fig.add_subplot(111)
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=2, blit=False)

plt.show()
ser.close()
