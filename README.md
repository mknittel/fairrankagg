# Individually Fair Rank Aggregation

Parts of this were cloned from https://github.com/ekhiru/top-k-mallows. Thank you for your implementation of the Mallows model!

## Dependencies
- matplotlib
- numpy
- pandas
- xlrd

## Quick Run
Resulting plots can be found in "plots/" directory

### Mallows
python3 main.py synthetic 50

python3 plot.py Mallows mallows.csv Pivot n alphas

## NFL
python3 main.py real_short 50

python3 plot.py NFL nfl.csv Pivot,Best-Fair n alphas

## Generally
python3 main.py {synthetic, real, real_short} {n_trials}

python3 plot.py {data name} {results csv file} {list of algs} {x var} {y var} {kwargs for filtering data}
