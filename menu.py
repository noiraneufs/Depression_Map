# menu.py
import streamlit as st

def display_menu():
  
    st.sidebar.header("Menu")
    
   
    option = st.sidebar.selectbox(
        'Choose an option:',
        ['Home', 'Artificial Intelligence']
    )
    
  # controle Menu 
    if option == 'Artificial Intelligence':
        st.title("Predicting Depression with Machine Learning")
    elif option == 'Home':
        st.title("DepressionMap")
    
    return option
