import streamlit as st
import pandas as pd
import os

file_list = []

def make_clickable(username):
    # target _blank to open new window
    # extract clickable text to display for your link
    
    link = f"https://twitter.com/{username}"
    return f'<a target="_blank" href="{link}">Twitter url</a>'




@st.cache
def load_data():

    datasets_paths = { "Political vs Random" : "https://www.dropbox.com/s/8roum7tvjeverac/pmi_political_vs_random.csv.gz?dl=1",
             "Random vs Political" : "https://www.dropbox.com/s/rvkaqcajpit0766/pmi_random_vs_political.csv.gz?dl=1",
             "Uncivil vs Political" : "https://www.dropbox.com/s/bsvpxdyrel8uzrb/pmi_uncivil_vs_political.csv.gz?dl=1", #### Replace this one
             "Political vs Uncivil" : "https://www.dropbox.com/s/1xfevw3d99dgupd/pmi_political_uncivil.csv.gz?dl=1",
            }



    popular_df = pd.read_pickle("https://www.dropbox.com/s/8w6m7o2qwfp3du1/users_with_over_200_DETAILS.pkl?dl=1")
    
    popular_df = popular_df[(popular_df['user_id'] != "nan") & (
        popular_df['user_id'] != "False") & (popular_df['user_id'] != "True") & (
        popular_df['followers_count'].isna() == False)]
    popular_df.user_id = popular_df.user_id.astype(int)
    popular_df.followers_count = popular_df.followers_count.astype(int)
    # link is the column with hyperlinks
    popular_df['link'] = popular_df['screen_name'].apply(make_clickable)
    
    wiki = pd.read_csv("https://www.dropbox.com/s/b4i77itlghso5fg/users_with_wikidata.csv.gz?dl=1",compression="gzip")
    wiki.user_id = wiki.user_id.astype(int)
    wiki['wikipedia'] = wiki['wikipedia'].apply(lambda link: f'<a target="_blank" href="{link}">wiki url</a>')
    
    popular_df = popular_df.merge(wiki, on="user_id",how="left")
    
    datasets = {}
    
    for key in datasets_paths.keys():
        datasets[key] = pd.read_csv(datasets_paths[key], compression="gzip")
    
    return popular_df, datasets

st.set_page_config(layout="wide")

popular_df, datasets = load_data()


# for path, subdirs, files in os.walk("data"):
#     for file in files:
#         if file.endswith(".csv"):
#             file_list.append(file)


selected_file = st.selectbox("select file", datasets.keys()) # add "Political vs Random" and Uncivil vs Political 

df = datasets[selected_file].copy() 

st_col1, st_col2, st_col3 = st.columns(3)
cic_filter = st_col1.slider("Filter users that appear less than:", 20, 100)
specific_user = st_col2.text_input("Search for a specific user:" ,key =1)


df.count_in_class = df.count_in_class.astype(int)
df.drop(df.columns[df.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
df.rename(columns={'user2': 'user_id'}, inplace=True)

df.sort_values(by=['pmi'], ascending=False, inplace=True)

merged_df = pd.merge(df, popular_df, on="user_id", how="left")

merged_df = merged_df[['pmi','class',
        'count_in_class',
        'other_class',
        'count_in_other_class',
        'user_id',
        'name',
        'screen_name',
        'description',
        'link',
        'followers_count',
        'wikipedia'
        ]]

merged_df.drop_duplicates(inplace=True)

merged_df = merged_df[merged_df['count_in_class'] >= cic_filter]
#df = 

placeholder_2 = st.empty()

if specific_user != "":
    with placeholder_2.form(key = 'my_form', clear_on_submit = False):
        st.write(f"Selected user: {specific_user}")
        st.write(merged_df[merged_df['screen_name']==specific_user])
        submit_button = st.form_submit_button(label = 'clear selection')	
        if submit_button:
            placeholder_2.empty()

st.write(merged_df.head(50).to_html(escape=False, index=False), unsafe_allow_html=True)
