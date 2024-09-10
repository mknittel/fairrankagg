

class Item:
    def __init__(self, name, group=None):
        self.name = str(name)
        self.group = group

    def __str__(self):
        return self.name


class Ranking:
    def __init__(self, l):
        self.rank = l

    def __str__(self):
        return str([str(item) for item in self.rank]).replace("'", "").replace('"', '')

    def get_ranking(self):
        return self.rank

    def at(self, index):
        return self.rank[index]

    def set_ranking(self, l):
        self.rank = l

    def compare(self, x, y):
        ix = self.rank.index(x)
        iy = self.rank.index(y)

        if ix > iy:
            return 1
        elif ix < iy:
            return -1
        else:
            return 0

    def get_dist(self, x, y):
        ix = self.rank.index(x)
        iy = self.rank.index(y)
        return abs(ix - iy)


class Ranking_Set:
    def __init__(self, rankings):
        self.rankings = rankings
    
    def __str__(self):
        return str([str(ranking) for ranking in self.rankings]).replace("'", "").replace('"', '')

    def get_rankings(self):
        return self.rankings

    def at(self, index):
        return self.rankings[index]

    def set_rankings(self, rankings):
        self.rankings = rankings

    def add_ranking(self, ranking):
        self.rankings += [ranking]

    def vote(self, ref, other):
        tally = sum([ranking.compare(ref, other) for ranking in self.rankings])
        if tally > 0:
            return 1
        elif tally < 0:
            return -1
        else:
            return 0
 
    def get_max_dist(self, item1, item2):
        dist = 0

        for ranking in self.rankings:
            rank_dist = ranking.get_dist(item1, item2)
            dist = max(dist, rank_dist)

        return dist
