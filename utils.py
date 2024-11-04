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

