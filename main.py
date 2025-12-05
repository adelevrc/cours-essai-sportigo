import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Analyse des inscriptions")

# 1️⃣ Télécharger le fichier CSV
uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
if uploaded_file is not None:
    # Lire le CSV
    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
    
    # Convertir creation_date en datetime
    df['creation_date_dt'] = df['creation_date'].apply(
        lambda x: datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
    )
    
    # Créer date_inscription au format dd-mm-yyyy
    df['date_inscription'] = df['creation_date_dt'].apply(lambda x: x.strftime("%d-%m-%Y"))
    
    # Nettoyer la colonne Type
    df['Type_clean'] = df['Type'].str.strip().str.lower()
    
    # Normaliser le téléphone
    def normalize_phone(x):
        if pd.isna(x) or str(x).strip() == '':
            return ''
        x_str = str(int(x)) if isinstance(x, float) else str(x).strip()
        if x_str.startswith('0') or x_str.startswith('33'):
            return x_str
        else:
            return '33' + x_str

    df['Téléphone'] = df['Téléphone'].apply(normalize_phone)
    
    # Trier par date croissante
    df = df.sort_values(by='creation_date_dt', ascending=True)
    
    # Colonnes finales
    df_final = df[['Nom', 'Prénom', 'Type', 'date_inscription', 'Téléphone']]

    # 2️⃣ Tableau des prospects
    prospects = df_final[df_final['Type'].str.lower() == 'prospect']
    st.subheader("Tableau des prospects")
    st.dataframe(prospects)

    # 3️⃣ Tableau des try_lesson
    try_lesson = df_final[df_final['Type'].str.lower() == 'try-lesson']
    st.subheader("Tableau des try_lesson")
    st.dataframe(try_lesson)
