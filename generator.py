
import mallows_kendall as mk
import numpy as np
from ranking import Ranking, Ranking_Set, Item
import pdb

def generate_adversarial(n, k):
    items = [Item(i) for i in range(n)]
    kk = int((k - 1) / 2)
    dums = n - 2 * k - 2

    x = items[0]
    y = items[1]
    S = items[2:kk+2]
    Z = items[kk+2:2*kk+2]
    D = items[2*kk+2:n]

    ranking_lists = []
    
    pi1 = S + Z + [x] + [y] + D
    ranking_lists += [pi1]

    for i in range(kk):
        Si = S[:i] + S[i+1:]
        pii2 = Si + Z + [x] + [S[i]] + [y] + D
        ranking_lists += [pii2]

    for i in range(kk):
        ranking_lists += [[x] + [y] + S + Z + D]

    rank_objects = [Ranking(l) for l in ranking_lists]
    ranking_set = Ranking_Set(rank_objects)

    return items, ranking_set


def generate_uar(n, k, seed=None):
    items = [Item(i) for i in range(n)]
    if seed:
        np.random.seed(seed)

    return items, Ranking_Set([Ranking(np.random.permutation(items).tolist()) for i in range(k)])

def generate_mallows(n, k, theta=0.25):
    items = [Item(i) for i in range(n)]

    ranking_lists = mk.sample(m=k,n=n, theta=theta)
    list_of_rankings = [Ranking([items[name] for name in ranking]) for ranking in ranking_lists]
    ranking_set = Ranking_Set(list_of_rankings)

    return items, ranking_set
    

def generate_from_data(ranking_lists):
    n = len(ranking_lists[0])
    items = [Item(i) for i in range(n)]

    list_of_rankings = [Ranking([items[name] for name in ranking]) for ranking in ranking_lists]
    ranking_set = Ranking_Set(list_of_rankings)

    return items, ranking_set, n


def avg_rank(item, rankings):
    rks = rankings.get_rankings()
    k = len(rks)
    average = 0

    for rk in rks:
        rank_list = rk.get_ranking()
        average += (1.0 * rank_list.index(item)) / k

    return average


def test_uar():
    n = 21
    k = 1000
    err = 1

    items, rankings = generate_uar(n, k)

    for item in items:
        average = avg_rank(items[0], rankings)
        assert(average >= (n-1.0-err)/2)
        assert(average <= (n-1.0+err)/2)
    


