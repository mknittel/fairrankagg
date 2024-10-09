from generator import generate_uar
import measures
import random
from ranking import Ranking_Set, Ranking, Item

def pivot_wrapper(items, rankings, seed=None, h=None, group_names=None):
    _, output = pivot_alg(items, rankings, seed=seed)
    return output

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


def closest_weak_fair(ranking, h, group_names, uppers, lowers):
    groups = {}
    for i in range(len(group_names)):
        name = group_names[i]
        up = uppers[i]
        low = lowers[i]

        groups[name] = {
                "up": up, # upper bound on number of top k
                "low": low, # lower bound on number of top k
                "items": [],
                "freq": 0, # frequency created ranking
        }

    fair_ranking = []
    remaining = []
    # Phase 1: fill minimums
    for item in ranking.rank:
        name = item.group
        group = groups[name]

        if group["freq"] < group['low']:
            fair_ranking += [item]
            group["freq"] += 1
        else:
            remaining += [item]

    tail = []
    # Phase 2: pad if fair
    for item in remaining:
        name = item.group
        group = groups[name]

        if group["freq"] <= group['up'] and len(fair_ranking) < h:
            fair_ranking += [item]
        else:
            tail += [item]

    if len(fair_ranking) >= h:
        return Ranking(fair_ranking + tail)
    else:
        print("ERROR no fair ranking")


def get_best(items, rankings):
    best = rankings.rankings[0]
    best_kt = float("inf")

    for ranking in rankings.rankings:
        this_kt = measures.kendall_tau_sum(items, ranking, rankings)

        if this_kt < best_kt :
            best = ranking
            best_kt = this_kt

    return best


def weak_fair_wrapper(h, group_names, uppers=None, lowers=None, fair_first=True, alg=get_best):
    return lambda items, rankings: weak_fair(items, rankings, h, group_names, uppers=uppers, lowers=lowers, fair_first=fair_first, alg=alg)


# uppers and lowers are None => run exact
def weak_fair(items, rankings, h, group_names, uppers=None, lowers=None, fair_first=True, alg=get_best):
    if uppers == None:
        assert(lowers == None)
        uppers = measures.get_freqs(items, group_names)
        lowers = uppers

    if fair_first:
        closest_fair = Ranking_Set([closest_weak_fair(ranking, h, group_names, uppers, lowers) for ranking in rankings.rankings])

        return alg(items, closest_fair)
    else:
        vanilla_soln = alg(items, rankings)

        return closest_weak_fair(vanilla_soln, h, group_names, uppers, lowers)


ALGS = {
        "Pivot": pivot_wrapper,
        "Pivot-Fair": weak_fair,
        "Best-Fair": weak_fair,
        "Fair-Pivot": weak_fair,
        "Fair-Best": weak_fair,
}


def test_group():
    n = 7
    k = 3
    seed = 100

    items, rankings = generate_uar(n, k, seed)
    fair = weak_fair_alg(items, rankings, 4, [0, 1], [2, 2], [2, 2])
    assert(str(fair) == '[5, 4, 3, 0, 1, 2, 6]')
    assert(measures.is_fair(fair, 4, [0, 1], [2, 2], [2, 2]))

def test():
    n = 7
    k = 3
    seed = 100

    items, rankings = generate_uar(n, k, seed)
    pivots, output = pivot_alg(items, rankings, seed=1)
    closest =  closest_weak_fair(rankings.rankings[1], 4, [0, 1], [2, 2], [2, 2])
    closest_s = [int(i.name) for i in closest]
    assert(str(output) == '[5, 4, 0, 3, 1, 2, 6]')
    assert(str(closest_s) == "[5, 1, 0, 6, 2, 3, 4]")
    #print(rankings)
    #print([str(pivot) for pivot in pivots])
    #print(output)

