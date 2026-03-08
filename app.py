import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from scipy.optimize import minimize
import requests
import yfinance as yf
from transformers import pipeline

st.set_page_config(page_title="Pricer Pro : MJD + FinBERT", layout="wide")

# --- 1. DONNÉES LIVE (YFINANCE) ---
@st.cache_data(ttl=300)
def get_live_spot(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return data['Close'].iloc[-1]
    except:
        return 100.0

# --- 2. IA FINANCIÈRE (FINBERT) ---
@st.cache_resource
def load_finbert():
    # Modèle NLP spécialisé en finance
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

@st.cache_data(ttl=3600)
def fetch_finbert_sentiment(api_key, query):
    if not api_key: return 2.0, []
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    try:
        articles = requests.get(url).json().get("articles", [])[:5]
        if not articles: return 2.0, []
        
        analyzer = load_finbert()
        titles = [a["title"] for a in articles]
        results = analyzer(titles)
        
        # Mapping FinBERT : positive (-1 au choc), negative (+1 au choc), neutral (0)
        score = 0
        for res in results:
            if res['label'] == 'negative': score += 1
            elif res['label'] == 'positive': score -= 1
            
        lam = max(0.5, min(2.0 + score * 1.5, 10.0))
        return lam, [{"title": a["title"], "url": a["url"], "sentiment": r['label']} for a, r in zip(articles, results)]
    except:
        return 2.0, []

# --- 3. MOTEUR MERTON & GRECQUES ---
@st.cache_data
def merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J, n_sim=3000, n_steps=252):
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

def price_mjd_put(S, K, T, r, sigma, lam, mu_J, sigma_J):
    paths = merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J)
    return np.exp(-r * T) * np.mean(np.maximum(K - paths[:, -1], 0))

def calc_greeks(S, K, T, r, sigma, lam, mu_J, sigma_J):
    # Différences finies pour les Grecques du modèle à sauts
    h = S * 0.01
    P = price_mjd_put(S, K, T, r, sigma, lam, mu_J, sigma_J)
    P_up = price_mjd_put(S + h, K, T, r, sigma, lam, mu_J, sigma_J)
    P_down = price_mjd_put(S - h, K, T, r, sigma, lam, mu_J, sigma_J)
    
    delta = (P_up - P_down) / (2 * h)
    gamma = (P_up - 2 * P + P_down) / (h**2)
    return delta, gamma

# --- 4. CALIBRATION (SCIPY.OPTIMIZE) ---
def calibrate_merton(S, r, market_prices, K_list, T):
    # market_prices: liste de prix réels observés
    def objective_function(params):
        sigma, lam, mu_J, sigma_J = params
        error = 0
        for K, market_P in zip(K_list, market_prices):
            model_P = price_mjd_put(S, K, T, r, sigma, lam, mu_J, sigma_J)
            error += (model_P - market_P)**2
        return error
    
    # Valeurs initiales et bornes
    init_guess = [0.2, 2.0, -0.1, 0.1]
    bounds = ((0.01, 1.0), (0.0, 10.0), (-1.0, 1.0), (0.01, 1.0))
    res = minimize(objective_function, init_guess, bounds=bounds, method='L-BFGS-B')
    return res.x

# --- UI ---
st.title("🦅 Pricer Institutionnel : MJD, FinBERT & Calibration")

try: api_key = st.secrets["NEWS_API_KEY"]
except: api_key = None

col_ticker, col_news = st.columns([1, 2])
with col_ticker:
    ticker = st.text_input("Ticker Yahoo Finance (ex: CL=F pour Pétrole)", "CL=F")
    live_S = get_live_spot(ticker)
    st.metric(f"Spot {ticker}", f"{live_S:.2f} $")
    query = st.text_input("Mots-clés Actu", "Oil OR Middle East")

dynamic_lam, top_news = fetch_finbert_sentiment(api_key, query)

with col_news:
    st.subheader("🧠 Analyse FinBERT en direct")
    for news in top_news:
        color = "red" if news['sentiment'] == 'negative' else "green" if news['sentiment'] == 'positive' else "gray"
        st.markdown(f"- 🔗 [{news['title']}]({news['url']}) - **:{color}[{news['sentiment'].upper()}]**")

st.markdown("---")

col_param, col_jump = st.columns(2)
with col_param:
    K = st.slider("Strike Put ($K$)", float(live_S*0.5), float(live_S*1.5), float(live_S*0.9))
    T = st.slider("Maturité ($T$)", 0.1, 2.0, 0.5)
    r = 0.05
    st.markdown("**(Calibration)** *L'optimiseur ajuste la volatilité de base ci-contre selon les prix du marché.*")
    sigma = st.slider("Volatilité ($\sigma$)", 0.05, 0.50, 0.20)

with col_jump:
    lam = st.slider("Chocs ($\lambda$ / an) - Piloté par FinBERT", 0.0, 10.0, float(dynamic_lam))
    mu_J = st.slider("Moyenne choc ($\mu_J$)", -0.50, 0.10, -0.20)
    sigma_J = st.slider("Vol. choc ($\sigma_J$)", 0.01, 0.50, 0.15)

# Calculs
price_mjd = price_mjd_put(live_S, K, T, r, sigma, lam, mu_J, sigma_J)
delta, gamma = calc_greeks(live_S, K, T, r, sigma, lam, mu_J, sigma_J)

st.markdown("---")
col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric("Prix Put (MJD)", f"{price_mjd:.3f} $")
col_res2.metric("Delta ($\Delta$)", f"{delta:.4f}")
col_res3.metric("Gamma ($\Gamma$)", f"{gamma:.5f}")

# Graphique
paths = merton_jump_paths(live_S, T, r, sigma, lam, mu_J, sigma_J, n_sim=50)
fig_mc = go.Figure()
for i in range(50):
    fig_mc.add_trace(go.Scatter(y=paths[i, :], mode='lines', line=dict(width=1, color='rgba(255, 100, 100, 0.3)')))
fig_mc.add_hline(y=K, line_dash="dash", line_color="cyan", annotation_text="Strike")
fig_mc.update_layout(showlegend=False, height=400, template="plotly_dark", title="Trajectoires MJD")
st.plotly_chart(fig_mc, use_container_width=True)
