

class Item:
    def__init__(self, name):
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

        if x > y:
            return 1
        elif x < y:
            return -1
        else:
            return 0
