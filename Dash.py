#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html # Deprecated.
from dash import html
#import dash_core_components as dcc # Deprecated.
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

import os
import wget

filename = 'spacex_launch_dash.csv'
if not os.path.exists(filename):
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
    wget.download(url)

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = list(set(spacex_df['Launch Site'].values))

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                *[{'label': site, 'value': site}  for site in launch_sites],
                                                ],
                                            value='ALL',
                                            placeholder="place holder here",
                                            searchable=True
                                            ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=100,
                                                marks={i : str(i) for i in [1000 * j for j in range(10 + 1)]},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
            names='Launch Site', 
            title='Total sucess launches by site')
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == entered_site], #values=, 
            names='class', 
            title=f'Total success launches for {entered_site}',
            # TODO: Need to fix some colors, because they get switched for different choices of entered_site.
            )
    return fig




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_plot(entered_site, payload_slider):
    # Filter by payload_slider:
    spacex_filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0]) & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
    
    if entered_site == 'ALL':
        fig = px.scatter(spacex_filtered_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title=f'Correlation between payload and success for all sites with payload in range {payload_slider}'
            )
    else:
        fig = px.scatter(spacex_filtered_df[spacex_filtered_df['Launch Site'] == entered_site], x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title=f'Correlation between payload and success for {entered_site} in range {payload_slider}'
            )
    # TODO: Need to fix colors for Booster Version Category, because they can get changed while sliding.
    # Some prettifying:
    fig.update_yaxes(type='category')
    fig.update_xaxes(range = [-100, 10100])
    fig.update_yaxes(range = [-.2, 1.2])
    fig.update_layout(height = 350)
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()


# In[ ]:




