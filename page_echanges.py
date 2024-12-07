import streamlit as st
import pandas as pd
from utils import create_dataframe, transform_dataframe, show_trades

# Parameters
CSV_ALL_OUTPUT_PATH = "data/global_vision.csv"

df = create_dataframe(CSV_ALL_OUTPUT_PATH)
df, column_order, column_configuration = transform_dataframe(df)

df_collection = df[df['En possession'] > 0].copy()
df_collection.drop(['Coût de main',
                    'Dont KS',
                    'Coût de réserve',
                    'Forêt-Montagne-Eau',
                    'Capacité',
                    'Capacité de soutien',
                    'Numéro'],
                    axis=1,
                    inplace=True)

left, right = st.columns(2)
left2, right2 = st.columns(2)

left.subheader("Mes cartes :", divider = 'gray')

right.subheader("Les cartes du poto :", divider = 'gray')
csv_poto = right.file_uploader("dépose le .csv de ton poto ici", label_visibility="collapsed")

if "name_user" not in st.session_state:
    st.session_state["name_user"] = ""

with left :
    st.text_input("Indique ton nom pour télécharger ton fichier :", key="name_user")
    
    
    if st.session_state.name_user != "" :
        # Download
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        
        csv = convert_df(df_collection)

        st.download_button(
            "Press to Download",
            csv,
            "cartes_de_" + st.session_state.name_user + ".csv",
            "text/csv",
            key='download-csv',
            type="primary"
            )

with left2 :
    cards_count, cards_tot = st.columns(2)
    nb_cards_user = df_collection['En possession'].sum()
    nb_cards_unique_user = df_collection['En possession'][df_collection['En possession']>0].copy().count()
    cards_count.write(f"Nombre de cartes différentes : **{nb_cards_unique_user}**")
    cards_tot.write(f"Nombre de cartes totales : **{nb_cards_user}**")
    

    st.dataframe(df_collection,
    column_config=column_configuration,
    column_order=column_order,
    use_container_width=True,
    hide_index=True)

    

    

if csv_poto is not None:
    file_name = csv_poto.name
    name_poto = file_name[10:-4]

    with right2 :
        df_poto = pd.read_csv(csv_poto)
        df_poto, column_order, column_configuration = transform_dataframe(df_poto)
        
        cards_count, cards_tot = st.columns(2)
        nb_cards_poto = df_poto['En possession'].sum()
        nb_cards_unique_poto = df_poto['En possession'][df_poto['En possession']>0].copy().count()
        cards_count.write(f"Nombre de cartes différentes : **{nb_cards_unique_poto}**")
        cards_tot.write(f"Nombre de cartes totales : **{nb_cards_poto}**")

        st.dataframe(df_poto,
        column_config=column_configuration,
        column_order=column_order,
        use_container_width=True,
        hide_index=True)

    df_get = show_trades(df_poto, df_collection)
    df_give = show_trades(df_collection, df_poto)
    nb_to_get = df_get.shape[0]
    nb_to_give = df_give.shape[0]

    df_get, column_order, column_configuration = transform_dataframe(df_get)

    left, center, right = st.columns(3)
    if center.button(label = f"Voir les cartes échangeables avec {name_poto}", use_container_width=True, type = 'primary'):

        left3, center3, right3 = st.columns([2, 1, 2])
        left3.subheader(f"Tu peux donner ces {nb_to_give} cartes à {name_poto} :", divider = 'red')
        left3.dataframe(df_give,
        column_config={'Image': st.column_config.ImageColumn(
                        "Image", 
                        help="Aperçut de la carte. Double cliquer pour agrandir.",
                        width = "small"
                        )},
        use_container_width=True,
        hide_index=True)

        center3.image("images/trade.jpg")

        right3.subheader(f"{name_poto} peut te donner ces {nb_to_get} cartes :", divider = 'blue')
        right3.dataframe(df_get,
        column_config={'Image': st.column_config.ImageColumn(
                        "Image", 
                        help="Aperçut de la carte. Double cliquer pour agrandir.",
                        width = "small"
                        )},
        use_container_width=True,
        hide_index=True)