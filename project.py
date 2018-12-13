import flask
import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import statsmodels.api as sm

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

pos_topics_df = pd.read_csv('datasets/pos_reviews.csv')
neg_topics_df = pd.read_csv('datasets/neg_reviews.csv')

pos_topics = ['menu/experience', 'burger/fries', 'service/atmosphere', 'breakfast/pancakes', 'food',
              'location']
pos_topics_avg = []
for y in range(0, 6):
    avg = pos_topics_df[str(y)].mean()
    pos_topics_avg.append(avg * 100)

neg_topics = ['wait/table', 'burger/fries', 'bad service', 'chicken/salad', 'breakfast/eggs', 'buffet/price']
neg_topics_avg = []
for y in range(0, 6):
    avg = neg_topics_df[str(y)].mean()
    neg_topics_avg.append(avg * 100)

price_ranges = [1, 2, 3, 4]
cuisines = ['Italian', 'American', 'Chinese']

data = pd.read_csv('datasets/vegas_sme_dataset.csv')
y = data["stars"]
x = data[['ambience_classy', 'ambience_trendy', 'good_for_dinner', 'review_count', 'good_for_brunch', 'parking_garage',
          'parking_street', 'parking_lot', 'none', 'full_bar', 'bestnight_friday', 'wifi_free',
          'noise_quiet', 'negative_reviews']]
x1 = sm.add_constant(x)
model = sm.OLS(y.astype(float), x1.astype(float)).fit()


insights_layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
    html.H1(
        children='Restaurant Insights Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Dropdown(
        id='cities_dropdown',
        options=[{'label': i, 'value': i} for i in available_cities],
        value='Las Vegas',
        placeholder='City'
    ),
    dcc.Dropdown(
        id='cuisines_dropdown',
        options=[{'label': i, 'value': i} for i in cuisines],
        value='American',
        placeholder='Cuisine'
    ),
    dcc.Dropdown(
        id='price_ranges_dropdown',
        options=[{'label': i, 'value': i} for i in price_ranges],
        value=2,
        placeholder='Restaurant Price Range'
    ),
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


#PREDICTION API
prediction_layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
    html.H1(
        children='Rating Prediction',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        dcc.Dropdown(
            id='cities_dropdown_2',
            options=[{'label': i, 'value': i} for i in available_cities],
            value='Las Vegas',
            placeholder='City'
        )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='cuisines_dropdown_2',
        options=[{'label': i, 'value': i} for i in cuisines],
        value='American',
        placeholder='Cuisine'
    )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='price_ranges_dropdown_2',
        options=[{'label': i, 'value': i} for i in price_ranges],
        value=2,
        placeholder='Restaurant Price Range'
    )], style={'width': '33%', 'display': 'inline-block'}),

    #Column 1
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
            html.Div(['Ambience'], style={'font-weight': 'bold'}),
            dcc.Checklist(
                id='ambience_checkbox',
                options=[
                    {'label': 'Trendy', 'value': 'trendy'},
                    {'label': 'Romantic', 'value': 'romantic'},
                    {'label': 'Classy', 'value': 'classy'},
                    {'label': 'Casual', 'value': 'casual'},
                    {'label': 'Hipster', 'value': 'hipster'},
                    {'label': 'Touristy', 'value': 'touristy'}
                ],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
        html.Br(),
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
        html.Br(),
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
        html.Br(),
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
              [dash.dependencies.State('slider_noise', 'value'),
               dash.dependencies.State('slider_wifi', 'value'),
               dash.dependencies.State('slider_alcohol', 'value'),
               dash.dependencies.State('ambience_checkbox', 'values'),
               dash.dependencies.State('good_for_checkbox', 'values'),
               dash.dependencies.State('best_night_checkbox', 'values'),
               dash.dependencies.State('parking_checkbox', 'values'),
               dash.dependencies.State('neg_reviews_keypress', 'value'),
               dash.dependencies.State('review_count_keypress', 'value')
               ])
def prediction(n_clicks, noise_level, wifi, alcohol, ambiences, good_fors, best_nights,
               parkings, neg_reviews, review_count):
    free_wifi = False
    no_alcohol = False
    full_bar = False
    quiet = False
    trendy = False
    classy = False
    good_for_dinner = False
    good_for_brunch = False
    best_night_friday = False
    parking_garage = False
    parking_lot = False
    parking_street = False

    neg_reviews = int(neg_reviews)
    review_count = int(review_count)
    constant = 1.0

    free_wifi = True if wifi is 1 else False
    no_alcohol = True if alcohol is 0 else False
    full_bar = True if alcohol is 2 else False
    quiet = True if noise_level is 0 else False
    trendy = True if 'trendy' in ambiences else False
    classy = True if 'classy' in ambiences else False
    good_for_dinner = True if 'dinner' in good_fors else False
    good_for_brunch = True if 'brunch' in good_fors else False
    best_night_friday = True if 'Friday' in best_nights else False
    parking_garage = True if 'garage' in parkings else False
    parking_lot = True if 'lot' in parkings else False
    parking_street = True if 'street' in parkings else False
    inputs = [[constant, classy, trendy, good_for_dinner, review_count, good_for_brunch, parking_garage,
               parking_street, parking_lot, no_alcohol, full_bar, best_night_friday, free_wifi,
               quiet, neg_reviews]]

    star_prediction = model.predict(inputs)
    stars = 5.0 if star_prediction[0] > 5 else star_prediction[0]
    stars = 1.0 if stars < 1 else stars
    return '{:.2f}'.format(stars)


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
app.run_server(debug=True)