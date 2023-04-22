from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    if 'total_value' not in st.session_state:
        st.session_state['total_value'] = 100
    if 'home' not in st.session_state:
        st.session_state['home'] = 0
    if 'food' not in st.session_state:
        st.session_state['food'] = 0
    if 'entertainment' not in st.session_state:
        st.session_state['entertainment'] = 0
    if 'transportation' not in st.session_state:
        st.session_state['transportation'] = 0
    if 'other' not in st.session_state:
        st.session_state['other'] = 0

    def update_state(key, value):
        inc = value > st.session_state[key]
        if not inc and value > st.session_state['total_value']:
            return
        st.session_state[key] = value
        if inc:
            st.session_state['total_value'] -= value
        else:
            st.session_state['total_value'] += value
    
    step = 1
    home = st.slider(
        "Select what percentage of your budget you'd like to spend on housing", 
        min_value=-1, 
        max_value=100, 
        step=step,
        value=st.session_state['home'])
    update_state('home', home),
    # total_value -= home
    food = st.slider(
        "Select what percentage of your budget you'd like to spend on food", 
        min_value=-1, 
        max_value=100, 
        value=st.session_state['food'],
        step=step)
    update_state('food', food)
    # total_value -= food
    entertainment = st.slider(
        "Select what percentage of your budget you'd like to spend on entertainment", 
        min_value=-1, 
        max_value=100,
        value=st.session_state['entertainment'],
        step=step)
    update_state('entertainment', entertainment)
    # total_value -= entertainment
    transportation = st.slider(
        "Select what percentage of your budget you'd like to spend on transportation", 
        min_value=-1, 
        max_value=100, 
        value=st.session_state['transportation'],
        step=step)
    update_state('transportation', transportation)
    # total_value -= transportation
    other = st.slider(
        "Select what percentage of your budget you'd like to spend on other", 
        min_value=-1, 
        max_value=100,
        value=st.session_state['other'],
        step=1)
    update_state('other', other),
    # total_value -= other
    # savings = total_value

    labels = 'Housing', 'Food', 'Entertainment', 'Transportation', 'Other'
    sizes = [home, food, entertainment, transportation, other + st.session_state['total_value']]
    fig1, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig1)


    # total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    # num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    # Point = namedtuple('Point', 'x y')
    # data = []

    # points_per_turn = total_points / num_turns

    # for curr_point_num in range(total_points):
    #     curr_turn, i = divmod(curr_point_num, points_per_turn)
    #     angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
    #     radius = curr_point_num / total_points
    #     x = radius * math.cos(angle)
    #     y = radius * math.sin(angle)
    #     data.append(Point(x, y))

    # st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
    #     .mark_circle(color='#0068c9', opacity=0.5)
    #     .encode(x='x:Q', y='y:Q'))
