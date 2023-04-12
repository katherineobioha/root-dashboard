import json

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import hvplot as hv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.DataFrame({
    "x": [1,2,1,2,2],
    "y": [1,2,3,4, 2],
    "customdata": [1,2,3,4,5],
    "fruit": ["apple", "apple", "orange", "orange", "apple"]
})

fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=20)

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        # html.Div([
        #     dcc.Markdown("""
        #         **Hover Data**
        #
        #         Mouse over values in the graph.
        #     """),
        #     html.Pre(id='hover-data', style=styles['pre'])
        # ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')


    ])
])

#
# @app.callback(
#     Output('hover-data', 'children'),
#     Input('basic-interactions', 'hoverData'))
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    print(clickData)
    return json.dumps(clickData, indent=2)


# @app.callback(
#     Output('selected-data', 'children'),
#     [Input('basic-interactions', 'selectedData')])
# def display_selected_data(selectedData):
#     return json.dumps(selectedData, indent=2)
#
#
# @app.callback(
#     Output('relayout-data', 'children'),
#     [Input('basic-interactions', 'relayoutData')])
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
