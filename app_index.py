# app_index.py
# App index page, launch app with this script, run: python3 app_index.py

import dash
from app import app
from apps import insights, prediction
import dash_core_components as dcc
import dash_html_components as html

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Display 2 different page options
layout = html.Div([
    html.Div([
        dcc.Link('Restaurant Insights', href='/insights'),
        html.Br(),
        dcc.Link('Rating Prediction', href='/prediction')],
        style={'fontFamily': 'Century Gothic'})
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/insights':
        return insights.layout
    elif pathname == '/prediction':
        return prediction.layout
    else:
        return layout


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
app.run_server(debug=True)
