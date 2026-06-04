"""
Page 2 - Étude de marché Creuse
Synthèse contextuelle pour le projet de système de recommandation
"""

import streamlit as st
import pandas as pd

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(page_title="Étude de marché Creuse", page_icon="📊", layout="wide")

# ===============================
# STYLE CUSTOM POUR LES BLOCS
# ===============================
def bloc_info(contenu):
    st.markdown(
        f'<div style="background-color: #F5F5F5; border-left: 4px solid #888888; padding: 15px 20px; border-radius: 4px; margin: 10px 0;">{contenu}</div>',
        unsafe_allow_html=True
    )

def bloc_swot(titre, items):
    items_html = "".join([f"<li>{item}</li>" for item in items])
    st.markdown(
        f'<div style="background-color: #F5F5F5; border-left: 4px solid #666666; padding: 15px 20px; border-radius: 4px; margin: 10px 0; min-height: 200px;"><h4 style="margin-top: 0; color: #333333;">{titre}</h4><ul style="margin-bottom: 0; padding-left: 20px;">{items_html}</ul></div>',
        unsafe_allow_html=True
    )

# ===============================
# EN-TÊTE
# ===============================
st.title("Étude de marché — Cinéma en Creuse")
st.markdown("### Phase 1 du projet — Analyse du contexte local")
st.markdown("---")

# ===============================
# CONTEXTE
# ===============================
st.header("1. Contexte et enjeux")

st.markdown("""
Un cinéma indépendant situé dans le département de la Creuse (23) souhaite engager 
un **virage numérique** pour fidéliser son public local et en attirer de nouveaux. 
La direction a fait appel à un data analyst freelance afin de concevoir un 
**système de recommandation de films personnalisé**, complété par un dashboard 
de pilotage des indicateurs clés.

Cette étude poursuit trois objectifs :
- Caractériser la zone de chalandise (démographie, pouvoir d'achat)
- Cartographier l'offre cinématographique existante en Creuse  
- Établir un profil-type du spectateur creusois pour orienter le système de recommandation
""")

st.markdown("---")

# ===============================
# DÉMOGRAPHIE
# ===============================
st.header("2. Profil démographique de la Creuse")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Population (2023)", "115 527", "-2,62% vs 2017")
col2.metric("Densité", "20,8 hab/km²", "5× moins que France")
col3.metric("Part des 60+", "39,3%", "+12,7 pts vs France")
col4.metric("Revenu moyen", "18 166 €", "-12% vs France")

st.markdown("""
La Creuse est le **deuxième département le moins peuplé de France métropolitaine**, 
après la Lozère. Sa population décroît régulièrement (-780 habitants/an en moyenne) 
et **vieillit fortement** : 39,3 % de la population a plus de 60 ans, contre 26,6 % 
au niveau national.

Cette structure démographique est un facteur **central** pour notre projet : 
le cœur de cible naturel du cinéma creusois est constitué de **spectateurs séniors**, 
qui ont des préférences cinématographiques bien identifiées par les études CNC.
""")

st.subheader("Comparaison Creuse / France")
demo_data = pd.DataFrame({
    "Tranche d'âge": ["Moins de 30 ans", "60 ans et plus", "Indice de vieillissement", "Part des retraités"],
    "Creuse": ["25,5 %", "39,3 %", "166", "39,7 %"],
    "France": ["35,1 %", "26,6 %", "≈ 80", "26,8 %"],
    "Écart": ["-9,6 pts", "+12,7 pts", "× 2", "+12,9 pts"]
})
st.dataframe(demo_data, use_container_width=True, hide_index=True)

st.markdown("---")

# ===============================
# OFFRE LOCALE
# ===============================
st.header("3. L'offre cinéma locale")

st.markdown("""
Le département dispose actuellement de **5 cinémas actifs**, répartis sur les 
principales villes du territoire. Tous sont des cinémas de proximité avec un 
petit nombre de salles, classés en majorité **Art et Essai**.
""")

