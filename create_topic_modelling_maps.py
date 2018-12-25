#!/usr/bin/env python
# coding: utf-8

# create_topic_modelling_map.py
# Create maps based on Topic Modelling results for dashboard.
# Maps can be created by specifying location and cuisine. Four different maps will be created for each
# cuisine and location combination (1 for each different price range). Each map will have a maximum of 600
# restaurants to ensure faster loading times for dashboard. Final maps are saved in 'maps' folder as
# <location>_<cuisine>_<price_range>.html
# Run this to create maps: create_topic_modelling_map -c <cuisine> -l <location>

import sys
import getopt
import folium
import pandas as pd
from folium import plugins
import branca.colormap as cm

COORDINATES = {'Las Vegas': (36.1699, -115.1398), 'Toronto': (43.6532, -79.3832), 'Calgary': (51.0486, -114.0708)}


# create folium Iframe & Popup by creating html
def get_popup(text):
    html = "" + text + ""
    iframe = folium.IFrame(html=html, width=300, height=200)
    return folium.Popup(iframe, max_width=1000)


# set map pin color based on star rating
# spectrum is red -> orange -> yellow -> green
def star_color(stars):
    if stars <= 1.5:
        return '#FF0000'
    elif stars <= 2.5:
        return '#FFAD00'
    elif stars <= 3.5:
        return '#FFFF00'
    elif stars < 4.5:
        return '#A1FF00'
    else:
        return '#007200'


def create_map(cuisine, location, price):
    # create map with coordinates of location specified
    tm_map = folium.Map(location=COORDINATES.get(location), zoom_start=11)

    pos_df = pd.read_csv('datasets/topic_modelling/pos_bsns_' + location.replace(" ", "").lower()
                         + "_" + cuisine.lower() + '.csv')
    neg_df = pd.read_csv('datasets/topic_modelling/neg_bsns_' + location.replace(" ", "").lower()
                         + "_" + cuisine.lower() + '.csv')

    # get restaurants in specified price range only
    pos_df = pos_df[pos_df['RestaurantsPriceRange2'] == price]
    neg_df = neg_df[neg_df['RestaurantsPriceRange2'] == price]

    pos_topics = list(pos_df)[9:15]
    neg_topics = list(neg_df)[9:15]

    for i, row in enumerate(neg_df.itertuples(), 0):
        # negative topic probabilities
        neg_scores = neg_df.iloc[i, 9:15].tolist()

        # get star rating from positive topic data set
        positive = pos_df.loc[pos_df['business_id'] == row.business_id]
        pos_star = row.stars
        if not positive.empty:
            pos_star = positive['stars'].values[0]

        # get average star rating of negative and positive dataset
        avg_stars = (row.stars + pos_star)/2

        # Create dynamically since some combinations have 5 topics instead of 6
        pos_html_topics = [''] * len(pos_topics)
        neg_html_topics = [''] * len(neg_topics)

        # get positive topics scores from positive topics dataset based on id from negative dataset
        positive = pos_df.loc[pos_df['business_id'] == row.business_id]
        pos_scores = [0] * len(pos_topics)
        if not positive.empty:
            pos_scores = positive.iloc[0, 9:15].tolist()

        # format html for popup
        for m in range(0, len(pos_topics)):
            pos_html_topics[m] = '{:18} {:.2f}%'.format(pos_topics[m].strip(), pos_scores[m] * 100)
        for n in range(0, len(neg_topics)):
            neg_html_topics[n] = '{:18} {:.2f}%'.format(neg_topics[n].strip(), neg_scores[n] * 100)

        pos_topics_text = 'Positive Topics<br>' + '<br>'.join(pos_html_topics)
        neg_topics_text = 'Negative Topics<br>' + '<br>'.join(neg_html_topics)
        stars_text = '<h3> Stars: ' + '{:.2f}'.format(avg_stars) + '</h3>'
        name_text = '<h3> Name: ' + row.name + '</h3>'
        popup_text = name_text + stars_text + '<p>' + pos_topics_text + '<br><br>' + neg_topics_text + '</p>'

        # set marker on map
        folium.Marker(location=[row.latitude, row.longitude], popup=get_popup(popup_text),
                      icon=plugins.BeautifyIcon(border_color='transparent', background_color=star_color(avg_stars),
                                                icon='circle', icon_shape='marker', text_color='#FFF')).add_to(tm_map)

        # only map 600 businesses to ensure faster rendering of map on dashboard
        if row.Index > 600:
            break

    # create color map, lower stars = red and higher stars = green
    colormap = cm.LinearColormap(
        ['red', 'orange', 'yellow', 'green'],
        vmin=0, vmax=5)

    colormap.caption = 'Star Rating'
    tm_map.add_child(colormap)

    # save map as html
    file_name = location.replace(" ", "").lower() + "_" + cuisine.lower() + "_" + str(price) + ".html"
    tm_map.save('maps/' + file_name)


# accept parameters
def main(argv):
    cuisine = ""
    location = ""
    try:
        opts, args = getopt.getopt(argv, "hc:l:", ["cuisine=", "location="])
    except getopt.GetoptError:
        print('create_topic_modelling_maps.py -c <cuisine> -l <location>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("create_topic_modelling_maps.py -c <cuisine> -l <location>")
            sys.exit()
        elif opt in ("-c", "--cuisine"):
            cuisine = arg
        elif opt in ("-l", "--location"):
            location = arg

    # cuisine and location parameters are required
    if not cuisine and not location:
        print('usage: cuisine and location are expected, use -h for more details')
        sys.exit()

    price_ranges = [1, 2, 3, 4]
    for price in price_ranges:
        create_map(cuisine, location, price)
    print("Maps created for " + cuisine + " restaurants of all 4 price ranges in " + location)


if __name__ == "__main__":
    main(sys.argv[1:])
