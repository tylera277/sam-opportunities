import streamlit as st
import pandas as pd


# Read in the csv file that I want to work with in this app
raw_data = pd.read_csv("streamlit_app/sam-opportunities/data/FilteredOpp.csv", encoding='utf-8')


st.set_page_config(layout='wide')


# I want to try to create a page where opportunities can be viewed at a very brief/summary glance,
# while then allowing to expand on each further if a person wants to.



with st.sidebar:
    st.title("Filters")


    # Department filter
    st.subheader('Department')
    selected_depts = st.multiselect(
        'Select departments:',
        options = raw_data['Sub-Tier'].unique(),
        default=None
    )
    st.divider()

    # Type of opportunity filter
    # (so RFI, solicitation,...)
    st.subheader('Opportunity Type')
    selected_type = st.multiselect(
        'Select Type:',
        options= raw_data['Type'].unique(),
        default=None
    )
    st.divider()

    # Columns selector
    st.subheader("Layout")
    num_columns = st.radio(
        "Cards per row:",
        options=[2,3,4],
        index=1,
        label_visibility='collapsed'
    )
filtered_df = raw_data[
    (raw_data['Sub-Tier'].isin(selected_depts) &
     raw_data['Type'].isin(selected_type))
]



# Main content
st.title("Opportunities Dashboard")
st.title(f'{len(filtered_df)} opportunities found')

cols = st.columns(num_columns)



for idx, row in filtered_df.iterrows():
    with cols[idx % num_columns]:
        with st.container(border=True):
            st.subheader(row['Title'])
            st.write("AI Summary goes here??")
            st.write(row['Sub-Tier'])
            st.write("Response Deadline:", row['ResponseDeadLine'])
            with st.expander("More Details"):
                st.write('More words can go here!')
                st.write('Solicitation Number: ', row['Sol#'])
                st.write("Link:", row['Link'])
