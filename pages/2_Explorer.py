"""
WildFlix — Explorer le catalogue
Cinéma de la Creuse — Projet Data Analyst RNCP 37837
"""

import streamlit as st
import pandas as pd
import pickle

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(
    page_title="WildFlix — Explorer",
    page_icon="🎬",
    layout="wide"
)

# ===============================
# CSS THÈME NOIR/ROUGE
# ===============================
st.markdown("""
<style>
  .stApp { background-color: #0a0a0a; color: #ffffff; }
  [data-testid="stHeader"] { display: none; }
  footer { display: none; }
  .block-container { padding-top: 2rem !important; }

  [data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #222222;
  }
  [data-testid="stSidebar"] * { color: #cccccc !important; }

  h1, h2, h3 { color: #ffffff !important; font-family: 'Arial Black', sans-serif; }
  hr { border-color: #222222 !important; }
  p, label, .stMarkdown { color: #cccccc !important; }

  .stSelectbox > div > div {
    background-color: #1a1a1a !important;
    border: 1px solid #333333 !important;
    color: #ffffff !important;
  }
  .stSlider { color: #cccccc !important; }
  .stRadio label { color: #cccccc !important; }
  .stRadio [data-testid="stMarkdownContainer"] p { color: #cccccc !important; }

  /* Radio buttons */
  .stRadio > div {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 8px 16px;
    gap: 16px;
  }

  /* Metric */
  [data-testid="stMetric"] {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-left: 3px solid #c0392b;
    border-radius: 4px;
    padding: 12px;
  }
  [data-testid="stMetricLabel"] { color: #888888 !important; }
  [data-testid="stMetricValue"] { color: #ffffff !important; }

  /* Expander */
  .streamlit-expanderHeader {
    background-color: #1a1a1a !important;
    color: #cccccc !important;
    border: 1px solid #333333 !important;
  }
  .streamlit-expanderContent {
    background-color: #111111 !important;
    color: #aaaaaa !important;
    border: 1px solid #333333 !important;
  }

  .stCaptionContainer, caption { color: #666666 !important; }

  /* Ligne rouge sous titre */
  .red-line {
    width: 48px;
    height: 3px;
    background: #c0392b;
    margin-bottom: 20px;
    border-radius: 2px;
  }

  /* Warning */
  .stAlert { background-color: #1a1a1a !important; border-color: #333333 !important; }
</style>
""", unsafe_allow_html=True)

# ===============================
# CHARGEMENT
# ===============================
@st.cache_resource
def charger_modele():
    with open('models/modele_reco.pkl', 'rb') as f:
        return pickle.load(f)

elements = charger_modele()
df = elements['df']

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("assets/wildflix_logo.png", use_container_width=True)
    st.markdown("---")
    st.markdown("[← Accueil](/Accueil)", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Harry • Thibaud • Owen • Vasanth")

# ===============================
# EN-TÊTE
# ===============================
st.markdown("# Explorer le catalogue")
st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)
st.markdown(f"Recherchez parmi **{len(df)} films** par genre, réalisateur ou acteur.")
st.markdown("---")

# ===============================
# MODE DE RECHERCHE
# ===============================
mode = st.radio(
    "Rechercher par :",
    ["Genre", "Réalisateur", "Acteur"],
    horizontal=True
)

st.markdown("---")

# ===============================
# MODE GENRE
# ===============================
if mode == "Genre":
    tous_genres = set()
    for col in ['genre_1', 'genre_2', 'genre_3']:
        tous_genres.update(df[col].dropna().unique())

    col1, col2 = st.columns([2, 1])
    with col1:
        genre_choisi = st.selectbox("Choisissez un genre :", sorted(tous_genres))
    with col2:
        n_films = st.slider("Nombre de films", 4, 24, 12)

    masque = (
        (df['genre_1'] == genre_choisi) |
        (df['genre_2'] == genre_choisi) |
        (df['genre_3'] == genre_choisi)
    )
    resultats = df[masque].sort_values('imdb_score', ascending=False).head(n_films)
    st.markdown(f"**{len(resultats)} films** trouvés dans le genre *{genre_choisi}*")

# ===============================
# MODE RÉALISATEUR
# ===============================
elif mode == "Réalisateur":
    reals = sorted(df['director_name'].dropna().unique().tolist())

    col1, col2 = st.columns([2, 1])
    with col1:
        real_choisi = st.selectbox("Choisissez un réalisateur :", reals)
    with col2:
        n_films = st.slider("Nombre de films", 4, 24, 12)

    resultats = df[df['director_name'] == real_choisi].sort_values('imdb_score', ascending=False).head(n_films)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Films dans le catalogue", len(resultats))
    col_b.metric("Note moyenne IMDb", f"{resultats['imdb_score'].mean():.1f} / 10")
    col_c.metric("Période", f"{int(resultats['title_year'].min())} – {int(resultats['title_year'].max())}")

# ===============================
# MODE ACTEUR
# ===============================
elif mode == "Acteur":
    acteurs = set()
    for col in ['actor_1_name', 'actor_2_name', 'actor_3_name']:
        acteurs.update(df[col].dropna().unique())

    col1, col2 = st.columns([2, 1])
    with col1:
        acteur_choisi = st.selectbox("Choisissez un acteur :", sorted(acteurs))
    with col2:
        n_films = st.slider("Nombre de films", 4, 24, 12)

    masque_a = (
        (df['actor_1_name'] == acteur_choisi) |
        (df['actor_2_name'] == acteur_choisi) |
        (df['actor_3_name'] == acteur_choisi)
    )
    resultats = df[masque_a].sort_values('imdb_score', ascending=False).head(n_films)
    st.markdown(f"**{len(resultats)} films** avec *{acteur_choisi}*")

# ===============================
# AFFICHAGE DES RÉSULTATS
# ===============================
if len(resultats) == 0:
    st.warning("Aucun film trouvé pour cette sélection.")
else:
    cols = st.columns(4)
    for i, (_, row) in enumerate(resultats.iterrows()):
        with cols[i % 4]:
            if pd.notna(row.get('poster')) and row['poster'] != 'N/A':
                st.image(row['poster'], use_container_width=True)
            else:
                st.markdown("*Affiche indisponible*")

            st.markdown(f"**{row['movie_title'].strip()}**")
            st.caption(f"{int(row['title_year'])} • {row['imdb_score']}/10")
            genres = [row[g] for g in ['genre_1','genre_2','genre_3'] if pd.notna(row[g])]
            st.caption(", ".join(genres))

            with st.expander("Synopsis"):
                st.write(row['plot'] if pd.notna(row.get('plot')) else "Non disponible")

st.markdown("---")
st.markdown("*Données IMDb + OMDb — Cinéma de la Creuse*")
