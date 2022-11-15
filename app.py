import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash_daq as daq
import requests
import calendar
import DBConnect as db
import readNews as news
from datetime import datetime
import json as json
from pandas import DataFrame
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
from plotly.subplots import make_subplots

import plotly.express as px

from datetime import datetime as dt
import hvplot.pandas




app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=[dbc.themes.LUX],
)
app.title = "Roots - Revemi"
server = app.server
##----------------------- call weather api
# def api_call(input_value="Ames,us"):
#     city = 'Delta'
#     state = 'Nigeria'
#     key = '399d8f4ee537173296522eb45d2f25b6'  # put api key here
#     r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}".format(city, state, key))
#     data = r.json()
#
#     day = [calendar.day_name[(datetime.strptime(data["list"][i]['dt_txt'].split(" ")[0], '%Y-%M-%d')).weekday()] for i
#            in range(3, 36, 8)]
#     description = [data["list"][i]["weather"][0]['description'] for i in range(3, 36, 8)]
#     temp = [round(data["list"][i]['main']['temp'] * (9 / 5) - 459.67) for i in range(3, 36, 8)]
#     wind_speed = [data["list"][i]['wind']['speed'] for i in range(3, 36, 8)]
#     humidity = [data["list"][i]['main']['humidity'] for i in range(3, 36, 8)]
#     df3 = pd.DataFrame(
#         data={'Day': day, 'Description': description, 'Temperature': temp, 'Humidity': humidity, 'Wind': wind_speed})
#
#     return df3

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

def api_call():
    latInitial =  5.544230
    lonInitial =  5.760269
    city = 'Delta'
    state = 'Nigeria'
    key = '399d8f4ee537173296522eb45d2f25b6'  # put api key here
   # r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}".format(city, state, key))
    r = requests.get("http://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}&units=imperial".format(latInitial, lonInitial, key))
    data = r.json()
    day = [calendar.day_name[(datetime.strptime((datetime.utcfromtimestamp(data["daily"][i]['dt']).strftime('%d-%m-%Y')),'%d-%m-%Y')).weekday()] for i
           in range(0, 5, 1)]
   # day = [calendar.day_name[(datetime.strptime(data["list"][i]['dt_txt'].split(" ")[0], '%Y-%M-%d')).weekday()] for i in range(3, 36, 8)]
    description = [html.Img(src="http://openweathermap.org/img/wn/"+data["daily"][i]["weather"][0]['icon']+".png") for i in range(0, 5, 1)]
    temp = [data["daily"][i]['temp']['min']for i in range(0, 5, 1)]
    tempMax = [data["daily"][i]['temp']['max'] for i in range(0, 5, 1)]
    wind_speed = [data["daily"][i]['wind_speed'] for i in range(0, 5, 1)]
    #humidity = [data["daily"][i]['humidity'] for i in range(0, 5, 1)]
    df = pd.DataFrame(
        data={'Day': day, 'Description': description, 'Temperature Low': temp,'Temperature High': tempMax, 'Wind': wind_speed})

    return df
#function from plotly example useful for parsing pandas dataframe into dash table.
def make_weather_table():
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    dtf = api_call()
    fontSize = "10px"
    table =[html.Tr([
						html.Th(['Day'],style={"font-size":fontSize}),html.Th([' '],style={"font-size":fontSize}),html.Th(['Low'],style={"font-size":fontSize}),html.Th(['High'],style={"font-size":fontSize}),html.Th(['Wind'],style={"font-size":fontSize})
					], className="center" )]
    for index, row in dtf.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([ row[i] ],style={"font-size":fontSize}, className="center") )
        table.append( html.Tr( html_row ) )

    return table

def getNews():
    newNews = news.getnews()
    neww= DataFrame(newNews)
    # print(neww)
    newss =[]
    for i in range(0,len(neww)):
        newss.append(html.Div([ html.Div(
                 [
                                                    html.A(
                                                        html.H5(neww.title[i], className="mt-0 mb-1"),
                                                        href=neww.link[i]
                                                    ),

                                                    # html.Small(newNews.description, className="text-success"),
                                                     html.Small(neww.published[i], className="text-success")

                                                ],
                                                className="media-body"
                                            ),]))#newNews.published, newNews.link, newNews.title, newNews.description

    return html.Div(newss)
# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Dictionary of important locations in New York
list_of_locations = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}