cinemas_data = pd.DataFrame({
    "Cinéma": ["Le Sénéchal", "Le Colbert", "Claude Miller", "L'Eden", "L'Alpha", "TOTAL"],
    "Commune": ["Guéret", "Aubusson", "Bourganeuf", "La Souterraine", "Évaux-les-Bains", "5 communes"],
    "Salles": ["5", "2", "1", "1", "1", "10"],
    "Fauteuils": ["697", "379", "287", "190", "172", "≈ 1 725"],
    "Entrées 2024": ["94 792", "≈ 22 000", "≈ 12 500", "12 305", "13 747", "≈ 155 000"]
})
st.dataframe(cinemas_data, use_container_width=True, hide_index=True)

bloc_info("<strong>Insight clé</strong> : avec ≈ 155 000 entrées en 2024 pour 115 527 habitants, l'indice de fréquentation creusois est de <strong>1,34 entrée par habitant</strong>, soit nettement inférieur à la moyenne nationale de <strong>2,73</strong>. Le potentiel d'attraction de nouveaux spectateurs existe, à condition de proposer une expérience adaptée.")

bloc_info("<strong>Bonne nouvelle</strong> : selon le CNC, la fréquentation cinématographique est en <strong>croissance forte de +20 % sur 10 ans</strong> dans les zones rurales. Le cinéma creusois s'inscrit dans un segment porteur.")

st.markdown("---")

# ===============================
# PROFIL SPECTATEUR
# ===============================
st.header("4. Profil-type du spectateur creusois")

st.markdown("""
Le croisement des données démographiques de la Creuse avec les études CNC sur les 
pratiques des Français permet de dresser un profil-type fiable du spectateur creusois moyen.
""")

profils_data = pd.DataFrame({
    "Profil": ["Sénior fidèle (50+)", "Famille / public mixte", "Jeune adulte (-30)"],
    "Part estimée": ["≈ 50 %", "≈ 30 %", "≈ 20 %"],
    "Attentes principales": [
        "Films français, drames, comédies, séances après-midi",
        "Animation, blockbuster, sorties week-end",
        "Blockbusters US, action, science-fiction"
    ],
    "Genres préférés": [
        "Comédie FR, drame, biopic, romance",
        "Animation, aventure, comédie familiale",
        "Action, SF, thriller, super-héros"
    ]
})
st.dataframe(profils_data, use_container_width=True, hide_index=True)

st.markdown("""
**Source CNC** : les seniors fréquentent les salles **plus assidûment** que la 
moyenne (4,2 entrées par an contre 3,8 toutes tranches confondues). Les films 
français réalisent **43,5 % de leurs entrées auprès des seniors**.
""")

st.markdown("---")

# ===============================
# PRÉFÉRENCES
# ===============================
st.header("5. Préférences cinématographiques")

st.subheader("Top 5 des films préférés des Français de 65+ (enquête BVA)")

st.markdown("""
1. **Le Vieux Fusil** (1975) — drame de guerre
2. **Intouchables** (2011) — comédie dramatique française
3. **La Grande Vadrouille** (1966) — comédie classique
4. **Les Tontons Flingueurs** (1963) — comédie patrimoniale
5. **Bienvenue chez les Ch'tis** (2008) — comédie populaire
""")

st.markdown("""
Cette hiérarchie reflète une orientation très marquée : **comédies françaises** 
(3 sur 5), **patrimoine cinématographique français** (2 sur 5). Les genres 
américains, les blockbusters d'action ou la science-fiction sont absents de ce classement.

**Implication directe** pour le système de recommandation : prioriser les genres 
**Comédie**, **Drame**, **Animation/Famille**, et **Aventure/Biopic**.
""")

st.markdown("---")

# ===============================
# SWOT
# ===============================
st.header("6. Analyse SWOT")

col_swot1, col_swot2 = st.columns(2)

