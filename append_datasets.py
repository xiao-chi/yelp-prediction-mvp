#!/usr/bin/env python
# coding: utf-8

# append_datasets.py
# This script will append similar datasets (please ensure columns are the same in all files being passed).
# Output file will be saved in datasets folder.
# This should preferably be run on several files after the extract_features.py or extract_reviews.py script.
# Run this: append_datasets.py -a <file_name> -a <file_name> [no limit to number of files] -o <output_file_name>

import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Merge datasets in different files to 1 cumulative file')
parser.add_argument('-a', action='append', dest='collection',
                    default=[],
                    help='Add repeated files to a list',)
parser.add_argument('--output', '-o', dest='output_file', action='store',
                    help='file where final dataset will be saved')

args = parser.parse_args()

# Loop through files and collect dataframes
dataframes = []
for file in args.collection:
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(file + " not found, please input valid file")
        sys.exit()
    dataframes.append(df)

# concat dataframes and save cumulative result to file
result = pd.concat(dataframes, axis='rows', ignore_index=True, sort=False)
result.to_csv('datasets/' + args.output_file, index=False)
print('Final dataset saved to  datasets/' + args.output_file)
