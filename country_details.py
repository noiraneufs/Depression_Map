import streamlit as st
import pandas as pd
import plotly.express as px
import country_data  
from tabel import create_table

def level_layout(df, selected_country):
   
    levels = {
        0: ("Normal", "white"),
        1: ("Mild", "#FDFD96"), 
        2: ("Moderate", "#FFA500"), 
        3: ("Severe", "#FF6F00"), 
        4: ("Extremely Severe", "#ED3419")  
    }

  
    gender_colors = {
        'Male': '#1f77b4', 
        'Female': '#ff69b4',  
        'Other': '#6a0dad'     
    }

  
    education_labels = {
        1: 'Less than high school',
        2: 'High school',
        3: 'University degree',
        4: 'Graduate degree'
    }

     #rotulos estado civel 
    married_labels = {
        1: 'Never married',
        2: 'Currently married',
        3: 'Previously married'
    }

    # tratar a aquestão da seleção de todos paises , ou pais especifico 
    if selected_country == 'All Countries':
        country_df = df  # Usa o DataFrame completo
        country_participants = country_df.shape[0]
    else:
   
        country_number = next(key for key, value in country_data.country_mapping.items() if value == selected_country)

        country_df = df[df['country'] == country_number]
        country_participants = country_df.shape[0]

  

    # css caixas 
    box_style = """
    <style>
    .box {
        border: 1px solid #d3d3d3;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        background-color: transparent;
    }
    .box-large-font {
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(box_style, unsafe_allow_html=True)

    # total de participantes
    st.markdown(
        f'<div class="box">Total participants: <span class="box-large-font">{country_participants}</span><br>Average depression score: {country_df["indice_depressao"].mean():.2f}</div>',
        unsafe_allow_html=True
    )

    # gráfico de pizza 3D  gênero
    gender_counts = country_df['gender'].value_counts().reindex([1, 2, 3], fill_value=0)
    gender_labels = {1: 'Male', 2: 'Female', 3: 'Other'}
    gender_counts.index = [gender_labels[i] for i in gender_counts.index]

    #  porcentagens e médias  gênero
    level_data = []
    hover_data = []
    for gender, label in gender_labels.items():
        gender_group = country_df[country_df['gender'] == gender]
        total_gender = gender_group.shape[0]
        if total_gender > 0:
            level_counts = gender_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression = gender_group['indice_depressao'].mean()
            hover_info = [f'{levels[level][0]}: {level_counts.get(level, 0):.2f}%' for level in range(5)]
            hover_info.append(f'Average Depression Index: {avg_depression:.2f}')
            hover_data.append('<br>'.join(hover_info))
            for level, count in level_counts.items():
                level_data.append({
                    'Gender': label,
                    'Level': levels[level][0],
                    'Percentage': count
                })

    level_df = pd.DataFrame(level_data)

    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title='Distribution by gender',
        hole=0.3,
        color=gender_counts.index,
        color_discrete_map=gender_colors,
        labels={'names': 'Gender', 'values': 'Number of Participants'}
    )
    fig_gender.update_traces(
        texttemplate='%{percent:.3%} %{label}',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data,
        pull=[0.1, 0.1, 0.1]
    )
    fig_gender.update_layout(showlegend=True)
    st.plotly_chart(fig_gender, use_container_width=True)

    # add o gráficode níveis de depressão por gênero
    gender_level_data = []

    for gender, label in gender_labels.items():
        gender_group_df = country_df[country_df['gender'] == gender]
        total_gender = gender_group_df.shape[0]
        if total_gender > 0:
            level_counts = gender_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = gender_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                gender_level_data.append({
                    'Gender': label,
                    'Level': levels[level][0],
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level]  
                })

    gender_level_df = pd.DataFrame(gender_level_data)

    
    fig_gender_level = px.bar(
        gender_level_df,
        x='Gender',
        y='Percentage',
        color='Level',
        text='Percentage',  # Mantém o texto de porcentagem no gráfico
        title='Percentage of Depression Levels by Gender',
        labels={'Gender': 'Gender', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level']  # Adiciona 'Count' e 'Level' ao custom data
    )

    # dados ao passar mouse 
    fig_gender_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        textposition='inside',  # Mantém a porcentagem visível
        hovertemplate=(
            "<b>Gender: %{x}</b><br>"
            "Level: %{customdata[1]}<br>"
            "Percentage: %{y:.2f}%<br>"
            "Count: %{customdata[0]}<br>"
            "<extra></extra>"
        )
    )

    fig_gender_level.update_layout(barmode='stack')

    st.plotly_chart(fig_gender_level, use_container_width=True)






       # idade
    age_bins = [18, 34, 54, float('inf')]
    age_labels = ['18-34', '35-54', '55+']
    country_df['age_group'] = pd.cut(country_df['age'], bins=age_bins, labels=age_labels, right=False)


    #  pizza idade
    age_counts = country_df['age_group'].value_counts().sort_index()

    # cores faixas etárias
    age_colors = {
        '18-34': '#77DD77',
        '35-54': '#FF33A8',
        '55+': '#D3D3D3',
    }

    #  níveis de depressão e a média idade
    hover_data_age = []
    age_avg_depression = country_df.groupby('age_group')['indice_depressao'].mean()

    for age_group in age_labels:
        age_group_df = country_df[country_df['age_group'] == age_group]
        total_in_group = age_group_df.shape[0]
        if total_in_group > 0:
            level_counts_age = age_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            hover_info_age = [f'{levels[level][0]}: {level_counts_age.get(level, 0):.2f}%' for level in range(5)]
            hover_info_age.append(f'Average Depression Index: {age_avg_depression[age_group]:.2f}')
            hover_data_age.append('<br>'.join(hover_info_age))
        else:
            hover_data_age.append('No data available')

    #  pizza da idade
    fig_age = px.pie(
        names=age_counts.index,
        values=age_counts.values,
        title='Age distribution',
        hole=0.3,
        color=age_counts.index,
        color_discrete_map=age_colors,
        labels={'names': 'Faixa Etária', 'values': 'Número de Participantes'}
    )

    # salto
    fig_age.update_traces(
        texttemplate='%{percent:.3%} %{label}',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_age,  # Passando os dados customizados para o hover
        pull=[0.1] * len(age_counts)  # Puxando as fatias para fora (efeito de "salto")
    )


    st.plotly_chart(fig_age, use_container_width=True)


        #  porcentagem de níveis de depressão por idade
    age_level_data = []

    for age_group in age_labels:
        age_group_df = country_df[country_df['age_group'] == age_group]
        total_in_group = age_group_df.shape[0]
        if total_in_group > 0:
            level_counts = age_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression = age_group_df['indice_depressao'].mean()  
            for level, count in level_counts.items():
                age_level_data.append({
                    'Age Group': age_group,
                    'Level': levels[level][0], 
                    'Level Name': levels[level][0],  
                    'Percentage': count,
                    'Count': age_group_df['indice_depressao'].value_counts().get(level, 0),  # Contagem real de cada nível
                    
                })

  
    age_level_df = pd.DataFrame(age_level_data)

 
    fig_age_level = px.bar(
        age_level_df,
        x='Age Group',
        y='Percentage',
        color='Level',
        text='Percentage',
        title='Percentage of Depression Levels by Age',
        labels={'Age Group': 'Age', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level Name']  
    )

    # dados ao passar o mouse
    fig_age_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.2f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>",
    )

    fig_age_level.update_layout(barmode='stack')

   
    st.plotly_chart(fig_age_level, use_container_width=True)

     # pizza  educação
    education_counts = country_df['education'].value_counts().reindex([1, 2, 3, 4], fill_value=0)
    education_counts.index = [education_labels[i] for i in education_counts.index]

    # cores educação  
    education_colors = {
        'Less than high school': '#FF5733',  
        'High school': '#33FF57',           
        'University degree': '#3357FF',     
        'Graduate degree': '#FF33A8'        
    }


    #  pizza  educação
    education_counts = country_df['education'].value_counts().reindex([1, 2, 3, 4], fill_value=0)
    education_counts.index = [education_labels[i] for i in education_counts.index]

    # depois ver possibilidade de apagar , repetido  
    education_colors = {
        'Less than high school': '#FF5733',  
        'High school': '#33FF57',             
        'University degree': '#3357FF',      
        'Graduate degree': '#FF33A8'          
    }

    # pizza educação
    fig_education = px.pie(
        names=education_counts.index,
        values=education_counts.values,
        title='Distribution by Education',
        hole=0.3,
        color=education_counts.index,
        color_discrete_map=education_colors,
        labels={'names': 'Nível de Educação', 'values': 'Número de Participantes'}
    )

    # porcentagens e médias de níveis de depressão / educação
    hover_data_education = []
    for education, label in education_labels.items():
        education_group = country_df[country_df['education'] == education]
        total_education = education_group.shape[0]
        if total_education > 0:
            level_counts_education = education_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression_education = education_group['indice_depressao'].mean()
            hover_info_education = [f'{levels[level][0]}: {level_counts_education.get(level, 0):.2f}%' for level in range(5)]
            hover_info_education.append(f'Average Depression Index: {avg_depression_education:.2f}')
            hover_data_education.append('<br>'.join(hover_info_education))
        else:
            hover_data_education.append('No data available')

    # fatias
    fig_education.update_traces(
        texttemplate='%{percent:.3%} %{label}',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_education,
        pull=[0.1] * len(education_counts)  
     
    )
       

    # Atualizando  para exibir a legenda
    fig_education.update_layout(
        showlegend=True,
        legend_title_text='Nível de Educação'
    )

 
    st.plotly_chart(fig_education, use_container_width=True)




    #  gráfico  educação
    education_level_data = []

    for education, label in education_labels.items():
        education_group_df = country_df[country_df['education'] == education]
        total_in_group = education_group_df.shape[0]
        if total_in_group > 0:
            level_counts = education_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = education_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                education_level_data.append({
                    'Education': label,
                    'Level': levels[level][0],
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level],  
                    'Level Name': levels[level][0]  
                })

  
    education_level_df = pd.DataFrame(education_level_data)

    # criando o gráfico de barras
    fig_education_level = px.bar(
        education_level_df,
        x='Education',
        y='Percentage',
        color='Level',
        text='Percentage',  
        title='Percentage of Depression Levels by Education',
        labels={'Education': 'Nível de Educação', 'Percentage': 'Porcentagem'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level Name']  
    )

    # dados ao passra mouse
    fig_education_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.2f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>"
    )

    fig_education_level.update_layout(barmode='stack')


    st.plotly_chart(fig_education_level, use_container_width=True)


   
   #  de pizza estado civil
    married_counts = country_df['married'].value_counts().reindex([1, 2, 3], fill_value=0)
    married_counts.index = [married_labels[i] for i in married_counts.index]

    married_colors = {
        'Never married': '#40e0d0',    
        'Currently married': '#33FF57',     
        'Previously married': '#db0075'   
    }

    # pizza estado civil
    fig_married = px.pie(
        names=married_counts.index,
        values=married_counts.values,
        title='Distribution by Civil Status',
        hole=0.3,
        color=married_counts.index,
        color_discrete_map=married_colors,
        labels={'names': 'Marital status', 'values': 'Number of Participants'}
    )

   

    #  porcentagens
    hover_data_married = []
    for married, label in married_labels.items():
        married_group = country_df[country_df['married'] == married]
        total_married = married_group.shape[0]
        if total_married > 0:
            level_counts_married = married_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression_married = married_group['indice_depressao'].mean()
            hover_info_married = [f'{levels[level][0]}: {level_counts_married.get(level, 0):.2f}%' for level in range(5)]
            hover_info_married.append(f'Average Depression Index: {avg_depression_married:.2f}')
            hover_data_married.append('<br>'.join(hover_info_married))
        else:
            hover_data_married.append('No data available')

    #  fatias
    fig_married.update_traces(
        texttemplate='%{percent:.3%} %{label}',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_married,
        pull=[0.1] * len(married_counts)  
    )

   

    #  legenda 
    fig_married.update_layout(
        showlegend=True,
        legend_title_text='Marital Status'
    )

    # Exibindo o gráfico
    st.plotly_chart(fig_married, use_container_width=True)


        # Gráfico de porcentagem estado civil
    married_level_data = []

    for married, label in married_labels.items():
        married_group_df = country_df[country_df['married'] == married]
        total_in_group = married_group_df.shape[0]
        if total_in_group > 0:
            level_counts = married_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = married_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                married_level_data.append({
                    'Marital Status': label,
                    'Level': levels[level][0], 
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level]  
                })


    married_level_df = pd.DataFrame(married_level_data)

    # gráfico de barras
    fig_married_level = px.bar(
        married_level_df,
        x='Marital Status',
        y='Percentage',
        color='Level',
        text='Percentage',  
        title='Percentage of Depression Levels by Marital Status',
        labels={'Marital Status': 'Marital Status', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level'] 
    )

    #  contagem e nome do nível, ao passra mouse
    fig_married_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.2f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>"
    )

    fig_married_level.update_layout(barmode='stack')

   
    st.plotly_chart(fig_married_level, use_container_width=True)



def show_country_details():
   
    df = pd.read_csv('dataset.csv')

    # lista de países
    countries = ['Select Country']+['All Countries'] + [country for country in country_data.country_mapping.values()]


    selected_country = st.selectbox('', countries, key='select_country')

    #  definir uma fonte 
    st.markdown(
        """
        <style>
        .custom-title {
            font-size: 20px;
            font-weight: bold;
        }
        </style>
        
        """, 
        unsafe_allow_html=True
    )

   
    if selected_country != 'Select Country':

        level_layout(df, selected_country)
        
        # CSS 
        st.markdown(
            """
            <style>
            .custom-title {
                font-size: 22px;  /* Ajuste o tamanho conforme necessário */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # título
        st.markdown('<h1 class="custom-title">Resume</h1>', unsafe_allow_html=True)
        
        #  tabela para o país selecionado
        create_table(selected_country)

    
