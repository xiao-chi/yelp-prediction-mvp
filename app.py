import flask
import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
from yelp_predict import predict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
server.debug = True
server.secret_key = 'development key'

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

colors = {
    'text': '#B70000'
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.Div([
        dcc.Link('Restaurant Insights', href='/insights'),
        html.Br(),
        dcc.Link('Rating Prediction', href='/prediction')],
        style={'fontFamily': 'Century Gothic'})
])

available_cities = ['Las Vegas', 'Calgary', 'Toronto']

price_ranges = [1, 2, 3, 4]
cuisines = ['Italian', 'American', 'Chinese']

insights_layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
    html.H1(
        children='Restaurant Insights Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        html.Div(['City'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='cities_dropdown',
            options=[{'label': i, 'value': i} for i in available_cities],
            value='Las Vegas',
            placeholder='City'
        )]),
    html.Div([
        html.Div(['Cuisine'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='cuisines_dropdown',
            options=[{'label': i, 'value': i} for i in cuisines],
            value='American',
        )]),
    html.Div([
        html.Div(['Price Range'], style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='price_ranges_dropdown',
            options=[{'label': i, 'value': i} for i in price_ranges],
            value=2,
        )]),
    html.Iframe(id='map', srcDoc=open('maps/lasvegas_american_2.html', 'r').read(), width='100%', height='600'),
    html.Div(id='insights-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


@app.callback(dash.dependencies.Output('map', 'srcDoc'),
              [dash.dependencies.Input('cities_dropdown', 'value'),
               dash.dependencies.Input('cuisines_dropdown', 'value'),
               dash.dependencies.Input('price_ranges_dropdown', 'value')
               ])
def render_map(city, cuisine, price_range):
    city = city.replace(" ", "")
    file_to_open = 'maps/' + city + '_' + cuisine + '_' + str(price_range) + '.html'
    file_to_open = file_to_open.lower()
    return open(file_to_open, 'r').read()


# PREDICTION API
prediction_layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
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
            options=[{'label': i, 'value': i} for i in price_ranges],
            value=2,
        )], style={'width': '33%', 'display': 'inline-block'}),

    # Column 1
    html.Div([
        html.H3(children="Business Features"),
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
            html.Div(['Music'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='music_checkbox',
                options=[
                    {'label': 'None', 'value': 'none'},
                    {'label': 'Background', 'value': 'background'},
                    {'label': 'Live', 'value': 'live'},
                    {'label': 'DJ', 'value': 'dj'},
                    {'label': 'Karaoke', 'value': 'karaoke'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )]
        ),
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
                    {'label': 'Intimate', 'value': 'intimate'}
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
            ])
        ], style={'width': '33%', 'display': 'inline-block'}),
    # Column 2
    html.Div([
        html.H3(children="Prediction after 6 months"),
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
        html.Button(id='submit_button', n_clicks=0, children='Submit')],
        style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top'}),

    # Column 3
    html.Div([
        html.H3('Yelp Rating Prediction'),
        html.H1(children='0.0', id='rating_prediction')],
        style={'width': '33%', 'display': 'inline-block', 'float': 'right'}),
    html.Div(id='prediction-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/insights':
        return insights_layout
    elif pathname == '/prediction':
        return prediction_layout
    else:
        return index_page


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
               dash.dependencies.State('music_checkbox', 'values'),
               dash.dependencies.State('ambience_checkbox', 'values'),
               dash.dependencies.State('good_for_checkbox', 'values'),
               dash.dependencies.State('best_night_checkbox', 'values'),
               dash.dependencies.State('parking_checkbox', 'values'),
               dash.dependencies.State('pos_reviews_keypress', 'value'),
               dash.dependencies.State('neu_reviews_keypress', 'value'),
               dash.dependencies.State('neg_reviews_keypress', 'value'),
               dash.dependencies.State('review_count_keypress', 'value')
               ])
