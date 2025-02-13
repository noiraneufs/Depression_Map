import json
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def graph_models():
    with open('resultados_validacao_cruzada.json', 'r') as file:
        dados = json.load(file)

    modelos = list(dados.keys())
    media_acuracia = [np.mean(dados[modelo]["acuracia"]) for modelo in modelos]
    media_f1 = [np.mean(dados[modelo]["f1_score"]) for modelo in modelos]

    modelos_ordenados, media_acuracia_ordenada, media_f1_ordenada = zip(*sorted(
        zip(modelos, media_acuracia, media_f1), key=lambda x: x[1]))

    fig, ax = plt.subplots(figsize=(8, 4))

    bar_width = 0.4
    indices = np.arange(len(modelos_ordenados))

    bars1 = ax.barh(indices - bar_width/2, media_acuracia_ordenada, bar_width, label='Acurácia', color='blue')
    bars2 = ax.barh(indices + bar_width/2, media_f1_ordenada, bar_width, label='Medida-F1', color='orange')

    for bar in bars1:
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.4f}', va='center', fontsize=12)
    for bar in bars2:
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.4f}', va='center', fontsize=12)

    ax.set_yticks(indices)
    ax.set_yticklabels(modelos_ordenados)
    ax.set_xlabel("Média das Métricas")
    ax.set_title("Comparação dos Modelos - Acurácia vs Medida-F1")
    ax.legend()
    ax.set_xlim(0, 1.2)

    plt.grid(axis='x', linestyle='--', alpha=0.6)

    st.pyplot(fig)
