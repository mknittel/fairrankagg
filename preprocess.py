import pandas as pd
import numpy as np

def txt_to_xlsx(fromf, tof):
    data = pd.read_csv(fromf, sep=" ", skiprows=1, header=None)
    data = data.drop([0, 1], axis=1)
    data.to_excel(tof)

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
    data.to_excel(tof)

def scores_to_ranking(row):
    return np.flip(np.argsort(row))

def main():
    path = 'data/'
    txt_to_xlsx(path + 'sushi3a.5000.10.order', path + 'sushia.xlsx')
    txt_to_xlsx(path + 'sushi3b.5000.10.order', path + 'sushib.xlsx')
    scores_to_rankings(path + 'jester-data-1.xls', path + 'jester.xlsx')

if __name__ == "__main__":
    main()
