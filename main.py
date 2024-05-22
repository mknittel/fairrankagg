import algorithm
import generator
import matplotlib.pyplot as plt
import measures
import numpy as np
import pandas as pd
import ranking


def main():
    maxn = 301
    maxk = 56
    ntrials = 1000

    run_mallows(maxn, maxk, ntrials)
    run_uar(maxn, maxk, ntrials)

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
    plt.savefig('boxplot_uar_' + varied + '_.png')

def run_mallows(maxn, maxk, ntrials):
    quick = False

    if quick:
        ns = [50]
        ks = [5]
        thetas = [0.01]
        ntrials = 10

        n = [50]
        k = [5]
        theta = [0.01]
    else:
        ns = list(range(50, maxn, 50))
        ks = list(range(5, maxk, 10))
        thetas = [0.001, 0.01, 0.1]

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

    for n in ns:
        for k in ks:
            for theta in thetas:
                print("n", n, "k", k, "theta", theta)
                n_pairs = int(n*(n-1)/2)
                avgs = [0 for i in range(n_pairs)]

                for i in range(ntrials):
                    items, inputs = generator.generate_mallows(n, k, theta=theta)
                    pivots, output = algorithm.pivot_alg(items, inputs)
                    alphas = measures.get_alphas(items, output, inputs)
                    alphas.sort()
                    #import pdb
                    #pdb.set_trace()

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
    plt.savefig('boxplot_mallows_' + varied + '_.png')

def read_jester():
   df = pd.read_excel("jester-data-1.xls") 
   import pdb
   pdb.set_trace()


if __name__ == "__main__":
    main()
