"""
Page 3 - Dashboard d'analyse exploratoire
Visualisations interactives du dataset
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# Configuration matplotlib globale
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
sns.set_style("whitegrid")

# ===============================
# STYLE CUSTOM POUR LES BLOCS
# ===============================
def bloc_info(contenu):
    st.markdown(
        f'<div style="background-color: #F5F5F5; border-left: 4px solid #888888; padding: 15px 20px; border-radius: 4px; margin: 10px 0;">{contenu}</div>',
        unsafe_allow_html=True
    )

# ===============================
# CHARGEMENT DES DONNÉES (en cache)
# ===============================
@st.cache_data
def charger_donnees():
    df_full = pd.read_csv('data/clean/imdb_5000_clean.csv')
    df_enriched = pd.read_csv('data/clean/imdb_4000_enriched.csv')
    return df_full, df_enriched

df_full, df_enriched = charger_donnees()

# ===============================
# EN-TÊTE
# ===============================
st.title("Dashboard — Analyse exploratoire")
st.markdown("### Visualisations clés du dataset cinéma")
st.markdown("---")

# ===============================
# KPI EN HAUT
# ===============================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total films", f"{len(df_full):,}")
col2.metric("Films cultes", f"{len(df_enriched):,}")
col3.metric("Note moyenne", f"{df_full['imdb_score'].mean():.2f}/10")
col4.metric("Année médiane", f"{int(df_full['title_year'].median())}")

st.markdown("---")

# ===============================
# SECTION 1 - DISTRIBUTION ANNÉES
# ===============================
st.header("1. Distribution des films par année de sortie")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.hist(df_full['title_year'], bins=50, color='#5B3E96', edgecolor='white')
ax1.set_xlabel('Année')
ax1.set_ylabel('Nombre de films')
ax1.set_title('Distribution des films par année', fontsize=13, fontweight='bold')
ax1.axvline(df_full['title_year'].median(), color='red', linestyle='--', 
            label=f"Médiane : {int(df_full['title_year'].median())}")
ax1.legend()
plt.tight_layout()
st.pyplot(fig1)

bloc_info(f"<strong>Lecture</strong> : le dataset s'étale de <strong>{int(df_full['title_year'].min())}</strong> à <strong>{int(df_full['title_year'].max())}</strong>, avec une concentration sur les années 2000-2015. Médiane : {int(df_full['title_year'].median())}.")

st.markdown("---")

# ===============================
# SECTION 2 - GENRES
# ===============================
st.header("2. Top des genres (toutes positions confondues)")

tous_genres = pd.concat([df_full['genre_1'], df_full['genre_2'], df_full['genre_3']])
genres_count = tous_genres.value_counts().head(15)

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.bar(genres_count.index, genres_count.values, color='#5B3E96', edgecolor='white')
ax2.set_xlabel('Genre')
ax2.set_ylabel('Nombre d\'occurrences')
ax2.set_title('Top 15 des genres les plus fréquents', fontsize=13, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig2)

col_g1, col_g2 = st.columns(2)
with col_g1:
    bloc_info(f"<strong>Top 3 des genres</strong><br>1. <strong>{genres_count.index[0]}</strong> — {genres_count.values[0]:,} films<br>2. <strong>{genres_count.index[1]}</strong> — {genres_count.values[1]:,} films<br>3. <strong>{genres_count.index[2]}</strong> — {genres_count.values[2]:,} films")
with col_g2:
    bloc_info("<strong>Insight</strong> : Drama domine largement, suivi de Comedy et Action. Ces 3 genres sont <strong>parfaitement alignés</strong> avec les préférences du public sénior creusois identifiées dans l'étude de marché.")

st.markdown("---")

# ===============================
# SECTION 3 - DISTRIBUTION DES NOTES
# ===============================
st.header("3. Distribution des notes IMDb")

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.hist(df_full['imdb_score'], bins=30, color='#5B3E96', edgecolor='white')
ax3.set_xlabel('Note IMDb (sur 10)')
ax3.set_ylabel('Nombre de films')
ax3.set_title('Distribution des notes IMDb', fontsize=13, fontweight='bold')
ax3.axvline(df_full['imdb_score'].mean(), color='red', linestyle='--', 
            label=f"Moyenne : {df_full['imdb_score'].mean():.2f}")
ax3.axvline(df_full['imdb_score'].median(), color='orange', linestyle='--', 
            label=f"Médiane : {df_full['imdb_score'].median():.2f}")
ax3.legend()
plt.tight_layout()
st.pyplot(fig3)

col_n1, col_n2, col_n3, col_n4 = st.columns(4)
col_n1.metric("Excellents (8+)", f"{(df_full['imdb_score'] >= 8).sum()}")
col_n2.metric("Bons (7-8)", f"{((df_full['imdb_score'] >= 7) & (df_full['imdb_score'] < 8)).sum()}")
col_n3.metric("Moyens (6-7)", f"{((df_full['imdb_score'] >= 6) & (df_full['imdb_score'] < 7)).sum()}")
col_n4.metric("Faibles (<6)", f"{(df_full['imdb_score'] < 6).sum()}")

st.markdown("---")

# ===============================
# SECTION 4 - PAYS
# ===============================
st.header("4. Top 15 des pays producteurs")

top_pays = df_full['country'].value_counts().head(15)

fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.barh(top_pays.index[::-1], top_pays.values[::-1], color='#5B3E96', edgecolor='white')
ax4.set_xlabel('Nombre de films')
ax4.set_ylabel('Pays')
ax4.set_title('Top 15 des pays producteurs', fontsize=13, fontweight='bold')
plt.tight_layout()
st.pyplot(fig4)

pct_usa = (df_full['country'] == 'USA').sum() / df_full['country'].notna().sum() * 100
pct_fr = (df_full['country'] == 'France').sum() / df_full['country'].notna().sum() * 100
pct_uk = (df_full['country'] == 'UK').sum() / df_full['country'].notna().sum() * 100

col_p1, col_p2, col_p3 = st.columns(3)
col_p1.metric("États-Unis", f"{pct_usa:.1f}%")
col_p2.metric("Royaume-Uni", f"{pct_uk:.1f}%")
col_p3.metric("France", f"{pct_fr:.1f}%")

bloc_info(f"<strong>Limite identifiée</strong> : {pct_usa:.0f} % des films sont américains. C'est un <strong>biais important</strong> à mentionner devant le jury : nos recommandations seront fortement orientées vers le cinéma US, ce qui ne correspond pas parfaitement aux préférences du public creusois (43,5 % des entrées seniors sur films français).")

st.markdown("---")

# ===============================
# SECTION 5 - CORRÉLATIONS
# ===============================
st.header("5. Corrélations entre variables numériques")

colonnes_num = ['title_year', 'duration', 'budget', 'gross', 'imdb_score', 
                'num_voted_users', 'num_critic_for_reviews', 'movie_facebook_likes']
corr_matrix = df_full[colonnes_num].corr()

fig5, ax5 = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, ax=ax5, cbar_kws={'label': 'Coefficient'})
ax5.set_title('Heatmap des corrélations', fontsize=13, fontweight='bold')
plt.tight_layout()
st.pyplot(fig5)

bloc_info("<strong>Insights clés issus de la heatmap :</strong><br>• <strong>gross ↔ num_voted_users (0,64)</strong> : les films à gros box-office attirent plus de votes<br>• <strong>imdb_score ↔ num_voted_users (0,43)</strong> : les bons films attirent plus d'avis<br>• <strong>title_year ↔ imdb_score (-0,21)</strong> : les films plus récents ont des notes légèrement plus basses (effet nostalgie)<br>• <strong>budget ↔ imdb_score (0,03)</strong> : <strong>AUCUNE corrélation</strong> entre budget et qualité — un gros budget ne fait pas un bon film !")

st.markdown("---")

# ===============================
# SECTION 6 - TOP RÉALISATEURS
# ===============================
st.header("6. Top 10 des réalisateurs et acteurs")

col_real, col_act = st.columns(2)

with col_real:
    st.subheader("Réalisateurs")
    top_real = df_full['director_name'].value_counts().head(10)
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    ax6.barh(top_real.index[::-1], top_real.values[::-1], color='#5B3E96', edgecolor='white')
    ax6.set_xlabel('Nombre de films')
    plt.tight_layout()
    st.pyplot(fig6)

with col_act:
    st.subheader("Acteurs principaux")
    top_act = df_full['actor_1_name'].value_counts().head(10)
    fig7, ax7 = plt.subplots(figsize=(8, 5))
    ax7.barh(top_act.index[::-1], top_act.values[::-1], color='#888888', edgecolor='white')
    ax7.set_xlabel('Nombre de films')
    plt.tight_layout()
    st.pyplot(fig7)

st.markdown("---")

# ===============================
# SECTION 7 - COMPARAISON DATASETS
# ===============================
st.header("7. Comparaison : tous les films vs Top 4000 enrichis")

fig8, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_full['imdb_score'], bins=30, color='#5B3E96', alpha=0.6, label=f'Tous ({len(df_full)})')
axes[0].hist(df_enriched['imdb_score'], bins=30, color='#888888', alpha=0.8, label=f'Top {len(df_enriched)}')
axes[0].set_title('Notes IMDb', fontweight='bold')
axes[0].set_xlabel('Note IMDb')
axes[0].set_ylabel('Nombre de films')
axes[0].legend()

axes[1].hist(df_full['title_year'], bins=40, color='#5B3E96', alpha=0.6, label=f'Tous ({len(df_full)})')
axes[1].hist(df_enriched['title_year'], bins=40, color='#888888', alpha=0.8, label=f'Top {len(df_enriched)}')
axes[1].set_title('Années', fontweight='bold')
axes[1].set_xlabel('Année')
axes[1].set_ylabel('Nombre de films')
axes[1].legend()

plt.tight_layout()
st.pyplot(fig8)

col_c1, col_c2, col_c3 = st.columns(3)
col_c1.metric("Note moyenne", f"{df_enriched['imdb_score'].mean():.2f}", 
              f"+{df_enriched['imdb_score'].mean() - df_full['imdb_score'].mean():.2f}")
col_c2.metric("Année médiane", f"{int(df_enriched['title_year'].median())}")
col_c3.metric("Durée moyenne", f"{df_enriched['duration'].mean():.0f} min",
              f"+{df_enriched['duration'].mean() - df_full['duration'].mean():.0f} min")

bloc_info(f"<strong>Validation</strong> : le top {len(df_enriched)} enrichi affiche une note moyenne <strong>supérieure</strong> au dataset complet (+{df_enriched['imdb_score'].mean() - df_full['imdb_score'].mean():.2f} point), confirmant la qualité de notre sélection pour le système de recommandation.")

st.markdown("---")
st.caption("Dashboard généré dynamiquement à partir des données nettoyées — Mis à jour automatiquement")

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("assets/wildflix_logo.png", use_container_width=True)
    st.markdown("---")
    st.caption("Un projet réalisé par Harry, Thibaud, Owen et Vasanth")