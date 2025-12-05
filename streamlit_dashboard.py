"sales_data 5.csv""sales_data 5.csv"import streamlit as st
import pandas as pd
import plotly.express as px
# ... (Gardez les autres imports si nécessaires)

# --- Configuration de la page ---
st.set_page_config(layout="wide")

# --- ÉTAPE 1 : CHARGEMENT ET PRÉPARATION DES DONNÉES ---
try:
    df = pd.read_csv("sales_data 5.csv")
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
except FileNotFoundError:
    st.error("ERREUR : Le fichier 'sales_data 6.csv' est introuvable. Assurez-vous qu'il est sur GitHub.")
    st.stop() # Arrête l'exécution si le fichier n'est pas trouvé

# --- ÉTAPE 2 : DÉFINITION DE LA MISE EN PAGE ET DES FILTRES ---
st.title('Dashboard Interactif des Ventes 📈')
st.markdown("Analyse des performances par région, catégorie et période.")

# Utilisation des 'sidebar' Streamlit pour les filtres
st.sidebar.header("Options de Filtrage")

# Filtre pour la région (Dropdown/Multiselect)
selected_regions = st.sidebar.multiselect(
    'Filtrer par Région :',
    options=df['Region'].unique().tolist(),
    default=df['Region'].unique().tolist()
)

# Filtre pour la date (Range Slider ou Selectbox)
min_date = df['Sale_Date'].min().date()
max_date = df['Sale_Date'].max().date()
# Note: Streamlit n'a pas de DatePickerRange aussi sophistiqué que Dash, on peut utiliser des inputs séparés
start_date = st.sidebar.date_input("Date de Début", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Date de Fin", value=max_date, min_value=min_date, max_value=max_date)

# 3. Filtrer les données en fonction des sélections de l'utilisateur
# Conversion des dates Streamlit en datetime pour la comparaison
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)

filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Sale_Date'] >= start_date_dt) &
    (df['Sale_Date'] <= end_date_dt)
]

# Affichage des graphiques (le 'callback' est implicite dans Streamlit)
if filtered_df.empty:
    st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
else:
    # Graphique en ligne : Évolution des ventes dans le temps
    sales_over_time = filtered_df.groupby(filtered_df['Sale_Date'].dt.date)['Sales_Amount'].sum().reset_index()
    fig_line = px.line(
        sales_over_time, x='Sale_Date', y='Sales_Amount',
        title='Évolution Temporelle des Ventes', labels={'Sale_Date': 'Date', 'Sales_Amount': 'Montant'}
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Disposition des deux autres graphiques côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres : Ventes par représentant
        fig_bar = px.bar(
            filtered_df, x='Sales_Rep', y='Sales_Amount', color='Region',
            title='Ventes par Représentant'
        ).update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Graphique circulaire : Répartition par catégorie
        fig_pie = px.pie(
            filtered_df, names='Product_Category', values='Sales_Amount',
            title='Répartition des Ventes par Catégorie'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
