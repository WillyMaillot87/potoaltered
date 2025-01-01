import streamlit as st

def run():

    # Version : 
    version = "(v2)"
    if version not in st.session_state:
        st.session_state['version'] = version

    st.set_page_config(
        page_title= "PotoAltered",
                    layout="wide",
                    page_icon=":material/playing_cards:",
                    menu_items={
            'Get Help': 'mailto:w.maillot@gmail.com',
            'Report a bug': "https://github.com/WillyMaillot87/PotoAltered/issues",
            'About': "# PotoAltered. \n Une app très cool faite par Willy Maillot"}
            )

    # MENU #
    page_home = st.Page("page_home.py", title="Accueil", icon=":material/home:")
    page_collection = st.Page("page_collection.py", title="Collection", icon=":material/style:")
    page_echanges = st.Page("page_echanges.py", title="Echanges", icon=":material/sync_alt:")

    pg = st.navigation([page_home, page_collection, page_echanges])
    pg.run()

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