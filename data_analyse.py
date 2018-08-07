import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly

import numpy as np
import pandas as pd
import scipy
import os
import random


def high_pass():
    data = pd.read_csv('data/material/paper cup with 250ml water-7.csv')
    x = np.arange(len(list(data['time'])))

    fc = 0.1
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)

    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = np.blackman(N)
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)

    # reverse function
    sinc_func = -sinc_func
    sinc_func[int((N - 1) / 2)] += 1

    s = list(data['value'])
    new_signal = np.convolve(s, sinc_func)

    trace1 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='High-Pass Filter',
        marker=dict(
            color='#C54C82'
        )
    )

    layout = go.Layout(
        title='High-Pass Filter',
        showlegend=True
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='high-pass-filter')


def detect_diff():
    data = pd.read_csv('data/material/plastic bottle with 500ml water-7.csv')
    x = np.arange(len(list(data['time'])))

    # low-pass filter
    fc = 0.05
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)

    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)

    s = list(data['value'])
    new_signal = np.convolve(s, sinc_func)

    trace1 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='Low-Pass Filter',
        marker=dict(
            color='#C54C82'
        )
    )

    new_signal2 = np.insert(new_signal, 0, 0)
    new_signal2 = np.delete(new_signal2, -1, 0)
    diff = new_signal - new_signal2
    index = np.where(np.logical_and(diff > 5, diff < 1000))
    points = []
    for item in index[0]:
        points.append(
            dict(
                x=item,
                y=new_signal[item],
                xref='x',
                yref='y',
                text=str(item),
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40)
        )

    layout = go.Layout(
        title='Low-Pass Filter',
        showlegend=True,
        annotations=points
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='low-pass-filter')


def draw_raw():
    data = pd.read_csv('data/material/iphone 7 plus back-7.csv')
    x = np.arange(len(list(data['time'])))

    trace1 = go.Scatter(
        x=np.arange(len(list(data['time']))),
        y=list(data['value']),
        mode='lines',
        name='Test Data'
    )

    layout = go.Layout(
        showlegend=True
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='raw-data-plot')


def main():
    detect_diff()
    # high_pass()
    #draw_raw()


main()