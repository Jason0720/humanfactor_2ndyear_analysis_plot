import csv
import numpy as np
import matplotlib.pyplot as plt

################
# get data from csv
def get_data_from_csv(path):
    with open(path) as f:
        # read csv file
        reader = csv.reader(f)
        _ = next(reader)

        # data
        raw_data = []
        temp_data = []

        # get data from csv
        for idx, row in enumerate(reader):
            if not row[0] == '':
                temp_data.append(row)
            else:
                raw_data.append(temp_data.copy())
                temp_data.clear()

        print("get data from {}".format(path))
        print(raw_data)
        return raw_data

#######################
# plot drawing function
# draw annotate brackets using p-value
def draw_barplot_annotate_brackets(num1, num2, data, center, height, yerr=None, dh=0.03, barh=0.03, fs=None, maxasterix=None):
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
        # ** is p < 0.01
        # *** is p < 0.001
        # etc.
        text = ''
        p = 0.05
        if data < p:
            text += '*'

        p = 0.01
        while data < p:
            text += '*'
            p /= 10.0

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

    plt.plot(barx, bary, c='#9400d3')

    kwargs = dict(ha='center', va='bottom', weight='bold', color='#9400d3')
    if fs is not None:
        kwargs['fontsize'] = fs

    plt.text(*mid, text, **kwargs)

# draw bar value on bar
def draw_barplot_value_label(barplot):
    for bar in barplot:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, 0.3 * height, height, ha='center', va='bottom', fontweight='bold')

# get bar list
def get_bar_list(barplot):
    list = []
    for bar in barplot:
        list.append(bar)
    return list

#################
# draw scene plot
def draw_scene_plot(scene_plot_data, scene_p_value_data):
    # check data size
    scene_plot_data_len = len(scene_plot_data)
    scene_p_value_data_len = len(scene_p_value_data)
    if not scene_plot_data_len == scene_p_value_data_len:
        print("data size does not match.")
        return

    # retrieve
    for scene_idx, scene in enumerate(scene_plot_data):
        # get plot data
        average = []
        stdev = []
        x_material = []
        legend_name = []
        for in_data in scene:
            average.append(round(float(in_data[0]), 6))
            stdev.append(round(float(in_data[1])**0.5, 6))
            x_material.append(in_data[2])
            legend_name.append(in_data[3])
        x_pos = np.arange(len(x_material)).tolist()

        # create error bar plot
        plt.figure()
        barplot = plt.bar(x_pos, average, yerr=stdev, color=['#fa8072', '#90ee90', '#87ceeb', '#ffd700'], align='center', capsize=3)
        plt.xlabel('Scene indices', fontsize=12, fontweight='bold')
        plt.ylabel('Mean Opinion Score', fontsize=10, fontweight='bold')
        plt.ylim(0, 5)
        plt.xticks(x_pos, x_material, color='k')
        plt.yticks([i*0.5 for i in range(0, 11)])
        plt.grid(alpha=0.5)
        plt.legend(get_bar_list(barplot), legend_name, loc=1, prop={'size': 12})

        # insert p-value plot
        p_value_plot_height = 0.03
        for p_data_idx, p_data in enumerate(scene_p_value_data[scene_idx]):
            # custom value
            # height
            if p_data_idx == 0:
                if scene_idx == 0 :
                    p_value_plot_height = -0.2
                elif scene_idx == 3:
                    p_value_plot_height = -0.15
            else:
                if scene_idx == 3:
                    if p_data_idx == 1:
                        p_value_plot_height += 0.1
                    elif p_data_idx == 2:
                        p_value_plot_height += 0.3
                else:
                    p_value_plot_height += 0.15

            # auto value
            # width
            x_pos_scale = x_pos.copy()
            num1 = int(p_data[0])
            num2 = int(p_data[1])
            x_pos_scale[num1] += 0.1
            x_pos_scale[num2] -= 0.1

            # insert annotate brackets
            draw_barplot_annotate_brackets(num1, num2, float(p_data[2]), x_pos_scale, average, yerr=stdev, dh=p_value_plot_height, maxasterix=3)

        # insert barplot data label
        draw_barplot_value_label(barplot)

        # save figure
        plt.savefig("./figure/scene_plot_{}.png".format(scene_idx), dpi=300)
        plt.show()

