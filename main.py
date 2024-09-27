import algorithm
import csv
import itertools
import generator
import matplotlib.pyplot as plt
import measures
import numpy as np
import pandas as pd
import ranking
import sys
import time
import xlrd

FULL_DATASETS = {
            "Sushi": {
                "file": "data/sushia.xlsx",
                "outpath": "results/sushia.csv",
                "groups": False,
            },
            "Movielens": {
                "file": "data/movielens.xlsx",
                "groupfile": "data/movielens_genres.xlsx",
                "outpath": "results/movielens.csv",
                "h": 4,
                "groups": True,
            },
            "Jester": {
                "file": "data/jester.xlsx",
                "outpath": "results/jester.csv",
                "groups": False,
            },
            "NFL": {
                "file": "data/nfl_players.xlsx",
                "groupfile": "data/nfl_divisions.xlsx",
                "outpath": "results/nfl.csv",
                "h": 25,
                "groups": True,
            },
        }

SHORT_DATASET = { "NFL": FULL_DATASETS["NFL"] }

SYN_OPTS = {
        "Mallows": {
            "nmax": 1000000,
            "kmax": 101,
            "nmin": 100000,
            "kmin": 11,
            "nskip": 100000,
            "kskip": 10,
            "thetas": [0.001, 0.01, 0.1, 0.5, 0.9],
            "generator": generator.generate_mallows,
            "outpath": "results/mallows.csv",
        },
        "UAR": {
            "nmax": 1000000,
            "kmax": 101,
            "nmin": 100000,
            "kmin": 11,
            "nskip": 100000,
            "kskip": 10,
            "thetas": [None],
            "generator": generator.generate_uar,
            "outpath": "results/uar.csv",
        },
}

def main(runtype, ntrials, **kwargs):
    opts = make_opts(runtype, kwargs)

    algs = { "Pivot": algorithm.pivot_alg, "Chakraborty et al.": algorithm.weak_fair_alg }

    if runtype == "synthetic":
        algs = { "Pivot": algs["Pivot"] }
        run_all_synthetic(opts, algs, ntrials)
    elif runtype == "real":
        run_all_real(opts, algs, ntrials)

def make_opts(runtype, kwargs):
    if runtype == "synthetic":
        opts = SYN_OPTS
    elif runtype == "real":
        opts = FULL_DATASETS
    elif runtype == "real_short":
        opts = SHORT_DATASET

    for kwargkey, kwargit in kwargs.items():
        kwargit = int(kwargit) if kwargit.isdigit() else kwargit

        for datakey in opts.keys():
            opts[datakey][kwargkey] = kwargit

    return opts

def run_all_synthetic(opts, algs, ntrials):
    for gentype in opts:
        run_synthetic(opts[gentype], algs, ntrials)

def run_synthetic(genopts, algs, ntrials):
    ns = list(range(genopts["nmin"], genopts["nmax"], genopts["nskip"]))
    ks = list(range(genopts["kmin"], genopts["kmax"], genopts["kskip"]))
    thetas = genopts["thetas"]

    columns = ["Algorithm", "n", "k", "Trial #", "Runtime", "Start Distances", "alphas", "Cost"]
    if thetas != [None]:
        columns.insert(3, "theta")
    init_csv(genopts["outpath"], columns)

    params = itertools.product(ns, ks, thetas)

    for param in params:
        n = param[0]
        k = param[1]
        theta = param[2]
        
        print("n", n, "k", k, "theta", theta)

        for i in range(ntrials):
            if theta != None:
                items, inputs = genopts["generator"](n, k, theta=theta)
            else:
                items, inputs = genopts["generator"](n, k)

            for alg_name in algs.keys():
                row = {
                        "Algorithm": alg_name,
                        "n": n,
                        "k": k,
                        "Trial #": i,
                }
                if theta != None:
                    row["theta"] = theta

                alg_func = algs[alg_name]

                start = time.time()
                pivots, output = alg_func(items, inputs)
                end = time.time()
                row["Runtime"] = end - start

                row["alphas"], row["Start Distances"] = measures.get_alphas(items, output, inputs)
                row["Cost"] = measures.kendall_tau_sum(items, output, inputs)

                add_csv_row(genopts["outpath"], columns, row)

def init_csv(fname, columns):
    with open(fname, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

def add_csv_row(fname, columns, rowdict):
    with open(fname, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow(rowdict)

def plot():
    fig, ax = plt.subplots()

    for position, column in enumerate(columns):
        ax.boxplot(data[position], positions=[position])

    ax.set_xticks(range(position+1))
    ax.set_xticklabels(columns)
    ax.set_xlim(xmin=-0.5)
    plt.xlabel(xlab)
    plt.ylabel('Pairwise Alpha Averages')
    plt.savefig('plots/mallows/boxplot_mallows_' + varied + '.png')
    plt.close()
    
    fig2 = plt.scatter(columns, times)
    plt.xlabel(xlab)
    plt.ylabel('Runtime')
    plt.savefig('plots/mallows/boxplot_mallows_' + varied + '_runtimes.png')
    plt.close()

def run_all_real(datasets, algs, ntrials):
    for dataset in datasets.keys():
        run_real(datasets[dataset], algs, ntrials)

def run_real(dataset, algs, ntrials):
    datafile = dataset["file"]
    rankings = pd.read_excel(datafile).to_numpy()
    
    if dataset["groups"]:
        groupfile = dataset["groupfile"]
        groups = pd.read_excel(groupfile).to_numpy()
        groups = groups.reshape((groups.shape[0],))
        h = dataset["h"]
    else:
        # TODO change when add algs
        algs = { "Pivot": algs["Pivot"] }
        
    print("Running on", datafile)

    if "kmax" not in dataset.keys():
        ks = [len(rankings)]
    else:
        ks = list(range(dataset["kmin"], dataset["kmax"], dataset["kskip"]))
    ks = [k if k%2 == 1 else k-1 for k in ks] 

    columns = ["Algorithm", "k", "Trial #", "Runtime", "Start Distances", "alphas", "Cost"]
    if dataset["groups"]:
        columns += ["Fairness"]
    init_csv(dataset["outpath"], columns)

    for k in ks:
        print("k", k)

        for i in range(ntrials):
            rand_inds = np.random.randint(len(rankings), size=k)
            rand_ranks = rankings[rand_inds]

            for alg_name in algs.keys():
                row = {
                        "Algorithm": alg_name,
                        "k": k,
                        "Trial #": i,
                }

                alg_func = algs[alg_name]

                items, inputs, n = generator.generate_from_data(rand_ranks, groups=groups)
                if dataset["groups"]:
                    group_names = np.unique(groups)

                start = time.time()
                if alg_name == "Pivot":
                    _, output = alg_func(items, inputs)
                else:
                    output = alg_func(items, inputs, h, group_names)

                end = time.time()
                row["Runtime"] = end - start

                row["alphas"], row["Start Distances"] = measures.get_alphas(items, output, inputs)
                row["Cost"] = measures.kendall_tau_sum(items, output, inputs)

                if dataset["groups"]:
                    row["Fairness"] = measures.fairness(output, group_names, dataset["h"])

                add_csv_row(dataset["outpath"], columns, row)
                
# Arg1 = runtype, Arg2 = ntrials
if __name__=='__main__':
    main(sys.argv[1], int(sys.argv[2]), **dict(arg.split('=') for arg in sys.argv[3:]))
