import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly

import numpy as np
import pandas as pd
import scipy
import os
import random

from scipy import signal


def low_pass(data):
    fc = 0.05
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1
    n = np.arange(N)

    sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
    window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)

    return np.convolve(data, sinc_func)


def get_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return 'rgb' + str((r, g, b))


def import_data(x, y):
    data = pd.read_csv('data/overlapping/' + x + ',' + y + '-1,3,4,10,11,13.csv')
    df = data[0:10]

    table = FF.create_table(df)
    plotly.offline.plot(table, filename='point_data_table')
    return data


def plot_data(data):
    # Create traces
    trace1 = go.Scatter(
        x=np.arange(len(list(data['time']))),
        y=list(data['1']),
        name='1',
        line=dict(
            color='rgb(205, 12, 24)',
            width=4)  # dash options include 'dash', 'dot', and 'dashdot'
    )
    trace3 = go.Scatter(
        x=np.arange(len(list(data['time']))),
        y=list(data['3']),
        name='3',
        line=dict(
            color='rgb(22, 96, 167)',
            width=4)
    )

    trace_data = [trace1, trace3]

    # trace1 = go.Scatter(
    #     x=np.arange(len(list(data['time']))),
    #     y=list(data['value']),
    #     mode='lines',    # lines, lines+markers, markers
    #     name='Test Data'
    # )

    layout = go.Layout(
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='raw-data-plot')


def compare_overlapping_touching(index):
    data_1_1 = pd.read_csv('data/overlapping/1,1-1,3,4,10,11,13.csv')
    data_1_2 = pd.read_csv('data/overlapping/1,2-1,3,4,10,11,13.csv')
    data_1_3 = pd.read_csv('data/overlapping/1,3-1,3,4,10,11,13.csv')
    data_2_1 = pd.read_csv('data/overlapping/2,1-1,3,4,10,11,13.csv')
    data_2_2 = pd.read_csv('data/overlapping/2,2-1,3,4,10,11,13.csv')
    data_2_3 = pd.read_csv('data/overlapping/2,3-1,3,4,10,11,13.csv')
    data_3_1 = pd.read_csv('data/overlapping/3,1-1,3,4,10,11,13.csv')
    data_3_2 = pd.read_csv('data/overlapping/3,2-1,3,4,10,11,13.csv')
    data_3_3 = pd.read_csv('data/overlapping/3,3-1,3,4,10,11,13.csv')

    s = list(data_1_1[index])
    new_signal = low_pass(s)

    trace1_1 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='1_1',
        marker=dict(
            color='#C54C82'
        )
    )

    s = list(data_1_2[index])
    new_signal = low_pass(s)

    trace1_2 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='1_2',
        marker=dict(
            color='rgb(25, 25, 24)'
        )
    )
    s = list(data_1_3[index])
    new_signal = low_pass(s)

    trace1_3 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='1_3',
        marker=dict(
            color='rgb(205, 125, 24)'
        )
    )
    s = list(data_2_1[index])
    new_signal = low_pass(s)

    trace2_1 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='2_1',
        marker=dict(
            color='rgb(105, 15, 94)'
        )
    )
    s = list(data_2_2[index])
    new_signal = low_pass(s)

    trace2_2 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='2_2',
        marker=dict(
            color='rgb(75, 155, 124)'
        )
    )
    s = list(data_2_3[index])
    new_signal = low_pass(s)

    trace2_3 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='2_3',
        marker=dict(
            color='rgb(205, 25, 214)'
        )
    )

    s = list(data_3_1[index])
    new_signal = low_pass(s)

    trace3_1 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='3_1',
        marker=dict(
            color='rgb(105, 215, 104)'
        )
    )
    s = list(data_3_2[index])
    new_signal = low_pass(s)

    trace3_2 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='3_2',
        marker=dict(
            color='rgb(175, 5, 24)'
        )
    )
    s = list(data_3_3[index])
    new_signal = low_pass(s)

    trace3_3 = go.Scatter(
        x=np.arange(len(new_signal)),
        y=new_signal,
        mode='lines',
        name='3_3',
        marker=dict(
            color='rgb(5, 25, 14)'
        )
    )

    layout = go.Layout(
        title='Low-Pass Filter',
        showlegend=True
    )

    trace_data = [trace1_1, trace1_2, trace1_3, trace2_1, trace2_2, trace2_3, trace3_1, trace3_2, trace3_3]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='compare' + index)


def compare_data(folder):
    trace_data = []

    path = "data/" + folder
    files = os.listdir(path)
    for file in files:
        if file[-3:] == 'csv':
            data = pd.read_csv(path + '/' + file)
            s = list(data['value'])
            new_signal = low_pass(s)
            trace = go.Scatter(
                x=np.arange(len(new_signal)),
                y=new_signal,
                mode='lines',
                name=file[:-6],
                marker=dict(
                    color=get_color()
                )
            )
            trace_data.append(trace)

    layout = go.Layout(
        title=folder,
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename=folder + '.html')


def compare_overlapping_screen():
    trace_data = []

    data = pd.read_csv("data/overlapping3*3-1/all-0,2,4,10,12,14.csv")
    points = ['0', '2', '4', '10', '12', '14']
    for point in points:
        s = list(data[point])
        new_signal = low_pass(s)
        trace = go.Scatter(
            x=np.arange(len(new_signal)),
            y=new_signal,
            mode='lines',
            name=point,
            marker=dict(
                color=get_color()
            )
        )
        trace_data.append(trace)

    layout = go.Layout(
        title='overlapping 3*3-all',
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='overlapping 3*3-all')


def filter_data():
    # import data
    data = pd.read_csv('test-data.csv')
    df = data[0:10]

    table = FF.create_table(df)
    #plotly.offline.plot(table, filename='data-sample')

    # plot data
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

    # low-pass filter
    fc = 0.1
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

    layout = go.Layout(
        title='Low-Pass Filter',
        showlegend=True
    )

    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='low-pass-filter')


def main():
    #import_data('1', '1')
    #plot_data(import_data('1', '1'))
    #low_pass_filter(import_data('3', '3'))
    # filter_data()
    # 1, 3, 4, 10, 11, 13
    # compare_overlapping_touching('13')
    compare_data('ink-4mm-1m-length')
    # compare_overlapping_screen()


main()
