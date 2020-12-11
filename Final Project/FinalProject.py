import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table

from dash.dependencies import Input, Output
import plotly.offline as offline
import chart_studio.plotly as py

# HEROKU STEPS
# -----------------------
# heroku login
# git init
# heroku git:remote -a dsc-data608project
# git add .
# git commit -am "nitial launch"
# git push heroku master


# -----------------------------------------------------------------------------
# DATA LOAD

protests = pd.read_csv(
    r'https://raw.githubusercontent.com/dhairavc/DATA608-KnowledgeAndVisualAnalytics/master/Final%20Project/Protests.csv',
    encoding='unicode_escape')

protests["Date"] = pd.to_datetime(protests['Date'], infer_datetime_format=False)
protest_dates = (protests["Date"].drop_duplicates()).reindex()
protest_dates2 = ((protests[["Stitle", "Date", "Title"]]).drop_duplicates()).reset_index(drop=True)

# p_table = protest_dates2[["Title"]]
# p_table.columns = ["Date"]

arr_2020 = pd.read_csv(
    r'https://raw.githubusercontent.com/dhairavc/DATA608-KnowledgeAndVisualAnalytics/master/Final%20Project/2020.csv',
    encoding='unicode_escape')

arr_2020["ARREST_DATE2"] = pd.to_datetime(arr_2020['ARREST_DATE2'], infer_datetime_format=False)

map_token = "pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg"

# ----------------------------------------------------------------------------
# ALL PROTESTS

style4 = "mapbox://styles/mapbox/light-v10"

protest_map = [go.Scattermapbox(
    lat=protests["Latitude"],
    lon=protests["Longitude"],
    hovertext=protests["Stitle"] + " :" + protests["Location"],
    mode='markers',
    marker=dict(
        size=8 * protests["Scale"],
        color='red',
        opacity=.3)
)]

protest_layout = go.Layout(autosize=True,
                           margin = dict(l = 5, r = 5, t = 5, b = 5),
                           mapbox=dict(accesstoken=map_token,
                                       bearing=10,
                                       pitch=50,
                                       zoom=12,
                                       center=dict(lat=40.721319, lon=-73.987130),
                                       style=style4),
                           width=1000,
                           height=800,
                           )

protests_fig = dict(data=protest_map, layout=protest_layout)
# ------------------------------------------------------------------------------

# ALL 2020 ARRESTS
arr_all = arr_2020.groupby(["ARREST_DATE2"]).count().reset_index()
arr_all = arr_all[["ARREST_DATE2", "ARREST_KEY"]]
# table2 = table[table["OFNS_DESC"]=="SEX CRIMES"]

arr_all["Rolling_7avg"] = arr_all.ARREST_KEY.rolling(7, min_periods=4).mean().round()
arr_all_fig = px.scatter(arr_all, x="ARREST_DATE2",
                         y="Rolling_7avg",
                         title="All 2020 Arrests (7 Day Average)",
                         labels={"ARREST_DATE2": "Date", "Rolling_7avg": "Arrest Count"}
                         )

arr_all_fig.update_traces(mode="lines")

arr_all_fig.add_shape(
    type="line",
    x0="2020-03-20",
    x1="2020-03-20",
    y0=0,
    y1=610,
    #y1=((arr_all[arr_all["ARREST_DATE2"] == "2020-03-20"])["Rolling_7avg"].values[0] + 50),
    line=dict(
        color="MediumPurple",
        width=1,
        dash="dashdot"
    )
)  # end Shape

arr_all_fig.add_shape(
    type="line",
    x0="2020-05-25",
    x1="2020-05-25",
    y0=0,
    y1=610,
    #y1=((arr_all[arr_all["ARREST_DATE2"] == "2020-05-25"])["Rolling_7avg"].values[0] + 50),
    line=dict(
        color="Green",
        width=1,
        dash="dashdot"
    )
)  # end Shape

arr_all_fig.add_annotation(
    text="NYC stay-at-home order",
    x="2020-03-20",
    y=5,
    # xshift=-60
)

arr_all_fig.add_annotation(
    text="George Floyd Death",
    x="2020-05-25",
    y=5,
    # xshift=-60
)

