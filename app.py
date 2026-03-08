import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import requests
from textblob import TextBlob

st.set_page_config(page_title="Pricer de Crise (MJD + NLP)", layout="wide")

# --- ANALYSE DE SENTIMENT & API ---
@st.cache_data(ttl=3600)
def fetch_sentiment_lambda(api_key, query="Middle East OR Iran OR war"):
    if not api_key: return 2.0 
    
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:20]
        
        if not articles: return 2.0
        
        polarities = [TextBlob(a["title"]).sentiment.polarity for a in articles]
        avg_sentiment = np.mean(polarities)
        
        lam = 2.0 - (avg_sentiment * 5)
        return max(0.5, min(lam, 10.0))
    except:
        return 2.0

# --- MOTEUR DE CALCUL : MERTON (MONTE CARLO) ---
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

# --- INTERFACE UTILISATEUR ---
st.title("Pricing de Crise : Merton + NLP Dynamique")

with st.sidebar:
    st.header("Connexion Live")
    # Ta clé est injectée ici par défaut
    api_key = st.secrets["NEWS_API_KEY"]
    query = st.text_input("Mots-clés (ex: Iran OR war)", "Iran OR war")

col_param, col_jump = st.columns(2)

with col_param:
    st.subheader("Paramètres Marché")
    S = st.slider("Sous-jacent ($S$)", 50, 150, 100)
    K = st.slider("Strike Put ($K$)", 50, 150, 80)
    T = st.slider("Maturité ($T$)", 0.1, 2.0, 0.5)
    sigma = st.slider("Volatilité de base ($\sigma$)", 0.05, 0.50, 0.15)
    r = 0.05

with col_jump:
    st.subheader("Paramètres Chocs (Merton)")
    dynamic_lam = fetch_sentiment_lambda(api_key, query)
    st.info(f"Fréquence des chocs ($\lambda$) calculée par l'IA : **{dynamic_lam:.2f} / an**")
    lam = st.slider("Ajustement manuel ($\lambda$)", 0.0, 10.0, float(dynamic_lam))
    mu_J = st.slider("Moyenne du choc ($\mu_J$)", -0.50, 0.10, -0.20)
    sigma_J = st.slider("Volatilité du choc ($\sigma_J$)", 0.01, 0.50, 0.15)

# --- SIMULATION ---
paths = merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J)
price_mjd = np.exp(-r * T) * np.mean(np.maximum(K - paths[:, -1], 0))
price_bs = bs_put(S, K, T, r, sigma)

# --- AFFICHAGE ---
col1, col2 = st.columns(2)
col1.metric("Prix Put (Paix - Black-Scholes)", f"{price_bs:.3f} €")
col2.metric("Prix Put (Crise - MJD)", f"{price_mjd:.3f} €", f"{(price_mjd-price_bs):.3f} € Prime de risque", delta_color="inverse")

fig = go.Figure()
for i in range(50):
    fig.add_trace(go.Scatter(y=paths[i, :], mode='lines', line=dict(width=1, color='rgba(255, 50, 50, 0.3)')))
fig.add_hline(y=K, line_dash="dash", line_color="white", annotation_text="Strike (K)")
fig.update_layout(showlegend=False, xaxis_title="Jours", yaxis_title="Prix du Sous-jacent", height=400)
st.plotly_chart(fig, use_container_width=True)
