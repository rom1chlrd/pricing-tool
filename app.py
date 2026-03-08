import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm
from scipy.optimize import minimize
import requests
import yfinance as yf
from transformers import pipeline

st.set_page_config(page_title="Pricer Pro", layout="wide")

# --- 1. DONNÉES & IA ---
@st.cache_data(ttl=300)
def get_live_spot(ticker):
    try: return float(yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1])
    except: return 100.0

def bs_put_simple(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

@st.cache_data(ttl=300)
def get_options_chain(ticker, S_ref, date=None):
    try:
        tkr = yf.Ticker(ticker)
        exps = tkr.options
        if not exps: raise ValueError("Pas d'options")
        return exps, tkr.option_chain(date or exps[0]).puts
    except Exception:
        st.toast("Yahoo API bloquée. Données simulées pour la démo.")
        strikes = np.round(np.linspace(S_ref * 0.8, S_ref * 1.2, 15), 2)
        vols = 0.20 + 0.15 * (strikes / S_ref - 1)**2
        prices = [bs_put_simple(S_ref, k, 0.5, 0.05, v) for k, v in zip(strikes, vols)]
        
        df = pd.DataFrame({
            'strike': strikes,
            'lastPrice': np.round(prices, 2),
            'bid': np.round(np.array(prices) - 0.1, 2),
            'ask': np.round(np.array(prices) + 0.1, 2),
            'impliedVolatility': np.round(vols, 4),
            'volume': np.random.randint(10, 500, size=len(strikes))
        })
        return ["Données Simulées (Rate Limit)"], df

@st.cache_resource
def load_finbert():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

@st.cache_data(ttl=3600)
def fetch_finbert_sentiment(api_key, query):
    if not api_key: return 2.0, []
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    try:
        articles = requests.get(url).json().get("articles", [])[:5]
        if not articles: return 2.0, []
        results = load_finbert()([a["title"] for a in articles])
        score = sum([-1 if r['label']=='positive' else 1 if r['label']=='negative' else 0 for r in results])
        return max(0.5, min(2.0 + score * 1.5, 10.0)), [{"title": a["title"], "url": a["url"], "sentiment": r['label']} for a, r in zip(articles, results)]
    except: return 2.0, []

# --- 2. MOTEUR MERTON ---
@st.cache_data
def merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J, n_sim=3000, n_steps=252):
    dt = T / n_steps
    paths = np.zeros((n_sim, n_steps + 1))
    paths[:, 0] = S
    drift = r - 0.5 * sigma**2 - lam * (np.exp(mu_J + 0.5 * sigma_J**2) - 1)
    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(n_sim)
        N = np.random.poisson(lam * dt, n_sim)
        J = np.where(N > 0, np.random.normal(mu_J * N, sigma_J * np.sqrt(N)), 0)
        paths[:, t] = paths[:, t-1] * np.exp(drift * dt + sigma * np.sqrt(dt) * Z + J)
    return paths

def price_mjd_put(S, K, T, r, sigma, lam, mu_J, sigma_J):
    paths = merton_jump_paths(S, T, r, sigma, lam, mu_J, sigma_J)
    return np.exp(-r * T) * np.mean(np.maximum(K - paths[:, -1], 0))

# --- UI & CALIBRATION ---
st.title("Pricer Institutionnel : MJD & Calibration Auto")

try: api_key = st.secrets["NEWS_API_KEY"]
except: api_key = None

col1, col2 = st.columns([1, 2])
with col1:
    ticker = st.text_input("Ticker", "CL=F")
    live_S = get_live_spot(ticker)
    st.metric(f"Spot {ticker}", f"{live_S:.2f} $")
    query = st.text_input("Mots-clés Actu", "Oil OR Middle East")

dynamic_lam, top_news = fetch_finbert_sentiment(api_key, query)

with col2:
    st.subheader("Analyse FinBERT")
    for news in top_news:
        color = "red" if news['sentiment'] == 'negative' else "green" if news['sentiment'] == 'positive' else "gray"
        st.markdown(f"- 🔗 [{news['title']}]({news['url']}) - **:{color}[{news['sentiment'].upper()}]**")

st.markdown("---")
st.subheader("Chaîne d'Options Réelle & Calibration")

if 'calibrated' not in st.session_state:
    st.session_state.calibrated = False

exps, puts = get_options_chain(ticker, live_S)

if exps:
    selected_exp = st.selectbox("Maturité", exps)
    _, puts = get_options_chain(ticker, live_S, selected_exp)
    
    if st.button("Calibrer sur le marché live"):
        with st.spinner("Calibration en cours..."):
            atm_puts = puts[(puts['strike'] >= live_S * 0.8) & (puts['strike'] <= live_S * 1.2) & (puts['volume'] > 0)]
            if not atm_puts.empty:
                K_list = atm_puts['strike'].values
                market_P = atm_puts['lastPrice'].values
                T_calib = 0.5 
                
                def loss(p):
                    sig, l, mj, sj = p
                    return sum((price_mjd_put(live_S, k, T_calib, 0.05, sig, l, mj, sj) - mp)**2 for k, mp in zip(K_list, market_P))
                
                res = minimize(loss, [0.2, dynamic_lam, -0.2, 0.15], bounds=((0.01, 1), (0, 10), (-1, 1), (0.01, 1)))
                st.session_state.opt_params = res.x
                st.session_state.calibrated = True
                st.success("Calibration réussie !")
            else:
                st.error("Pas assez d'options liquides proches de la monnaie.")

    st.dataframe(puts[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'volume']].head(5), use_container_width=True)

# Application des paramètres
st.markdown("---")
col_p, col_j = st.columns(2)

opt = st.session_state.opt_params if st.session_state.calibrated else [0.20, dynamic_lam, -0.20, 0.15]

with col_p:
    K = st.slider("Strike Put ($K$)", float(live_S*0.5), float(live_S*1.5), float(live_S*0.9))
    T = st.slider("Maturité ($T$)", 0.1, 2.0, 0.5)
    sigma = st.slider("Volatilité ($\sigma$)", 0.01, 1.00, float(opt[0]))

with col_j:
    lam = st.slider("Chocs ($\lambda$ / an)", 0.0, 10.0, float(opt[1]))
    mu_J = st.slider("Moyenne choc ($\mu_J$)", -1.0, 1.0, float(opt[2]))
    sigma_J = st.slider("Vol. choc ($\sigma_J$)", 0.01, 1.0, float(opt[3]))

price_mjd = price_mjd_put(live_S, K, T, 0.05, sigma, lam, mu_J, sigma_J)

st.metric("Prix Put (MJD Calculé)", f"{price_mjd:.3f} $")

paths = merton_jump_paths(live_S, T, 0.05, sigma, lam, mu_J, sigma_J, n_sim=50)
fig_mc = go.Figure()
for i in range(50): fig_mc.add_trace(go.Scatter(y=paths[i, :], mode='lines', line=dict(width=1, color='rgba(255, 100, 100, 0.3)')))
fig_mc.add_hline(y=K, line_dash="dash", line_color="cyan")
fig_mc.update_layout(showlegend=False, height=400, template="plotly_dark", title="Trajectoires MJD")
st.plotly_chart(fig_mc, use_container_width=True)
