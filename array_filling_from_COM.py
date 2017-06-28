import serial
import numpy as np
from timeit import timeit
import time

interval = 1# Интервал таймера в милисекундах
array_size = 100 # Размер массива (some changes)
a = np.zeros([array_size,2], dtype=np.int)

comport = 6
portname = "COM{}".format(comport)
try:
    ser = serial.Serial(portname)
    ser.baudrate = 115200
    ser.timeout = 0.1
except serial.SerialException:
    print("error of serial")
    exit(1)

def getcurrenttime():
    return time.clock()

def getinterval(lasttime):
    return (time.clock() - lasttime) * 1000

lasttime = getcurrenttime()

def add_element(n): # Добавление в массив очередного элемента
    a[n, 0] = int(ser.readline()[:-2])
    a[n, 1] = int(time.clock() * 1000)

def filling_up_array(): # Заполнение массива по таймеру
    global lasttime
    global interval
    global array_size
    i = 0
    while i < array_size:
        currentinterval = getinterval(lasttime)
        if currentinterval >= interval:
            lasttime = getcurrenttime()
            add_element(i)
            i += 1

def time_control():
    global a
    a[0, 1] = int(ser.readline()[:-2])

if __name__ =='__main__':
        print(timeit(time_control, number=1))
        filling_up_array()
        print(a.size)
        print(a)
        ser.close()

