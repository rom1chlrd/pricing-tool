import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import requests
from textblob import TextBlob

st.set_page_config(page_title="Pricer de Crise NLP", layout="wide", initial_sidebar_state="expanded")

# --- ANALYSE DE SENTIMENT & API ---
@st.cache_data(ttl=3600)
def fetch_news_and_sentiment(api_key, query="Middle East OR Iran OR war"):
    if not api_key: return 2.0, []
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:10] # Garder les 10 plus récents
        if not articles: return 2.0, []
        
        polarities = [TextBlob(a["title"]).sentiment.polarity for a in articles]
        lam = 2.0 - (np.mean(polarities) * 5)
        return max(0.5, min(lam, 10.0)), [a["title"] for a in articles[:3]]
    except:
        return 2.0, []

# --- MOTEUR DE CALCUL : MERTON ---
@st.cache_data
def merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J, n_sim=2000, n_steps=252):
    dt = T / n_steps
    paths = np.zeros((n_sim, n_steps + 1))
    paths[:, 0] = S
    k = np.exp(mu_J + 0.5 * sigma_J**2) - 1 
    drift = r - 0.5 * sigma**2 - lam * k
    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(n_sim)
        N = np.random.poisson(lam * dt, n_sim)
        J = np.zeros(n_sim)
        for i in range(n_sim):
            if N[i] > 0:
                J[i] = np.sum(np.random.normal(mu_J, sigma_J, N[i]))
        paths[:, t] = paths[:, t-1] * np.exp(drift * dt + sigma * np.sqrt(dt) * Z + J)
    return paths

def bs_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# --- UI : EN-TÊTE & NEWS ---
st.title("Pricing de Dérivés sous Stress Géopolitique")
st.markdown("Ce pricer connecte l'algorithme de **Merton Jump Diffusion** à l'analyse de sentiment **NLP** des flux d'actualité en direct.")

try:
    api_key = st.secrets["NEWS_API_KEY"]
except KeyError:
    api_key = None
    st.error("Clé API manquante dans les secrets.")

dynamic_lam, top_news = fetch_news_and_sentiment(api_key)

col_gauge, col_news = st.columns([1, 2])

with col_gauge:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = dynamic_lam,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Indice de Peur (Sauts $\lambda$ / an)", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 2], 'color': "lightgreen"},
                {'range': [2, 5], 'color': "orange"},
                {'range': [5, 10], 'color': "salmon"}],
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_news:
    st.subheader("Titres dictant le marché à l'instant T")
    if top_news:
        for news in top_news:
            st.info(f"**{news}**")
    else:
        st.warning("Aucune actualité récupérée ou API non configurée.")

st.markdown("---")

# --- UI : PARAMÈTRES & GRAPHIQUES ---
col_param, col_jump = st.columns(2)

with col_param:
    st.subheader("Paramètres Options")
    S = st.slider("Sous-jacent ($S$)", 50, 150, 100)
    K = st.slider("Strike Put ($K$)", 50, 150, 80)
    T = st.slider("Maturité ($T$)", 0.1, 2.0, 0.5)
    sigma = st.slider("Volatilité ($\sigma$)", 0.05, 0.50, 0.15)
    r = 0.05

with col_jump:
    st.subheader("⚡ Paramètres de Krach")
    lam = st.slider("Ajustement manuel de l'Indice ($\lambda$)", 0.0, 10.0, float(dynamic_lam))
    mu_J = st.slider("Moyenne du choc ($\mu_J$)", -0.50, 0.10, -0.20)
    sigma_J = st.slider("Volatilité du choc ($\sigma_J$)", 0.01, 0.50, 0.15)

paths = merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J)
price_mjd = np.exp(-r * T) * np.mean(np.maximum(K - paths[:, -1], 0))
price_bs = bs_put(S, K, T, r, sigma)

st.markdown("---")

col_res1, col_res2 = st.columns(2)
col_res1.metric("Prix Put Théorique (BS - Temps de Paix)", f"{price_bs:.3f} €")
col_res2.metric("Prix Put de Couverture (MJD - Actualité Live)", f"{price_mjd:.3f} €", f"{(price_mjd-price_bs):.3f} € de Surprime liée à l'actualité", delta_color="inverse")

st.subheader("Simulation des Sauts du Marché (Monte Carlo)")
fig_mc = go.Figure()
for i in range(50):
    fig_mc.add_trace(go.Scatter(y=paths[i, :], mode='lines', line=dict(width=1, color='rgba(255, 75, 75, 0.4)')))
fig_mc.add_hline(y=K, line_dash="dash", line_color="cyan", annotation_text="Niveau d'Exercice (Strike K)", annotation_font_color="cyan")
fig_mc.update_layout(showlegend=False, height=400, template="plotly_dark", xaxis_title="Jours", yaxis_title="Prix du Sous-jacent")
st.plotly_chart(fig_mc, use_container_width=True)
