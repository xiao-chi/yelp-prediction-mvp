#!/usr/bin/env python
# coding: utf-8

# create_topic_modelling_map
# Create maps based on Topics Modelling results for dashboard.
# Thirty-six maps can be created with this but must be done manually since
# there's a lot of variation (some location, cuisine, price range combinations have 5 topics instead of 6).

import sys
import getopt
import folium
import pandas as pd
from folium import plugins
import branca.colormap as cm


COORDINATES = {'Las Vegas': (36.1699, -115.1398), 'Toronto': (43.6532, -79.3832), 'Calgary': (51.0486, -114.0708) }
# calgary italian has 5
# toronto italian has 5

# read positive topics dataset based on id from negative dataset loop
def get_pos_topic_scores(id):
    positive = pos_df.loc[pos_df['business_id'] == id]
    pos_scores=[0, 0, 0, 0, 0, 0]
    if not positive.empty:
        pos_scores = positive.iloc[0,9:15].tolist()
    return pos_scores


# create html text to format text in map pin popup
def html_text(business_id, stars, neg_scores, name):
    html_topics1 = ['', '', '', '', '', ''] #dynamic
    html_topics2 = ['', '', '', '', '', ''] #dynamic

    pos_scores = get_pos_topic_scores(business_id)
    for m in range(0, len(pos_topics)):
        html_topics1[m] = '{:18}: {:.2f}%'.format(pos_topics[m], pos_scores[m] * 100)
    for n in range(0, len(neg_topics)):
        html_topics2[n] = '{:18} {:.2f}%'.format(neg_topics[n], neg_scores[n] * 100)

    pos_topics_text = 'Positive Topics<br>' + '<br>'.join(html_topics1)
    neg_topics_text = 'Negative Topics<br>' + '<br>'.join(html_topics2)
    stars_text = '<h3> Stars: ' + '{:.2f}'.format(stars) + '</h3>'
    name_text = '<h3> Name: ' + name + '</h3>'
    return name_text + stars_text + '<p>' + pos_topics_text + '<br><br>' + neg_topics_text + '</p>'


# create folium Iframe & Popup by creating html
def get_popup(business_id, stars, neg_scores, name):
    html = "" + html_text(business_id, stars, neg_scores, name) + ""
    iframe = folium.IFrame(html=html, width=300, height=200)
    return folium.Popup(iframe, max_width=1000)


# set map pin color based on star rating
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
    map = folium.Map(location=COORDINATES.get(location), zoom_start=11)

    pos_df = pd.read_csv('datasets/topic_modelling/pos_bsns_' + location.replace(" ", "").lower()
                         + "_" + cuisine.lower() + '.csv')
    neg_df = pd.read_csv('datasets/topic_modelling/neg_bsns_' + location.replace(" ", "").lower()
                         + "_" + cuisine.lower() + '.csv')

    # get restaurants in specified price range only
    pos_df = pos_df[pos_df['RestaurantsPriceRange2'] == price]
    neg_df = neg_df[neg_df['RestaurantsPriceRange2'] == price]

    pos_topics = list(pos_df)[9:15]
    neg_topics = list(neg_df)[9:15]

    for row in neg_df.itertuples():
        #   print(row)
        probs = [row.Atmosphere, row._11, row._12, row._13, row._14, row._15] # dynamic
        # positive.iloc[0,9:15].tolist()

        # get star rating from positive topic data set
        positive = pos_df.loc[pos_df['business_id'] == id]
        pos_star = row.stars
        if not positive.empty:
            pos_star = positive['stars'].values[0]

        avg_stars = (row.stars + pos_star)/2 # get average star rating of negative and positive dataset
        folium.Marker(location=[row.latitude, row.longitude], popup=get_popup(row.business_id, avg_stars, probs, row.name),
                  icon=plugins.BeautifyIcon(border_color='transparent', background_color=star_color(avg_stars),
                                icon='circle', icon_shape='marker', text_color='#FFF')).add_to(map)

        # only map 600 businesses
        if row.Index > 600:
            break

    colormap = cm.LinearColormap(
        ['red', 'orange', 'yellow', 'green'],
        vmin=0, vmax=5)

    colormap.caption = 'Star Rating'
    map.add_child(colormap)

    file_name= location.replace(" ", "").lower() + "_" + cuisine.lower() + "_" + str(price) + ".html"
    map.save('maps/' + file_name)


#  accept parameters
def main(argv):
    cuisine = ""
    location = ""
    try:
        opts, args = getopt.getopt(argv, "ic:l:", ["cuisine=", "location="])
    except getopt.GetoptError:
        print('create_topic_modelling_maps.py -c <cuisine> -l <location>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            print("create_topic_modelling_maps.py -c <cuisine> -l <location>")
            sys.exit()
        elif opt in ("-c", "--cuisine"):
            cuisine = arg
        elif opt in ("-l", "--location"):
            location = arg

    # cuisine and location parameters are required
    if not cuisine and not location:
        print('usage: cuisine and location are expected, use -i for more details')
        sys.exit()

    price_ranges = [1, 2, 3, 4]
    for price in price_ranges:
        create_map(cuisine, location, price)
    print("Maps created for " + cuisine + " restaurants of all 4 price ranges in " + location)


if __name__ == "__main__":
    main(sys.argv[1:])