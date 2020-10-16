import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


#-----------------------------------------------------------------------------
# Question 1 data 
q1_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=600000' +\
        '&$select=spc_common,boroname,health,count(tree_id)' +\
        '&$where=health!=\'NaN\'' +\
        '&$group=spc_common,boroname,health').replace(' ', '%20')

q1 = pd.read_json(q1_url)
q1.columns = ["spc_common", "boroname","health", "healthtotal"]


q1_url_a = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=600000' +\
        '&$select=spc_common,boroname,count(tree_id)' +\
        '&$where=health!=\'NaN\'' +\
        '&$group=spc_common,boroname').replace(' ', '%20')
q1_a = pd.read_json(q1_url_a)
q1_a.columns = ["spc_common", "boroname", "borototal"]

q1_trees = pd.merge(q1, q1_a, on=["boroname", "spc_common"])
q1_trees["perct"] = q1_trees["healthtotal"]/q1_trees["borototal"]


species = q1.sort_values("spc_common")["spc_common"].unique()
boro = q1_trees.sort_values("boroname")["boroname"].unique()


q1_trees = q1_trees.reset_index(drop=False)



#---------------------------------------------------------------------------
# Question 2 data
q2_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=600000' +\
        '&$select=spc_common,boroname,health,steward,count(tree_id)' +\
        '&$where=health!=\'NaN\'' +\
        '&$group=spc_common,boroname,health,steward').replace(' ', '%20')
q2 = pd.read_json(q2_url)



app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Data 608: Module 4", style={'text-align': 'center'}),
    html.H4("Dhairav Chhatbar", style={'text-align': 'center'}),
    html.P("In this module we’ll be looking at data from the New York City tree census:"),
    html.A("2015 Street Tree Census",href='https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh', target="_blank"),
    html.P("This data is collected by volunteers across the city, and is meant to catalog information about every single tree in the city."), 
    html.P("Build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) across"\
           " each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each"\
           " species and in each borough"),
        
    html.Br(),
    html.Br(),
    
    html.P("Question 1: What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?"),

    dcc.Dropdown(id="sel_species",
                 options=[{'label':i, 'value':i} for i in species],
                 multi=False,
                 value="American beech",
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='q1_graph', 
              figure={}),
    
    html.Br(),
    html.P("Question 2: Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?"),
    
    dcc.Dropdown(id="sel_boro",
                 options=[{'label':i, 'value':i} for i in boro],
                 multi=False,
                 value="Bronx",
                 style={'width': "40%"}
                 ),
    dcc.Graph(id='q2_graph', 
              figure={})
])

#-----------------------------------------------------------------------------
#App Callback
@app.callback(
    dash.dependencies.Output('q1_graph', 'figure'),
    [Input(component_id='sel_species', component_property='value')]
    )
def update_q1_graph(plant_sel):
    q1_df = q1_trees[q1_trees["spc_common"]==plant_sel]

    q1_chart = px.bar(data_frame=q1_df,
                      x="boroname", 
                      y="perct", 
                      color="health", 
                      barmode="group",
                      labels={
                          "boroname":"Boroughs",
                          "perct":"Percentage of Health",
                          "health":"Health"},
                      title="Proportion of Tree Health",
                      width=900,
                      height=500
                     )
    return q1_chart

@app.callback(
    dash.dependencies.Output('q2_graph', 'figure'),
    [
        Input(component_id='sel_species', component_property='value'),
        Input(component_id='sel_boro', component_property='value')
    ])
def update_q2_graph(plant_sel, boro_sel):
    q2_df = q2[q2["spc_common"]==plant_sel]
    q2_df = q2_df[q2_df["boroname"]==boro_sel]

    q2_chart = px.bar(data_frame=q2_df, 
                      x="steward", 
                      y="count_tree_id", 
                      color="health", 
                      barmode="group",
                      labels={
                          "steward":"Stewardship Noted",
                          "count_tree_id":"Tree Count",
                          "health":"Health"},
                      title="Stewardship Impact",
                      width=700,
                      height=500
                     )
    return q2_chart

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)

