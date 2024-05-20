

class Item:
    def __init__(self, name):
        self.name = name


class Ranking:
    def __init__(self, l):
        self.rank = l

    def get_ranking(self):
        return self.rank

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

class Ranking_Set:
    def __init__(self, rankings):
        self.rankings = rankings
        self.items = rankings[0]

    def get_rankings(self):
        return self.rankings

    def set_rankings(self, rankings):
        self.rankings = rankings

    def add_ranking(self, ranking):
        self.rankings += [ranking]
 



