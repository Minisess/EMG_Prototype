from collections import deque
from matplotlib import pyplot as plt
import serial
import time

# class that holds analog data for N samples
class AnalogData:
    # constr

    def __init__(self, maxLen):
        self.ax = range(maxLen)
        self.maxLen = maxLen
        self.datas = 0

    # ring buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        self.addToBuf(self.ax, data)
        self.datas+=1

# plot class
class AnalogPlot:
    # constr
    def __init__(self, analogData):
        # set plot to animated
        plt.ion()
        self.axline, = plt.plot(analogData.ax)
        plt.ylim([0, 500])

    # update plot
    def update(self, analogData):
        self.axline.set_ydata(analogData.ax)
        plt.draw()


# main() function
def main():
    # expects 1 arg - serial port string
    com = 'COM5'
    analogData = AnalogData(500)
    analogPlot = AnalogPlot(analogData)
    # open serial port
    ser = serial.Serial(com, 9600)
    while True:
        try:
            ser.write(b'0xff')
            if ser.inWaiting():
                current_data = int(ser.readline().decode("ASCII"))
                analogData.add(data_processing(current_data))
            analogPlot.update(analogData)
            time.sleep(0.05)

        except KeyboardInterrupt:
            print('exiting')
            break
    # close serial
    ser.flush()
    ser.close()


def data_processing(current_data):
    processed_data = current_data/200
    return processed_data


# call main
if __name__ == '__main__':
    main()