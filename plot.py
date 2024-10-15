Near-Optimal k-Clustering in the Sliding Window Modelimport csv
import matplotlib.pyplot as plt
import numpy as np
import pdb
import statistics as st
import sys

LINESTYLES = ['solid', 'dotted', 'dashed', 'dashdot', (5, (10, 3)), (0, (3, 5, 1, 5))]
PALETTE = ["#009292", "#924900", "#490092", "#6db6ff", "#ff6db6", "#24ff24"]

def main(datatype, fname, algs, xname, yname, **specs):
    algs = algs.split(',')
    is_box = yname in ["Distances", "alphas"]

    with open(fname, newline='') as file:
        reader = csv.DictReader(file)
        data = {}
        columns = {}
        avgs = {}
        stddevs = {}
        for alg in algs:
            data[alg] = {}
            columns[alg] = []
            avgs = []
            stddevs = []

        for row in reader:
            good_row = row["Algorithm"] in algs

            for spec in specs.keys():
                good_row = good_row and (row[spec] == specs[spec])

            if good_row:
                alg = row["Algorithm"]
                x = float(row[xname])

                if is_box:
                    y = ast.literal_eval(row[yname])
                    y.sort()
                    num_pairs = len(y)

                    if x in data[alg].keys():
                        data[alg][x] = [data[alg][x][i] + [y[i]] for i in range(num_pairs)]
                    else:
                        data[alg][x] = [[alpha] for alpha in y]
                else:
                    y = float(row[yname])

                    if x in data[alg].keys():
                        data[alg][x] += [y]
                    else:
                        data[alg][x] = [y]

        if not is_box:
            scatter(data, datatype, algs, xname, yname)
        else:
            boxplot(data, datatype, algs, xname, yname)

def scatter(data, datatype, algs, xname, yname):
    style_it = 0
    columns = list(data[algs[0]].keys())
    columns.sort()

    for alg in algs:
        val_lists = [data[alg][key] for key in columns]
        avgs = [st.mean(val_list) for val_list in val_lists]
        stddevs = [st.stdev(val_list) for val_list in val_lists]

        color = PALETTE[style_it]
        linestyle = LINESTYLES[style_it]
        style_it += 1
        fig = plt.plot(columns, avgs, marker='o', label=alg, color=color)

    plt.title(datatype + " " + yname)
    plt.xlabel(xname)
    plt.ylabel(yname)
    if len(algs) > 1:
        plt.legend()
    plt.subplots_adjust(bottom=.1, left=.15)
    outname = 'plots/' + datatype + '/scatter_' + datatype + '_' + xname + '_vs_' + yname + '.png'
    plt.savefig(outname)
    plt.close()


def boxplot(data, datatype, algs, xname, yname):
    columns = list(data[algs[0]].keys())
    columns.sort()
    positions = np.asarray([i*(len(algs)+1) for i in range(len(columns))])
    plots = []

    for i, alg in enumerate(algs):
        shifted_pos = [pos + 0.2*i for pos in positions]
        num_pairs = len(data[alg][list(data[alg].keys())[0]][0])
        val_lists = [data[alg][key] for key in columns]
        avgs = [[st.mean(alpha_list) for alpha_list in val_list] for val_list in val_lists]
        stddevs = [[st.stdev(alpha_list) for alpha_list in val_list] for val_list in val_lists]

        plot = plt.boxplot(avgs, positions=shifted_pos, widths=0.15)
        define_box_properties(plot, PALETTE[i], alg)

    plt.title(datatype + " " + yname + " Distributions")
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.xticks(positions, [int(col) for col in columns])
    if len(algs) > 1:
        plt.legend()
    plt.subplots_adjust(bottom=.1, left=.15)
    outname = 'plots/' + datatype + '/boxplot_' + datatype + "_" + xname + '_vs_' + yname + '.png'
    plt.savefig(outname)
    plt.close()


def define_box_properties(plot_name, color_code, label):
    for k, v in plot_name.items():
        plt.setp(plot_name.get(k), color=color_code)

    # use plot function to draw a small line to name the legend.
    plt.plot([], c=color_code, label=label)


if __name__=='__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], **dict(arg.split('=') for arg in sys.argv[6:]))
