import joblib
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import PercentFormatter
import json
import zipfile
import os

def graph_models():
  
    with open('metricas_modelos.json', 'r') as f:
        resultados = json.load(f)

    # plotar o gráfico de barras
    fig, ax = plt.subplots()
    modelos = list(resultados.keys())
    acuracias = list(resultados.values())
    
    barras = ax.bar(modelos, acuracias, color='orange')
    ax.set_xlabel('Models')
    ax.set_ylabel('Accuracy (%)')  # Indica que os valores estão em porcentagem
    ax.set_title('Accuracy in Predicting Depression Level')

    # rotação dos rótulos do eixo x
    plt.xticks(rotation=45, ha='right')

    # adicionar o valor da acurácia 
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2.0, altura, f'{altura * 100:.2f}%', 
                ha='center', va='bottom', fontsize=8)  # Ajuste o tamanho da fonte aqui

    # configurar o eixo y para exibir como porcentagem com duas casas decimais
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=2))


    st.pyplot(fig)




 
