
import pandas as pd
from transformers import pipeline

# File location where you want to pull the raw CSV file from
# of all of the opportunities

raw_file_location = "data/ContractOpp_data/raw_data/ContractOpportunitiesFullCSV_29Mar.csv"
output_file_location = "data/ContractOpp_data/filtered_and_summarized_data/filtered_data_29mar.csv"

# Load in the raw data
raw_data = pd.read_csv(raw_file_location, encoding='Windows-1252')


# Filtering based on the columns I want to keep
columns_to_keep = ['NoticeId', 'Title', 'Sol#', 'Department/Ind.Agency', 'CGAC',
       'Sub-Tier', 'FPDS Code', 'Office', 'AAC Code', 'PostedDate', 'Type',
       'BaseType', 'ArchiveType', 'SetASideCode', 'SetASide','PostedDate',
       'ResponseDeadLine', 'NaicsCode', 'ClassificationCode',
       'Active', 'Link',
       'Description'];

early_filtered_data = raw_data[columns_to_keep].copy()
early_filtered_data_two = early_filtered_data[~(early_filtered_data['SetASide'] == 'Total Small Business Set-Aside (FAR 19.5)')]
early_filtered_data_three = early_filtered_data_two[early_filtered_data_two['ClassificationCode'].str.startswith('A', na=False)]


# Filtering the ResponseDeadline field by the current date, so I only see the currently
# active opportunities listed
now = pd.Timestamp('2026-03-29T00:00:00+00:00')
early_filtered_data_three['ResponseDeadLine_Converted'] = pd.to_datetime(early_filtered_data_three['ResponseDeadLine'],utc=True,format='mixed')
early_filtered_data_four = early_filtered_data_three[early_filtered_data_three['ResponseDeadLine_Converted'] > now]



list_of_departments = early_filtered_data_four['Sub-Tier'].unique()

#####################
# Code used previously, may need again
#with pd.ExcelWriter("ContractOppData\Summaries\Mar13_SAM_Opp_Summary.xlsx") as writer:
#temp_data_selective.to_excel(writer, sheet_name=f'{department}', index=False)
#####################

# AI summarizing tools
def load_model():
    # Using a fast, lightweight model perfect for summarization
    return pipeline('summarization', model="sshleifer/distilbart-cnn-12-6")

summarizer = load_model()



# After dropping duplicates, clean the descriptions
temp_data_selective = early_filtered_data_four.drop_duplicates(subset=['Title'], keep='first').copy()

# Fill NaN descriptions with empty string (or drop them)
temp_data_selective['Description'] = temp_data_selective['Description'].fillna('')

# Now extract as list
descriptions = temp_data_selective['Description'].tolist()

# 2. Extract descriptions as a list for batch processing
descriptions = temp_data_selective['Description'].tolist()



# 3. BATCH SUMMARIZATION - this is the key improvement
batch_size = 8
summaries = []

for i in range(0, len(descriptions), batch_size):
    print("Progress: ", i, "/", len(descriptions))
    batch = descriptions[i:i + batch_size]
    batch_summaries = []
    
    for desc in batch:
        # If description is already short, just use it as-is
        if len(desc.split()) < 30:  # Adjust threshold as needed
            batch_summaries.append(desc)
        else:
            # Only summarize longer descriptions
            summary = summarizer(
                desc, 
                max_length=70, 
                min_length=30, 
                do_sample=False,
                truncation=True
            )
            batch_summaries.append(summary[0]['summary_text'])
    
    summaries.extend(batch_summaries)

# 4. Assign all at once (much faster than row-by-row)
temp_data_selective = temp_data_selective.copy()  # Avoid SettingWithCopyWarning
temp_data_selective['ai_summary_description'] = summaries

# 5. Write to CSV
temp_data_selective.to_csv(output_file_location, index=False)





