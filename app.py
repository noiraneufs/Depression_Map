import streamlit as st
import menu  
import country_details
from artificial_intelligence import graph_models
from tabel import create_table  


def load_map():
    html_file_path = 'mapa_de_calor_com_legenda.html'

    with open(html_file_path, 'r') as file:
        html_content = file.read()

    st.components.v1.html(html_content, height=600) 
    st.session_state.map_loaded = True


if 'map_loaded' not in st.session_state:
    st.session_state.map_loaded = False 


selected_option = menu.display_menu()

if selected_option == 'Artificial Intelligence':
    graph_models()
   

elif selected_option == 'Home':  # Verifica se a opção Home foi selecionada

    load_map()

    # Apenas mostrar os detalhes do país se o mapa foi carregado
    if st.session_state.map_loaded:
        country_details.show_country_details()

    

