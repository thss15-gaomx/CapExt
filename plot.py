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

def average_num(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)


def get_list_average():
    data = pd.read_csv('data/P20/1-1.5m-length/1-1m-10.csv')
    s = list(data['value'])
    print(s[100:150])
    print(average_num(s[100:150]))
    print(np.std(s, ddof=1))


def still_length_test_on_material_p20():
    length = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1]

    copper = [0.8, 1.1, 0.32, 696.56, 810.52, 922.82, 933.56, 935.76]
    ito = [0.32, 0.44, 0.98, 586.20, 781.36, 904.08, 949.14, 965.36]
    ink = [0.24, 0.44, 0.02, 603.86, 780.74, 857.82, 867.66, 880.86]

    trace_copper = go.Scatter(
        x=length,
        y=copper,
        mode='lines',
        name='copper',
        line=dict(
            color='rgb(205, 12, 24)',
            width=2)
    )

    trace_ito = go.Scatter(
        x=length,
        y=ito,
        mode='lines',
        name='ito',
        line=dict(
            color='rgb(0,100,80)',
            width=2)
    )

    trace_ink = go.Scatter(
        x=length,
        y=ink,
        mode='lines',
        name='ink',
        line=dict(
            color='rgb(22, 96, 167)',
            width=2)
    )

    trace_data = [trace_copper, trace_ito, trace_ink]

    layout = go.Layout(
        title="P20 Initial Data",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='initial-test-p20.html')


def low_pass(data):
    fc = 1
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

    path = "data/P20/1-1.5m-length"
    files = os.listdir(path)
    for file in files:
        if file[-3:] == 'csv':
            data = pd.read_csv(path + '/' + file)
            s = list(data['value'])
            # new_signal = low_pass(s)
            new_signal = s
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
            # s = list(data['down'])
            # new_signal = low_pass(s)
            # trace = go.Scatter(
            #     x=np.arange(len(new_signal)),
            #     y=new_signal,
            #     mode='lines',
            #     name=file[:-3] + " down",
            #     marker=dict(
            #         color=get_color()
            #     )
            # )
            # trace_data.append(trace)
            # s = list(data['up'])
            # new_signal = low_pass(s)
            # trace = go.Scatter(
            #     x=np.arange(len(new_signal)),
            #     y=new_signal,
            #     mode='lines',
            #     name=file[:-3] + "up",
            #     marker=dict(
            #         color=get_color()
            #     )
            # )
            # trace_data.append(trace)

    layout = go.Layout(
        title="copper-1-length",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='copper-1-length.html')


def compare_overlapping_screen():
    trace_data = []

    data = pd.read_csv("data/p20/overlapping-1-3*3-1m-touch/0-1m.csv")
    points = ['13', '15', '17', '19', '21', '23']
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
        title='3*3-0-1m-touch',
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='3-3-0-touch.html')


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


def length_test_on_width_material_p20():
    length = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1]

    copper_half = [625, 560, 467, 215, 90, 45, 30, 20]
    copper_1 = [880, 685, 425, 240, 110, 70, 44, 32]
    copper_2 = [1020, 830, 510, 370, 180, 110, 60, 47]

    ink_half = [645, 510, 370, 343, 97, 53, 45, 30]
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

    trace_ink_half = go.Scatter(
        x=length,
        y=ink_half,
        mode='lines',
        name='ink-0.5',
        line=dict(
            color='rgb(22, 96, 167)',
            width=2,
            dash='dash')
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

    trace_data = [trace_copper_half, trace_copper_1, trace_copper_2, trace_ink_half, trace_ink_1, trace_ink_2, trace_ito_half, trace_ito_1, trace_ito_2]

    layout = go.Layout(
        title="P20 Length Test",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='length-test.html')


def length_test_on_width_material_p10():
    length = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3]

    copper_half = [1160, 961, 732, 506, 274, 125, 85, 61, 52, 29, 13, 11]
    copper_1 = [1338, 1075, 787, 547, 251, 152, 114, 96, 76, 48, 42, 38]
    copper_2 = [2016, 1828, 1580, 1150, 384, 212, 199, 143, 132, 86, 71, 70]

    ito_half = [1160, 756, 569, 409, 154, 83, 59, 54, 22, 13, 11, 9]
    ito_1 = [1284, 1105, 892, 619, 288, 171, 114, 102, 52, 47, 27, 20]
    ito_2 = [1444, 1273, 802, 536, 322, 172, 122, 108, 63, 38, 35, 11]

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

    trace_data = [trace_copper_half, trace_copper_1, trace_copper_2, trace_ito_half, trace_ito_1, trace_ito_2]

    layout = go.Layout(
        title="P10 Length Test",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='length-test-p10.html')


def overlapping_length_test_p20():
    length = [0.25, 0.5, 0.75, 1]

    copper_up = [155, 85, 54, 43]
    copper_down = [165, 68, 55, 40]

    trace_up = go.Scatter(
        x=length,
        y=copper_up,
        mode='lines',
        name='up',
        line=dict(
            color='rgb(205, 12, 24)',
            width=2)
    )

    trace_down = go.Scatter(
        x=length,
        y=copper_down,
        mode='lines',
        name='down',
        line=dict(
            color='rgb(0,100,80)',
            width=2)
    )

    trace_data = [trace_up, trace_down]

    layout = go.Layout(
        title="P20 Overlapping Length Test",
        showlegend=True
    )

    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename='overlapping-length-test-p20.html')


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
            title='diff data',
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
    data = pd.read_csv('data/p20/overlapping-length-test/1m-fullscreen.csv')
    temp_data = []
    for row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
        for column in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            index = row * 16 + column
            s = list(data[str(index)])
            new_signal = low_pass(s)
            temp_data.append(new_signal[117]- new_signal[96])
            # temp_data.append(s[5])

    z_data=[]
    for row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
        z_data.append(temp_data[row * 16:row * 16 + 15])

    trace = go.Heatmap(z=z_data,
                       x=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
                       y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                          17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
                       colorscale='Viridis')   # Earth, Rainbow
    # ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
    #  'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
    #  'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis']
    data = [trace]
    plotly.offline.plot(data, filename='full screen-1m.html')

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
    # compare_data('P20/overlapping-length-test')
    # compare_overlapping_screen()
    # length_test_on_width_material_p20()
    # length_test_on_width_material_p10()
    # plot_full()
    # test_materials()
    # overlapping_length_test_p20()
    # get_list_average()
    still_length_test_on_material_p20()


main()