arr_all_fig.update_layout(
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    ))
# -------------------------------------------------------------------------------


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
external_stylesheets = ["https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-uber-rides-demo/assets/style.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# ------------------------------------------------------------------------------
# App layout


app.layout = html.Div( children=[

    # div1
    html.Div([
        html.H2(children='Data 608 - Final Project: BLM Protests'),
        html.H4(children='Dhairav Chhatbar'),

    ]),  # end div1

    # Div Text
    html.Div([

        html.P(
            "The year 2020 has been definitely a unique year around the world there were so many issues occurring concurrently such as the COVID-19 pandemic, racial injustice protest, climate change activism, etc."),
        html.P(
            "Here the focus is on the Black Lives Matter (BLM) racial injustice movement. There is a split consensus across the country on the “peacefulness” of the protests that have resulted from this movement. The two diverging consensus points have been that a portion of the country believes that these are peaceful protests and another part believes that these are not peaceful protests and is riddled by looting and anti-law enforcement sentiment."),
        html.P(
            "It is true that there has been looting and violence in these protests, however to claim that the BLM movement itself is entirely riddled by looting is an opinion. Does the data show a similar view for the NYC area?"),
        html.P(
            "Following the death of George Floyd various protests had erupted across NYC. These protests occurred in various times of the day, attended with varying sizes from 100s of people to thousands. The exact documentation and data on the protests is not conclusive, though according to Wikipedia there were protests on the following dates:"),
        dcc.Markdown('''
         * May: 28th, 29th, 30th, 31st
         * June: 1st, 2nd, 3rd, 4th, 5th, 7th, 8th, 9th, 10th, 11th, 12th, 14th, 23rd
         * July: 28th
         * September: 4th, 5th
         * October: 3rd           
        '''),
        html.P(
            "The data from protests can be compared with data from arrests that occurred in the same time period. NYC OpenData provides a dataset of all arrests made by the New York City Police Department. This can be overlaid with the protest data and knowing some timeline of events such as:"),
        dcc.Markdown('''
         * March 20th: New York's Stay-At-Home order goes into effect
         * May 25th:  The death of George Floyd      
        '''),
        html.P(
            "With these 3 elements in place, we may better understand if the Black Live Matter protests were entirely full of looting")

    ]),

    # div arrests
    html.Div([
        html.Br(),
        html.Br(),
        dcc.Markdown('''**All Documented BLM Protests**'''),
        dcc.Graph(
            id='all_protest_map',
            figure=protests_fig)

    ],style={'textAlign': 'center'}),

    html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Markdown('''**BLM Protests Dashboard**''')

    ],style={'textAlign': 'center'}),
    # div2
    html.Div([

        dcc.Graph(id='protests_arrests',
                  hoverData={'points': 'customdata'},
                  figure={}),
        dcc.Slider(
            id="sel_date",
            min=0,
            max=len(protest_dates2),
            value=0,
            marks=pd.Series(protest_dates2.Stitle.values, index=protest_dates2.index).to_dict(),
            updatemode="drag"
        )
    ], style={'width': '49%', 'display': 'inline-block'}),  # end div2

    # div3: barchart and series
    html.Div([

        dcc.Graph(id='bar_chart', hoverData="customdata2", figure={}),
        dcc.Graph(id="series_chart", figure={})

    ], style={'display': 'inline-block', 'width': '49%','padding': '0:20'}),  # end div 3

    html.Div([
        html.Br(),
        dcc.Graph(
            id='all_arrests',
            figure=arr_all_fig)

    ]),

    html.Div([
        dcc.Markdown('''**General Obserations and Conclusions**'''),
        html.P(
            "The the arrest time series data we see that the 7 day average for arrests in general have been trending down after the NYC stay-at-home order. After a bottom in April crime in general had been trending up. Following the death of George Floyd there was an up tick in arrests, specifically these up-tick offenses are Offenses Against Public Administration, Offenses against Public Order, and Burglary, all of which spiked during the protests. An interesting observation is that Dangerous Drug arrests which were trending down after the BLM protests."),
        html.P(
            "It is worthwhile noting that while there was a spike in arrests, the level of arrests was well below the level of arrests prior to the Stay-At-Home order. While there were times on mischief and looting, these instances given the data seem to be taken out of context and generalized for the overall BLM movement in NYC.")
    ]),

    html.Div([
        html.Br(),
        dcc.Markdown('''**References:**'''),
        dcc.Link('George Floyd protests in New York City',
                 href='https://en.wikipedia.org/wiki/George_Floyd_protests_in_New_York_City'),
        html.Br(),
        dcc.Link("NYPD Arrest Data (Year to Date)",
                 href="https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc")
    ])

])  # end main div


