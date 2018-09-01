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
    fc = 0.04
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
                name=file[:-3],
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
    plotly.offline.plot(fig, filename=folder + '2.html')


def compare_overlapping_screen():
    trace_data = []

    data = pd.read_csv("data/yogamat/1,2.csv")
    points = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28']
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
        title='yogamat',
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='yogamat.html')


def filter_data():
    # import data
    data = pd.read_csv('data/ink-2.7mm-1m-length/0.01m-7.csv')
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
    #plotly.offline.plot(fig, filename='raw-data-plot')

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


def length_test_on_width_material():
    length = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1]

    copper_half = [625, 560, 467, 215, 90, 45, 30, 20]
    copper_1 = [880, 685, 425, 240, 110, 70, 44, 32]
    copper_2 = [1020, 830, 400, 135, 180, 110, 60, 47]   # 0.05, 0.1

    ink_half = []
    ink_1 = [650, 633, 388, 357, 200, 95, 65, 35]
    ink_2 = [825, 690, 512, 337, 129, 82, 65, 41]

    ito_half = [500, 460, 300, 163, 80, 60, 45, 25]
    ito_1 = [720, 665, 550, 355, 263, 132, 90, 68]
    ito_2 = [778, 525, 500, 311, 150, 85, 55, 36]   #0.02

    trace_copper_half = go.Scatter(
        x=length,
        y=copper_half,
        mode='lines',
        name='copper-0.5',
        line=dict(
            color='rgb(205, 12, 24)',
            width=2,
            dash='dash')
    )

    trace_copper_1 = go.Scatter(
        x=length,
        y=copper_1,
        mode='lines',
        name='copper-1',
        line=dict(
            color='rgb(205, 12, 24)',
            width=2,
            dash='dot')
    )

    trace_copper_2 = go.Scatter(
        x=length,
        y=copper_2,
        mode='lines',
        name='copper-2',
        line=dict(
            color='rgb(205, 12, 24)',
            width=2)
    )

    trace_ink_1 = go.Scatter(
        x=length,
        y=ink_1,
        mode='lines',
        name='ink-1',
        line=dict(
            color='rgb(22, 96, 167)',
            width=2,
            dash='dot')
    )

    trace_ink_2 = go.Scatter(
        x=length,
        y=ink_2,
        mode='lines',
        name='ink-2',
        line=dict(
            color='rgb(22, 96, 167)',
            width=2)
    )

    trace_ito_half = go.Scatter(
        x=length,
        y=ito_half,
        mode='lines',
        name='ito-0.5',
        line=dict(
            color='rgb(0,100,80)',
            width=2,
            dash='dash')
    )

    trace_ito_1 = go.Scatter(
        x=length,
        y=ito_1,
        mode='lines',
        name='ito-1',
        line=dict(
            color='rgb(0,100,80)',
            width=2,
            dash='dot')
    )

    trace_ito_2 = go.Scatter(
        x=length,
        y=ito_2,
        mode='lines',
        name='ito-2',
        line=dict(
            color='rgb(0,100,80)',
            width=2)
    )

    trace_data = [trace_copper_half, trace_copper_1, trace_copper_2, trace_ink_1, trace_ink_2, trace_ito_half, trace_ito_1, trace_ito_2]

    layout = go.Layout(
        title="length test",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='length-test.html')


def test_materials():
    trace = go.Bar(
        x=['hand', 'macbook pro 15', '80p A5 notebook', 'porcelain cup', 'plastic bottle 500ml', 'plastic bottle 250ml',
           'iphone 7 plus', 'iphone 6'],
        y=[120, 92, 50, 40, 50, 40, 55, 40],
        name='Rest of world',
        marker=dict(
            color='rgb(55, 83, 109)'
        )
    )
    data = [trace]
    layout = go.Layout(
        title='Material test',
        xaxis=dict(
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='USD (millions)',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='material.html')


def plot_full():
    data = pd.read_csv('data/3-1.5m-length/3-0.01m-full.csv')
    temp_data = []
    for row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
        for column in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            index = row * 16 + column
            s = list(data[str(index)])
            new_signal = low_pass(s)
            # temp_data.append(new_signal[424]- new_signal[10])
            temp_data.append(s[5])

    z_data=[]
    for row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
        z_data.append(temp_data[row * 16:row * 16 + 15])

    trace = go.Heatmap(z=z_data,
                       x=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
                       y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                          17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
                       colorscale='Earth')   # Earth, Rainbow
    # ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
    #  'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
    #  'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis']
    data = [trace]
    plotly.offline.plot(data, filename='full screen3.html')

    # fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')
    # py.iplot(fig, filename='annotated_heatmap_text')

    # trace_data = []
    # trace = go.Scatter(
    #     x=np.arange(len(new_signal)),
    #     y=new_signal,
    #     mode='lines',
    #     name='19-0',
    #     marker=dict(
    #         color=get_color()
    #     )
    # )
    # trace_data.append(trace)
    #
    # layout = go.Layout(
    #     title='full screen',
    #     showlegend=True
    # )
    #
    # fig = go.Figure(data=trace_data, layout=layout)
    # plotly.offline.plot(fig, filename='full screen.html')


def main():
    #import_data('1', '1')
    #plot_data(import_data('1', '1'))
    #low_pass_filter(import_data('3', '3'))
    # filter_data()
    # 1, 3, 4, 10, 11, 13
    # compare_overlapping_touching('13')
    # compare_data('selected material')
    # compare_overlapping_screen()
    # length_test_on_width_material()
    # plot_full()
    test_materials()


main()