def prediction(n_clicks, city, cuisine, price, noise_level, wifi, alcohol, musics, ambiences, good_fors, best_nights,
               parkings, pos_reviews, neu_reviews, neg_reviews, review_count):
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

    trendy = 1 if 'trendy' in ambiences else 0
    classy = 1 if 'classy' in ambiences else 0
    romantic = 1 if 'romantic' in ambiences else 0
    intimate = 1 if 'intimate' in ambiences else 0
    hipster = 1 if 'hipster' in ambiences else 0
    casual = 1 if 'casual' in ambiences else 0

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

    no_music = 1 if 'none' in musics else 0
    music_dj = 1 if 'dj' in musics else 0
    music_live = 1 if 'live' in musics else 0
    music_background = 1 if 'background' in musics else 0
    music_karaoke = 1 if 'karaoke' in musics else 0

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

    y = ['BikeParking', 'BusinessAcceptsCreditCards', 'Caters', 'CoatCheck', 'GoodForKids', 'HappyHour', 'HasTV',
         'OutdoorSeating', 'RestaurantsDelivery', 'RestaurantsGoodForGroups', 'RestaurantsReservations',
         'RestaurantsTableService', 'RestaurantsTakeOut', 'WheelchairAccessible', 'Friday', 'Monday', 'Saturday',
         'Sunday', 'Thursday', 'Tuesday', 'Wednesday', review_count, 'cat_Calgary_american_1.0',
         'cat_Calgary_american_2.0',
         'cat_Calgary_american_3.0', 'cat_Calgary_american_4.0', 'cat_Calgary_american_nan',
         'cat_Calgary_chinese_1.0', 'cat_Calgary_chinese_2.0', 'cat_Calgary_chinese_3.0', 'cat_Calgary_chinese_nan',
         'cat_Calgary_italian_1.0', 'cat_Calgary_italian_2.0', 'cat_Calgary_italian_3.0', 'cat_Calgary_italian_4.0',
         'cat_Calgary_italian_nan', 'cat_Las Vegas_american_1.0', 'cat_Las Vegas_american_2.0',
         'cat_Las Vegas_american_3.0',
         'cat_Las Vegas_american_4.0', 'cat_Las Vegas_american_nan', 'cat_Las Vegas_chinese_1.0',
         'cat_Las Vegas_chinese_2.0',
         'cat_Las Vegas_chinese_3.0', 'cat_Las Vegas_chinese_4.0', 'cat_Las Vegas_chinese_nan',
         'cat_Las Vegas_italian_1.0',
         'cat_Las Vegas_italian_2.0', 'cat_Las Vegas_italian_3.0', 'cat_Las Vegas_italian_4.0',
         'cat_Las Vegas_italian_nan',
         'cat_Toronto_american_1.0', 'cat_Toronto_american_2.0', 'cat_Toronto_american_3.0', 'cat_Toronto_american_4.0',
         'cat_Toronto_american_nan', 'cat_Toronto_chinese_1.0', 'cat_Toronto_chinese_2.0', 'cat_Toronto_chinese_3.0',
         'cat_Toronto_chinese_4.0', 'cat_Toronto_chinese_nan', 'cat_Toronto_italian_1.0', 'cat_Toronto_italian_2.0',
         'cat_Toronto_italian_3.0', 'cat_Toronto_italian_4.0', 'cat_Toronto_italian_nan', neg_reviews,
         neu_reviews, pos_reviews, romantic, intimate, classy,
         hipster, 'ambience_touristy', trendy, 'ambience_upscale', casual,
         good_for_dessert, good_for_late_night, good_for_lunch, good_for_dinner, good_for_breakfast,
         good_for_brunch, parking_garage, parking_street, parking_validated, parking_lot, parking_valet,
         'TotalOpenTimeInWeek', 'NumberOfWeekdaysWithEarlyOpening', 'NumberOfWeekdaysWithLateClosing', 'OpenOnWeekends',
         best_night_monday, best_night_tuesday, best_night_wednesday, best_night_thursday, best_night_friday,
         best_night_saturday, best_night_sunday, music_dj, music_background, no_music, music_karaoke,
         music_live, 'music_video', 'music_jukebox', full_bar, beer_and_wine, no_alcohol, 'smoking_outdoor',
         'smoking_no', 'smoking_yes', free_wifi, no_wifi, paid_wifi, noise_average, noise_loud, noise_quiet,
         noise_very_loud, 0, 0]
    inputs = np.array([])
    inputs = inputs.reshape(1, -1)
    star_prediction = predict(inputs)
    stars = 5.0 if star_prediction > 5 else star_prediction
    stars = 1.0 if stars < 1 else stars
    return '{:.2f}'.format(stars)


if __name__ == '__main__':
    app.run_server(debug=False, port=8050, host='127.0.0.1')
app.run_server(debug=False)
