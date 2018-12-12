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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Restaurant Insights', href='/insights'),
    html.Br(),
    dcc.Link('Rating Prediction', href='/prediction'),
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

price_range = [1, 2, 3, 4]
cuisines = ['Italian', 'American', 'Chinese']

data = pd.read_csv('datasets/vegas_sme_dataset.csv')
y = data["stars"]
x = data[['ambience_trendy', 'good_for_dinner', 'review_count', 'good_for_brunch', 'parking_garage',
              'parking_street', 'parking_lot', 'noise_quiet', 'negative_reviews']]
x = sm.add_constant(x)
model = sm.OLS(y.astype(float), x.astype(float)).fit()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

insights_layout = html.Div(style={'fontFamily': 'helvetica'}, children=[
    html.H1(
        children='Restaurants Insights Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        dcc.Dropdown(
            id='crossfilter-xaxis-column1',
            options=[{'label': i, 'value': i} for i in price_range],
            value='Price Range',
            placeholder='Restaurant Price Range',
            searchable=True
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='crossfilter-xaxis-column2',
            options=[{'label': i, 'value': i} for i in cuisines],
            value='Cuisines',
            placeholder='Cuisine',
            searchable=True
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='crossfilter-xaxis-column3',
            options=[{'label': i, 'value': i} for i in available_cities],
            value='City',
            placeholder='City',
            searchable=True
        )
    ]),
    html.Iframe(id='map', srcDoc=open('vegas.html', 'r').read(), width='100%', height='600'),
    html.Div(id='insights-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

prediction_layout = html.Div(children=[
    html.H1(
        children='Rating Prediction',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        html.Label('Noise Level'),
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
        html.Label('Ambience'),
        dcc.Checklist(
            id='ambience_checkbox',
            options=[
                {'label': 'Trendy', 'value': 'trendy'},
                {'label': 'Romantic', 'value': 'romantic'},
                {'label': 'Classy', 'value': 'classy'},
                {'label': 'Intimate', 'value': 'intimate'},
                {'label': 'Casual', 'value': 'casual'},
                {'label': 'Hipster', 'value': 'hipster'},
                {'label': 'Touristy', 'value': 'touristy'},
                {'label': 'Upscale', 'value': 'upscale'}
            ],
            values=[],
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Br(),
    html.Div([
        html.Label('Good For'),
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
        html.Label('Parking'),
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
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Br(),
    html.Div([
        html.Label('Number of Negative Reviews'),
        dcc.Input(id='neg_reviews_keypress', type='number', min='0', value='0'),
    ]),
    html.Br(),
    html.Div([
        html.Label('Total Number of Reviews'),
        dcc.Input(id='review_count_keypress', type='number', min='0', value='0'),
    ]),
    #html.Button(id='submit_button', n_clicks=0, children='Submit'),
    html.Br(),
    html.Label('Yelp Rating Prediction'),
    html.H1(children='0.0', id='rating_prediction'),
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


@app.callback(dash.dependencies.Output('rating_prediction', 'children'),
              #[dash.dependencies.Input('submit_button', 'n_clicks')], add to parameter
              [dash.dependencies.Input('slider_noise', 'value'),
               dash.dependencies.Input('ambience_checkbox', 'values'),
               dash.dependencies.Input('good_for_checkbox', 'values'),
               dash.dependencies.Input('parking_checkbox', 'values'),
               dash.dependencies.Input('neg_reviews_keypress', 'value'),
               dash.dependencies.Input('review_count_keypress', 'value')
               ])
def prediction(noise_level, ambiences, good_fors, parkings, neg_reviews, review_count):
    trendy = False
    good_for_dinner = False
    good_for_brunch = False
    parking_garage = False
    parking_street = False
    parking_lot = False
    quiet = False
    constant = 1.0

    neg_reviews = int(neg_reviews)
    review_count = int(review_count)

    quiet = True if noise_level is 0 else False
    trendy = True if 'trendy' in ambiences else False
    good_for_brunch = True if 'brunch' in good_fors else False
    good_for_dinner = True if 'dinner' in good_fors else False
    parking_garage = True if 'garage' in parkings else False
    parking_lot = True if 'lot' in parkings else False
    parking_street = True if 'street' in parkings else False
    inputs = [[constant, trendy, good_for_dinner, review_count, good_for_brunch, parking_garage,
               parking_street, parking_lot, quiet, neg_reviews]]
    star_prediction = model.predict(inputs)
    stars = 5.0 if star_prediction[0] > 5 else star_prediction[0]
    return '{:.2f}'.format(stars)


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
app.run_server(debug=True)