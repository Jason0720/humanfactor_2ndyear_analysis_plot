import csv
import numpy as np
import matplotlib.pyplot as plt

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

def draw_chart(graph_data, p_value_data):
    # check data size
    graph_data_len = len(graph_data)
    p_value_data_len = len(p_value_data)
    if not graph_data_len == p_value_data_len:
        print("data size does not match.")
        return

    # retrieve
    for chart_idx, chart in enumerate(graph_data):
        # get data
        material = []
        average = []
        variance = []
        for in_data_idx, in_data in enumerate(chart):
            material.append(in_data[2])
            average.append(in_data[0])
            variance.append(in_data[1])
        x_len = np.arange(len(material))

        # build plot
        fig, ax = plt.subplots()
        ax.bar(x_len, average, yerr=variance, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Scene indices')
        ax.set_ylabel('Mean Opinion Score')
        ax.set_xticks(x_len)
        ax.set_xticklabels(material)
        ax.set_title('chart_{}'.format(chart_idx))
        ax.yaxis.grid(True)

        # save figure and show
        plt.tight_layout()
        plt.savefig('chart_{}.png'.format(chart_idx))
        plt.show()


# main
if __name__ == '__main__':
    graph_data = get_graph_data()
    p_value_data = get_p_value_data()
    draw_chart(graph_data, p_value_data)
