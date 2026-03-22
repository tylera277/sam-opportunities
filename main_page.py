import streamlit as st

st.title("Main Page")
st.write('This will ultimately refer to where I get the data, initial processing Im doing in another script, ...')

sam_gov_file_link = "https://sam.gov/data-services/Contract%20Opportunities/datagov?privacy=Public"

st.write('I am pulling the raw CSV file from SAM.gov, which has all of the contract opportunities listed on it, ' \
'from [here](%s)' % sam_gov_file_link)