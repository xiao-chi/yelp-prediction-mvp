#!/usr/bin/env python
# coding: utf-8

# Step 3: sentiment_analysis.py
# This script reads all reviews from the passed reviews csv file and performs sentiment analysis.
# Reviews are categorized into Positive, Neutral, or Negative categories.
# One dataset (with business ids and reviews) is saved as <original file name>_sentiments.csv (used for topic
# modelling
# The second dataset (with business ids) is saved as <original file name>_sentiments_grouped.csv (used to merge
# with business features dataset)
# Run this to perform sentiment analysis: sentiment_analysis.py -f <file_with_reviews>

import sys
import getopt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analysis(reviews_file):
    """
    sentiment_analysis performs text analysis on each review and categorises it as positive, neutral or negative
    :param reviews_file: Reviews data set file to be analysed
    """
    # Ensure file exists before performing sentiment analysis
    try:
        reviews_df = pd.read_csv(reviews_file)
    except FileNotFoundError:
        print(reviews_file + " not found, please input valid file")
        sys.exit()

    # Change 'text' column type from float to str
    reviews_df['text'] = reviews_df['text'].astype(str)

    # Create a new column text length to quantify the length of the review
    reviews_df['text length'] = reviews_df['text'].apply(len)

    sia = SentimentIntensityAnalyzer()
    results = []

    # Determine polarity
    for business_id, line, stars in zip(reviews_df['business_id'], reviews_df['text'], reviews_df['stars']):
        pol_score = sia.polarity_scores(line)
        pol_score['review'] = line
        pol_score['business_id'] = business_id
        pol_score['stars'] = stars
        results.append(pol_score)

    # Create a df for our results:
    df = pd.DataFrame.from_records(results)

    # Categorising positive and negative sentiment:
    df['label'] = 0
    df.loc[df['compound'] > 0.75, 'label'] = 1
    df.loc[df['compound'] < 0.3, 'label'] = -1

    df.groupby(['business_id'])[['compound']].mean()

    review_dataset = df[['business_id', 'review', 'label', 'stars']]
    review_dataset = review_dataset.rename(index=str, columns={"review": "text"})

    # group reviews by business id and label (-1, 0, 1)
    grouped = review_dataset.groupby(['business_id', 'label']).size().reset_index(name='size')

    file_list = reviews_file.split(".")
    file_name1 = file_list[0] + "_sentiments.csv"
    file_name2 = file_list[0] + "_sentiments_grouped.csv"

    review_dataset.to_csv(file_name1, index=False)
    grouped.to_csv(file_name2, index=False)
    print('Sentiment Analysis is completed, results stored in: ' + file_name1 + ' and ' + file_name2)


# accept parameters
def main(argv):
    file = ""
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print('sentiment_analysis.py -f <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: sentiment_analysis.py -f <file>")
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg

    # file name is required
    if not file:
        print('usage: file name expected, use -h for more details')
        sys.exit()

    sentiment_analysis(file)


if __name__ == "__main__":
    main(sys.argv[1:])