with col_swot1:
    bloc_swot("FORCES", [
        "Public sénior fidèle et assidu (4,2 entrées/an)",
        "Faible concurrence locale (5 cinémas seulement)",
        "Maillage Art et Essai bien implanté",
        "Dynamique nationale rurale en croissance (+20 % sur 10 ans)",
        "Année 2024 en hausse partout dans le département"
    ])
    
    bloc_swot("OPPORTUNITÉS", [
        "Outil de recommandation = différenciation forte",
        "Tarifs préférentiels seniors (potentiel non saturé)",
        "Films français porteurs (43,5 % entrées seniors)",
        "Partenariats avec EHPAD, MJC, associations seniors",
        "Cinéma comme lien social en zone rurale"
    ])

with col_swot2:
    bloc_swot("FAIBLESSES", [
        "Indice de fréquentation creusois bas (1,34 vs 2,73 national)",
        "Pouvoir d'achat -12 % vs moyenne nationale",
        "Public peu nombreux (115 527 habitants)",
        "Faible appétence pour le numérique chez les +60 ans",
        "Trajets parfois longs en zone rurale"
    ])
    
    bloc_swot("MENACES", [
        "Concurrence du streaming (Netflix, Prime, Disney+)",
        "Vieillissement et baisse démographique continue",
        "Hausse des coûts d'exploitation (énergie, salaires)",
        "Départ des jeunes hors département (études)",
        "Concurrence des grandes salles (Limoges, Montluçon)"
    ])

st.markdown("---")

# ===============================
# RECOMMANDATIONS
# ===============================
st.header("7. Recommandations pour le projet data")

st.markdown("""
Cette étude oriente directement les choix techniques du projet. Les conclusions 
principales sont :

##### Pour la sélection des données
- Privilégier les films **post-1990**, avec attention sur **2010-2024**
- Conserver les **classiques français des années 1960-1980**
- Filtrer par seuil minimum de votes pour exclure les œuvres confidentielles

##### Pour les features du modèle ML
- Le **genre** doit être la feature principale (Comédie, Drame, Animation)
- L'**année de sortie** intégrée pour équilibrer récence et patrimoine  
- La **durée** comme feature secondaire (préférence pour formats < 2h)
- Le **réalisateur** comme feature catégorielle pour cohérence stylistique
- Le **score IMDb** pour filtrer la qualité (seuil 6,0)

##### Pour l'interface Streamlit
- Interface simple, lisible, **typographie large** pour public sénior
- Affichage des **affiches de films** (récupérées via OMDb) pour intuitivité
- Possibilité de **filtrer par genre** dès l'accueil
- Limitation à 5 recommandations par défaut
""")

st.markdown("---")

# ===============================
# SOURCES
# ===============================
with st.expander("Voir toutes les sources de cette étude"):
    st.markdown("""
    **Sources institutionnelles**
    - INSEE — Dossier complet du département de la Creuse (23)
    - INSEE — Recensement de la population, données 2023 publiées en décembre 2025
    - CNC — Géographie du cinéma 2024
    - CNC — Pratiques cinématographiques des Français en 2025
    - CNC — Le public du cinéma en 2022
    - Sénat — Rapport sur l'évolution du secteur de l'exploitation cinématographique
    
    **Sources presse et professionnelles**
    - France Bleu Creuse — Articles sur la fréquentation 2024 et le recensement 2025
    - Boxoffice Pro — Géographie du cinéma 2024 et pratiques 2025
    - Wikipedia — Démographie de la Creuse, Creuse (département)
    
    **Sources données salles**
    - Allociné, fan-de-cinema.com, Tourisme Creuse Limousin
    
    **Données comportementales**
    - BVA — Enquête sur les Français et le cinéma (préférences seniors)
    - Médiamétrie — Étude « Cinémas en mouvement » (2025)
    """)

st.caption("Document rédigé en avril 2026 — Phase 1 du projet de système de recommandation cinématographique")

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("assets/wildflix_logo.png", use_container_width=True)
    st.markdown("---")
    st.caption("Un projet réalisé par Harry, Thibaud, Owen et Vasanth")