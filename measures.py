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


def test_kendall_tau():
    for n in range(100):
        n = 10

        items = [Item(i) for i in range(n)]
        
        r1 = Ranking(items)
        r2 = Ranking(list(reversed(items)))

        assert(kendall_tau(items, r1, r1) == 0)
        assert(kendall_tau(items, r1, r2) == n*(n-1)/2)
