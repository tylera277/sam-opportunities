import streamlit as st
import pandas as pd


# Define the pages
main_page = st.Page('main_page.py', title='Main Page')
raw_data_exploration = st.Page('raw_data_exploration.py', title='Raw Data Exploration')
opportunities_dashboard = st.Page('opportunities_dashboard.py', title='Opportunities Dashboard')


# Set up navigation
pg = st.navigation([main_page, raw_data_exploration, opportunities_dashboard])

pg.run()