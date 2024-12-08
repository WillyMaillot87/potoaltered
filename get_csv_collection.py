import io
import csv
import itertools
import streamlit as st
from utils import load_json

# Paramètres
NAME_LANGUAGES = ["fr"]
ABILITIES_LANGUAGES = ["fr"]
MAIN_LANGUAGE = "fr"
GROUP_SUBTYPES = False
INCLUDE_WEB_ASSETS = False

COLLECTION_DATA_PATH = "data/collection.json"
FACTIONS_DATA_PATH = "data/factions.json"
TYPES_DATA_PATH = "data/types.json"
SUBTYPES_DATA_PATH = "data/subtypes.json"
RARITIES_DATA_PATH = "data/rarities.json"

def get_csv_collec():
    if not check_files_exist():
        return
    
    data = load_json(COLLECTION_DATA_PATH)
    factions = load_json(FACTIONS_DATA_PATH)
    types = load_json(TYPES_DATA_PATH)
    subtypes = load_json(SUBTYPES_DATA_PATH)
    rarities = load_json(RARITIES_DATA_PATH)

    cards_dicts = []
    subtypes_cols = {}
    if not GROUP_SUBTYPES:
        subtypes_cols = get_subtypes_cols(data)

    fieldnames = ["collectorNumber"]

    for card in data.values():
        card_id = card["id"]
        card_dict = {
            "collectorNumber": card["collectorNumberFormatted"][MAIN_LANGUAGE],
            "id": card_id,
            "type": types[card["type"]][MAIN_LANGUAGE],
            "faction": factions[card["mainFaction"]][MAIN_LANGUAGE],
            "rarity": rarities[card["rarity"]][MAIN_LANGUAGE],
            "imagePath": card["imagePath"][MAIN_LANGUAGE],
        }
        if GROUP_SUBTYPES:
            card_dict["subtypes"] = ", ".join(sorted([subtypes[subtype][MAIN_LANGUAGE] for subtype in card["subtypes"]]))
        else:
            for subtype in card["subtypes"]:
                card_dict["subtype_" + str(subtypes_cols[subtype]+1)] = subtypes[subtype][MAIN_LANGUAGE]

        if "foiled" in card:
            card_dict["foiled"] = card["foiled"]
            if "foiled" not in fieldnames:
                fieldnames.append("foiled")
        if "inMyTradelist" in card:
            card_dict["inMyTradelist"] = card["inMyTradelist"]
            if "inMyTradelist" not in fieldnames:
                fieldnames.append("inMyTradelist")
        if "inMyCollection" in card:
            card_dict["inMyCollection"] = card["inMyCollection"]
            if "inMyCollection" not in fieldnames:
                fieldnames.append("inMyCollection")
        if "inMyWantlist" in card:
            card_dict["inMyWantlist"] = card["inMyWantlist"]
            if "inMyWantlist" not in fieldnames:
                fieldnames.append("inMyWantlist")

        if "elements" in card:
            if "MAIN_COST" in card["elements"]:
                card_dict["handCost"] = card["elements"]["MAIN_COST"]
            if "RECALL_COST" in card["elements"]:
                card_dict["reserveCost"] = card["elements"]["RECALL_COST"]
            if "FOREST_POWER" in card["elements"]:
                card_dict["forestPower"] = card["elements"]["FOREST_POWER"]
            if "MOUNTAIN_POWER" in card["elements"]:
                card_dict["mountainPower"] = card["elements"]["MOUNTAIN_POWER"]
            if "OCEAN_POWER" in card["elements"]:
                card_dict["waterPower"] = card["elements"]["OCEAN_POWER"]
            if "PERMANENT" in card["elements"]:
                card_dict["landmarksSize"] = card["elements"]["PERMANENT"]
            if "RESERVE" in card["elements"]:
                card_dict["reserveSize"] = card["elements"]["RESERVE"]
            if "MAIN_EFFECT" in card["elements"]:
                for language in ABILITIES_LANGUAGES:
                    card_dict["abilities" + "_" + language] = card["elements"]["MAIN_EFFECT"][language]
            if "ECHO_EFFECT" in card["elements"]:
                for language in ABILITIES_LANGUAGES:
                    card_dict["supportAbility" + "_" + language] = card["elements"]["ECHO_EFFECT"][language]
        for language in NAME_LANGUAGES:
            card_dict["name" + "_" + language] = card["name"][language]
        if INCLUDE_WEB_ASSETS and "WEB" in card["assets"]:
            web_assets = card["assets"]["WEB"]
            for i in range(min(3, len(web_assets))):
                card_dict["webAsset" + str(i)] = web_assets[i]

        cards_dicts.append(card_dict)
    
    for language in NAME_LANGUAGES:
        if "name_" + language not in fieldnames:
            fieldnames.append("name_" + language)
    if "faction" not in fieldnames:
        fieldnames.append("faction")
    if "rarity" not in fieldnames:
        fieldnames.append("rarity")
    if "type" not in fieldnames:
        fieldnames.append("type")
    if GROUP_SUBTYPES and "subtypes" not in fieldnames:
        fieldnames.append("subtypes")
    else:
        try:
            for i in range(max(subtypes_cols.values()) + 1):
                fieldnames.append("subtype_" + str(i+1))
        except:
            pass
    for col in ["handCost", "reserveCost", "forestPower", "mountainPower", "waterPower", "landmarksSize", "reserveSize"]:
        if col not in fieldnames:
            fieldnames.append(col)
    for language in ABILITIES_LANGUAGES:
        if "abilities_" + language not in fieldnames:
            fieldnames.append("abilities_" + language)
        if "supportAbility_" + language not in fieldnames:
            fieldnames.append("supportAbility_" + language)
    if "id" not in fieldnames:
        fieldnames.append("id")
    if "imagePath" not in fieldnames:
        fieldnames.append("imagePath")
    if INCLUDE_WEB_ASSETS:
        for i in range(3):
            if "webAsset" + str(i) not in fieldnames:
                fieldnames.append("webAsset" + str(i))
    
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    for card_dict in sorted(cards_dicts, key=custom_sort):
        writer.writerow(card_dict)
    
    csv_buffer.seek(0)
    st.session_state["csv_data"] = csv_buffer.getvalue()

