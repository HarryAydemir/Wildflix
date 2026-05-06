"""
Page 4 - Explorer
Filtres par genre, réalisateur ou acteur
"""

import streamlit as st
import pandas as pd
import pickle

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(page_title="Explorer", page_icon="🔍", layout="wide")

# ===============================
# CHARGEMENT DES DONNÉES
# ===============================
@st.cache_resource
def charger_donnees():
    with open('models/modele_reco.pkl', 'rb') as f:
        elements = pickle.load(f)
    return elements['df']

df = charger_donnees()

# ===============================
# EN-TÊTE
# ===============================
st.title("🔍 Explorer le catalogue")
st.markdown("**Trouvez des films selon vos critères** : par genre, réalisateur ou acteur favori.")
st.markdown("---")

# ===============================
# CHOIX DU MODE DE RECHERCHE
# ===============================
mode = st.radio(
    "🎯 Comment voulez-vous explorer ?",
    options=["🎭 Par genre", "🎬 Par réalisateur", "⭐ Par acteur"],
    horizontal=True
)

st.markdown("---")

# ===============================
# FONCTION D'AFFICHAGE DES FILMS
# ===============================
def afficher_films(films_df, n_max=12):
    """Affiche une grille de films avec leurs affiches"""
    if len(films_df) == 0:
        st.warning("Aucun film trouvé pour ce critère.")
        return
    
    # Limiter à n_max films
    films_df = films_df.head(n_max).reset_index(drop=True)
    
    st.success(f"✅ **{len(films_df)} film(s) trouvé(s)** (affichage des {min(len(films_df), n_max)} meilleurs)")
    
    # Affichage en grille de 4 colonnes
    cols_par_ligne = 4
    for i in range(0, len(films_df), cols_par_ligne):
        cols = st.columns(cols_par_ligne)
        for j, col in enumerate(cols):
            if i + j < len(films_df):
                film = films_df.iloc[i + j]
                with col:
                    # Affiche
                    if pd.notna(film.get('poster')) and film['poster'] != 'N/A':
                        st.image(film['poster'], use_container_width=True)
                    else:
                        st.markdown("🎞️ *Affiche non disponible*")
                    
                    # Infos
                    st.markdown(f"**{film['movie_title'].strip()}**")
                    st.caption(f"📅 {int(film['title_year'])} • ⭐ {film['imdb_score']}/10")
                    
                    genres = [film[g] for g in ['genre_1', 'genre_2', 'genre_3'] if pd.notna(film[g])]
                    st.caption(f"🏷️ {', '.join(genres)}")
                    
                    if pd.notna(film.get('director_name')):
                        st.caption(f"🎬 {film['director_name']}")
                    
                    # Synopsis dans un expander
                    with st.expander("📖 Synopsis"):
                        if pd.notna(film.get('plot')):
                            st.write(film['plot'])
                        else:
                            st.write("Synopsis non disponible")

# ===============================
# MODE 1 — FILTRE PAR GENRE
# ===============================
if mode == "🎭 Par genre":
    st.subheader("🎭 Recherche par genre")
    
    # Liste des genres disponibles (toutes positions)
    tous_genres = pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).dropna().unique()
    tous_genres = sorted(tous_genres)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        genre_choisi = st.selectbox(
            "Choisissez un genre :",
            options=tous_genres,
            index=tous_genres.index('Action') if 'Action' in tous_genres else 0
        )
    
    with col2:
        n_resultats = st.slider("Nombre de films à afficher", 4, 24, 12)
    
    # Filtrage des films contenant ce genre dans n'importe quelle colonne
    masque = (
        (df['genre_1'] == genre_choisi) |
        (df['genre_2'] == genre_choisi) |
        (df['genre_3'] == genre_choisi)
    )
    
    films_filtres = df[masque].sort_values('imdb_score', ascending=False)
    
    st.markdown(f"### 🎬 Top films de genre **{genre_choisi}**")
    afficher_films(films_filtres, n_max=n_resultats)


# ===============================
# MODE 2 — FILTRE PAR RÉALISATEUR
# ===============================
elif mode == "🎬 Par réalisateur":
    st.subheader("🎬 Recherche par réalisateur")
    
    # Liste des réalisateurs (avec au moins 1 film, triés alphabétiquement)
    realisateurs = sorted(df['director_name'].dropna().unique())
    
    real_choisi = st.selectbox(
        "Choisissez un réalisateur :",
        options=realisateurs,
        index=realisateurs.index('Christopher Nolan') if 'Christopher Nolan' in realisateurs else 0
    )
    
    # Filtrage
    films_filtres = df[df['director_name'] == real_choisi].sort_values('imdb_score', ascending=False)
    
    # Stats sur le réalisateur
    if len(films_filtres) > 0:
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("🎬 Films dans la base", len(films_filtres))
        col_s2.metric("⭐ Note moyenne", f"{films_filtres['imdb_score'].mean():.2f}/10")
        col_s3.metric("📅 Période", f"{int(films_filtres['title_year'].min())}–{int(films_filtres['title_year'].max())}")
    
    st.markdown(f"### 🎬 Films réalisés par **{real_choisi}**")
    afficher_films(films_filtres, n_max=24)


# ===============================
# MODE 3 — FILTRE PAR ACTEUR
# ===============================
elif mode == "⭐ Par acteur":
    st.subheader("⭐ Recherche par acteur")
    
    # On combine les 3 colonnes d'acteurs pour avoir tous les acteurs uniques
    tous_acteurs = pd.concat([df['actor_1_name'], df['actor_2_name'], df['actor_3_name']])
    tous_acteurs = sorted(tous_acteurs.dropna().unique())
    
    acteur_choisi = st.selectbox(
        "Choisissez un acteur :",
        options=tous_acteurs,
        index=tous_acteurs.index('Leonardo DiCaprio') if 'Leonardo DiCaprio' in tous_acteurs else 0
    )
    
    # Filtrage : l'acteur peut être en position 1, 2 ou 3
    masque = (
        (df['actor_1_name'] == acteur_choisi) |
        (df['actor_2_name'] == acteur_choisi) |
        (df['actor_3_name'] == acteur_choisi)
    )
    
    films_filtres = df[masque].sort_values('imdb_score', ascending=False)
    
    # Stats sur l'acteur
    if len(films_filtres) > 0:
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("🎬 Films dans la base", len(films_filtres))
        col_s2.metric("⭐ Note moyenne", f"{films_filtres['imdb_score'].mean():.2f}/10")
        col_s3.metric("📅 Période", f"{int(films_filtres['title_year'].min())}–{int(films_filtres['title_year'].max())}")
    
    st.markdown(f"### ⭐ Films avec **{acteur_choisi}**")
    afficher_films(films_filtres, n_max=24)


# ===============================
# PIED DE PAGE
# ===============================
st.markdown("---")
st.caption("🔍 Catalogue de 1000 films cultes — Données IMDb + OMDb")

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("assets/wildflix_logo.png", use_container_width=True)
    st.markdown("---")
    st.caption("Un projet réalisé par Harry, Thibaud, Owen et Vasanth")