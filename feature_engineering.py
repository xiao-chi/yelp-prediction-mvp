#!/usr/bin/env python
# coding: utf-8

# ## yelpBusinessFeatureRestructure
# This script breaks down business features from yelp business json file (nested json objects each become a
# subsequent column). For example, the 6 parking categories are each moved to their own column.
# This will filter out restaurants of cuisine specified in location specified and write this new dataset to
# `datasets/[location]_[cuisine]_[price_range]_restaurants.csv`
# Script is contigent on having 'yelp_academic_dataset_business.json' in datasets folder.
# Run this by feature_engineering.py -c <cuisine> -l <location> -p <price_range_value>"
# Ex: feature_engineering.py -c American -l 'Las Vegas' -p 2

import json
import pandas as pd
import numpy as np
import sys
import getopt
from ast import literal_eval
from datetime import datetime
from datetime import timedelta
from pandas.io.json import json_normalize

# total time open in hours
def total_time_in_hours(time):
    l = time.split('-')
    s1 = l[0]
    s2 = l[1] # for example
    FMT = '%H:%M'
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    if tdelta.days < 0:
        tdelta = timedelta(days=0,seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    hours, minutes = tdelta.seconds // 3600, tdelta.seconds // 60 % 60
    return hours + minutes/60


# open before 8am (weekdays)
def opening_hour_by_8(time):
    l = time.split('-')
    s1 = l[0]
    FMT = '%H:%M'
    tdelta = datetime.strptime(s1, FMT)
    if tdelta.hour <= 8:
        return 1
    else:
        return 0


# closing after 9pm (weekdays)
def closing_after_9(time):
    l = time.split('-')
    s2 = l[1]
    FMT = '%H:%M'
    tdelta = datetime.strptime(s2, FMT)
    if tdelta.hour >= 21 or tdelta.hour <= 4:
        return 1
    else:
        return 0

def basic_details(df):
    print('Row:{}, columns:{}'.format(df.shape[0],df.shape[1]))
    k = pd.DataFrame()
    k['number of Unique value'] = df.nunique()
    k['Number of missing value'] = df.isnull().sum()
    k['Data type'] = df.dtypes
    return k


def feature_breakdown(cuisine, location, price_range_value, file):
    dataset = None

    if file: # read from file if file provided
        data_frame = pd.read_csv(file)
        dataset = data_frame.copy()
    else:
        businesses = []
        with open('datasets/yelp_academic_dataset_business.json', 'r') as f:
            for line in f:
                businesses.append(json.loads(line))
        df = json_normalize(businesses)
        df.columns = df.columns.map(lambda x: x.split(".")[-1])

        restaurants = df[df['categories'].str.contains("Restaurant") == True]
        location_restaurants = restaurants[restaurants['city'] == location]
        cuisine_data = location_restaurants[location_restaurants['categories'].str.contains(cuisine) == True]

        dataset = cuisine_data.copy()

    dataset = dataset.drop(columns=['is_open', 'BYOB', 'BYOBCorkage', 'AcceptsInsurance', 'AgesAllowed',
                                    'BusinessAcceptsBitcoin', 'ByAppointmentOnly', 'Corkage', 'DietaryRestrictions',
                                    'RestaurantsCounterService', 'Open24Hours', 'HairSpecializesIn', 'DriveThru',
                                    'DogsAllowed', 'GoodForDancing']) #, 'hours', 'attributes'])

    # Ambience: romantic, intimate, classy, hipster, touristy, trendy, upscale, casual
    ambience = ['romantic', 'intimate', 'classy', 'hipster', 'touristy', 'trendy', 'upscale', 'casual']
    for a in ambience:
        dataset['ambience_' + a] = dataset['Ambience'].apply(lambda df: df if pd.isnull(df) else literal_eval(df).get(a))
    dataset = dataset.drop(columns='Ambience')

    # GoodForMeal: dessert, latenight, lunch, dinner, breakfast, brunch
    good_for_meal = ['dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch']
    for meal in good_for_meal:
        dataset['good_for_' + meal] = dataset['GoodForMeal'].apply(
            lambda df: df if pd.isnull(df) else literal_eval(df).get(meal))
    dataset = dataset.drop(columns='GoodForMeal')

    # BusinessParking: garage, street, validated, lot, valet
    parking = ['garage', 'street', 'validated', 'lot', 'valet']
    for p in parking:
        dataset['parking_' + p] = dataset['BusinessParking'].apply(
            lambda df: df if pd.isnull(df) else literal_eval(df).get(p))
    dataset = dataset.drop(columns='BusinessParking')

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dataset['TotalOpenTimeInWeek'] = 0
    for day in days_of_week:
        dataset['TotalOpenTimeInWeek'] += dataset[day].apply(lambda x: 0 if pd.isnull(x) else total_time_in_hours(x))

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dataset['NumberOfWeekdaysWithEarlyOpening'] = 0
    for day in weekdays:
        dataset['NumberOfWeekdaysWithEarlyOpening'] += dataset[day].apply(
            lambda x: x if pd.isnull(x) else opening_hour_by_8(x))

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dataset['NumberOfWeekdaysWithLateClosing'] = 0
    for day in weekdays:
        dataset['NumberOfWeekdaysWithLateClosing'] += dataset[day].apply(
            lambda x: x if pd.isnull(x) else closing_after_9(x))

    # open on weekends
    weekend = ['Saturday', 'Sunday']
    dataset['OpenOnWeekends'] = 0
    for day in weekend:
        dataset['OpenOnWeekends'] += dataset[day].apply(lambda x: x if pd.isnull(x) else 1)

    for day in days_of_week:
        dataset[day] = dataset[day].apply(lambda x: 0 if pd.isnull(x) else total_time_in_hours(x))

    # break down best nights
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in days:
        dataset['bestnight_' + day] = dataset['BestNights'].apply(
            lambda df: df if pd.isnull(df) else literal_eval(df).get(day))
    dataset = dataset.drop(columns='BestNights')

    # break down music
    musics = ['dj', 'background_music', 'no_music', 'karaoke', 'live', 'video', 'jukebox']
    for m in musics:
        dataset['music_' + m] = dataset['Music'].apply(lambda df: df if pd.isnull(df) else literal_eval(df).get(m))
    dataset = dataset.drop(columns='Music')

    # break down alcohol
    alcohol = ['full_bar', 'beer_and_wine', 'no_alcohol']
    for a in alcohol:
        dataset[a] = dataset['Alcohol'].apply(lambda df: True if df == a else False)
    dataset = dataset.drop(columns='Alcohol')

    # Smoking is outdoor, no, yes
    smoking = ['outdoor', 'no', 'yes']
    for s in smoking:
        dataset['smoking_' + s] = dataset['Smoking'].apply(lambda df: True if df == s else False)
    dataset = dataset.drop(columns='Smoking')

    # WiFi is free, no, paid
    wifi = ['free', 'no', 'paid']
    for w in wifi:
        dataset['wifi_' + w] = dataset['WiFi'].apply(lambda df: True if df == w else False)
    dataset = dataset.drop(columns='WiFi')

    # NoiseLevel is average, loud, quiet, very_loud
    noise_levels = ['average', 'loud', 'quiet', 'very_loud']
    for n in noise_levels:
        dataset['noise_' + n] = dataset['NoiseLevel'].apply(lambda df: True if df == n else False)
    dataset = dataset.drop(columns='NoiseLevel')

    # RestaurantPriceRange2 is 1, 2, 3, 4
    price_range = ['1', '2', '3', '4']
    for p in price_range:
        dataset['price_range_' + p] = dataset['RestaurantsPriceRange2'].apply(lambda df: True if df == p else False)
    dataset = dataset.drop(columns='RestaurantsPriceRange2')

    # Restaurant Attire is casual or dressy
    attire = ['casual', 'dressy']
    for a in attire:
        dataset['attire_' + a] = dataset['RestaurantsAttire'].apply(lambda df: True if df == a else False)
    dataset = dataset.drop(columns='RestaurantsAttire')

    # Assume 0 if missing
    num_cols = ['positive_reviews', 'neutral_reviews', 'negative_reviews', 'OpenOnWeekends',
                'NumberOfWeekdaysWithEarlyOpening', 'NumberOfWeekdaysWithLateClosing']
    for col in num_cols:
        dataset[col] = dataset[col].replace(np.NaN, 0.0)

    # Assume false value if missing
    cols = ['ambience_romantic', 'ambience_intimate', 'ambience_classy', 'ambience_hipster', 'ambience_touristy',
            'ambience_trendy', 'ambience_upscale', 'ambience_casual', 'good_for_dessert', 'good_for_latenight',
            'good_for_lunch', 'good_for_dinner', 'good_for_breakfast', 'good_for_brunch', 'parking_garage',
            'parking_validated', 'parking_lot', 'parking_valet', 'bestnight_monday', 'bestnight_tuesday',
            'bestnight_wednesday', 'bestnight_thursday', 'bestnight_friday', 'bestnight_saturday', 'bestnight_sunday',
            'music_dj', 'music_background_music', 'music_no_music', 'music_karaoke', 'music_live', 'music_video',
            'music_jukebox', 'parking_street']
    for col in cols:
        dataset[col] = dataset[col].replace(np.NaN, False)

    file_name = ""
    if file:
        file_list = file.split(".")
        file_name = file_list[0] + "_updated.csv"

    else:
        location = location.replace(" ", "")
        file_name = 'datasets/' + str(location) + '_' + str(cuisine)
        if price_range_value:
            pr = 'price_range_' + str(price_range_value)
            dataset = dataset[dataset[pr] == True]
            file_name += '_pr' + str(price_range_value)
        file_name += '_restaurants.csv'

    file_name = file_name.lower()
    dataset.to_csv(file_name, mode='w', encoding='utf-8', index=False)
    print('dataset collected and written to: ' + file_name)


def main(argv):
    cuisine = ""
    location = ""
    price_range = ""
    file = ""
    try:
        opts, args = getopt.getopt(argv, "ic:l:f:p:", ["cuisine=", "location=", "file=", "price="])
    except getopt.GetoptError:
        print('feature_engineering.py -c <cuisine> -l <location> -f <file> -p <price_range_value>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            print("usage: feature_engineering.py -c <cuisine> -l <location> -f <file> -p <price_range_value>")
            sys.exit()
        elif opt in ("-c", "--cuisine"):
            cuisine = arg
        elif opt in ("-l", "--location"):
            location = arg
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-p", "--price"):
            price_range = arg

    if (not cuisine and not location) and not file:
        print('usage: cuisine and location or file parameters expected, use -i for more details')
        sys.exit()
    feature_breakdown(cuisine, location, price_range, file)


if __name__ == "__main__":
    main(sys.argv[1:])

