# Script by Maverick CHARDET
# CC-BY

LANGUAGE_HEADERS = {
    "en": {
        "Accept-Language": "en-en"
    },
    "fr": {
        "Accept-Language": "fr-fr"
    },
    "es": {
        "Accept-Language": "es-es"
    },
    "it": {
        "Accept-Language": "it-it"
    },
    "de": {
        "Accept-Language": "de-de"
    }
}

# Imports
import requests
import os
import json
import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_file(url, filename, log=False, headers=None):
    if log: print(f"Downloading {filename} from {url}")
    response = requests.get(url, stream=True, headers=headers)
    if not response.ok:
        print(response)
        return False
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return True

def dump_json(data, filename):
    with open(filename, 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filename):
    with open(filename, encoding="utf8") as f:
        return json.load(f)

def load_txt(filename):
    with open(filename, encoding="utf8") as f:
        return f.read()
    
def create_or_read_file(filename):
  """Crée un fichier s'il n'existe pas et lit son contenu.

  Args:
    filename: Le nom du fichier.

  Returns:
    Le contenu du fichier, ou une chaîne vide si le fichier est nouveau.
  """

  if not os.path.exists(filename):
    with open(filename, "w") as f:
      # Écrire un contenu par défaut si besoin
      f.write("")
  
  with open(filename, "r") as f:
    return f.read()

def create_dataframe():
    if 'global_df' in st.session_state:
        df = st.session_state['global_df']
        return df
    else:
        st.error("La collection n'est pas créée. Merci d'ajouter votre token via la page 'Home'.")
        return pd.DataFrame()  # Return an empty DataFrame if not available

def transform_dataframe(df) :   
    columns_power = ['forestPower', 'mountainPower', 'waterPower']

    if all(column in df.columns for column in columns_power) :
        df['Forest-Mountain-Water'] = df[['forestPower', 'mountainPower', 'waterPower']].apply(lambda x: list(x), axis=1)

    new_names_fr = {'name_fr' : 'Nom',
                    'faction' : 'Faction', 
                    'collectorNumber' : 'Numéro',
                    'type' : 'Type', 
                    'rarity' : 'Rareté',
                    'handCost' : 'Coût de main', 
                    'reserveCost' : 'Coût de réserve', 
                    'Forest-Mountain-Water' : 'Forêt-Montagne-Eau',
                    'forestPower' : 'Fôret', 
                    'mountainPower' : 'Montagne', 
                    'waterPower' : 'Eau', 
                    'abilities_fr' : 'Capacité',
                    'supportAbility_fr' : 'Capacité de soutien',
                    'imagePath' : 'Image', 
                    'inMyCollection' : 'En possession', 
                    'Kickstarter' : 'Dont KS', 
                    'to_give' : 'En excès', 
                    'to_get' : 'Manquantes',
                    'progress' : 'Complétion'
                    }

    df = df.rename(columns = new_names_fr)

    column_order = ('Image',
                    'Nom',
                    'Faction',
                    'Type', 
                    'Rareté',
                    'En possession',
                    'Dont KS',
                    'En excès', 
                    'Manquantes',
                    'Complétion',
                    'Coût de main', 
                    'Coût de réserve', 
                    'Forêt-Montagne-Eau',
                    # 'Fôret', 
                    # 'Montagne', 
                    # 'Eau', 
                    'Capacité',
                    'Capacité de soutien',
                    'Numéro'
                    )

    column_configuration = {
        'Complétion' : st.column_config.ProgressColumn(
            "Complétion",
            help="Progression sur l'atteinte du maximum par deck pour cette carte",
            format="%d%%",
            min_value=0,
            max_value=100
        ),
        'Image': st.column_config.ImageColumn(
            "Image", 
            help="Aperçut de la carte. Double cliquer pour agrandir.",
            width = "small"
            ),
        }
  
    return df, column_order, column_configuration

def show_trades(df_give, df_get):
    df_give = df_give[df_give['En excès'] > 0].copy()

    df_merge = pd.merge(df_give, df_get[['id','Manquantes']], how='left', on='id', suffixes = ('_give', '_get'))

    df_merge['max_card'] = df_merge['Type'].apply(lambda x: 1 if x == 'Héros' else 3) 
    
    df_merge.fillna({'Manquantes_get' : df_merge['max_card']}, inplace=True)

    df_merge['Manquantes_get'] = df_merge['Manquantes_get'].astype(int)

    df_result = df_merge[['Image','Nom', 'Faction', 'Rareté', 'Type', 'En excès', 'Manquantes_get']].copy()
    df_result['Nombre d\'exemplaires'] = df_merge[['En excès', 'Manquantes_get']].min(axis=1)
    df_result = df_result[df_result['Nombre d\'exemplaires'] > 0]
    df_result.drop(['En excès', 'Manquantes_get'], axis=1, inplace=True)

    return df_result