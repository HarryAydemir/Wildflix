"""
WildFlix — Page d'accueil
Cinéma de la Creuse — Projet Data Analyst RNCP 37837
"""

import streamlit as st
import time

# ===============================
# CONFIGURATION DE LA PAGE
# ===============================
st.set_page_config(
    page_title="WildFlix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# CSS GLOBAL — Design premium sombre
# ===============================
st.markdown("""
<style>
  /* Masquer sidebar et header Streamlit */
  [data-testid="stSidebar"] { display: none; }
  [data-testid="stHeader"]  { display: none; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  footer { display: none; }

  /* Fond noir cinéma */
  .stApp {
    background-color: #0a0a0a;
    color: #ffffff;
  }

  /* ---- HERO ---- */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 40px;
    background: radial-gradient(ellipse at center, #1a0a0a 0%, #0a0a0a 70%);
    overflow: hidden;
  }

  /* Lignes décoratives verticales */
  .hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
      90deg,
      transparent,
      transparent 120px,
      rgba(180, 20, 20, 0.04) 120px,
      rgba(180, 20, 20, 0.04) 121px
    );
    pointer-events: none;
  }

  /* ---- LOGO ---- */
  .wildflix-logo {
    font-family: 'Arial Black', sans-serif;
    font-size: clamp(64px, 10vw, 96px);
    font-weight: 900;
    letter-spacing: -2px;
    color: #ffffff;
    margin-bottom: 8px;
    line-height: 1;
  }
  .wildflix-logo span {
    color: #c0392b;
  }

  /* Trait rouge sous le logo */
  .logo-line {
    width: 80px;
    height: 4px;
    background: #c0392b;
    margin: 0 auto 24px auto;
    border-radius: 2px;
  }

  /* ---- TAGLINE ---- */
  .tagline {
    font-size: 16px;
    color: #888888;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 60px;
    font-family: 'Calibri', sans-serif;
  }

  /* ---- CITATION ---- */
  .citation-wrapper {
    max-width: 760px;
    margin: 0 auto 60px auto;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .citation-text {
    font-size: clamp(18px, 2.5vw, 26px);
    color: #f0f0f0;
    font-style: italic;
    line-height: 1.55;
    text-align: center;
    font-family: Georgia, serif;
    margin-bottom: 16px;
    opacity: 1;
    transition: opacity 0.5s ease;
  }

  .citation-text::before { content: '\u201c'; color: #c0392b; }
  .citation-text::after  { content: '\u201d'; color: #c0392b; }

  .citation-author {
    font-size: 13px;
    color: #c0392b;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'Calibri', sans-serif;
  }

  /* ---- BOUTON ---- */
  .btn-enter-wrapper {
    margin-top: 10px;
  }
  .btn-enter {
    display: inline-block;
    background: #c0392b;
    color: white !important;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 18px 52px;
    border: none;
    border-radius: 2px;
    cursor: pointer;
    text-decoration: none;
    font-family: 'Arial Black', sans-serif;
    transition: background 0.2s ease, transform 0.1s ease;
  }
  .btn-enter:hover {
    background: #a93226;
    transform: translateY(-1px);
  }

  /* ---- BAS DE PAGE ---- */
  .hero-footer {
    position: absolute;
    bottom: 32px;
    left: 0; right: 0;
    text-align: center;
    font-size: 11px;
    color: #333333;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Calibri', sans-serif;
  }

  /* ---- FILMS EN FOND (ticker) ---- */
  .films-ticker {
    position: absolute;
    bottom: 70px;
    left: 0; right: 0;
    overflow: hidden;
    white-space: nowrap;
    opacity: 0.12;
    font-size: 13px;
    color: #ffffff;
    letter-spacing: 2px;
    font-family: 'Calibri', sans-serif;
  }
  .films-ticker span {
    display: inline-block;
    animation: ticker 30s linear infinite;
    padding-right: 80px;
  }
  @keyframes ticker {
    from { transform: translateX(100vw); }
    to   { transform: translateX(-100%); }
  }

  /* Cacher le bouton Streamlit natif */
  div[data-testid="stHorizontalBlock"] button { display: none; }
</style>
""", unsafe_allow_html=True)

# ===============================
# CITATIONS CINEMA
# ===============================
CITATIONS = [
    {
        "texte": "Le cinema, c'est l'ecriture moderne dont l'encre est la lumiere.",
        "auteur": "Jean Cocteau"
    },
    {
        "texte": "Je fais des films pour ne pas vivre ma vie.",
        "auteur": "Francois Truffaut"
    },
    {
        "texte": "Un film, c'est une fille et un revolver.",
        "auteur": "Jean-Luc Godard"
    },
    {
        "texte": "La perfection n'est pas atteinte quand il n'y a plus rien a ajouter, mais quand il n'y a plus rien a enlever.",
        "auteur": "Stanley Kubrick"
    },
    {
        "texte": "Pour moi, les films sont comme des reves que tu te rappelles encore en etant eveille.",
        "auteur": "Steven Spielberg"
    },
    {
        "texte": "Je vole des films a des gens qui font de grands films.",
        "auteur": "Quentin Tarantino"
    },
    {
        "texte": "L'idee est de compresser le temps pour que les gens vivent quelque chose d'impossible.",
        "auteur": "Christopher Nolan"
    },
    {
        "texte": "Si tu veux envoyer un message, utilise Western Union. Un film, c'est fait pour raconter une histoire.",
        "auteur": "Samuel Goldwyn"
    },
    {
        "texte": "Il n'y a pas de regles au cinema. C'est ce qui est excitant.",
        "auteur": "Orson Welles"
    },
    {
        "texte": "Le cinema est un miroir de la societe, et parfois il la devance.",
        "auteur": "Martin Scorsese"
    },
]

FILMS_TICKER = "Inception  •  Pulp Fiction  •  2001 l'Odyssee de l'Espace  •  The Dark Knight  •  Parasite  •  Le Parrain  •  Blade Runner  •  Interstellar  •  Forrest Gump  •  Schindler's List  •  Fight Club  •  The Matrix  •  Good Fellas  •  Casablanca  •  Metropolis  •  7th Art  •  "

# ===============================
# GESTION DE LA CITATION COURANTE
# ===============================
if "citation_idx" not in st.session_state:
    st.session_state.citation_idx = 0
if "last_change" not in st.session_state:
    st.session_state.last_change = time.time()

# Changer la citation toutes les 5 secondes
now = time.time()
if now - st.session_state.last_change > 5:
    st.session_state.citation_idx = (st.session_state.citation_idx + 1) % len(CITATIONS)
    st.session_state.last_change = now

citation = CITATIONS[st.session_state.citation_idx]

# ===============================
# RENDU HTML
# ===============================
st.markdown(f"""
<div class="hero">

  <!-- Ticker films en fond -->
  <div class="films-ticker">
    <span>{FILMS_TICKER * 3}</span>
  </div>

  <!-- Logo -->
  <div class="wildflix-logo">WILD<span>FLIX</span></div>
  <div class="logo-line"></div>

  <!-- Tagline -->
  <div class="tagline">Systeme de recommandation — Cinema de la Creuse</div>

  <!-- Citation -->
  <div class="citation-wrapper">
    <div class="citation-text">{citation['texte']}</div>
    <div class="citation-author">{citation['auteur']}</div>
  </div>

  <!-- Bouton -->
  <div class="btn-enter-wrapper">
    <a href="/Recommandations" class="btn-enter" target="_self">
      Entrer &nbsp;&#8594;
    </a>
  </div>

  <!-- Footer -->
  <div class="hero-footer">
    Projet Data Analyst RNCP 37837 &nbsp;•&nbsp; Wild Code School &nbsp;•&nbsp; 2026
  </div>

</div>
""", unsafe_allow_html=True)

# ===============================
# AUTO-REFRESH toutes les 5 secondes
# (pour changer la citation sans interaction)
# ===============================
time.sleep(5)
st.rerun()
