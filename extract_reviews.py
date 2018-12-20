#!/usr/bin/env python
# coding: utf-8

# extract_reviews.py
# This script extracts all reviews from Yelp json file and filters out only reviews from business ids in file passed.
# Reviews are saved as <original file name>_reviews.csv
# Run this to perform review extraction: extract_reviews.py -f <file_with_business_ids>

import json
import sys
import getopt
import pandas as pd
from pandas.io.json import json_normalize


def extract_reviews(file_name):
    """
    extract_reviews extracts and filters reviews of business ids provided within data of file passed
    :param file_name: file with business_ids
    """

    try:  # ensure file exists
        restaurants_df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(file_name + " not found, please input valid file")
        sys.exit()

    business_ids = restaurants_df['business_id']

    reviews = []
    with open('datasets/yelp_academic_dataset_review.json', encoding='utf8') as f:
        for line in f:
            reviews.append(json.loads(line))

    reviews_df = json_normalize(reviews)
    reviews_df.columns = reviews_df.columns.map(lambda x: x.split(".")[-1])

    extracted_reviews = reviews_df.loc[reviews_df['business_id'].isin(business_ids)]

    file_list = file_name.split(".")
    file_name = file_list[0] + "_reviews.csv"

    extracted_reviews.to_csv(file_name, index=False)
    print('Review extraction is completed, results stored in: ' + file_name)


#  accept parameters
def main(argv):
    file = ""
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print('extract_reviews.py -f <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: extract_reviews.py -f <file>")
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg

    # file name is required
    if not file:
        print('usage: file expected, use -h for more details')
        sys.exit()

    extract_reviews(file)


if __name__ == "__main__":
    main(sys.argv[1:])
