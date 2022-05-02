#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 21:48:42 2022

@author: zidong
"""

import altair as alt
import pandas as pd

# os.getcwd()
# os.chdir('/Users/zidong/Documents/GitHub/hw4-spring-2022-Zidong2020')

df_p = pd.read_csv("data_viz.csv")
df_p['Date'] = pd.to_datetime(df_p['Date'])

# print columns type in dataframe
print(df_p.dtypes)

interval = alt.selection_interval(encodings=['y'])

domain_pd = pd.to_datetime(['2012-06-27', '2013-01-13']).astype(int) / 10 ** 6

# scatter plot shows each day energy consumption
scatter = alt.Chart(df_p).mark_point().encode(
    x=alt.X("powerallphases", title="daily energy comsumption (kWh)"),
    y=alt.Y("Date", timeUnit='yearmonthdate', scale=alt.Scale(domain=list(domain_pd), reverse=True), title="Date"),
    color=alt.condition(interval, 'powerallphases', alt.value('lightgray'), legend=None)
).properties(
    title="Daily Energy Consumption",
    width=400,
    height=600,
    selection=interval
)

# bar plot shows the count of different energy consumption day
bar = alt.Chart(df_p).mark_bar().encode(
    x=alt.X("powerallphases", title="daily energy comsumption (kWh)", bin=alt.Bin(extent=[0, 70], step=5)),
    y=alt.Y("count()", title="Date count"),
    color=alt.Color('powerallphases',
                    legend=alt.Legend(title='energy comsumption (kWh)'))
).transform_filter(
    interval
).properties(
    title="Daily Energy Consumption Distribution (powerallphase)",
    width=400,
    height=250,
)

# plot shows the count of different energy consumption day (by plugs and others)
plug = alt.Chart(df_p).transform_fold(
    ['Fridge', 'Kitchen appliances', 'Lamp', 'Stereo_laptop', 'Freezer',
     'Tablet', 'Entertainment', 'Microwave', 'others'],
    as_=['Plug', 'Measurement']
).mark_bar(
    opacity=0.3,
    binSpacing=0
).encode(
    alt.X('Measurement:Q', title="energy comsumption (kWh)", bin=alt.Bin(maxbins=100)),
    alt.Y('count()', title="Date count", stack=None),
    alt.Color('Plug:N')
).transform_filter(
    interval
).properties(
    title="Energy Consumption distribution (each plug & others)",
    width=400,
    height=270,
)

# Merge subgraphs
p = alt.vconcat(bar, plug)
p = alt.hconcat(scatter, p)

p.save("altair.html")
