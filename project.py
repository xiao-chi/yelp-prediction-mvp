import flask
import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Restaurant Insights', href='/insights'),
    html.Br(),
    dcc.Link('Rating Prediction', href='/prediction'),
])

df = pd.read_csv('datasets/restaurants.csv')
available_cities = df['city'].unique()

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
cuisines = ['Italian', 'Pizza', 'Chinese', 'Indian', 'Steakhouses', 'Japanese', 'Mexican', 'American', 'Greek',
            'Thai', 'Fast Food', 'Bakeries', 'Canadian', 'Asian Fusion']

piedata = go.Pie(labels=pos_topics, values=pos_topics_avg)
piedata2 = go.Pie(labels=neg_topics, values=neg_topics_avg)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

insights_layout = html.Div(style={'fontFamily': 'helvetica'}, children=[
    html.H1(
        children='Restaurants Insight Dashboard',
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
    html.Iframe(id = 'map', srcDoc=open('vegas.html', 'r').read(), width='100%', height='600'),
    html.Div(id='insights-content'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

prediction_layout = html.Div([
    html.H1('Rating Prediction'),
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


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
app.run_server(debug=True)