###################
# draw session plot
def draw_session_plot(session_plot_data, session_p_value_data):
    # check data size
    session_plot_data_len = len(session_plot_data)
    session_p_value_data_len = len(session_p_value_data)
    if not session_plot_data_len == session_p_value_data_len:
        print("data size does not match.")
        return

    # retrieve
    y_label = ['$S_N$', '$S_O$', '$S_D$', '$S_T$']
    for session_idx, session in enumerate(session_plot_data):
        # get plot data
        average = []
        stdev = []
        x_material = ['Rest', 'Session1', 'Session 2', 'Session 3']
        for in_data in session:
            average.append(round(float(in_data[0]), 6))
            stdev.append(round(float(in_data[1]) ** 0.5, 6))
        x_pos = np.arange(len(x_material)).tolist()

        # create error bar plot
        plt.figure()
        barplot = plt.bar(x_pos, average, yerr=stdev, color=['#3cb371', '#ffd700', '#ffa500', '#ff0000'],
                          align='center', capsize=3)
        plt.ylabel(y_label[session_idx], fontsize=16, fontweight='bold')
        plt.ylim(0, 70)
        plt.xticks(x_pos, x_material, color='k')
        plt.yticks([i * 10 for i in range(0, 8)])
        plt.grid(alpha=0.5)

        # insert p-value plot
        p_value_plot_height = 0.03
        for p_data_idx, p_data in enumerate(session_p_value_data[session_idx]):
            # custom value
            # height
            if p_data_idx == 0:
                if session_idx == 2:
                    p_value_plot_height = -0.1
                else:
                    p_value_plot_height = 0.03
            else:
                if session_idx == 2:
                    p_value_plot_height += 0.06
                elif session_idx == 3:
                    p_value_plot_height += 0.07
                else:
                    p_value_plot_height += 0.1

            # auto value
            # width
            x_pos_scale = x_pos.copy()
            num1 = int(p_data[0])
            num2 = int(p_data[1])
            x_pos_scale[num1] += 0.1
            x_pos_scale[num2] -= 0.1

            # insert annotate brackets
            draw_barplot_annotate_brackets(num1, num2, float(p_data[2]), x_pos_scale, average, yerr=stdev,
                                           dh=p_value_plot_height, fs=14, maxasterix=3)

        # insert barplot data label
        draw_barplot_value_label(barplot)

        # save figure
        plt.savefig("./figure/session_plot_{}.png".format(session_idx), dpi=300)
        plt.show()

def draw_ssq_plot():
    # set data
    x_label = ['Rest', 'Session1', 'Session 2', 'Session 3']
    x_material = ['$S_N$', '$S_O$', '$S_D$', '$S_T$']

    x_pos = np.arange(len(x_label))
    under_30 = [[9.321, 21.694, 15.680, 18.571],
                [7.018, 13.505, 21.280, 15.132],
                [16.448, 22.043, 34.240, 26.524],
                [33.445, 34.502, 58.720, 45.912]]
    upper_30 = [[7.281, 16.756, 17.217, 15.747],
                [27.616, 26.131, 54.581, 38.384],
                [24.854, 26.131, 46.888, 35.235],
                [29.875, 24.934, 54.947, 38.778]]
    upper_error = [[1.694155289, 2.328995977, 3.051727685, 2.455390913],
                   [6.881550702, 5.444572, 11.21568042, 8.207618539],
                   [4.698759009, 4.285391819, 7.561152367, 5.723901607],
                   [5.552840516, 4.626641382, 9.550828326, 6.604742974]]
    under_error = [[1.665806139, 2.684244972, 3.801622064, 2.684373347],
                   [1.096934175, 1.980647987, 3.094156533, 2.067204269],
                   [2.677546155, 2.127234873, 3.881021203, 2.801211577],
                   [4.391940919, 3.541785169, 6.7758916, 5.051116455]]

    # loop
    for i in range(4):
        # create error bar plot
        plt.figure()
        under_30_barplot = plt.bar(x_pos - 0.15, under_30[i], yerr=under_error[i], color='#ffd700', align='center',
                                   capsize=3, tick_label=x_material, label='Under 30', width=0.3)
        upper_30_barplot = plt.bar(x_pos + 0.15, upper_30[i], yerr=upper_error[i], color='#808080', align='center',
                                   capsize=3, tick_label=x_material, label='Upper 30', width=0.3)
        plt.xlabel(x_label[i], fontsize=12, fontweight='bold')
        plt.ylabel('SSQ score', fontsize=14, fontweight='bold')
        plt.ylim(0, 80)
        plt.xticks(x_pos, x_material, color='k')
        plt.yticks([i * 20 for i in range(0, 5)])
        plt.grid(alpha=0.5)
        plt.legend(loc=1, prop={'size': 12})

        # insert p-value plot
        if i == 1:
            for j in range(4):
                p_value = "***"
                if j == 1:
                    p_value = "**"

                lx = j - 0.2
                rx = j + 0.2
                barx = [lx, lx, rx, rx]
                y = max(under_30[i][j] + under_error[i][j], upper_30[i][j] + upper_error[i][j]) + 2
                barh = 3
                bary = [y, y + barh, y + barh, y]
                mid = ((lx + rx) / 2, y + barh)
                plt.plot(barx, bary, c='#9400d3')

                kwargs = dict(ha='center', va='bottom', weight='bold', color='#9400d3', fontsize=14)

                plt.text(*mid, p_value, **kwargs)

        # save figure
        plt.savefig("./figure/ssq_plot_{}.png".format(i), dpi=300)
        plt.show()


# main
if __name__ == '__main__':
    # scene
    scene_plot_data = get_data_from_csv("scene_plot_data.csv")
    scene_p_value_data = get_data_from_csv("scene_p_value_data.csv")
    draw_scene_plot(scene_plot_data, scene_p_value_data)

    # session
    session_plot_data = get_data_from_csv("session_plot_data.csv")
    session_p_value_data = get_data_from_csv("session_p_value_data.csv")
    draw_session_plot(session_plot_data, session_p_value_data)

    # SSQ
    draw_ssq_plot()

