from generator import generate_uar
import random
from ranking import Ranking_Set, Ranking, Item

def pivot_alg(items, rankings, seed=None):
    pivots, rank_list = pivot_helper(items, rankings, seed)
    ranking = Ranking(rank_list)

    return pivots, ranking

def pivot_helper(items, rankings, seed):
    if len(items) == 0:
        return [], []
    if seed:
        random.seed(seed)

    pivot = random.choice(items)
    first = []
    last = []

    for item in items:
        vote = rankings.vote(pivot, item)

        if vote == 1:
            first += [item]
        elif vote == -1:
            last += [item]

    pvt_first, rec_first = pivot_helper(first, rankings, seed)
    pvt_last, rec_last = pivot_helper(last, rankings, seed)
    
    output = rec_first + [pivot] + rec_last
    pivots = [pivot] + pvt_first + pvt_last

    return pivots, output

def test():
    n = 7
    k = 3
    seed = 9

    items, rankings = generate_uar(n, k, seed)
    pivots, output = pivot_alg(items, rankings, seed-1)
    assert(str(output) == '[5, 2, 6, 4, 1, 3, 0]')
    #print(rankings)
    #print([str(pivot) for pivot in pivots])
    #print(output)

