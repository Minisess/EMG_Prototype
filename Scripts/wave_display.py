import json
from multiprocessing import Process, Pipe
import plotly.plotly as py
import plotly.graph_objs as go
from pathlib import Path
import pandas as pd
import statistics as stat
import scipy as sp
import scipy.integrate
from scipy import signal
from cont_list import main_read

integral_threshold = 150
amplitude_threshold = 0.3


def main(data_list):
    time_list = [x * 0.001 for x in range(len(data_list))]
    # construct dataframe with time and voltage
    df = pd.DataFrame({'time': time_list, 'voltage': data_list})

    mean = stat.mean(df['voltage'])  # determine offset
    df.voltage = df.voltage - mean  # correct offset
    df.voltage = abs(df.voltage)
    low_pass = 3
    sfreq = 1000
    low_pass = low_pass / sfreq  # the lowpass value
    b2, a2 = sp.signal.butter(4, low_pass, btype='lowpass')
    df.voltage = sp.signal.filtfilt(b2, a2, df.voltage)  # an envelop detector
    above_thresh = [x for x in df.voltage if x > amplitude_threshold]
    integral = sp.integrate.trapz(above_thresh)
    if integral > integral_threshold:
        print(f"Muscles! {integral}")


def save_data():
    with open(Path('run_trial_2.json'), 'w') as save_file:
        json.dump(data_list, save_file)


def plot(x, y):
    data = [go.Scatter(x=x, y=y)]
    py.iplot(data, filename='Voltage of Left Bicep Trial 1')


def load_data():
    with open(Path('run_trial.json'), 'r') as f:
        data_o = json.load(f)
    return data_o


if __name__ == '__main__':
    parent_conn, child_conn = Pipe(duplex=False)
    p = Process(target=main_read, args=(child_conn,))
    p.start()
    try:
        while True:
            if not p.is_alive():
                raise ChildProcessError
            data_list = parent_conn.recv()
            main(data_list)
    except KeyboardInterrupt:
        p.kill()
