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

    st.title('Budgeting App')
    st.write('This app will help you budget your money')
    st.write('Please enter your monthly income')
    st.write('Year in Review')
    st.write('Income')
    last_year_income = st.number_input('Enter what you earned last year income', min_value=0.0, value=0.0, step=100.0)

    st.write('Expenses')
    st.write('Upload your expenses over the last year')
    # uploaded_file = st.file_uploader("Choose a file")
    uploaded_file = pd.read_csv('last_year_trends_raw.csv')
    df = pd.DataFrame(uploaded_file)

    if last_year_income != 0.0:
        def get_perc(last_year_income):
            return lambda x: float(''.join(c for c in x[1] if (c.isdigit() or c =='.')))/ float(last_year_income)
        def format_perc(x):
            return "{:.2%}".format(x)
        percentage_column_num = list(map(get_perc(last_year_income), df.values.tolist()))
        percentage_column_str = list(map(format_perc, percentage_column_num))
        df.insert(2, 'Percentage', percentage_column_str)
        # st.write(df.values.tolist())
        st.write(df)

        labels = df['CATEGORY'].values.tolist()[:-1]
        sizes = percentage_column_num[:-1]
        fig1, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig1)
    st.write('Let\'s plan for the future)')
    potential_income = st.number_input('Enter your monthly potential income', min_value=0.0, value=0.0, step=100.0)
    potential_annual_income = potential_income * 12

    st.write('Expenses')
    st.write('What would you like to spend on each category?')

    formatted_df_expenses_input = list(map(lambda x: { 'Category': x, 'Percentage': 0 }, df['CATEGORY'].values.tolist()[:-1]))
    df_expenses = pd.DataFrame(
        formatted_df_expenses_input
    )
    st.write(list(map(lambda x: float(x), df_expenses['Percentage'].values.tolist())))
    amount_left = 100 - sum(list(map(lambda x: float(x), df_expenses['Percentage'].values.tolist())))
    st.write(amount_left)

    df_expenses_with_percentages = st.experimental_data_editor(df_expenses)
    st.write('Based on your projected income, here is what you should spend on each category')

    formatted_df_budget = list(map(lambda x: { 'Category': x[0], 'Amount': 0.01 * float(x[1]) * potential_annual_income, 'Monthly': 0.01 * float(x[1]) * potential_annual_income / 12 }, df_expenses_with_percentages.values.tolist()))
    st.write(pd.DataFrame(formatted_df_budget))


