import streamlit as st
import pandas as pd
from os.path import join
import subprocess
from streamlit_option_menu import option_menu
from get_cards_data import get_cards_data
from get_csv_data import get_csv
from get_csv_collection import get_csv_collec
from get_all_data import get_dataframes
from utils import dump_json, create_folder_if_not_exists

# Version : 
version = "v2"

# Parameters
LANGUAGES = ["fr"]
DUMP_TEMP_FILES = False
OUTPUT_FOLDER = "data"
TEMP_FOLDER = "temp"
INCLUDE_PROMO_CARDS = False
INCLUDE_UNIQUES = False
INCLUDE_KS = True
FORCE_INCLUDE_KS_UNIQUES = False 
INCLUDE_FOILERS = False
SKIP_NOT_ALL_LANGUAGES = False
COLLECTION_TOKEN=None

NAME_LANGUAGES = ["fr"]
ABILITIES_LANGUAGES = ["fr"]
MAIN_LANGUAGE = "fr"
GROUP_SUBTYPES = False
INCLUDE_WEB_ASSETS = False

CARDS_DATA_PATH = "data/cards.json"
COLLECTION_DATA_PATH = "data/collection.json"
FACTIONS_DATA_PATH = "data/factions.json"
TYPES_DATA_PATH = "data/types.json"
SUBTYPES_DATA_PATH = "data/subtypes.json"
RARITIES_DATA_PATH = "data/rarities.json"
CSV_OUTPUT_PATH = "data/cards_" + MAIN_LANGUAGE + ".csv"
CSV_COLLEC_OUTPUT_PATH = "data/collection_" + MAIN_LANGUAGE + ".csv"
ALL_CARDS_PATH = "data/cards_fr.csv"
MY_COLLECTION_PATH = "data/collection_fr.csv"
CSV_ALL_OUTPUT_PATH = "data/global_vision.csv"

# PAGES #
page_home = st.Page("page_home.py", title="Accueil", icon=":material/home:")
page_collection = st.Page("page_collection.py", title="Collection", icon=":material/style:")
page_echanges = st.Page("page_echanges.py", title="Echanges", icon=":material/sync_alt:")

pg = st.navigation([page_home, page_collection, page_echanges])
pg.run()

st.set_page_config(
    page_title= "PotoAltered",
                 layout="wide",
                 page_icon=":material/playing_cards:",
                 menu_items={
        'Get Help': 'mailto:w.maillot@gmail.com',
        'Report a bug': "https://github.com/WillyMaillot87/PotoAltered/issues",
        'About': "# PotoAltered. \n Une app très cool faite par Willy Maillot"}
        )


#Cacher le bouton 'view fullscreen' des images :
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

if __name__ == "__main__":
    run()