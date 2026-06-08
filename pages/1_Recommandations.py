"""
WildFlix — Recommandations
Cinéma de la Creuse — Projet Data Analyst RNCP 37837
"""

import streamlit as st
import pandas as pd
import pickle

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(
    page_title="WildFlix — Recommandations",
    page_icon="🎬",
    layout="wide"
)

# ===============================
# CSS THÈME NOIR/ROUGE
# ===============================
st.markdown("""
<style>
  /* Fond noir */
  .stApp { background-color: #0a0a0a; color: #ffffff; }
  [data-testid="stHeader"] { display: none; }
  footer { display: none; }
  .block-container { padding-top: 2rem !important; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #222222;
  }
  [data-testid="stSidebar"] * { color: #cccccc !important; }

  /* Titres */
  h1, h2, h3 { color: #ffffff !important; font-family: 'Arial Black', sans-serif; }

  /* Séparateurs */
  hr { border-color: #222222 !important; }

  /* Texte standard */
  p, label, .stMarkdown { color: #cccccc !important; }

  /* Selectbox et slider */
  .stSelectbox > div > div {
    background-color: #1a1a1a !important;
    border: 1px solid #333333 !important;
    color: #ffffff !important;
  }
  .stSlider { color: #cccccc !important; }

  /* Bouton principal */
  .stButton > button[kind="primary"] {
    background-color: #c0392b !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 12px 36px !important;
    border-radius: 2px !important;
    font-family: 'Arial Black', sans-serif !important;
  }
  .stButton > button[kind="primary"]:hover {
    background-color: #a93226 !important;
  }

  /* Progress bar */
  .stProgress > div > div > div {
    background-color: #c0392b !important;
  }

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

  /* Metric */
  [data-testid="stMetric"] {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 12px;
  }
  [data-testid="stMetricLabel"] { color: #888888 !important; }
  [data-testid="stMetricValue"] { color: #ffffff !important; }

  /* Caption */
  .stCaptionContainer, caption { color: #777777 !important; }

  /* Encart "Pourquoi ce film" */
  .pourquoi-box {
    background: #1a1a1a;
    border-left: 3px solid #c0392b;
    padding: 8px 12px;
    border-radius: 2px;
    margin: 6px 0;
    font-size: 12px;
    color: #aaaaaa;
  }
  .pourquoi-box strong { color: #ffffff; }
  .pourquoi-box ul { margin: 4px 0 0 0; padding-left: 16px; }

  /* Titre logo dans sidebar */
  .sidebar-logo {
    font-family: 'Arial Black', sans-serif;
    font-size: 22px;
    color: #ffffff;
    letter-spacing: -1px;
  }
  .sidebar-logo span { color: #c0392b; }

  /* Ligne rouge décorative sous h1 */
  .red-line {
    width: 48px;
    height: 3px;
    background: #c0392b;
    margin-bottom: 20px;
    border-radius: 2px;
  }
</style>
""", unsafe_allow_html=True)

# ===============================
# CHARGEMENT DU MODÈLE
# ===============================
@st.cache_resource
def charger_modele():
    with open('models/modele_reco.pkl', 'rb') as f:
        return pickle.load(f)

elements = charger_modele()
modele   = elements['modele']
X_scaled = elements['X_scaled']
df       = elements['df']

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
st.markdown("# Recommandations")
st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)
st.markdown("Choisissez un film que vous avez aimé et découvrez des films similaires.")
st.markdown("---")

# ===============================
# FORMULAIRE
# ===============================
col1, col2 = st.columns([3, 1])

with col1:
    liste_films = sorted(df['movie_title'].str.strip().unique().tolist())
    film_choisi = st.selectbox(
        "Choisissez un film :",
        options=liste_films,
        index=liste_films.index('Inception') if 'Inception' in liste_films else 0
    )
with col2:
    n_recos = st.slider("Nombre de recommandations", 3, 10, 5)

# ===============================
# FONCTIONS
# ===============================
def recommander(titre, n=5):
    masque = df['movie_title'].str.strip() == titre
    if not masque.any():
        return None
    idx = df[masque].index[0]
    distances, indices = modele.kneighbors([X_scaled[idx]], n_neighbors=n+1)
    return list(zip(indices[0][1:], distances[0][1:]))

