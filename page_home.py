import streamlit as st
from os.path import join
import subprocess
from get_cards_data import get_cards_data
from get_csv_data import get_csv
from get_all_data import get_dataframes

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

def run_script():
    saved_token = st.session_state.get("input_token")
    if not saved_token:
        st.error("Le token n'est pas défini. Merci de le saisir sur la page 'Home'.")
        return

    try:
        # get_cards_data :
        cards, types, subtypes, factions, rarities = get_cards_data()
        # Store data in session_state instead of files
        st.session_state['cards'] = cards
        st.session_state['types'] = types
        st.session_state['subtypes'] = subtypes
        st.session_state['factions'] = factions
        st.session_state['rarities'] = rarities

        # get_csv_data :
        cards_csv_buffer = get_csv(cards)
        st.session_state['cards_csv'] = cards_csv_buffer.getvalue()

        # get_collection_data :
        collection_dict, _, _, _, _ = get_cards_data(collection_token=saved_token)
        st.session_state['collection'] = collection_dict

        # get_csv_collection :
        collection_csv_buffer = get_csv(st.session_state['collection'])
        st.session_state['collection_csv'] = collection_csv_buffer.getvalue()

        # get_all_data
        global_df = get_dataframes("cards_csv", "collection_csv")
        st.session_state['global_df'] = global_df

        st.success("Le chargement de la collection est terminé.")
    except subprocess.CalledProcessError as e:
        st.error(f"Erreur lors de l'execution du script : {e}")

st.title("PotoAltered") 
st.text(st.session_state.version)

col1, col2 = st.columns([2,1])

with col1 : 

    st.markdown("""Dans le but de pouvoir récupérer les données de ta collection personnelle, je t'invite à coller ton token JWT dans le champ ci-dessous.
Ce token est utilisé dans la requête envoyée à l'API d'Altered pour t'identifier et accéder à ta collection. Le token n'est pas conservé ni stocké sur l'application en ligne.
Cette étape n'est à faire qu'une seule fois pour télécharger les données de ta collection.
            
Ne communiques ton token à personne !
            """)

    mini_col1, mini_col2 = st.columns(2, vertical_alignment="bottom")

    if "input_token" not in st.session_state:
        st.session_state["input_token"] = ""

    with mini_col1 :
        input_token = st.text_input("COLLER LE TOKEN ICI :", st.session_state["input_token"])
    
    with mini_col2 :
        submit = st.button("Charger la collection")

    if submit:
        st.session_state["input_token"] = input_token
        run_script()

    with col2 :
        st.image("images/potoaltered_anime.jpeg", use_column_width =True)
    with col1 :
        with st.expander(":bulb: Comment récupérer son token ?"):
            st.markdown('''

    Pour accéder à ta collection de cartes, tu dois obtenir ton propre token JWT sur le site altered.gg. Voici comment procéder :

    - Connecte-toi sur [**altered.gg**](https://www.altered.gg/) avec ton compte.
    - Appuie sur :red[**F12**] pour accéder aux outils de développement de ton navigateur
    - Appuie sur :red[**F5**] pour rafraichir la page
    - Dans les outils de développement, va dans la section **"Réseau"**
    - Cherche la ligne affichant la requête ***api.altered.gg/me***
    - Copie le jeton Bearer dans l'en-tête **"Authorization"**
    - Colle-le dans le champ ci-dessus :arrow_up:
    - C'est tout ! :heavy_check_mark:

            ''')

            st.image("images/tuto_token.png")