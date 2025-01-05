import streamlit as st
import pandas as pd
from country_data import country_mapping 


gender_labels = {1: 'Gender Male', 2: 'Gender Female', 3: 'Gender Other'}
age_labels = ['18-34', '35-54', '55+']
depression_labels = {0: 'Normal', 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Extremely'}
married_labels = {1: 'Never Married', 2: 'Currently Married', 3: 'Previously Married'}

education_labels = {1: 'Less than high school', 2: 'High school', 3: 'University degree', 4: 'Graduate degree'}


def create_table(selected_country):
    try:
       
        df = pd.read_csv('dataset.csv')
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

  
    if selected_country != 'All Countries':
        country_code = next((key for key, value in country_mapping.items() if value == selected_country), None)
        if country_code is not None:
            df = df[df['country'] == country_code]

  
    if 'gender' in df.columns:
        df['gender'] = df['gender'].map(gender_labels)
    if 'age' in df.columns:
        max_age = df['age'].max()
        age_bins = [18, 34, 54, float('inf')]
        df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    if 'indice_depressao' in df.columns:
        df['depression_level'] = df['indice_depressao'].map(depression_labels)
    if 'married' in df.columns:
        df['married_status'] = df['married'].map(married_labels).fillna('Unknown')
    if 'education' in df.columns:
        df['education_level'] = df['education'].map(education_labels)

  
    gender_counts = df['gender'].value_counts()
    age_group_counts = df['age_group'].value_counts()
    married_counts = df['married_status'].value_counts()
    education_counts = df['education_level'].value_counts()

    # incialização do dataframe para receber porcentagens e m,edias 
    data = {
        'Category': [
            'Gender Male', 'Gender Female', 'Gender Other',
            'Age Group (18-34)', 'Age Group (35-54)', 'Age Group (55+)',
            'Never Married', 'Currently Married', 'Previously Married',
            'Less than high school', 'High school', 'University degree', 'Graduate degree'
        ],
        'Total': [
            gender_counts.get('Gender Male', 0),
            gender_counts.get('Gender Female', 0),
            gender_counts.get('Gender Other', 0),
            age_group_counts.get('18-34', 0),
            age_group_counts.get('35-54', 0),
            age_group_counts.get('55+', 0),
            married_counts.get('Never Married', 0),
            married_counts.get('Currently Married', 0),
            married_counts.get('Previously Married', 0),
            education_counts.get('Less than high school', 0),
            education_counts.get('High school', 0),
            education_counts.get('University degree', 0),
            education_counts.get('Graduate degree', 0)
        ]
    }

   
    for level in depression_labels.values():
        data[f'{level} (%)'] = [0] * len(data['Category'])

    data['Mean Depression Index'] = [0] * len(data['Category'])

    
    summary_df = pd.DataFrame(data)
    

 
    if 'gender' in df.columns and 'depression_level' in df.columns:
        depression_counts_gender = df.groupby(['gender', 'depression_level']).size().unstack(fill_value=0)
        for gender in gender_labels.values():
            if gender in depression_counts_gender.index:
                total = gender_counts.get(gender, 0)
                for level in depression_labels.values():
                    count = depression_counts_gender.loc[gender, level] if level in depression_counts_gender.columns else 0
                    percentage = (count / total) * 100 if total > 0 else 0
                    summary_df.loc[summary_df['Category'] == gender, f'{level} (%)'] = f'{percentage:.2f}'

              
                mean_depression = df[df['gender'] == gender]['indice_depressao'].mean()
                summary_df.loc[summary_df['Category'] == gender, 'Mean Depression Index'] = f'{mean_depression:.2f}'

   
    if 'age_group' in df.columns and 'depression_level' in df.columns:
        depression_counts_age = df.groupby(['age_group', 'depression_level']).size().unstack(fill_value=0)
        for age_group in age_labels:
            if age_group in depression_counts_age.index:
                total = age_group_counts.get(age_group, 0)
                for level in depression_labels.values():
                    count = depression_counts_age.loc[age_group, level] if level in depression_counts_age.columns else 0
                    percentage = (count / total) * 100 if total > 0 else 0
                    summary_df.loc[summary_df['Category'] == f'Age Group ({age_group})', f'{level} (%)'] = f'{percentage:.2f}'

               
                mean_depression = df[df['age_group'] == age_group]['indice_depressao'].mean()
                summary_df.loc[summary_df['Category'] == f'Age Group ({age_group})', 'Mean Depression Index'] = f'{mean_depression:.2f}'

   
    if 'married_status' in df.columns and 'depression_level' in df.columns:
        depression_counts_married = df.groupby(['married_status', 'depression_level']).size().unstack(fill_value=0)
        for married_status in married_labels.values():
            if married_status in depression_counts_married.index:
                total = married_counts.get(married_status, 0)
                for level in depression_labels.values():
                    count = depression_counts_married.loc[married_status, level] if level in depression_counts_married.columns else 0
                    percentage = (count / total) * 100 if total > 0 else 0
                    summary_df.loc[summary_df['Category'] == married_status, f'{level} (%)'] = f'{percentage:.2f}'

               
                mean_depression = df[df['married_status'] == married_status]['indice_depressao'].mean()
                summary_df.loc[summary_df['Category'] == married_status, 'Mean Depression Index'] = f'{mean_depression:.2f}'

   
    if 'education_level' in df.columns and 'depression_level' in df.columns:
        depression_counts_education = df.groupby(['education_level', 'depression_level']).size().unstack(fill_value=0)
        for education_level in education_labels.values():
            if education_level in depression_counts_education.index:
                total = education_counts.get(education_level, 0)
                for level in depression_labels.values():
                    count = depression_counts_education.loc[education_level, level] if level in depression_counts_education.columns else 0
                    percentage = (count / total) * 100 if total > 0 else 0
                    summary_df.loc[summary_df['Category'] == education_level, f'{level} (%)'] = f'{percentage:.2f}'

              
                mean_depression = df[df['education_level'] == education_level]['indice_depressao'].mean()
                summary_df.loc[summary_df['Category'] == education_level, 'Mean Depression Index'] = f'{mean_depression:.2f}'

   
    st.write(summary_df)



def main():
    st.title("Mental Health Indicators Analysis")

    selected_country = st.selectbox('Select a country', ['All Countries'] + list(country_mapping.values()))

    create_table(selected_country)


if __name__ == "__main__":
    main()
