#!/bin/bash
rm data/sushia.xlsx
rm data/sushib.xlsx
rm data/jester.xlsx

python3 preprocess.py

rm /mnt/c/Users/marin/Documents/fairrank/data/*
cp -a data/. /mnt/c/Users/marin/Documents/fairrank/data/
