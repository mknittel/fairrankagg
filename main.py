import algorithm
import generator
import matplotlib.pyplot as plt
import measures
import numpy as np
import pandas as pd
import ranking
import time
import xlrd


def main():
    maxn = 301
    maxk = 80
    ntrials = 10#100
    datasets = {
            "Sushi": {
                "file": "data/sushia.xlsx",
                "krange": [None], # Run once on all data
                "groups": None, # No groups
            },
            "Movielens": {
                "file": "data/movielens.xlsx",
                "krange": [None], # Run once on all data
                "groups": "data/movielens_genres.xlsx", # No groups
                "h": 4,
            },
            "Jester": {
                "file": "data/jester.xlsx",
                "krange": list(range(5, maxk, 10)),
                "groups": None, # No groups
            },
            "NFL": {
                "file": "data/nfl_players.xlsx",
                "krange": list(range(5, maxk, 10)),
                "groups": "data/nfl_divisions.xlsx",
                "h": 25,
            },
        }
    short_name = "NFL"
    short_dataset = { short_name: datasets[short_name] }

    run_on_all_data(short_dataset, ntrials)
    #run_on_all_data(datasets, ntrials) 
    #run_mallows(maxn, maxk, ntrials, quick=False)
    #run_uar(maxn, maxk, ntrials)

def run_uar(maxn, maxk, ntrials):
    ns = list(range(50, maxn, 50))
    ks = list(range(5, maxk, 10))

    n = [100]
    k = [5]

    run_uar_helper(ns, k, ntrials, "n")
    run_uar_helper(n, ks, ntrials, "k")

# Assume one of the lists is a singleton
def run_uar_helper(ns, ks, ntrials, varied):
    columns = None

    if varied == "n":
        columns = ns
        assert(len(ks) == 1)
        xlab = "Number of Items (n)"
    elif varied == "k":
        columns = ks
        assert(len(ns) == 1)
        xlab = "Number of Agents (k)"
    else:
        print("Error: one input list must be a singleton")

    print("Varying", varied)

    data = []

    for n in ns:
        for k in ks:
            print("n", n, "k", k)
            n_pairs = int(n*(n-1)/2)
            avgs = [0 for i in range(n_pairs)]

            for i in range(ntrials):
                items, inputs = generator.generate_uar(n, k)
                pivots, output = algorithm.pivot_alg(items, inputs)
                alphas = measures.get_alphas(items, output, inputs)
                alphas.sort()

                avgs = [avgs[j] + alphas[j]/ntrials for j in range(n_pairs)]

            data += [avgs]

    fig, ax = plt.subplots()

    for position, column in enumerate(columns):
        ax.boxplot(data[position], positions=[position])

    ax.set_xticks(range(position+1))
    ax.set_xticklabels(columns)
    ax.set_xlim(xmin=-0.5)
    plt.xlabel(xlab)
    plt.ylabel('Pairwise Alpha Averages')
    plt.savefig('plots/uar/boxplot_uar_' + varied + '_.png')

def run_mallows(maxn, maxk, ntrials, quick=False):
    if quick:
        ns = [25, 50]
        ks = [5, 15]
        thetas = [0.01, .1]
        ntrials = 10

        n = [50]
        k = [5]
        theta = [0.01]
    else:
        ns = list(range(50, maxn, 50))
        ks = list(range(5, maxk, 10))
        thetas = [0.001, 0.01, 0.1, 0.5, 0.9]

        n = [100]
        k = [5]
        theta = [0.01]

    run_mallows_helper(ns, k, theta, ntrials, "n")
    run_mallows_helper(n, ks, theta, ntrials, "k")
    run_mallows_helper(n, k, thetas, ntrials, "theta")

# Assume two of the lists are singletons
def run_mallows_helper(ns, ks, thetas, ntrials, varied):
    columns = None

    if varied == "theta":
        columns = thetas
        assert(len(ns) == 1 and len(ks) == 1)
        xlab = "Theta"
    elif varied == "n":
        columns = ns
        assert(len(thetas) == 1 and len(ks) == 1)
        xlab = "Number of Items (n)"
    elif varied == "k":
        columns = ks
        assert(len(ns) == 1 and len(thetas) == 1)
        xlab = "Number of Agents (k)"
    else:
        print("Error: two input lists must be singletons")

    print("Varying", varied)

    data = []
    times = []

    for n in ns:
        for k in ks:
            for theta in thetas:
                print("n", n, "k", k, "theta", theta)
                n_pairs = int(n*(n-1)/2)
                avgs = [0 for i in range(n_pairs)]
                avg_time = 0

                for i in range(ntrials):
                    items, inputs = generator.generate_mallows(n, k, theta=theta)
                    start = time.time()
                    pivots, output = algorithm.pivot_alg(items, inputs)
                    end = time.time()
                    runtime = end - start

                    alphas = measures.get_alphas(items, output, inputs)
                    alphas.sort()

                    avgs = [avgs[j] + alphas[j]/ntrials for j in range(n_pairs)]
                    avg_time += runtime / ntrials

                data += [avgs]
                times += [avg_time]

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


