
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


def generate_uar(n, k, seed=None, p=0.5):
    if seed:
        np.random.seed(seed)

    groups = [np.random.binomial(1, p) for i in range(n)]
    items = [Item(i, group=groups[i]) for i in range(n)]

    return items, Ranking_Set([Ranking(np.random.permutation(items).tolist()) for i in range(k)])

def generate_mallows(n, k, theta=0.25):
    items = [Item(i) for i in range(n)]

    ranking_lists = mk.sample(m=k,n=n, theta=theta)
    list_of_rankings = [Ranking([items[name] for name in ranking]) for ranking in ranking_lists]
    ranking_set = Ranking_Set(list_of_rankings)

    return items, ranking_set
    
def generate_adversarial_mallows(n, k, theta=0.25):
    items = [Item(i) for i in range(n)]
    upsamp = 1
    assert(n > k)
    k2 = int((k-1)/(2*upsamp)) # Size of S and Z, we upsample each perm
    pdb.set_trace()

    # x, y S, Z, D is order
    pi_1 = [items[i] for i in range(n)]
    
    pi_2 = pi_1[2:]
    pi_2.insert(2*k2, items[0])
    pi_2.insert(2*k2+1, items[1])
    
    sources = (k2*[Ranking(pi_1)]) + [Ranking(pi_2)]

    list_of_rankings = mallows_from_reference(pi_1, upsamp * k2, n, theta)
    list_of_rankings += mallows_from_reference(pi_2, upsamp, n, theta)

    for i in range(k2):
        pi_i = [item for item in pi_2]
        item = pi_i.pop(i)
        pi_i.insert(2*k2, item)
        list_of_rankings += [Ranking(pi_i)]

    ranking_set = Ranking_Set(list_of_rankings)
    pdb.set_trace()

    return items, ranking_set


def mallows_from_reference(ranking, m, n, theta):
    adjusts = mk.sample(m=m, n=n, theta=theta)

    return [Ranking([ranking[i] for i in adjust]) for adjust in adjusts]


def generate_from_data(ranking_lists, groups=None):
    n = len(ranking_lists[0])

    if groups is not None:
        items = [Item(i, groups[i]) for i in range(n)]
    else:
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
    