# Initialize data frame
df1 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv",
    dtype=object,
)
# df2 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data2.csv",
#     dtype=object,
# )
# df3 = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data3.csv",
#     dtype=object,
# )
# df = pd.concat([df1, df2, df3], axis=0)
df = pd.concat([df1], axis=0)
df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
df.index = df["Date/Time"]
df.drop("Date/Time", 1, inplace=True)
totalList = []
for month in df.groupby(df.index.month):
    dailyList = []
    for day in month[1].groupby(month[1].index.day):
        dailyList.append(day[1])
    totalList.append(dailyList)
totalList = np.array(totalList)

# Layout of Dash App


def farmerData():
    # percentdata = db.getpercent()
    # data = dict(
    #     # character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    #     # parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    #     # value=[10, 14, 12, 10, 2, 6, 6, 4, 4])
    #     character=["Total", "Men", "Women", "<30yrs", "<30yrs"],
    #     parent=["", "Total", "Total", "Men", "Women"],
    #     value=[percentdata["Total"], percentdata["Men"], percentdata["Women"], percentdata["Men30"],
    #            percentdata["Women30"]])
    #
    # fig = px.sunburst(
    #     data,
    #     names='character',
    #     parents='parent',
    #     values='value',
    # color_discrete_map={'(?)':'black', '(?)':'gold', '(?)':'darkblue'}, width=800, height=400)
    # fig.update_layout(uniformtext=dict(minsize=30))
    # return fig
    labels = [ "Men", "Women", "Men <30yrs", "Women <30yrs"]
    values = [ 1150, 1350, 600, 300]
    # fig = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    #                     subplot_titles=['<30 years', 'Total'])
    # fig.add_trace(go.Pie(labels=labels, values=[600, 300], scalegroup='one',
    #                      name="<30 years"), 1, 1)
    # fig.add_trace(go.Pie(labels=labels, values=[1150, 1350], scalegroup='one',
    #                      name="Total"), 1, 2)
    colors=["green", "darg green", "light green", "yellow"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update_traces( marker=dict(colors=colors))
    fig.update_layout(legend=dict(
        orientation="h",
        #yanchor="bottom",
        #y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout( paper_bgcolor='rgba(0,0,0,0)')
    return fig


app.layout = html.Div(
    children=[
        html.Div(
            className="row bordercontainer",
            children=[
                # Column for user controls
                dbc.Modal(
                    [   dbc.ModalHeader("Add Farmer", style={"color":"green"}),
                        dbc.FormText(
                            [
                                dbc.Label("Name", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="name-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ],
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Sex", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="sex-input",

                                    type="text"

                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Age", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="age-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Phone no", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="phone-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Farm Location", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="farm-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("LGA", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="lga-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Product", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="product-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        dbc.FormText(
                            [
                                dbc.Label("Farm size", size="md", style={"color":"green"}),
                                dcc.Input(
                                    id="size-input",

                                    type="text"
                                    # className="form-control",
                                ),
                            ]
                        ),
                        # dbc.Input("BODY OF MODAL"),

                        dbc.ModalFooter([
                            html.Button('SUBMIT', id='submit-val', n_clicks=0, style={"color":"green"}),
                            html.Button('CLOSE', id='close', n_clicks=0, style={"color":"green"}),
                            # dbc.Button("SUBMIT", id="", className="")
                            html.Div(id="container-button-basic", className="container-basic" )
                        ]),
                    ],
                    id="modal",
                ),
                html.Div(
                    className="card three columns dashboard-box div-user-controls-left",
                    children=[
                        html.Div(className="card-header",
                        children=[
                            dcc.Markdown("""
                                 Farmer Profile
                             """),
                        html.Button("Add Farmer",id='open-modal', n_clicks=0, style={"color":"white"})
                            #, style=styles['pre']
                        ]),
                        html.Div(className="card-body",
                        children=[
                            dcc.Markdown("""
                        
                                 Click on points in the graph to view farmers in that location.
                             """),
                            html.Pre(id='click-data' ),
                            #, style=styles['pre']
dbc.Row([
                                dbc.Col([
                                    dcc.Input(id='{}'.format(field), type='text', value='{}'.format(field))
                                ])
                            ]) for field in ["a", "b", "c"]
                        ]),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="card three columnlarge div-for-charts bg-grey dashboard-boxlarge",
                    children=[
                        html.Div(className="card-header",
                                 children=[
                                     dcc.Markdown("""
                                Map
                            """),
                                     # , style=styles['pre']
                                 ]),
                    html.Div(className="card-body",
                    children=[
                        dcc.Graph(id="map-graph")
                        # html.Div(
                        #     className="text-padding",
                        #     children=[
                        #         "Select any of the bars on the histogram to section data by time."
                        #     ],
                        # ),
                        # dcc.Graph(id="histogram"),
                        #dcc.Textarea(id="")
                    ]),
                    ],
                ),

              #column for another

                html.Div(
                    className=" card three columns div-user-controls-left dashboard-box",
                    children=[
                    html.Div(className="card-header",
                        children=[
                            dcc.Markdown("""
                                Food security risk
                             """),
                            #, style=styles['pre']
                        ]),
                    html.Div(className="card-body center-body",
                    children=[
                        # html.A(
                        #     html.Img(
                        #         className="logo",
                        #         src=app.get_asset_url("dash-logo-new.png"),
                        #     ),
                        #     href="https://plotly.com/dash/",
                        # ),

                        # html.P(id="grad1"),
                        # html.H2("Food security risk."),
                        daq.Gauge(
                            color={"gradient":True,"ranges":{"green":[0,3],"yellow":[3,7],"red":[7,10]}},
                            value=7,
                            size=200,

                            max=10,
                            min=0,
                        scale={
                                "custom": {
                                    1: {"label": "Low"},
                                    5: {"label": "Medium"},
                                    9: {"label": "High"},

                                }
                            },
                        ),
                    ]),
                    ],
                ),
                html.Div(
                    className="card three columns dashboard-box div-user-controls-left",
                    children=[
                        html.Div(className="card-header",
                                 children=[
                                     dcc.Markdown("""
                                Weather Information
                            """),
                                     # , style=styles['pre']
                                 ]),
                    html.Div(className="card-body",
                    children=[
                            #html.P("Weather Information", style={"textAlign": "center", "font-size": "20px"}),

                            html.Table(
                                make_weather_table()
                            ,style={"width":"2%", "border":"1px"}),

                    ]),
                    ],
                ),
                html.Div(
                    className="card three columns  dashboard-box",
        children=[
        html.Div(className="card-header",
                        children=[
                            dcc.Markdown("""
                                Information
                             """),
                            #, style=styles['pre']
                        ]),
            html.Div(className="card-body noBackground",
                    children=[
                        dbc.ListGroup(
                            [

                                    dbc.ListGroupItem(

                                    [
                                      getNews()
                                    ],className="media"
                                ),

                            ]),
                    ]),
                    ],
                ),
        html.Div(
                    className="card three columns div-for-charts dashboard-box",
            children=[
            html.Div(className="card-header",
                        children=[
                            dcc.Markdown("""
                                Total  - 2500 farmers
                             """),
                            #, style=styles['pre']
                        ]),
            html.Div(className="card-body piechartg ",
                    children=[
                        dcc.Graph(figure=farmerData())
                     ]
                    ),
                    ],
                ),

        html.Div(
                    className="card three columns  dashboard-box",
            children=[
            html.Div(className="card-header",
                        children=[
                            dcc.Markdown("""
                                Contact
                             """),
                            #, style=styles['pre']
                        ]),
            html.Div(className="card-body",
                    children=[
                dcc.Markdown("""
                               For any information or inquiries, contact us at
                               
                               
                             """),
                        dcc.Markdown("""
                              
                              Email: contact@revemi.com
                            """),
                    ]),
                    ],
                ),

            ],
        )
    ]
)

# Gets the amount of days in the specified month
# Index represents month (0 is April, 1 is May, ... etc.)
daysInMonth = [30, 31, 30, 31, 31, 30]

# Get index for the specified month in the dataframe
monthIndex = pd.Index(["Apr", "May", "June", "July", "Aug", "Sept"])

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(month, day, selection):
    xVal = []
    yVal = []
    xSelected = []
    colorVal = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]

    # Put selected times into a list of numbers xSelected
    xSelected.extend([int(x) for x in selection])

    for i in range(24):
        # If bar is selected then color it white
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = "#FFFFFF"
        xVal.append(i)
        # Get the number of rides at a particular time
        yVal.append(len(totalList[month][day][totalList[month][day].index.hour == i]))
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]


# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
# @app.callback(
#     Output("bar-selector", "value"),
#     [Input("histogram", "selectedData"), Input("histogram", "clickData")],
# )
# def update_bar_selector(value, clickData):
#     holder = []
#     if clickData:
#         holder.append(str(int(clickData["points"][0]["x"])))
#     if value:
#         for x in value["points"]:
#             holder.append(str(int(x["x"])))
#     return list(set(holder))

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    [State('name-input', 'value'),
    State('age-input', 'value'),
     State('farm-input', 'value'),State('phone-input', 'value'),
     State('lga-input', 'value'),State('sex-input', 'value'),
     State('product-input', 'value'),State('size-input', 'value')]

)
def update_output(n_clicks, value, value1, value2, value3, value4, value5, value6, value7):
    #return value ,value1, value2, value3, value4, value5, value6, value7
    # msg = " "
    # if "submit-val" == dash.callback_context.triggered:
    msg=' '
    try:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'submit-val' in changed_id:
            farmer = {"NAME":value,
                  "AGE": value1,
                  "FARM LOCATION":value2,
                  "PHONE NO": value3,
                  "LGA": value4,
                  "SEX": value5,
                  "PRODUCT TYPE": value6,
                  "FARM SIZE": value7
            }

            x= db.addFarmerToDB(farmer)
            print(farmer)
            msg = html.Div("You have succesfully saved the farmer. Click the close button.", style ={"color":"green", "align-content":"stretch","font-size":"11px", "border":"2px","border-color": "green"}, className="alert alert-success", role="alert")
    except:
        msg=html.Div("An error occured. Please contact the administrator.", style ={"color":"red", "align-content":"stretch","font-size":"11px", "border":"2px",
                                                                                          "border-color": "red"}, className="alert alert-danger", role="alert")
    return msg


@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



@app.callback(
    Output('click-data', 'children'),
    [Input('map-graph', 'clickData')])
def display_click_data(clickData):
    data=None
    if clickData is not None:
        # print()
        data =db.getFarmsByLocation(clickData["points"][0]["customdata"])
    if clickData is None:
        return ''
    return json.dumps(data, indent=2)

# Clear Selected Data if Click Data is used
# @app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
# def update_selected_data(clickData):
#     if clickData:
#         return {"points": []}
#
#
# # Update the total number of rides Tag
# @app.callback(Output("total-rides", "children"), [Input("date-picker", "date")])
# def update_total_rides(datePicked):
#     date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#     return "Total Number of rides: {:,d}".format(
#         len(totalList[date_picked.month - 4][date_picked.day - 1])
#     )
#
#
# # Update the total number of rides in selected times
# @app.callback(
#     [Output("total-rides-selection", "children"), Output("date-value", "children")],
#     [Input("date-picker", "date"), Input("bar-selector", "value")],
# )
# def update_total_rides_selection(datePicked, selection):
#     firstOutput = ""
#
#     if selection is not None or len(selection) is not 0:
#         date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#         totalInSelection = 0
#         for x in selection:
#             totalInSelection += len(
#                 totalList[date_picked.month - 4][date_picked.day - 1][
#                     totalList[date_picked.month - 4][date_picked.day - 1].index.hour
#                     == int(x)
#                 ]
#             )
#         firstOutput = "Total rides in selection: {:,d}".format(totalInSelection)
#
#     if (
#         datePicked is None
#         or selection is None
#         or len(selection) is 24
#         or len(selection) is 0
#     ):
#         return firstOutput, (datePicked, " - showing hour(s): All")
#
#     holder = sorted([int(x) for x in selection])
#
#     if holder == list(range(min(holder), max(holder) + 1)):
#         return (
#             firstOutput,
#             (
#                 datePicked,
#                 " - showing hour(s): ",
#                 holder[0],
#                 "-",
#                 holder[len(holder) - 1],
#             ),
#         )
#
#     holder_to_string = ", ".join(str(x) for x in holder)
#     return firstOutput, (datePicked, " - showing hour(s): ", holder_to_string)
#
#
# # Update Histogram Figure based on Month, Day and Times Chosen
# @app.callback(
#     Output("histogram", "figure"),
#     [Input("date-picker", "date"), Input("bar-selector", "value")],
# )
# def update_histogram(datePicked, selection):
#     date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#     monthPicked = date_picked.month - 4
#     dayPicked = date_picked.day - 1
#
#     [xVal, yVal, colorVal] = get_selection(monthPicked, dayPicked, selection)
#
#     layout = go.Layout(
#         bargap=0.01,
#         bargroupgap=0,
#         barmode="group",
#         margin=go.layout.Margin(l=10, r=0, t=0, b=50),
#         showlegend=False,
#         plot_bgcolor="#323130",
#         paper_bgcolor="#323130",
#         dragmode="select",
#         font=dict(color="white"),
#         xaxis=dict(
#             range=[-0.5, 23.5],
#             showgrid=False,
#             nticks=25,
#             fixedrange=True,
#             ticksuffix=":00",
#         ),
#         yaxis=dict(
#             range=[0, max(yVal) + max(yVal) / 4],
#             showticklabels=False,
#             showgrid=False,
#             fixedrange=True,
#             rangemode="nonnegative",
#             zeroline=False,
#         ),
#         annotations=[
#             dict(
#                 x=xi,
#                 y=yi,
#                 text=str(yi),
#                 xanchor="center",
#                 yanchor="bottom",
#                 showarrow=False,
#                 font=dict(color="white"),
#             )
#             for xi, yi in zip(xVal, yVal)
#         ],
#     )
#
#     return go.Figure(
#         data=[
#             go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
#             go.Scatter(
#                 opacity=0,
#                 x=xVal,
#                 y=yVal / 2,
#                 hoverinfo="none",
#                 mode="markers",
#                 marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
#                 visible=True,
#             ),
#         ],
#         layout=layout,
#     )
#

# Get the Coordinates of the chosen months, dates and times
def getLatLonColor(selectedData, month, day):
    listCoords = totalList[month][day]

    # No times selected, output all times for chosen month and date
    if selectedData is None or len(selectedData) is 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) is not len(selectedData) - 1:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)


# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        # Input("date-picker", "date"),
        # Input("bar-selector", "value"),
         Input("map-graph", 'selectedData'),
    ],
)
def update_graph( selectedData):
    zoom = 10.0
    latInitial = 5.6704358#5.7575982
    lonInitial = 5.8353837#5.3125705
    bearing = 0

    list_of_locations = db.getFarmLocation()
    # if selectedLocation:
    #     zoom = 15.0
    #     latInitial = list_of_locations[selectedLocation]["LOCATION"]["lat"]
    #     lonInitial = list_of_locations[selectedLocation]["LOCATION"]["lng"]
    x=0
    sizeGeoLoc={}
    ### count each farm location found
    for i in range(0,len(list_of_locations)):
        q=list_of_locations[i]["FARM LOCATION"]
        if list_of_locations[i]["FARM LOCATION"] in sizeGeoLoc:
            sizeGeoLoc[q]=sizeGeoLoc[q]+1
        else:
            sizeGeoLoc[q]=1
    print(sizeGeoLoc)
    # date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    # monthPicked = date_picked.month - 4
    # dayPicked = date_picked.day - 1
    # listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)

    f= go.Figure(
        data=[
            # Data for all rides based on date and time
            # Scattermapbox(
            #     lat=listCoords["Lat"],
            #     lon=listCoords["Lon"],
            #     mode="markers",
            #     hoverinfo="lat+lon+text",
            #     text=listCoords.index.hour,
            #     marker=dict(
            #         showscale=True,
            #         color=np.append(np.insert(listCoords.index.hour, 0, 0), 23),
            #         opacity=0.5,
            #         size=5,
            #         colorscale=[
            #             [0, "#F4EC15"],
            #             [0.04167, "#DAF017"],
            #             [0.0833, "#BBEC19"],
            #             [0.125, "#9DE81B"],
            #             [0.1667, "#80E41D"],
            #             [0.2083, "#66E01F"],
            #             [0.25, "#4CDC20"],
            #             [0.292, "#34D822"],
            #             [0.333, "#24D249"],
            #             [0.375, "#25D042"],
            #             [0.4167, "#26CC58"],
            #             [0.4583, "#28C86D"],
            #             [0.50, "#29C481"],
            #             [0.54167, "#2AC093"],
            #             [0.5833, "#2BBCA4"],
            #             [1.0, "#613099"],
            #         ],
            #         colorbar=dict(
            #             title="Time of<br>Day",
            #             x=0.93,
            #             xpad=0,
            #             nticks=24,
            #             tickfont=dict(color="#d8d8d8"),
            #             titlefont=dict(color="#d8d8d8"),
            #             thicknessmode="pixels",
            #         ),
            #     ),
            # ),
            # Plot of important locations on the map
            Scattermapbox(
                lat=[list_of_locations[i]["LOCATION"]["lat"] for i in range(0, len(list_of_locations))],
                lon=[list_of_locations[i]["LOCATION"]["lng"] for i in range(0, len(list_of_locations))],
                mode="markers",
                hoverinfo="text",
                customdata=[list_of_locations[i]["FARM LOCATION"] for i in range(0, len(list_of_locations))],
                marker=dict(size=8, color="#000000"),
                text= [sizeGeoLoc[i["FARM LOCATION"]] for i in list_of_locations]
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
               # accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="open-street-map", #dark
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 4, #12
                                        "mapbox.center.lon": " 5.8353837",#"-73.991251",
                                        "mapbox.center.lat":"5.6704358", #"40.7272",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )
    #clickMe(f.data[0].on_click)
    return f


def clickMe(clickEvent):
    return "Test click event"

# def update_graph(datePicked, selectedData, selectedLocation):
#     zoom = 12.0
#     latInitial = 40.7272#5.7575982
#     lonInitial = -73.991251#5.3125705
#     bearing = 0
#
#     if selectedLocation:
#         zoom = 15.0
#         latInitial = list_of_locations[selectedLocation]["lat"]
#         lonInitial = list_of_locations[selectedLocation]["lon"]
#
#     date_picked = dt.strptime(datePicked, "%Y-%m-%d")
#     monthPicked = date_picked.month - 4
#     dayPicked = date_picked.day - 1
#     listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)
#
#     return go.Figure(
#         data=[
#             # Data for all rides based on date and time
#             # Scattermapbox(
#             #     lat=listCoords["Lat"],
#             #     lon=listCoords["Lon"],
#             #     mode="markers",
#             #     hoverinfo="lat+lon+text",
#             #     text=listCoords.index.hour,
#             #     marker=dict(
#             #         showscale=True,
#             #         color=np.append(np.insert(listCoords.index.hour, 0, 0), 23),
#             #         opacity=0.5,
#             #         size=5,
#             #         colorscale=[
#             #             [0, "#F4EC15"],
#             #             [0.04167, "#DAF017"],
#             #             [0.0833, "#BBEC19"],
#             #             [0.125, "#9DE81B"],
#             #             [0.1667, "#80E41D"],
#             #             [0.2083, "#66E01F"],
#             #             [0.25, "#4CDC20"],
#             #             [0.292, "#34D822"],
#             #             [0.333, "#24D249"],
#             #             [0.375, "#25D042"],
#             #             [0.4167, "#26CC58"],
#             #             [0.4583, "#28C86D"],
#             #             [0.50, "#29C481"],
#             #             [0.54167, "#2AC093"],
#             #             [0.5833, "#2BBCA4"],
#             #             [1.0, "#613099"],
#             #         ],
#             #         colorbar=dict(
#             #             title="Time of<br>Day",
#             #             x=0.93,
#             #             xpad=0,
#             #             nticks=24,
#             #             tickfont=dict(color="#d8d8d8"),
#             #             titlefont=dict(color="#d8d8d8"),
#             #             thicknessmode="pixels",
#             #         ),
#             #     ),
#             # ),
#             # Plot of important locations on the map
#             Scattermapbox(
#                 lat=[list_of_locations[i]["lat"] for i in list_of_locations],
#                 lon=[list_of_locations[i]["lon"] for i in list_of_locations],
#                 mode="markers",
#                 hoverinfo="text",
#                 text=[i for i in list_of_locations],
#                 marker=dict(size=8, color="#000000"),
#             ),
#         ],
#         layout=Layout(
#             autosize=True,
#             margin=go.layout.Margin(l=0, r=35, t=0, b=0),
#             showlegend=False,
#             mapbox=dict(
#                # accesstoken=mapbox_access_token,
#                 center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
#                 style="open-street-map", #dark
#                 bearing=bearing,
#                 zoom=zoom,
#             ),
#             updatemenus=[
#                 dict(
#                     buttons=(
#                         [
#                             dict(
#                                 args=[
#                                     {
#                                         "mapbox.zoom": 12,
#                                         "mapbox.center.lon": "-73.991251",
#                                         "mapbox.center.lat": "40.7272",
#                                         "mapbox.bearing": 0,
#                                         "mapbox.style": "dark",
#                                     }
#                                 ],
#                                 label="Reset Zoom",
#                                 method="relayout",
#                             )
#                         ]
#                     ),
#                     direction="left",
#                     pad={"r": 0, "t": 0, "b": 0, "l": 0},
#                     showactive=False,
#                     type="buttons",
#                     x=0.45,
#                     y=0.02,
#                     xanchor="left",
#                     yanchor="bottom",
#                     bgcolor="#323130",
#                     borderwidth=1,
#                     bordercolor="#6d6d6d",
#                     font=dict(color="#FFFFFF"),
#                 )
#             ],
#         ),
#     )


if __name__ == "__main__":
    app.run_server(debug=True)
