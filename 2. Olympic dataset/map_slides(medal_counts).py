#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 02:08:20 2022

@author: zidong
"""

import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

### data preparation
# load data
gdp = pd.read_csv("data/GDP by country.csv", skiprows=4)

# clean data
gdp = gdp.drop(['Indicator Name', 'Indicator Code', 'Country Name'], 1)

# wide to long
gdp = pd.melt(gdp, id_vars=['Country Code'], value_vars=list(gdp.columns[1:]),
              var_name='Year', value_name='GDP')

pop = pd.read_csv("data/Population by country.csv", skiprows=4)
pop = pop.drop(['Indicator Name', 'Indicator Code', 'Country Name'], 1)
pop = pd.melt(pop, id_vars=['Country Code'], value_vars=list(pop.columns[1:]),
              var_name='Year', value_name='POP')

medal_count = pd.read_csv("data/Summer_Olympic_medallists.csv")
medal_count = medal_count.groupby(['NOC', 'Edition']).size().reset_index(name='medal number')
medal_count = medal_count.rename(columns={'NOC': 'Country Code', 'Edition': 'Year'})

regions = pd.read_csv("data/Regions.csv")
regions.columns = ['Country Name', 'Regions', 'Country Code']

# before merge, check columns type
gdp.dtypes
medal_count.dtypes

gdp['Year'] = gdp['Year'].astype('int')

# merge dataframes
merge = pd.merge(gdp, medal_count)
merge = pd.merge(regions, merge, how="inner", on=['Country Code'])

### try single static plot:
# use year 2008

df = merge[merge['Year'] == 2008]

init_notebook_mode(connected=True)

scl = [[0.0, '#ffffff'], [0.2, '#ff9999'], [0.4, '#ff4d4d'],
       [0.6, '#ff1a1a'], [0.8, '#cc0000'], [1.0, '#4d0000']]  # reds

data = [dict(
    type='choropleth',  # type of map-plot
    colorscale=scl,
    autocolorscale=False,
    locations=df['Country Name'],  # the column with the state
    z=df['medal number'],  # the variable I want to color-code
    locationmode='country names',
    marker=dict(  # for the lines separating states
        line=dict(
            color='rgb(255,255,255)',
            width=2)),
    colorbar=dict(
        title="Medal counts")
)
]

layout = dict(title="Number of medals won by country: 2008")

fig = dict(data=data, layout=layout)

plotly.offline.iplot(fig)

# offline.plot(fig, auto_open=True, image='png', image_width=2000, image_height=1000, filename='map_slides(medal_count_2008).html.html')

### try add sliders:

### create empty list for data object 
data_slider = []

for year in merge.Year.unique():
    # select the year (and remove DC for now)
    df_medal_count = merge[merge['Year'] == year]

    # create the dictionary with the data for the current year
    data_one_year = dict(
        type='choropleth',  # type of map-plot
        colorscale=scl,
        autocolorscale=False,
        locations=df_medal_count['Country Name'],
        z=df_medal_count['medal number'],  # the variable I want to color-code
        locationmode='country names',
        marker=dict(  # for the lines separating states
            line=dict(
                color='rgb(255,255,255)',
                width=2)),
        colorbar=dict(
            title="Medal counts")
    )

    data_slider.append(data_one_year)  # add the dictionary to the list of dictionaries for the slider

# create the steps for the slider
steps = []

for i in range(len(data_slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)],
                label='Year {}'.format(i * 4 + 1960))  # label to be displayed for each step (year)
    step['args'][1][i] = True
    steps.append(step)

# create the 'sliders' object from the 'steps' 
sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

# set up the layout (including slider option)
layout = dict(sliders=sliders, title="Number of medals won by country 1960-2008")

# create the figure object:
fig = dict(data=data_slider, layout=layout)

# plot in the notebook
plotly.offline.iplot(fig)

# plot in a separete browser window
offline.plot(fig, auto_open=True, image='png', image_width=2000, image_height=1000,
             filename='map_slides(medal_counts).html', validate=True)


# REFERENCE:https://amaral.northwestern.edu/blog/step-step-how-plot-map-slider-represent-time-evolu