# -----------------------------------------------------------------------------
# App Callback map
@app.callback(
    dash.dependencies.Output('protests_arrests', 'figure'),
    [Input(component_id='sel_date', component_property='value')]
)
def update_map(date_selected):
    protests_df = protests[protests["Date"] == protest_dates2["Date"][date_selected]]
    arr_df = arr_2020[arr_2020["ARREST_DATE2"] == protest_dates2["Date"][date_selected]]

    protest_arrest_map = [
        go.Scattermapbox(
            name="Protests",
            lat=protests_df["Latitude"],
            lon=protests_df["Longitude"],
            hovertext=protests_df["Location"],
            mode='markers',
            marker=dict(
                size=5 * protests_df["Scale"],
                # size_max = protests_df["Scale"],
                color='red',
                opacity=.3)),

        go.Scattermapbox(
            name="Arrests",
            lat=arr_df["Latitude"],
            lon=arr_df["Longitude"],
            hovertext=arr_df["OFNS_DESC"],
            mode='markers',
            marker=dict(
                size=8,
                color='green',
                opacity=.3))
    ]

    protest_arrest_layout = go.Layout(autosize=True,
                                      margin = dict(l = 5, r = 5, t = 5, b = 5),
                                      mapbox=dict(accesstoken=map_token,
                                                  bearing=10,
                                                  pitch=50,
                                                  zoom=11,
                                                  center=dict(lat=40.721319, lon=-73.987130),
                                                  style=style4),
                                      width=900,
                                      height=900,
                                      showlegend=False,
                                      #legend_orientation="h",
                                      # legend_yanchor="top",
                                      # legend_xanchor="center"
                                      )

    protests_arrest_fig = dict(data=protest_arrest_map, layout=protest_arrest_layout)

    return protests_arrest_fig


# app callback, barchart
@app.callback(
    dash.dependencies.Output('bar_chart', 'figure'),
    [
        Input(component_id='sel_date', component_property='value')
    ])
def update_barchart(date_selected):
    print(date_selected)
    print(protest_dates2["Date"][date_selected])
    arr_df = arr_2020[arr_2020["ARREST_DATE2"] == protest_dates2["Date"][date_selected]]
    arr_offences = ((arr_df["OFNS_DESC"].value_counts()).to_frame()).head(10)
    arr_offences["Offense"] = arr_offences.index
   
    
    bar_chart = px.bar(data_frame=arr_offences,
                       x="Offense",
                       y="OFNS_DESC",
                       width=900,
                       height=500,
                       title="Top 10 Offenses on " + str(protest_dates2["Title"][date_selected]),
                       labels={"Offense": "Offense Type", "OFNS_DESC": "Count"}
                       )
    bar_chart.update_layout(
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    ))
    return bar_chart


# app callback, serieschart
@app.callback(
    dash.dependencies.Output('series_chart', 'figure'),
    [
        Input(component_id='protests_arrests', component_property='hoverData'),
        Input(component_id="bar_chart", component_property="hoverData")
    ])
def update_serieschart(hoverData, hoverData_bar):
    hovered = dash.callback_context
    #print(hovered.triggered[0])
    if hovered.triggered[0]["prop_id"] == "protests_arrests.hoverData":
        if hoverData['points'][0]['curveNumber']==1:
          crime_type = hoverData['points'][0]['hovertext']
        #if hoverData['points'][0]['curveNumber']==0:
         #   return
        
    if hovered.triggered[0]["prop_id"]=="bar_chart.hoverData":
        crime_type = hoverData_bar['points'][0]['x']

    crime_series = arr_2020[arr_2020["OFNS_DESC"] == crime_type]
    crime_series = crime_series.groupby(["ARREST_DATE2", "OFNS_DESC"]).count().reset_index()
    crime_series = crime_series[["ARREST_DATE2", "OFNS_DESC", "ARREST_KEY"]]
    crime_series["Rolling_Avg"] = crime_series.ARREST_KEY.rolling(7, min_periods=5).mean().round()

    serieschart = px.scatter(crime_series, 
                             width=900,
                             x="ARREST_DATE2",
                             y="Rolling_Avg",
                             title=" 7 Day Average: " + crime_type,
                             labels={"ARREST_DATE2": "Arrests", "Rolling_Avg": "Count"},
                             )
    serieschart.update_traces(mode="lines")
    serieschart.add_shape(
        type="line",
        x0="2020-03-20",
        x1="2020-03-20",
        y0=0,
        y1=110,
        #y1=((crime_series[crime_series["ARREST_DATE2"] == "2020-03-20"])["Rolling_Avg"].values[0] + 15),
        line=dict(
            color="MediumPurple",
            width=1,
            dash="dashdot"
        )
    )  # end Shape

    serieschart.add_shape(
        type="line",
        x0="2020-05-25",
        x1="2020-05-25",
        y0=0,
        y1=110,
        #y1=((crime_series[crime_series["ARREST_DATE2"] == "2020-05-25"])["Rolling_Avg"].values[0] + 15),
        line=dict(
            color="Green",
            width=1,
            dash="dashdot"
        )
    )  # end Shape

    serieschart.add_annotation(
        text="NYC stay-at-home order",
        x="2020-03-20",
        y=100,
        showarrow=False,
        xshift=-95
    )

    serieschart.add_annotation(
        text="George Floyd Death",
        x="2020-05-25",
        y=100,
        xshift=80,
        showarrow=False
    )

    serieschart.update_yaxes(range=[0, 110])
    serieschart.update_layout(
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
    ))

    return serieschart


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)

