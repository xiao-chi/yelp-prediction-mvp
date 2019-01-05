#!/usr/bin/env python
# coding: utf-8

# Step 4: clean_and_prep_data.py
# This script uses the restaurants data, reviews data, and sentiments data to create a final dataset to use for
# the prediction models. The reviews dataset is used to get an average star-rating to replace the Yelp categorized
# star-rating. The sentiments dataset is merged with the restaurants dataset. Dummy variables are also created for
# each cuisine, location, and price range combination.
# Output file will be saved in datasets folder.
# Run this: clean_and_prep_data.py -b <restaurants_file> -r <reviews_file> -s <sentiments_file> -o <output_file_name>

import sys
import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description='Update stars from reviews average and prepare dataset for regression')
parser.add_argument('--businesses', '-b', action='store', dest='restaurants',
                    help='File with restaurants (can be extracted from extract_features.py)')
parser.add_argument('--reviews', '-r', dest='reviews', action='store',
                    help='File with reviews (can be extracted from extract_reviews.py)')
parser.add_argument('--sentiments', '-s', dest='sentiments', action='store',
                    help='File with sentiments (can be extracted from sentiment_analysis.py)')
parser.add_argument('--output', '-o', dest='output_file', action='store',
                    help='file where final dataset will be saved')

args = parser.parse_args()


try:  # ensure file exists
    features_df = pd.read_csv(args.restaurants)
except FileNotFoundError:
    print(args.restaurants + " not found, please input valid file")
    sys.exit()

try:  # ensure file exists
    reviews_df = pd.read_csv(args.reviews)
except FileNotFoundError:
    print(args.reviews + " not found, please input valid file")
    sys.exit()

try:
    sentiment_df = pd.read_csv(args.sentiments)
except FileNotFoundError:
    print(args.sentiments + " not found, please input valid file")
    sys.exit()

# Clean Out Data
reviews_df = reviews_df[reviews_df['stars'] != 'stars']
reviews_df['stars'] = reviews_df['stars'].map({'5': 5, '4': 4, '3': 3, '2': 2, '1': 1, 5: 5, 4: 4, 3: 3, 2: 2, 1: 1})


# Pivot Sentiment Data
sentiment_df = sentiment_df.pivot(index='business_id', columns='label', values='size')
sentiment_df = sentiment_df.rename_axis(None, axis=1).reset_index() 
sentiment_df.columns = ['business_id', 'negative_reviews', 'neutral_reviews', 'positive_reviews']


# Average out Actual Star-Ratings per business
reviews_df = reviews_df[['business_id', 'stars']]
reviews_df = reviews_df.groupby(['business_id']).mean().reset_index()

# Drop categorised Star Ratings
features_df = features_df.drop(columns=['stars'])

# Dummy Variables for City_Cuisine
price_ranges = ['price_range_1', 'price_range_2', 'price_range_3', 'price_range_4']
for price in price_ranges:
    features_df['cat'] = features_df['city'] + "_" + features_df['cuisine'] + "_" + features_df[price].map(str)
features_df = pd.concat([features_df, pd.get_dummies(features_df['cat'], prefix='cat')], axis=1)

# Merge new columns into Features Dataset
features_df = pd.merge(features_df, sentiment_df, how='left', on='business_id')
features_df = pd.merge(features_df, reviews_df, on='business_id', how='left')

# Assume 0 if missing
num_cols = ['positive_reviews', 'neutral_reviews', 'negative_reviews']
for col in num_cols:
    features_df[col] = features_df[col].replace(np.NaN, 0.0)

# Remove unneeded columns
col_remove = ['address', 'categories', 'city', 'cuisine', 'latitude', 'longitude',
              'name', 'state', 'cat', 'price_range_1', 'price_range_2', 'price_range_3',
              'price_range_4', 'postal_code']
yelp_df = features_df.drop(col_remove, axis=1)

# Set business_id as Index
yelp_df.set_index('business_id', inplace=True)

# Save Updated Business Features Dataset
yelp_df.to_csv('datasets/' + args.output_file, index=False)
print('Final dataset saved to  datasets/' + args.output_file)
