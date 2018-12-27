# prediction.py
# Rating Prediction Page

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from app import app
from yelp_predict import predict

colors = {'text': '#B70000'}
available_cities = ['Las Vegas', 'Calgary', 'Toronto']
three_price_ranges = [1, 2, 3]
all_price_ranges = [1, 2, 3, 4]
cuisines = ['Italian', 'American', 'Chinese']

# set average values from training data
weekdays_early_opening = 0.92
weekdays_late_closing = 3.28

# PREDICTION API
layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
    html.H1(
        children='Rating Prediction',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        html.Div(['City'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='cities_dropdown_2',
            options=[{'label': i, 'value': i} for i in available_cities],
            value='Las Vegas',
            placeholder='City'
        )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
        html.Div(['Cuisine'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='cuisines_dropdown_2',
            options=[{'label': i, 'value': i} for i in cuisines],
            value='American',
        )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
        html.Div(['Price Range'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='price_ranges_dropdown_2',
            options=[{'label': i, 'value': i} for i in all_price_ranges],
            value=2,
        )], style={'width': '33%', 'display': 'inline-block'}),

    # Column 1
    html.Div([
        html.H4(children="Business Features"),
        html.Div([
            html.Div(['Noise Level'], style={'font-weight': 'bold'}),
            dcc.Slider(
                id='slider_noise',
                min=0,
                max=3,
                marks={
                    0: 'Quiet',
                    1: 'Average',
                    2: 'Loud',
                    3: 'Very Loud'
                },
                value=1
            )],
            style={'marginLeft': 25, 'width': '60%'}
        ),
        html.Br(),
        html.Div([
            html.Div(['WiFi'], style={'font-weight': 'bold'}),
            dcc.Slider(
                id='slider_wifi',
                min=0,
                max=2,
                marks={
                    0: 'None',
                    1: 'Free',
                    2: 'Paid'
                },
                value=0
            )],
            style={'marginLeft': 25, 'width': '60%'}
        ),
        html.Br(),
        html.Div([
            html.Div(['Alcohol'], style={'font-weight': 'bold'}),
            dcc.Slider(
                id='slider_alcohol',
                min=0,
                max=2,
                marks={
                    0: 'None',
                    1: 'Beer & Wine',
                    2: 'Full Bar'
                },
                value=0
            )],
            style={'marginLeft': 25, 'width': '60%'}
        ),
        html.Br(),
        html.Div([
            html.Div(['Smoking'], style={'font-weight': 'bold'}),
            dcc.Slider(
                id='slider_smoking',
                min=0,
                max=2,
                marks={
                    0: 'No',
                    1: 'Outdoor',
                    2: 'Yes'
                },
                value=0
            )],
            style={'marginLeft': 25, 'width': '60%'}
        ),
        html.Br(),
        html.Div([
            html.Div(['Ambience'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='ambience_checkbox',
                options=[
                    {'label': 'Trendy', 'value': 'trendy'},
                    {'label': 'Romantic', 'value': 'romantic'},
                    {'label': 'Classy', 'value': 'classy'},
                    {'label': 'Casual', 'value': 'casual'},
                    {'label': 'Hipster', 'value': 'hipster'},
                    {'label': 'Intimate', 'value': 'intimate'},
                    {'label': 'Upscale', 'value': 'upscale'},
                    {'label': 'Touristy', 'value': 'touristy'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
        html.Div([
            html.Div(['Good For'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='good_for_checkbox',
                options=[
                    {'label': 'Breakfast', 'value': 'breakfast'},
                    {'label': 'Brunch', 'value': 'brunch'},
                    {'label': 'Lunch', 'value': 'lunch'},
                    {'label': 'Dinner', 'value': 'dinner'},
                    {'label': 'Dessert', 'value': 'dessert'},
                    {'label': 'Late Night', 'value': 'late_night'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
        html.Div([
            html.Div(['Best Night'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='best_night_checkbox',
                options=[
                    {'label': 'Monday', 'value': 'Monday'},
                    {'label': 'Tuesday', 'value': 'Tuesday'},
                    {'label': 'Wednesday', 'value': 'Wednesday'},
                    {'label': 'Thursday', 'value': 'Thursday'},
                    {'label': 'Friday', 'value': 'Friday'},
                    {'label': 'Saturday', 'value': 'Saturday'},
                    {'label': 'Sunday', 'value': 'Sunday'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
        html.Div([
            html.Div(['Parking'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='parking_checkbox',
                options=[
                    {'label': 'Garage', 'value': 'garage'},
                    {'label': 'Street', 'value': 'street'},
                    {'label': 'Lot', 'value': 'lot'},
                    {'label': 'Validated', 'value': 'validated'},
                    {'label': 'Valet', 'value': 'valet'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'})
        ]),
        html.Div([
            html.Div(['Music'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='music_checkbox',
                options=[
                    {'label': 'None', 'value': 'no_music'},
                    {'label': 'Background', 'value': 'background'},
                    {'label': 'Live', 'value': 'live'},
                    {'label': 'DJ', 'value': 'dj'},
                    {'label': 'Karaoke', 'value': 'karaoke'},
                    {'label': 'Jukebox', 'value': 'jukebox'},
                    {'label': 'Video', 'value': 'video'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )]
        )], style={'width': '33%', 'display': 'inline-block'}),
    # Column 2
    html.Div([
        html.H4(children='Hours Open'),
        html.Div(children="Input number of hours open each day from 0-24"),
        html.Div([
            html.Span(['Monday'], style={'font-weight': 'bold', 'padding-right': '44px'}),
            dcc.Input(id='monday_hours', type='number', min='0', max='24', value='0')]
        ),
        html.Div([
            html.Span(['Tuesday'], style={'font-weight': 'bold', 'padding-right': '45px'}),
            dcc.Input(id='tuesday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Div([
            html.Span(['Wednesday'], style={'font-weight': 'bold', 'padding-right': '18px'}),
            dcc.Input(id='wednesday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Div([
            html.Span(['Thursday'], style={'font-weight': 'bold', 'padding-right': '41px'}),
            dcc.Input(id='thursday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Div([
            html.Span(['Friday'], style={'font-weight': 'bold', 'padding-right': '61px'}),
            dcc.Input(id='friday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Div([
            html.Span(['Saturday'], style={'font-weight': 'bold', 'padding-right': '41px'}),
            dcc.Input(id='saturday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Div([
            html.Span(['Sunday'], style={'font-weight': 'bold', 'padding-right': '51px'}),
            dcc.Input(id='sunday_hours', type='number', min='0', max='24', value='0')
        ]),
        html.Br(),
        html.Div([
            html.H4(children='Additional Features'),
            html.Div('Optional Features', style={'font-style': 'italic'}),
            dcc.Checklist(
                id='additional_features_checkbox',
                options=[
                    {'label': 'Bike Parking', 'value': 'bike_parking'},
                    {'label': 'Accepts Credit Card', 'value': 'accept_card'},
                    {'label': 'Catering', 'value': 'caters'},
                    {'label': 'Coat Check', 'value': 'coat_check'},
                    {'label': 'Good For Kids', 'value': 'good_for_kids'},
                    {'label': 'Happy Hour', 'value': 'happy_hour'},
                    {'label': 'Has TV', 'value': 'has_tv'},
                    {'label': 'Outdoor Seating', 'value': 'outdoor_seating'},
                    {'label': 'Delivery', 'value': 'delivery'},
                    {'label': 'Good For Groups', 'value': 'good_for_groups'},
                    {'label': 'Reservations', 'value': 'reservations'},
                    {'label': 'Table Service', 'value': 'table_service'},
                    {'label': 'Take Out', 'value': 'take_out'},
                    {'label': 'Wheelchair Accessible', 'value': 'wheelchair_accessible'},
                    {'label': 'Casual Attire', 'value': 'attire_casual'},
                    {'label': 'Dressy Attire', 'value': 'attire_dressy'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
    ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),
    # Column 3
    html.Div([
        html.H4(children="Prediction after 6 months"),
        html.Div([
            html.Div(['Number of Positive Reviews'], style={'font-weight': 'bold'}),
            dcc.Input(id='pos_reviews_keypress', type='number', min='0', value='0'),
        ]),
        html.Br(),
        html.Div([
            html.Div(['Number of Neutral Reviews'], style={'font-weight': 'bold'}),
            dcc.Input(id='neu_reviews_keypress', type='number', min='0', value='0'),
        ]),
        html.Br(),
        html.Div([
            html.Div(['Number of Negative Reviews'], style={'font-weight': 'bold'}),
            dcc.Input(id='neg_reviews_keypress', type='number', min='0', value='0'),
        ]),
        html.Br(),
        html.Div([
            html.Div(['Total Number of Reviews'], style={'font-weight': 'bold'}),
            dcc.Input(id='review_count_keypress', type='number', min='0', value='0'),
        ]),
        html.Br(),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.H3('Yelp Rating Prediction'),
        html.H1(children='0.0', id='rating_prediction', style={'color': colors['text']})],
        style={'width': '33%', 'display': 'inline-block', 'float': 'right'}),
    html.Div(id='prediction-content'),
    html.Br(),
    html.Div([dcc.Link('Go back to home', href='/')])
])


# exclude price range 4 for calgary + chinese
@app.callback(dash.dependencies.Output('price_ranges_dropdown_2', 'options'),
              [dash.dependencies.Input('cities_dropdown_2', 'value'),
               dash.dependencies.Input('cuisines_dropdown_2', 'value')])
def set_price_range_options(city, cuisine):
    if city == 'Calgary' and cuisine == 'Chinese':
        return [{'label': i, 'value': i} for i in three_price_ranges]
    else:
        return [{'label': i, 'value': i} for i in all_price_ranges]


# remove other music options if none is selected
@app.callback(dash.dependencies.Output('music_checkbox', 'options'),
              [dash.dependencies.Input('music_checkbox', 'values')])
def set_music_options(value):
    no_music = [{'label': 'None', 'value': 'no_music'}]
    music_options = [
        {'label': 'None', 'value': 'no_music'},
        {'label': 'Background', 'value': 'background'},
        {'label': 'Live', 'value': 'live'},
        {'label': 'DJ', 'value': 'dj'},
        {'label': 'Karaoke', 'value': 'karaoke'},
        {'label': 'Jukebox', 'value': 'jukebox'},
        {'label': 'Video', 'value': 'video'}]
    if 'no_music' in value:
        return no_music
    else:
        return music_options


# total up reviews
@app.callback(dash.dependencies.Output('review_count_keypress', 'value'),
              [dash.dependencies.Input('pos_reviews_keypress', 'value'),
               dash.dependencies.Input('neu_reviews_keypress', 'value'),
               dash.dependencies.Input('neg_reviews_keypress', 'value')
               ])
def calculate_total_reviews(pos_count, neu_count, neg_count):
    return int(pos_count) + int(neu_count) + int(neg_count)


@app.callback(dash.dependencies.Output('rating_prediction', 'children'),
              [dash.dependencies.Input('submit_button', 'n_clicks')],
              [dash.dependencies.State('cities_dropdown_2', 'value'),
               dash.dependencies.State('cuisines_dropdown_2', 'value'),
               dash.dependencies.State('price_ranges_dropdown_2', 'value'),
               dash.dependencies.State('slider_noise', 'value'),
               dash.dependencies.State('slider_wifi', 'value'),
               dash.dependencies.State('slider_alcohol', 'value'),
               dash.dependencies.State('slider_smoking', 'value'),
               dash.dependencies.State('music_checkbox', 'values'),
               dash.dependencies.State('ambience_checkbox', 'values'),
               dash.dependencies.State('good_for_checkbox', 'values'),
               dash.dependencies.State('best_night_checkbox', 'values'),
               dash.dependencies.State('parking_checkbox', 'values'),
               dash.dependencies.State('monday_hours', 'value'),
               dash.dependencies.State('tuesday_hours', 'value'),
               dash.dependencies.State('wednesday_hours', 'value'),
               dash.dependencies.State('thursday_hours', 'value'),
               dash.dependencies.State('friday_hours', 'value'),
               dash.dependencies.State('saturday_hours', 'value'),
               dash.dependencies.State('sunday_hours', 'value'),
               dash.dependencies.State('additional_features_checkbox', 'values'),
               dash.dependencies.State('pos_reviews_keypress', 'value'),
               dash.dependencies.State('neu_reviews_keypress', 'value'),
               dash.dependencies.State('neg_reviews_keypress', 'value'),
               dash.dependencies.State('review_count_keypress', 'value')
               ])
def prediction(n_clicks, city, cuisine, price, noise_level, wifi, alcohol, smoking, musics, ambiences, good_fors,
               best_nights, parkings, m_hours, tu_hours, w_hours, th_hours, f_hours, sa_hours, su_hours,
               additional_features, pos_reviews, neu_reviews, neg_reviews, review_count):
    m_hours = int(m_hours)
    tu_hours = int(tu_hours)
    w_hours = int(w_hours)
    th_hours = int(th_hours)
    f_hours = int(f_hours)
    sa_hours = int(sa_hours)
    su_hours = int(su_hours)

    total_hours = m_hours + tu_hours + w_hours + th_hours + f_hours + sa_hours + su_hours
    open_on_weekends = 0
    if sa_hours > 0:
        open_on_weekends += 1
    if su_hours > 0:
        open_on_weekends += 1

    pos_reviews = int(pos_reviews)
    neu_reviews = int(neu_reviews)
    neg_reviews = int(neg_reviews)
    review_count = int(review_count)

    no_wifi = 1 if wifi is 0 else 0
    free_wifi = 1 if wifi is 1 else 0
    paid_wifi = 1 if wifi is 2 else 0

    no_alcohol = 1 if alcohol is 0 else 0
    beer_and_wine = 1 if alcohol is 1 else 0
    full_bar = 1 if alcohol is 2 else 0

    noise_quiet = 1 if noise_level is 0 else 0
    noise_average = 1 if noise_level is 1 else 0
    noise_loud = 1 if noise_level is 2 else 0
    noise_very_loud = 1 if noise_level is 3 else 0

    smoking_no = 1 if smoking is 0 else 0
    smoking_outdoor = 1 if smoking is 1 else 0
    smoking_yes = 1 if smoking is 2 else 0

    trendy = 1 if 'trendy' in ambiences else 0
    classy = 1 if 'classy' in ambiences else 0
    romantic = 1 if 'romantic' in ambiences else 0
    intimate = 1 if 'intimate' in ambiences else 0
    hipster = 1 if 'hipster' in ambiences else 0
    casual = 1 if 'casual' in ambiences else 0
    upscale = 1 if 'upscale' in ambiences else 0
    touristy = 1 if 'touristy' in ambiences else 0

    good_for_dinner = 1 if 'dinner' in good_fors else 0
    good_for_brunch = 1 if 'brunch' in good_fors else 0
    good_for_breakfast = 1 if 'breakfast' in good_fors else 0
    good_for_lunch = 1 if 'lunch' in good_fors else 0
    good_for_dessert = 1 if 'dessert' in good_fors else 0
    good_for_late_night = 1 if 'late_night' in good_fors else 0

    best_night_monday = 1 if 'Monday' in best_nights else 0
    best_night_tuesday = 1 if 'Tuesday' in best_nights else 0
    best_night_wednesday = 1 if 'Wednesday' in best_nights else 0
    best_night_thursday = 1 if 'Thursday' in best_nights else 0
    best_night_friday = 1 if 'Friday' in best_nights else 0
    best_night_saturday = 1 if 'Saturday' in best_nights else 0
    best_night_sunday = 1 if 'Sunday' in best_nights else 0

    parking_garage = 1 if 'garage' in parkings else 0
    parking_lot = 1 if 'lot' in parkings else 0
    parking_street = 1 if 'street' in parkings else 0
    parking_valet = 1 if 'valet' in parkings else 0
    parking_validated = 1 if 'validated' in parkings else 0

    no_music = 1 if 'no_music' in musics else 0
    music_dj = 1 if 'dj' in musics else 0
    music_live = 1 if 'live' in musics else 0
    music_background = 1 if 'background' in musics else 0
    music_karaoke = 1 if 'karaoke' in musics else 0
    music_jukebox = 1 if 'jukebox' in musics else 0
    music_video = 1 if 'video' in musics else 0

    bike_parking = 1 if 'bike_parking' in additional_features else 0
    accept_card = 1 if 'accept_card' in additional_features else 0
    caters = 1 if 'caters' in additional_features else 0
    coat_check = 1 if 'coat_check' in additional_features else 0
    good_for_kids = 1 if 'good_for_kids' in additional_features else 0
    happy_hour = 1 if 'happy_hour' in additional_features else 0
    has_tv = 1 if 'has_tv' in additional_features else 0
    outdoor_seating = 1 if 'outdoor_seating' in additional_features else 0
    delivery = 1 if 'delivery' in additional_features else 0
    good_for_groups = 1 if 'good_for_groups' in additional_features else 0
    reservations = 1 if 'reservations' in additional_features else 0
    table_service = 1 if 'table_service' in additional_features else 0
    take_out = 1 if 'take_out' in additional_features else 0
    wheelchair_accessible = 1 if 'wheelchair_accessible' in additional_features else 0
    attire_casual = 1 if 'attire_casual' in additional_features else 0
    attire_dressy = 1 if 'attire_dressy' in additional_features else 0

    cat_dict = {'cat_Calgary_american_1.0': 0, 'cat_Calgary_american_2.0': 0, 'cat_Calgary_american_3.0': 0,
                'cat_Calgary_american_4.0': 0, 'cat_Calgary_american_nan': 0, 'cat_Calgary_chinese_1.0': 0,
                'cat_Calgary_chinese_2.0': 0, 'cat_Calgary_chinese_3.0': 0, 'cat_Calgary_chinese_nan': 0,
                'cat_Calgary_italian_1.0': 0, 'cat_Calgary_italian_2.0': 0, 'cat_Calgary_italian_3.0': 0,
                'cat_Calgary_italian_4.0': 0, 'cat_Calgary_italian_nan': 0, 'cat_Las Vegas_american_1.0': 0,
                'cat_Las Vegas_american_2.0': 0, 'cat_Las Vegas_american_3.0': 0, 'cat_Las Vegas_american_4.0': 0,
                'cat_Las Vegas_american_nan': 0, 'cat_Las Vegas_chinese_1.0': 0, 'cat_Las Vegas_chinese_2.0': 0,
                'cat_Las Vegas_chinese_3.0': 0, 'cat_Las Vegas_chinese_4.0': 0, 'cat_Las Vegas_chinese_nan': 0,
                'cat_Las Vegas_italian_1.0': 0, 'cat_Las Vegas_italian_2.0': 0, 'cat_Las Vegas_italian_3.0': 0,
                'cat_Las Vegas_italian_4.0': 0, 'cat_Las Vegas_italian_nan': 0, 'cat_Toronto_american_1.0': 0,
                'cat_Toronto_american_2.0': 0, 'cat_Toronto_american_3.0': 0, 'cat_Toronto_american_4.0': 0,
                'cat_Toronto_american_nan': 0, 'cat_Toronto_chinese_1.0': 0, 'cat_Toronto_chinese_2.0': 0,
                'cat_Toronto_chinese_3.0': 0, 'cat_Toronto_chinese_4.0': 0, 'cat_Toronto_chinese_nan': 0,
                'cat_Toronto_italian_1.0': 0, 'cat_Toronto_italian_2.0': 0, 'cat_Toronto_italian_3.0': 0,
                'cat_Toronto_italian_4.0': 0, 'cat_Toronto_italian_nan': 0}
    category = 'cat_' + city + '_' + cuisine.lower() + '_' + str(float(price))
    cat_dict[category] = 1

    inputs = np.array([
        bike_parking, accept_card, caters, coat_check, good_for_kids, happy_hour, has_tv, outdoor_seating, delivery,
        good_for_groups, reservations, table_service, take_out, wheelchair_accessible, f_hours, m_hours, sa_hours,
        su_hours, th_hours, tu_hours, w_hours, review_count, cat_dict['cat_Calgary_american_1.0'],
        cat_dict['cat_Calgary_american_2.0'], cat_dict['cat_Calgary_american_3.0'],
        cat_dict['cat_Calgary_american_4.0'], cat_dict['cat_Calgary_american_nan'],
        cat_dict['cat_Calgary_chinese_1.0'], cat_dict['cat_Calgary_chinese_2.0'], cat_dict['cat_Calgary_chinese_3.0'],
        cat_dict['cat_Calgary_chinese_nan'], cat_dict['cat_Calgary_italian_1.0'], cat_dict['cat_Calgary_italian_2.0'],
        cat_dict['cat_Calgary_italian_3.0'], cat_dict['cat_Calgary_italian_4.0'], cat_dict['cat_Calgary_italian_nan'],
        cat_dict['cat_Las Vegas_american_1.0'], cat_dict['cat_Las Vegas_american_2.0'],
        cat_dict['cat_Las Vegas_american_3.0'], cat_dict['cat_Las Vegas_american_4.0'],
        cat_dict['cat_Las Vegas_american_nan'], cat_dict['cat_Las Vegas_chinese_1.0'],
        cat_dict['cat_Las Vegas_chinese_2.0'], cat_dict['cat_Las Vegas_chinese_3.0'],
        cat_dict['cat_Las Vegas_chinese_4.0'], cat_dict['cat_Las Vegas_chinese_nan'],
        cat_dict['cat_Las Vegas_italian_1.0'], cat_dict['cat_Las Vegas_italian_2.0'],
        cat_dict['cat_Las Vegas_italian_3.0'], cat_dict['cat_Las Vegas_italian_4.0'],
        cat_dict['cat_Las Vegas_italian_nan'], cat_dict['cat_Toronto_american_1.0'],
        cat_dict['cat_Toronto_american_2.0'], cat_dict['cat_Toronto_american_3.0'],
        cat_dict['cat_Toronto_american_4.0'], cat_dict['cat_Toronto_american_nan'],
        cat_dict['cat_Toronto_chinese_1.0'], cat_dict['cat_Toronto_chinese_2.0'], cat_dict['cat_Toronto_chinese_3.0'],
        cat_dict['cat_Toronto_chinese_4.0'], cat_dict['cat_Toronto_chinese_nan'], cat_dict['cat_Toronto_italian_1.0'],
        cat_dict['cat_Toronto_italian_2.0'], cat_dict['cat_Toronto_italian_3.0'], cat_dict['cat_Toronto_italian_4.0'],
        cat_dict['cat_Toronto_italian_nan'], neg_reviews, neu_reviews, pos_reviews, romantic, intimate, classy,
        hipster, touristy, trendy, upscale, casual, good_for_dessert, good_for_late_night, good_for_lunch,
        good_for_dinner, good_for_breakfast, good_for_brunch, parking_garage, parking_street, parking_validated,
        parking_lot, parking_valet, total_hours, weekdays_early_opening, weekdays_late_closing, open_on_weekends,
        best_night_monday, best_night_tuesday, best_night_wednesday, best_night_thursday,
        best_night_friday, best_night_saturday, best_night_sunday, music_dj, music_background, no_music, music_karaoke,
        music_live, music_video, music_jukebox, full_bar, beer_and_wine, no_alcohol, smoking_outdoor,
        smoking_no, smoking_yes, free_wifi, no_wifi, paid_wifi, noise_average, noise_loud, noise_quiet,
        noise_very_loud, attire_casual, attire_dressy])
    inputs = inputs.reshape(1, -1)
    star_prediction = predict(inputs)
    stars = 5.0 if star_prediction > 5 else star_prediction
    stars = 1.0 if stars < 1 else stars
    return '{:.2f}'.format(stars)
