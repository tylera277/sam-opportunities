import streamlit as st
import pandas as pd


# Read in the csv file that I want to work with in this app
raw_data = pd.read_csv('streamlit_app/sam-opportunities/data/ContractOpp_data/filtered_and_summarized_data/filtered_data_22mar.csv', encoding='utf-8')


st.title("SAM.gov Opportunities Interactive Tool")



# Make some simple radio buttons allowing users to select which fields they want to see
columns_selected = st.multiselect(
    'Select Columns to view:',
    options=raw_data.columns,
    default = raw_data.columns
)
#print(columns_selected)

filtered_df = raw_data[columns_selected]


st.dataframe(filtered_df)

