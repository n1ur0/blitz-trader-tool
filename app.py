import pandas as pd
import streamlit as st
import re
# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv('the_cards.csv')
    return data

ref_df = load_data()

def process_card_info(user_input):
    # Split the input into 'missing' and 'duplicates' sections
    parts = user_input.split("And I have duplicates of:")
    missing_part = parts[0]
    duplicates_part = parts[1] if len(parts) > 1 else ""

    # Extract missing cards
    missing_cards = re.findall(r'\d+\.\s(.+)', missing_part)
    duplicates = re.findall(
        r'\d+\.\s(.+?)\s\((\d+)\s+duplicates\)', duplicates_part)
    # Convert to DataFrame
    missing_df = pd.DataFrame(missing_cards, columns=['Card Name'])
    missing_df['Status'] = 'Missing'

    # duplicates_df = pd.DataFrame(duplicates, columns=['Card Name'])
    duplicates_df = pd.DataFrame(duplicates, columns=['Card Name', 'Count'])

    # duplicates_df['Count'] = duplicates_df['Count'].astype(int)
    duplicates_df['Status'] = 'Duplicates'

    # Combine both DataFrames
    combined_df = pd.concat([missing_df, duplicates_df.drop(columns=['Count'])], ignore_index=True)

    return combined_df

# Streamlit layout
st.title('Card Database Interaction Tool')
col1, col2 = st.columns(2)
# Sidebar for filtering after processing input
st.sidebar.header('Filter Options')
selected_rarity = st.sidebar.multiselect(
    'Select Rarity', options=ref_df['Rarity'].unique(), default=ref_df['Rarity'].unique())
selected_Bracket = st.sidebar.multiselect(
    'Select Bracket', options=ref_df['Bracket'].unique(), default=ref_df['Bracket'].unique())
selected_cards = st.sidebar.multiselect(
    'Write Card Names', options=ref_df['Card Name'].unique())
selected_status = st.sidebar.multiselect(
    'Select Status', options=['Missing', 'Duplicates'], default=['Missing', 'Duplicates'], disabled=True)
my_input = col1.text_area(
    "Paste your card list here (one per line):", height=100)
friend_input = col2.text_area(
    "Paste your friend list here (one per line):", height=100)

process_button = col1.button('Process and Display')

if process_button and friend_input and my_input:
    st.session_state['friend_df'] = process_card_info(friend_input)
    st.session_state['friend_df']['Card Owner'] = 'Friend'
    st.session_state['my_df'] = process_card_info(my_input)
    st.session_state['my_df']['Card Owner'] = 'Me'


    # Merge with database to filter available cards with details
    # st.session_state['friend_df'] = st.session_state['friend_df'].merge(
    #     ref_df, on='Card Name', how='inner')
    
    st.session_state['merged_df'] = st.session_state['friend_df'][st.session_state['friend_df']['Status'] == 'Missing'].merge(
        st.session_state['my_df'][st.session_state['my_df']['Status']=='Duplicates'], on='Card Name', how='inner', suffixes=('_friendsCards', '_myCards'))
    
    st.session_state['merged_df'] = st.session_state['merged_df'].merge(
        ref_df, on='Card Name', how='inner')
    # col1.write(st.session_state['friend_merged_df'].head())
    
if 'merged_df' in st.session_state:

    # Apply selected filters
    if selected_cards:
        st.session_state['filtered_data'] = st.session_state['merged_df'][(st.session_state['merged_df']['Rarity'].isin(selected_rarity)) &
                                                                                 (st.session_state['merged_df']['Bracket'].isin(selected_Bracket)) &
                                                                                 (st.session_state['merged_df']['Card Name'].isin(selected_cards)) &
                                                                                 ((st.session_state['merged_df']['Status_friendsCards'].isin(selected_status)) |
                                                                                  (st.session_state['merged_df']['Status_myCards'].isin(selected_status)))]
    else:
        st.session_state['filtered_data'] = st.session_state['merged_df'][(st.session_state['merged_df']['Rarity'].isin(selected_rarity)) &
                                                                                        (st.session_state['merged_df']['Bracket'].isin(selected_Bracket)) &
                                                                                        ((st.session_state['merged_df']['Status_friendsCards'].isin(selected_status)) |
                                                                                         (st.session_state['merged_df']['Status_myCards'].isin(selected_status)))]
    col1.write('Filtered Cards:')
    new_order = ['Card Name', 'Rarity', 'Bracket', 'Card Owner_friendsCards',
                 'Status_friendsCards', 'Card Owner_myCards', 'Status_myCards']
    st.session_state['filtered_data'] = st.session_state['filtered_data'][new_order]
    st.dataframe(st.session_state['filtered_data'], width=1000)

else:
    st.error("Please input some card names to proceed.")

# Instructions on running this:
# 1. Save this script as `app.py`.
# 2. Make sure you have streamlit installed: `pip install streamlit`.
# 3. Run the app by typing `streamlit run app.py` in your terminal.

