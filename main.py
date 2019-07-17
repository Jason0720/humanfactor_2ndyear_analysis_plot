import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# get graph data
def get_graph_data():
    graph_data_path = "data_graph.csv"
    with open(graph_data_path) as f:
        # read csv file
        reader = csv.reader(f)
        _ = next(reader)

        # data
        graph_data = []
        temp_data = []

        # get data from csv
        for idx, row in enumerate(reader):
            if not row[0] == '':
                temp_data.append(row)
            else:
                graph_data.append(temp_data.copy())
                temp_data.clear()

        print("graph data: {}".format(graph_data))
        return graph_data

def get_p_value_data():
    p_value_data_path = "data_p_value.csv"
    with open(p_value_data_path) as f:
        # read csv file
        reader = csv.reader(f)
        _ = next(reader)

        # data
        p_value_data = []
        temp_data = []

        # get data from csv
        for idx, row in enumerate(reader):
            if not row[0] == '':
                temp_data.append(row)
            else:
                p_value_data.append(temp_data.copy())
                temp_data.clear()

        print("p-value data: {}".format(p_value_data))
        return p_value_data

def barplot_annotate_brackets(num1, num2, data, center, height, yerr=None, dh=.03, barh=.03, fs=None, maxasterix=None):
    """
    Annotate barplot with p-values.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    if type(data) is str:
        text = data
    else:
        # * is p < 0.05
        # ** is p < 0.005
        # *** is p < 0.0005
        # etc.
        text = ''
        p = .05

        while data < p:
            text += '*'
            p /= 10.

            if maxasterix and len(text) == maxasterix:
                break

        if len(text) == 0:
            text = 'n. s.'

    lx, ly = center[num1], height[num1]
    rx, ry = center[num2], height[num2]

    if yerr:
        ly += yerr[num1]
        ry += yerr[num2]

    ax_y0, ax_y1 = plt.gca().get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= (ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, y+barh)

    plt.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom', weight='bold')
    if fs is not None:
        kwargs['fontsize'] = fs

    plt.text(*mid, text, **kwargs)

def barplot_label(barplot):
    for bar in barplot:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, 0.5 * height, height, ha='center', va='bottom', fontweight='bold')

def get_bar_list(barplot):
    list = []
    for bar in barplot:
        list.append(bar)
    return list

def draw_chart(graph_data, p_value_data):
    # check data size
    graph_data_len = len(graph_data)
    p_value_data_len = len(p_value_data)
    if not graph_data_len == p_value_data_len:
        print("data size does not match.")
        return

    # retrieve
    for chart_idx, chart in enumerate(graph_data):
        # get graph data
        average = []
        variance = []
        material = []
        legend_name = []
        for in_data in chart:
            average.append(round(float(in_data[0]), 6))
            variance.append(round(float(in_data[1])/2.0, 6))
            material.append(in_data[2])
            legend_name.append(in_data[3])
        x_pos = np.arange(len(material))

        # create error bar plot
        plt.figure()
        barplot = plt.bar(x_pos, average, yerr=variance, color=['#fa8072', '#90ee90', '#87ceeb', '#ffd700'], align='center', capsize=5)
        plt.xlabel('Scene indices', fontsize=12, fontweight='bold')
        plt.ylabel('Mean Opinion Score', fontsize=10, fontweight='bold')
        plt.ylim(0, 5)
        plt.xticks(x_pos, material, color='k')
        plt.yticks([i*0.5 for i in range(0, 11)])
        plt.grid(alpha=0.5)
        plt.legend(get_bar_list(barplot), legend_name, loc=1, prop={'size': 12})

        # insert p-value graph
        for p_data_idx, p_data in enumerate(p_value_data[chart_idx]):
            height = .03
            if not p_data_idx == 0:
                height = p_data_idx * .1
            barplot_annotate_brackets(int(p_data[0]), int(p_data[1]), float(p_data[2]), x_pos, average, yerr=variance, dh=height, maxasterix=3)

        # insert barplot data label
        barplot_label(barplot)

        # save figure
        plt.savefig("plot_{}.png".format(chart_idx), dpi=300)
        plt.show()


# main
if __name__ == '__main__':
    graph_data = get_graph_data()
    p_value_data = get_p_value_data()
    draw_chart(graph_data, p_value_data)
