from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
import serial
from collections import deque


def main_read(conn):
    base = 2.5
    port_name = "COM5"  # replace this port name by yours!
    baudrate = 115200
    data = serial.Serial(port_name, baudrate)
    size = 200
    data_list = deque([base] * size, maxlen=200)
    j = 0
    win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window
    p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
    curve = p.plot()

    while True:
        data.write(b's')
        if data.inWaiting():
            current_data = int(data.readline().decode("ASCII"))
            processed_data = data_processing(current_data)
            data_list.append(processed_data)
            update_graph(curve, data_list)
            j += 1
        if j == 10:
            conn.send(data_list)
            j = 0


def data_processing(current_data):
    processed_data = current_data*5/1023
    return processed_data


# Realtime data plot. Each time this function is called, the data display is updated
def update_graph(curve, data_list):
    curve.setData(data_list)                     # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now

# if __name__ == '__main__':
#     conn = None
#     main_read(conn)