def custom_sort(card):
    beforeRarity = card["collectorNumber"][:-4]
    afterRarity = card["collectorNumber"][-3:]
    rarity = card["collectorNumber"][-4]
    fixedRarity = rarity if rarity != "R" else "D"
    return beforeRarity + fixedRarity + afterRarity

def get_subtypes_cols(data):
    subtypes_counts = {}
    subtypes_incompatibilities = set()
    for card in data.values():
        for subtype in card["subtypes"]:
            if subtype not in subtypes_counts:
                subtypes_counts[subtype] = 0
            subtypes_counts[subtype] += 1
        for comb in itertools.combinations(card["subtypes"], 2):
            subtypes_incompatibilities.add(comb)
    ordered_subtypes = sorted(subtypes_counts, key=lambda x: subtypes_counts[x], reverse=True)
    subtypes_cols = {}
    for subtype in ordered_subtypes:
        col = 0
        while col in [subtypes_cols[other] for other in subtypes_cols if tuple(sorted((subtype, other))) in subtypes_incompatibilities]:
            col += 1
        subtypes_cols[subtype] = col
    return subtypes_cols

def check_files_exist():
    for path in [COLLECTION_DATA_PATH, FACTIONS_DATA_PATH, TYPES_DATA_PATH, SUBTYPES_DATA_PATH, RARITIES_DATA_PATH]:
        if not os.path.exists(path):
            print(f"File {path} not found. Have you run get_cards_data.py?")
            return False
    return True

if __name__ == "__main__":
    get_csv_collec()
