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
    maxn = 51#301
    maxk = 51#56
    ntrials = 1000
    datasets = {
            "jester": "data/jester-data-1.xls",
        }

    #run_on_all_data(datasets, ntrials, k=maxk, n=maxn) 
    run_mallows(maxn, maxk, ntrials, quick=True)
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
    import pdb
    #pdb.set_trace()

    for position, column in enumerate(columns):
        ax.boxplot(data[position], positions=[position])

    ax.set_xticks(range(position+1))
    ax.set_xticklabels(columns)
    ax.set_xlim(xmin=-0.5)
    plt.xlabel(xlab)
    plt.ylabel('Pairwise Alpha Averages')
    plt.savefig('plots/mallows/boxplot_mallows_' + varied + '.png')
    plt.close()
    
    fig2 = plt.plot(times, columns)
    plt.xlabel(xlab)
    plt.ylabel('Runtime')
    plt.savefig('plots/mallows/boxplot_mallows_' + varied + '_runtimes.png')
    plt.close()


def run_on_all_data(datasets, ntrials, k=0, n=0):
    out_data = []
    columns = []

    for dataset in datasets.keys():
        columns += [dataset]
        
        datafile = datasets[dataset]
        avg_alphas, _ = run_on_data(datafile, ntrials, k=k, n=n)
        out_data += [avg_alphas]

    fig, ax = plt.subplots()

    for position, column in enumerate(columns):
        ax.boxplot(out_data[position], positions=[position])

    ax.set_xticks(range(position+1))
    ax.set_xticklabels(columns)
    ax.set_xlim(xmin=-0.5)
    plt.xlabel("Dataset")
    plt.ylabel('Pairwise Alpha Averages')
    plt.savefig('plots/real/boxplot_real.png')


def run_on_data(datafile, ntrials, k=0, n=0):
    rank_data = read_data(datafile, k=k, n=n)
    items, inputs, n = generator.generate_from_data(rank_data)
    n_pairs = int(n*(n-1)/2)
    avgs = [0 for i in range(n_pairs)]
    avg_time = 0

    for i in range(ntrials):
        start = time.time()
        pivots, output = algorithm.pivot_alg(items, inputs)
        end = time.time()
        runtime = end - start
        print(runtime)

        alphas = measures.get_alphas(items, output, inputs)
        alphas.sort()

        avgs = [avgs[j] + alphas[j]/ntrials for j in range(n_pairs)]
        avg_time += float(runtime) / ntrials

    return avgs, avg_time

def read_data(datafile, k=0, n=0):
    scores = pd.read_excel(datafile).to_numpy()
    print(scores.shape)
    
    if n > 0 and n < len(scores[0]):
        scores = scores[:,:n]
    if k > 0 and k < len(scores):
        scores = scores[:k,:]
    if not len(scores)%2:
        print("Truncating odd k")
        scores = scores[:-1,:]

    rankings = [scores_to_ranking(row) for row in scores]

    return rankings

def scores_to_ranking(row):
    return np.flip(np.argsort(row))

if __name__ == "__main__":
    main()
