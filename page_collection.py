import streamlit as st
from app import create_dataframe, transform_dataframe

# Parameters
CSV_ALL_OUTPUT_PATH = "data/global_vision.csv"

df = create_dataframe(CSV_ALL_OUTPUT_PATH)
df, column_order, column_configuration = transform_dataframe(df)
df_all = df.copy()
filter_col, df_col = st.columns([1, 4])

with filter_col :
    columns_cat = ['Faction', 
                    'Rareté',
                    'Type']
    
    columns_string = ['Nom',
                        'Numéro',
                        'id']
    
    columns_int = ['En possession',
                    'Dont KS',
                    'En excès',
                    'Manquantes',
                    'Coût de main',
                    'Coût de réserve',
                    'Fôret',
                    'Montagne',
                    'Eau']
    
    columns_float = ['Complétion']
    
    columns_to_select = columns_cat + columns_string + columns_int + columns_float

    st.subheader(f"Filtres")

    df = df.copy()

    modification_container = st.container(border=True)

    with modification_container:
        to_filter_columns = st.multiselect("Filtrer le tableau", columns_to_select)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            if column in columns_cat :
                user_cat_input = right.multiselect(
                f"Valeurs pour {column}",
                df[column].unique(),
                default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]

            elif column in columns_float:
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 4
                user_num_input = right.slider(
                    f"Valeurs pour {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]

            elif column in columns_int:
                _min = int(df[column].min())
                _max = int(df[column].max())
                step = 1
                user_num_input = right.slider(
                    f"Valeurs pour {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]


    excess = st.button("Afficher les cartes en trop", use_container_width=True)
    missing = st.button("Afficher les cartes manquantes", use_container_width=True)
    possessed = st.button("Afficher les cartes possédées", use_container_width=True)
    st.button("Reset", use_container_width=True)

    if excess :
        df = df[df['En excès'] > 0]
    elif missing :
        df = df[df['Manquantes'] > 0]
    elif possessed :
        df = df[df['En possession'] > 0]
    else :
        df = df

    # Download
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(df)

    st.download_button(
        "Press to Download",
        csv,
        "cartes_altered.csv",
        "text/csv",
        key='download-csv',
        type="primary",
        use_container_width=True
        )
    
    #### STATISTIQUES #####
    shape_all = df_all.shape[0]
    shape_filtered = df.shape[0]
    st.markdown(f"**{shape_filtered}** cartes sélectionnées sur **{shape_all}** disponibles")

with df_col :
    st.subheader("Collection")

    st.dataframe(df,
    column_config=column_configuration,
    column_order=column_order,
    use_container_width=True,
    hide_index=True,
    # on_select="rerun",
    # selection_mode="multi-row",
    )

# cards = event.selection.rows
# second_df = df[['Image','Nom','Faction','Rareté','Type','Numéro','En excès', 'Manquantes']].iloc[cards]

# st.header(f"Cartes sélectionnées : {len(cards)}")
# st.dataframe(second_df, column_config=column_configuration, use_container_width=True)