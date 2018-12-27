# insights.py
# Restaurant Insights Layout Page

import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app

colors = {'text': '#B70000'}
available_cities = ['Las Vegas', 'Calgary', 'Toronto']
three_price_ranges = [1, 2, 3]
all_price_ranges = [1, 2, 3, 4]
cuisines = ['Italian', 'American', 'Chinese']

# INSIGHTS API
layout = html.Div(style={'fontFamily': 'Century Gothic'}, children=[
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
            options=[{'label': i, 'value': i} for i in all_price_ranges],
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