def expliquer_similarite(ref, reco):
    raisons = []
    if pd.notna(ref.get('director_name')) and pd.notna(reco.get('director_name')):
        if ref['director_name'] == reco['director_name']:
            raisons.append(f"<strong>Même réalisateur</strong> : {ref['director_name']}")
    genres_ref  = set([ref[g]  for g in ['genre_1','genre_2','genre_3']  if pd.notna(ref[g])])
    genres_reco = set([reco[g] for g in ['genre_1','genre_2','genre_3']  if pd.notna(reco[g])])
    communs = genres_ref & genres_reco
    if communs:
        nb = len(communs)
        label = "Genre commun" if nb == 1 else f"{nb} genres communs"
        raisons.append(f"<strong>{label}</strong> : {', '.join(sorted(communs))}")
    if pd.notna(ref.get('title_year')) and pd.notna(reco.get('title_year')):
        ecart = abs(int(ref['title_year']) - int(reco['title_year']))
        if ecart == 0:
            raisons.append(f"<strong>Même année</strong> ({int(ref['title_year'])})")
        elif ecart <= 3:
            raisons.append(f"<strong>Période très proche</strong> ({ecart} an{'s' if ecart > 1 else ''} d'écart)")
        elif ecart <= 8:
            raisons.append(f"Période proche ({ecart} ans d'écart)")
    if pd.notna(ref.get('imdb_score')) and pd.notna(reco.get('imdb_score')):
        ecart_note = abs(float(ref['imdb_score']) - float(reco['imdb_score']))
        if ecart_note <= 0.3:
            raisons.append(f"<strong>Notes très proches</strong> ({ref['imdb_score']} vs {reco['imdb_score']})")
        elif ecart_note <= 0.7:
            raisons.append(f"Notes similaires ({ref['imdb_score']} vs {reco['imdb_score']})")
    if not raisons:
        return "<em>Caractéristiques globales similaires.</em>"
    items = "".join([f"<li>{r}</li>" for r in raisons])
    return f"<ul style='margin:4px 0 0 0; padding-left:16px;'>{items}</ul>"

# ===============================
# AFFICHAGE
# ===============================
if st.button("Voir les recommandations", type="primary"):

    info_film = df[df['movie_title'].str.strip() == film_choisi].iloc[0]

    st.markdown("### Film de référence")
    col_aff, col_info = st.columns([1, 3])

    with col_aff:
        if pd.notna(info_film.get('poster')) and info_film['poster'] != 'N/A':
            st.image(info_film['poster'], width=200)
        else:
            st.markdown("*Affiche non disponible*")

    with col_info:
        st.markdown(f"### {info_film['movie_title'].strip()} ({int(info_film['title_year'])})")
        st.markdown(f"**Note IMDb** : {info_film['imdb_score']} / 10")
        st.markdown(f"**Réalisateur** : {info_film.get('director_name', 'N/A')}")
        genres = [info_film[g] for g in ['genre_1','genre_2','genre_3'] if pd.notna(info_film[g])]
        st.markdown(f"**Genres** : {', '.join(genres)}")
        if pd.notna(info_film.get('plot')):
            st.markdown(f"**Synopsis** : *{info_film['plot']}*")

    st.markdown("---")
    st.markdown(f"### Top {n_recos} recommandations")

    recos = recommander(film_choisi, n_recos)

    if recos:
        cols_par_ligne = min(5, n_recos)
        cols = st.columns(cols_par_ligne)

        for i, (idx_voisin, dist) in enumerate(recos):
            v = df.iloc[idx_voisin]
            similarite = round((1 - dist) * 100, 1)
            valeur_progress = max(0.0, min(1.0, similarite / 100))

            with cols[i % cols_par_ligne]:
                if pd.notna(v.get('poster')) and v['poster'] != 'N/A':
                    st.image(v['poster'], use_container_width=True)
                st.markdown(f"**{v['movie_title'].strip()}**")
                st.caption(f"{int(v['title_year'])} • {v['imdb_score']}/10")
                st.caption(f"{v.get('director_name', 'N/A')}")
                st.progress(valeur_progress, text=f"Similarité : {similarite}%")

                explication = expliquer_similarite(info_film, v)
                st.markdown(
                    f'<div class="pourquoi-box"><strong>Pourquoi ce film ?</strong>{explication}</div>',
                    unsafe_allow_html=True
                )
                with st.expander("Synopsis"):
                    st.write(v['plot'] if pd.notna(v.get('plot')) else "Non disponible")

st.markdown("---")
st.markdown("*Données IMDb + OMDb — Modèle Nearest Neighbors avec Cosine Similarity*")
