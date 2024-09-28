import csv
import matplotlib.pyplot as plt
import pdb
import statistics as st
import sys

def main(datatype, fname, algs, xname, yname, boxplot, **specs):
    algs = algs.split(',')

    if datatype in ["Mallows", "UAR"]:
        plot_synthetic(datatype, fname, algs, xname, yname, boxplot, specs)
    elif datatype in ["Sushi", "Movielens", "Jester", "NFL"]:
        plot_real(datatype, fname, algs, xname, yname, boxplot, specs)

def plot_synthetic(datatype, fname, algs, xname, yname, boxplot, specs):
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
            good_row = True

            for spec in specs.keys():
                good_row = good_row and (row[spec] == specs[spec])

            if good_row:
                alg = row["Algorithm"]
                x = float(row[xname])
                y = float(row[yname])

                if x in data[alg].keys():
                    data[alg][x] += [y]
                else:
                    data[alg][x] = [y]

        palette = ["#009292", "#924900", "#490092", "#6db6ff", "#ff6db6"]
        col_it = 0

        for alg in algs:
            columns = list(data[alg].keys())
            columns.sort()
            val_lists = [data[alg][key] for key in columns]
            avgs = [st.mean(val_list) for val_list in val_lists]
            stddevs = [st.stdev(val_list) for val_list in val_lists]

            color = palette[col_it]
            col_it += 1
            fig = plt.plot(columns, avgs, label=alg, color=color)

        plt.title(datatype + " " + yname)
        plt.xlabel(xname)
        plt.ylabel(yname)
        if len(algs) > 1:
            plt.legend()
        plt.subplots_adjust(bottom=.1, left=.15)
        outname = 'plots/synthetic/' + datatype + '_' + xname + '_vs_' + yname + '.png'
        plt.savefig(outname)
        plt.close()

def plot_real(datatype, fname, algs, xname, yname, boxplot, specs):
    pass

if __name__=='__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]=="True", **dict(arg.split('=') for arg in sys.argv[7:]))
