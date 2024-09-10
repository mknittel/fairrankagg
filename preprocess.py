import pandas as pd
import numpy as np

MOVIELENS = [
        [9,7,2,4,6,10,1,5,3,8],
        [7,5,3,1,8,10,4,2,6,9],
        [7,1,3,5,4,8,6,2,10,9],
        [7,9,3,1,10,8,5,4,6,2],
        [4,3,10,5,6,8,7,2,9,1],
    ]

MLGENRES = ['C','W','W','D','D','C','W','D','D','C']

def hard_to_xlsx(hard, tof, sub=False):
    if sub:
        hard = [[x - 1 for x in row] for row in hard]
    data = pd.DataFrame(hard)
    data.to_excel(tof, index=False)

def txt_to_xlsx(fromf, tof):
    data = pd.read_csv(fromf, sep=" ", skiprows=1, header=None)
    data = data.drop([0, 1], axis=1)
    data.to_excel(tof, index=False)

# Assume excel file, no headea
def scores_to_rankings(fromf, tof, n=0, k=0):
    scores = pd.read_excel(fromf, header=None).to_numpy()

    # First column in jester is bad
    scores = scores[:,1:]

    if n > 0 and n < len(scores[0]):
        scores = scores[:,:n]
    if k > 0 and k < len(scores):
        scores = scores[:k,:]
    #if not len(scores)%2:
    #    print("Truncating odd k")
    #    scores = scores[:-1,:]
    
    rankings = [scores_to_ranking(row) for row in scores]
    data = pd.DataFrame(rankings)
    data.to_excel(tof, index=False)

def scores_to_ranking(row):
    return np.flip(collapse_rankings(row))

def collapse_rankings(row):
    return np.argsort(row)

# From MouinullIslamNJIT, Rank Aggregation Proportionate Fairness
def read_group_pickle(fromf, tof, groupf, group_ind):
    object = pd.read_pickle(fromf)
    read_data = object[1]
    read_data = read_data.transpose()
    np_read_data = read_data.to_numpy()
    num_of_player = 55

    rankings = [collapse_rankings(row) for row in np_read_data]
    data = pd.DataFrame(rankings)
    data.to_excel(tof, index=False)

    groups = read_data.iloc[group_ind,:]
    groups.to_excel(groupf, index=False)

def main():
    path = 'data/'
    read_group_pickle(path + 'top25_dfs.pickle', path + 'nfl_players.xlsx', path + 'nfl_divisions.xlsx', 25)
    txt_to_xlsx(path + 'sushi3a.5000.10.order', path + 'sushia.xlsx')
    txt_to_xlsx(path + 'sushi3b.5000.10.order', path + 'sushib.xlsx')
    scores_to_rankings(path + 'jester-data-1.xls', path + 'jester.xlsx')
    hard_to_xlsx(MOVIELENS, path + 'movielens.xlsx', sub=True)
    hard_to_xlsx(MLGENRES, path + 'movielens_genres.xlsx')

if __name__ == "__main__":
    main()
