import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from ggplot import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import time
import os



def convert_time(origin_time):
    date_time, millisecond = origin_time.split('.')
    return time.mktime(time.strptime(date_time, '%Y/%m/%d-%H:%M:%S')) + float(millisecond) / 1000

# (10, 1): 304   32(i- 1）+ 16j  (i from 0, j from 1)
# total: 577
def count_index(num):
    index = [49, 81, 113, 145, 177, 209, 225, 241, 257, 273, 305, 337, 369, 401, 433]
    return index[num]


# for 0<=i<32: point_value[i] = raw_diff_data[i*col_num]
# for 32<=i<47: point_value[i] = raw_diff_data[(row_num-1)*col_num+i-row_num+1], where row_num=32 and col_num=16
def count_index2(num):
    col_num = 16
    return col_num * num + 1


def dict2list(dic:dict):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


def convert_file(origin_file, new_file, points):
    file = open(origin_file)
    with open(new_file, "a") as f:
        data = {}
        while 1:
            lines = file.readlines(10000)
            if not lines:
                break
            for line in lines:
                content = line.split(' ')
                time = convert_time(content[0])
                value = []
                for point in points:
                    value.append(content[count_index2(point)])
                data[time] = value

        f.write('time,value\n')
        for item in sorted(dict2list(data), key=lambda x: x[0], reverse=False):
            f.write(str(item[0]))
            for point in item[1]:
                f.write(',' + point)
            f.write('\n')

    f.close()



def convert_full_screen(origin_file, new_file):
    file = open(origin_file)
    with open(new_file, "w") as f:
        data = {}
        while 1:
            lines = file.readlines(10000)
            if not lines:
                break
            for line in lines:
                content = line.split(' ')
                time = convert_time(content[0])
                data[time] = content[1:-65]

        title_string = 'time'
        for row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
            for column in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                index = row * 16 + column
                title_string += ',' + str(index)
        title_string += '\n'
        f.write(title_string)
        for item in sorted(dict2list(data), key=lambda x: x[0], reverse=False):
            f.write(str(item[0]))
            for point in item[1]:
                f.write(',' + point)
            f.write('\n')

    f.close()


def draw_chart():
    with open('data/0.5-1.5m-1.5m-10.txt', "r") as f:
        x = []
        y = []
        while 1:
            lines = f.readlines(10000)
            if not lines:
                break
            for line in lines:
                time, volume = line.split(' ')
                x.append(float(time))
                y.append(int(volume))

    f.close()

    plt.figure()
    plt.plot(x, y)
    # plt.xticks([])
    plt.yticks(np.arange(min(y), max(y) + 1, 10.0))
    plt.savefig("easyplot.png")
    # plt.show()


def count_item():
    with open("data/overlapping/3,3.txt", "r") as f:
        while 1:
            lines = f.readlines(10000)
            if not lines:
                break
            for line in lines:
                print(len(line.split(' ')))


def main():
    # '0.01m', '0.02m', '0.05m', '0.1m', '0.25m',
    # pos = ['0.01m', '0.02m', '0.05m', '0.1m', '0.25m', '0.5m', '0.75m', '1m', '1.25m', '1.5m']
    # for item in pos:
    #     file_name = 'data/5-' + item + '.txt'
    #     new = 'data/5-' + item + '-6,7,8,9.txt'
    #     convert_file(file_name, new, [6, 7, 8, 9])
    # draw_chart()

    path = "data/ink-0.5-1m-length"
    files = os.listdir(path)
    for file in files:
        if file[-3:] == 'txt':
            # num = file[file.find('-') + 1:-4]
            convert_file(path + '/' + file, path + '/' + file[:-4] + '.csv', [22])

    # full screen
    # convert_full_screen("data/3-1.5m-length/3-0.01m.txt", "data/3-1.5m-length/3-0.01m-full.csv")

    # path = "data/overlapping"
    # files = os.listdir(path)
    # for file in files:
    #     if file[-3:] == 'txt':
    #         convert_file(path + '/' + file, path + '/' + file[:-4] + '-1,3,4,10,11,13.txt', [1, 3, 4, 10, 11, 13])

    # count_item()


main()