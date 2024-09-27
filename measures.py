from itertools import combinations
from ranking import Ranking, Ranking_Set, Item

def kendall_tau(items, r1, r2):
    cost = 0

    item_pairs = list(combinations(items, 2))

    for pair in item_pairs:
        item1 = pair[0]
        item2 = pair[1]

        compare1 = r1.compare(item1, item2)
        compare2 = r2.compare(item1, item2)

        if compare1 != compare2:
            cost += 1

    return cost

def kendall_tau_sum(items, reference, rankings):
    cost = 0

    for ranking in rankings.rankings:
        cost += kendall_tau(items, reference, ranking)

    return cost

def get_alphas(items, output, rankings):
    alphas = []
    max_dists = [] # Debugging
    out_dists = [] # Debugging

    item_pairs = list(combinations(items, 2))

    for pair in item_pairs:
        item1 = pair[0]
        item2 = pair[1]

        max_dist = rankings.get_max_dist(item1, item2)
        out_dist = output.get_dist(item1, item2)

        alphas += [(1.0 * out_dist) / max_dist]
        max_dists += [max_dist]
        out_dists += [out_dist]

    return alphas, max_dists

def is_fair(ranking, h, group_names, uppers, lowers):
    groups = {}

    for i in range(len(group_names)):
        name = group_names[i]
        up = uppers[i]
        low = lowers[i]

        groups[name] = {
                "up": up,
                "low": low,
                "freq": 0,
        }

    for item in ranking.rank[:h]:
        groups[item.group]["freq"] += 1

    for name in group_names:
        freq = groups[name]["freq"]
        up = groups[name]["up"]
        low = groups[name]["low"]

        if freq > up or freq < low:
            return False
    return True

def get_freqs(ranking, group_names, h=None):
    if h == None:
        h = len(ranking)

    groups = {}

    for i in range(len(group_names)):
        name = group_names[i]
        groups[name] = 0

    for i, item in enumerate(ranking[:h]):
        groups[item.group] += 1
    
    return [groups[name] for name in group_names]

def get_ratios(ranking, group_names, h=None):
    if h == None:
        h = len(ranking)

    freqs = get_freqs(ranking, group_names, h)

    return [float(freq) / h for freq in freqs]

def fairness(ranking, group_names, h):
    groups = {}
    n = len(ranking.rank)

    ratios = get_ratios(ranking.rank, group_names)
    top_ratios = get_ratios(ranking.rank, group_names, h)

    deviations = []
    for i in range(len(group_names)):
        ratio = ratios[i]
        top_ratio = top_ratios[i]
        
        if ratio == 0 or top_ratio == 0:
            deviations += [n]
        else:
            deviations += [max(ratio/top_ratio, top_ratio/ratio)]

    return max(deviations)

def test_kendall_tau():
    for n in range(100):
        n = 10

        items = [Item(i) for i in range(n)]
        
        r1 = Ranking(items)
        r2 = Ranking(list(reversed(items)))

        assert(kendall_tau(items, r1, r1) == 0)
        assert(kendall_tau(items, r1, r2) == n*(n-1)/2)
