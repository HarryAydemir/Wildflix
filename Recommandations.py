"""
Application Streamlit - Système de recommandation de films
Cinéma de la Creuse - Projet Data Analyst RNCP 37837
"""

import streamlit as st
import pandas as pd
import pickle

# ===============================
# CONFIGURATION DE LA PAGE
# ===============================
st.set_page_config(
    page_title="🎬 Cinéma Creuse",
    page_icon="🎬",
    layout="wide"
)

# ===============================
# CHARGEMENT DU MODÈLE (en cache)
# ===============================
@st.cache_resource
def charger_modele():
    """Charge le modèle pré-entraîné depuis le fichier pickle"""
    with open('models/modele_reco.pkl', 'rb') as f:
        elements = pickle.load(f)
    return elements

elements = charger_modele()
modele = elements['modele']
X_scaled = elements['X_scaled']
df = elements['df']

# ===============================
# EN-TÊTE DE LA PAGE
# ===============================
st.title("🎬 Cinéma Creuse — Recommandations personnalisées")
st.markdown("**Trouvez votre prochain film coup de cœur** à partir d'un titre que vous avez aimé.")
st.markdown("---")

# ===============================
# BARRE LATÉRALE
# ===============================
with st.sidebar:
    st.image("assets/wildflix_logo.png", use_container_width=True)
    st.markdown("---")
    st.caption("Un projet réalisé par Harry, Thibaud, Owen et Vasanth")
    
# ===============================
# FORMULAIRE PRINCIPAL
# ===============================
col1, col2 = st.columns([3, 1])

with col1:
    # Liste déroulante avec tous les films (triés alphabétiquement)
    liste_films = sorted(df['movie_title'].str.strip().unique().tolist())
    film_choisi = st.selectbox(
        "🎥 Choisissez un film que vous avez aimé :",
        options=liste_films,
        index=liste_films.index('Inception') if 'Inception' in liste_films else 0
    )

with col2:
    n_recos = st.slider("Nombre de recommandations", 3, 10, 5)

# ===============================
# FONCTION DE RECOMMANDATION
# ===============================
def recommander(titre, n=5):
    masque = df['movie_title'].str.strip() == titre
    if not masque.any():
        return None
    idx = df[masque].index[0]
    distances, indices = modele.kneighbors([X_scaled[idx]], n_neighbors=n+1)
    return list(zip(indices[0][1:], distances[0][1:]))

# ===============================
# AFFICHAGE DES RECOMMANDATIONS
# ===============================
if st.button("🎯 Voir les recommandations", type="primary"):
    
    # Infos du film de référence
    info_film = df[df['movie_title'].str.strip() == film_choisi].iloc[0]
    
    st.markdown("### 📽️ Film de référence")
    col_aff, col_info = st.columns([1, 3])
    
    with col_aff:
        if pd.notna(info_film.get('poster')) and info_film['poster'] != 'N/A':
            st.image(info_film['poster'], width=200)
        else:
            st.markdown("🎞️ *Affiche non disponible*")
    
    with col_info:
        st.markdown(f"### {info_film['movie_title'].strip()} ({int(info_film['title_year'])})")
        st.markdown(f"**⭐ Note IMDb** : {info_film['imdb_score']} / 10")
        st.markdown(f"**🎬 Réalisateur** : {info_film.get('director_name', 'N/A')}")
        genres = [info_film[g] for g in ['genre_1', 'genre_2', 'genre_3'] if pd.notna(info_film[g])]
        st.markdown(f"**🏷️ Genres** : {', '.join(genres)}")
        if pd.notna(info_film.get('plot')):
            st.markdown(f"**📖 Synopsis** : *{info_film['plot']}*")
    
    st.markdown("---")
    st.markdown(f"### 🎯 Top {n_recos} recommandations pour vous")
    
    # Recommandations
    recos = recommander(film_choisi, n_recos)
    
    if recos:
        # Affichage en colonnes (5 par ligne max)
        cols_par_ligne = min(5, n_recos)
        cols = st.columns(cols_par_ligne)
        
        for i, (idx_voisin, dist) in enumerate(recos):
            v = df.iloc[idx_voisin]
            similarite = round((1 - dist) * 100, 1)
            
            with cols[i % cols_par_ligne]:
                # Affiche
                if pd.notna(v.get('poster')) and v['poster'] != 'N/A':
                    st.image(v['poster'], use_container_width=True)
                
                # Infos
                st.markdown(f"**{v['movie_title'].strip()}**")
                st.caption(f"📅 {int(v['title_year'])} • ⭐ {v['imdb_score']}/10")
                st.caption(f"🎬 {v.get('director_name', 'N/A')}")
                st.progress(similarite / 100, text=f"Similarité : {similarite}%")
                
                # Bouton détails (optionnel)
                with st.expander("Voir le synopsis"):
                    if pd.notna(v.get('plot')):
                        st.write(v['plot'])
                    else:
                        st.write("Synopsis non disponible")

# ===============================
# PIED DE PAGE
# ===============================
st.markdown("---")
st.markdown("*Données IMDb + OMDb — Modèle Nearest Neighbors avec Cosine Similarity*")