def run_on_all_data(datasets, ntrials):
    for dataset in datasets.keys():
        out_data = []
        out_data2 = []
        columns = []
        times = []
        times2 = []
        fairnesses = []
        fairnesses2 = []
        datafile = datasets[dataset]["file"]
        rankings = pd.read_excel(datafile).to_numpy()
        h = datasets[dataset]["h"]
        
        groupfile = datasets[dataset]["groups"]
        if groupfile != None:
            groups = pd.read_excel(groupfile).to_numpy()
            groups = groups.reshape((groups.shape[0],))
        else:
            groups = None
        print("Running on", datafile)

        for k in datasets[dataset]["krange"]:
            if k == None:
                k = len(rankings)
            if k%2 == 0:
                k -= 1

            rand_inds = np.random.randint(len(rankings), size=k)
            rand_ranks = rankings[rand_inds]

            columns += [k]
            avg_alphas, avg_time, avg_fairness, avg_alphas2, avg_time2, avg_fairness2 = run_on_data(rand_ranks, ntrials, h=h, groups=groups, k=k)

            out_data += [avg_alphas]
            times += [avg_time]
            fairnesses += [avg_fairness]
            out_data2 += [avg_alphas2]
            times2 += [avg_time2]
            fairnesses2 += [avg_fairness2]

        fig, ax = plt.subplots()

        for position, column in enumerate(columns):
            ax.boxplot(out_data[position], positions=[position])
            ax.boxplot(out_data2[position], positions=[position])

        ax.set_xticks(range(position+1))
        ax.set_xticklabels(columns)
        ax.set_xlim(xmin=-0.5)
        plt.title(dataset + " Alpha Distributions")
        plt.xlabel("Number of Rankings")
        plt.ylabel('Pairwise Alpha Averages')
        plt.savefig('plots/real/boxplot_' + dataset + '.png')
        plt.close()

        if groups is not None:
            fig2 = plt.plot(columns, times, label="Pivot")
            plt.plot(columns, times2, label="Greedy Fair")
            plt.title(dataset + " Runtimes")
            plt.xlabel("Number of Rankings")
            plt.ylabel('Runtime')
            plt.legend()
            plt.savefig('plots/real/boxplot_' + dataset + '_runtimes.png')
            plt.close()

            fig3 = plt.plot(columns, fairnesses, label="Pivot")
            plt.plot(columns, fairnesses2, label="Greedy Fair")
            plt.title(dataset + " Fairness Deviation")
            plt.xlabel("Number of Rankings")
            plt.ylabel('Fairness Deviation')
            plt.legend()
            plt.savefig('plots/real/boxplot_' + dataset + '_fairness.png')
            plt.close()
   

def run_on_data(rank_data, ntrials, h=None, groups=None, k=None):
    items, inputs, n = generator.generate_from_data(rank_data, groups=groups)
    n_pairs = int(n*(n-1)/2)
    avgs = [0 for i in range(n_pairs)]
    avg_time = 0
    print("n", n, "k", k)

    # Only used for group fairness
    avg_fairness = 0
    avgs2 = [0 for i in range(n_pairs)]
    avg_time2 = 0
    avg_fairness2 = 0

    for i in range(ntrials):
        if i%10 == 9:
            print("trial", i)

        print("Running")
        start = time.time()
        pivots, output = algorithm.pivot_alg(items, inputs)
        end = time.time()
        runtime = end - start
        print(runtime)

        alphas = measures.get_alphas(items, output, inputs)
        alphas.sort()

        deltas = [alphas[j]/ntrials for j in range(n_pairs)]
        avgs = [avgs[j] + deltas[j] for j in range(n_pairs)]
        avg_time += float(runtime) / ntrials

        if groups is not None:
            group_names = np.unique(groups)
            avg_fairness += float(measures.fairness(output, group_names, h)) / ntrials

            start2 = time.time()
            output2 = algorithm.weak_fair_exact(items, inputs, h, group_names)
            end2 = time.time()
            runtime2 = end2 - start2

            alphas2 = measures.get_alphas(items, output2, inputs)
            alphas2.sort()

            deltas2 = [alphas2[j]/ntrials for j in range(n_pairs)]
            avgs2 = [avgs2[j] + deltas2[j] for j in range(n_pairs)]
            avg_time2 += float(runtime2) / ntrials
            avg_fairness2 += float(measures.fairness(output2, group_names, h)) / ntrials

    return avgs, avg_time, avg_fairness, avgs2, avg_time2, avg_fairness2

def read_data(datafile, k=None):
    rankings = pd.read_excel(datafile, nrows=k).to_numpy()
   
    if not len(rankings)%2:
        print("Truncating to odd k")
        rankings = rankings[:-1,:]

    return rankings

if __name__ == "__main__":
    main()
