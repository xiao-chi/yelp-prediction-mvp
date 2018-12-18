#!/usr/bin/env python
# coding: utf-8

# merge_sentiments.py
# This script combines the business features dataset with the sentiment analysis dataset.
# Requires that both datasets are saved to csv files (use feature_engineering.py and sentiment_analysis.py)
# Missing values for positive reviews, negative reviews, and neutral reviews columns are set to 0.
# The final merged dataset is overwritten to restaurants file (argument provided)

import pandas as pd
import numpy as np
import sys
import getopt


# merge restaurant business features with review sentiment analysis
def merge_data(restaurants_file, sentiments_file):
    """
    merge_data merges restaurant data after feature engineering and review sentiment analysis data per business
    :param restaurants_file: Restaurants data set
    :param sentiments_file: Sentiment Analysis data set (grouped by business id and positive/neutral/negative label)
    """
    # Ensure files exist before merging
    try:
        reviews_sentiment_df = pd.read_csv(sentiments_file)
    except FileNotFoundError:
        print(sentiments_file + " not found, please input valid file")
        sys.exit()

    try:
        restaurants_df = pd.read_csv(restaurants_file)
    except FileNotFoundError:
        print(restaurants_file + " not found, please input valid file")
        sys.exit()

    # Rearrange reviews sentiment data frame
    reviews_df = reviews_sentiment_df.pivot(index='business_id', columns='label', values='size')
    reviews_df = reviews_df.rename_axis(None, axis=1).reset_index()
    reviews_df.columns = ['business_id', 'negative_reviews', 'neutral_reviews', 'positive_reviews']

    # merge categorized reviews and business features
    features_df = pd.merge(restaurants_df, reviews_df, how='left', on='business_id')

    if len(restaurants_df) != len(features_df):
        print("Mismatch in restaurants dataset length and final merged dataset")

    # Assume 0 if missing
    num_cols = ['positive_reviews', 'neutral_reviews', 'negative_reviews']
    for col in num_cols:
        features_df[col] = features_df[col].replace(np.NaN, 0.0)

    # Overwrite and save to restaurants file
    features_df.to_csv(restaurants_file, mode='w', encoding='utf-8', index=False)
    print('dataset merged and overwritten to: ' + restaurants_file)


#  accept parameters
def main(argv):
    restaurants_file = ""
    sentiments_file = ""
    try:
        opts, args = getopt.getopt(argv, "ir:s:", ["restaurants=", "sentiments="])
    except getopt.GetoptError:
        print('merge_features_and_sentiments.py -r <restaurants csv file> -s <sentiments csv file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            print("usage: merge_features_and_sentiments.py -r <restaurants csv file> -s <sentiments csv file>")
            sys.exit()
        elif opt in ("-r", "--restaurants"):
            restaurants_file = arg
        elif opt in ("-s", "--sentiments"):
            sentiments_file = arg

    # restaurants file and sentiments file names are required
    if not restaurants_file and not sentiments_file:
        print('usage: restaurants file name and sentiments file name are expected, use -i for more details')
        sys.exit()

    merge_data(restaurants_file, sentiments_file)


if __name__ == "__main__":
    main(sys.argv[1:])
