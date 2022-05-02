#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:01:46 2022

@author: zidong
"""

import pandas as pd
import altair as alt


height_age_medal = pd.read_csv("data/athlete_events.csv")

height_age_medal = height_age_medal[["Height","Age","Medal"]]

# drop rows with na
height_age_medal.dropna(axis=0, how='any', inplace=True)


brush = alt.selection(type='interval')


# set color
dom = ['Gold','Silver','Bronze']
rng = ['#ffdd00','#8b939c','#a27033']


points = alt.Chart(height_age_medal).mark_point(size=30, opacity=0.3).encode(
    x=alt.X('Height:Q',scale=alt.Scale(domain=[120, 230]),title="Height(cm)"),
    y='Age:Q',
    color=alt.condition(brush, 'Medal:N', alt.value('lightgray'), scale=alt.Scale(domain=dom, range=rng))
).add_selection(
    brush
).properties(
    title="Number of medals by age and height"
)


bars = alt.Chart(height_age_medal).mark_bar(opacity=0.7).encode(
    alt.X('count(Medal):N', title="Medal counts"),
    alt.Y('Medal:N', title="Medal type"),
    color='Medal:N'
).transform_filter(
    brush
)


p = alt.vconcat(points, bars)

p.save("link_vis1(height_age_medas.html")
