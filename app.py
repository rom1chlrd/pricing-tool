import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Impact Choc Géopolitique", layout="wide")

# --- MOTEUR MATHÉMATIQUE ---
@st.cache_data
def simulate_paths(S, T, r, sigma, lam, mu_J, sigma_J, n_sim=50, n_steps=100):
    dt = T / n_steps
    paths_bs = np.zeros((n_sim, n_steps + 1))
    paths_mjd = np.zeros((n_sim, n_steps + 1))
    paths_bs[:, 0] = S
    paths_mjd[:, 0] = S
    
    k = np.exp(mu_J + 0.5 * sigma_J**2) - 1 
    drift_mjd = r - 0.5 * sigma**2 - lam * k
    drift_bs = r - 0.5 * sigma**2
    
    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(n_sim)
        N = np.random.poisson(lam * dt, n_sim)
        J = np.where(N > 0, np.random.normal(mu_J * N, sigma_J * np.sqrt(N)), 0)
        
        paths_bs[:, t] = paths_bs[:, t-1] * np.exp(drift_bs * dt + sigma * np.sqrt(dt) * Z)
        paths_mjd[:, t] = paths_mjd[:, t-1] * np.exp(drift_mjd * dt + sigma * np.sqrt(dt) * Z + J)
    return paths_bs, paths_mjd

def price_bs_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def price_mjd_put_fast(S, K, T, r, sigma, lam, mu_J, sigma_J, n_sim=2000):
    paths_bs, paths_mjd = simulate_paths(S, T, r, sigma, lam, mu_J, sigma_J, n_sim, 1)
    return np.exp(-r * T) * np.mean(np.maximum(K - paths_mjd[:, -1], 0))

# --- INTERFACE ---
st.title("💥 Impact Visuel d'un Choc Géopolitique (ex: Iran)")
st.markdown("Comparaison immédiate : **Temps de Paix** vs **Temps de Guerre**.")

col_param, col_choc = st.columns(2)

with col_param:
    st.subheader("1. Marché Normal (Paix)")
    S = st.slider("Prix du Sous-jacent", 50, 150, 100)
    K = st.slider("Strike (Couverture)", 50, 150, 80)
    T = st.slider("Maturité (Années)", 0.1, 2.0, 0.5)
    sigma = st.slider("Volatilité Normale", 0.05, 0.50, 0.15)

with col_choc:
    st.subheader("2. Paramètres du Choc (Guerre)")
    lam = st.slider("Fréquence du krach (Nb/an)", 0.0, 10.0, 3.0)
    mu_J = st.slider("Sévérité du krach (%)", -0.80, 0.0, -0.30)
    sigma_J = st.slider("Incertitude du krach", 0.05, 0.50, 0.20)

# --- GRAPHIQUE 1 : TRAJECTOIRES ---
st.markdown("---")
st.subheader("Visualisation des Krachs (Simulation des prix du sous-jacent)")

paths_bs, paths_mjd = simulate_paths(S, T, 0.05, sigma, lam, mu_J, sigma_J)

fig_paths = go.Figure()
for i in range(25):
    fig_paths.add_trace(go.Scatter(y=paths_bs[i, :], mode='lines', line=dict(color='rgba(100, 150, 255, 0.4)'), name="Paix" if i==0 else ""))
    fig_paths.add_trace(go.Scatter(y=paths_mjd[i, :], mode='lines', line=dict(color='rgba(255, 50, 50, 0.6)'), name="Guerre" if i==0 else ""))

fig_paths.add_hline(y=K, line_dash="dash", line_color="white", annotation_text="Strike")
fig_paths.update_layout(height=400, template="plotly_dark", showlegend=False)
st.plotly_chart(fig_paths, use_container_width=True)

# --- GRAPHIQUE 2 : SURFACE 3D DE LA SURPRIME ---
st.markdown("---")
st.subheader("Surprime de Risque (Combien coûte la peur ?)")
st.markdown("Ce graphique montre la **différence de prix** entre l'option en temps de guerre et l'option en temps de paix.")

with st.spinner("Calcul de la surface 3D..."):
    strikes = np.linspace(50, 150, 15)
    maturities = np.linspace(0.1, 1.0, 15)
    X, Y = np.meshgrid(strikes, maturities)
    Z = np.zeros_like(X)
    
    for i in range(len(maturities)):
        for j in range(len(strikes)):
            p_bs = price_bs_put(S, X[i,j], Y[i,j], 0.05, sigma)
            p_mjd = price_mjd_put_fast(S, X[i,j], Y[i,j], 0.05, sigma, lam, mu_J, sigma_J)
            Z[i,j] = max(0, p_mjd - p_bs) # Surprime

fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Reds")])
fig_3d.update_layout(
    scene=dict(
        xaxis_title='Strike (K)',
        yaxis_title='Maturité (T)',
        zaxis_title='Surprime (€)'
    ),
    height=600,
    template="plotly_dark"
)
st.plotly_chart(fig_3d, use_container_width=True)
