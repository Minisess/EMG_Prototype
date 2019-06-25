from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
from collections import deque


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.01):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = deque(maxlen=1000)
        self.ydata = deque(maxlen=1000)
        self.tdata.append(0)
        self.ydata.append(0)
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(0, 5)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1], ]
            self.ydata = [self.ydata[-1], ]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()
        t = self.time_generator(self.tdata[-1], len(y))
        self.ydata.extend(y)
        self.tdata.extend(t)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

    def time_generator(self, tttime, x):
        next_value = tttime
        while True:
            time_list = []
            for _ in range(x):
                time_list.append(next_value)
                next_value = next_value+self.dt
            return time_list


def voltage_read() -> list:
    """return a random value with probability p, else 0"""
    while True:
        data_list = []
        for _ in range(10):
            data.write(b's')
            if data.inWaiting():
                current_data = int(data.readline().decode("ASCII").strip(r'\n'))
                data_list.append(data_processing(current_data))
        yield data_list


def data_processing(current_data: int):
    # adjust number received from arduino
    return current_data * 5 / 1024



if __name__ == '__main__':
    baudrate = 115200
    data = serial.Serial('COM5', baudrate)
    fig, ax = plt.subplots()
    plt.title("Arduino Oscilloscope Data")
    plt.xlabel("Time (Sec)")
    plt.ylabel("Voltage (V)")
    scope = Scope(ax)
    ani = FuncAnimation(fig, scope.update, voltage_read(), blit=True, interval=80)
    plt.show()
    # pass a generator in "emitter" to produce data for the update func

