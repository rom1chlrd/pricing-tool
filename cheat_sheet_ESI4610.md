# ESI 4610 — Cheat Sheet Exam 3

---

## CONCEPTS CLÉS (Vrai/Faux fréquents)

| Affirmation | Vrai/Faux | Note |
|---|---|---|
| Seaborn est séparé de Matplotlib | **FAUX** | Seaborn est construit *sur* Matplotlib |
| Scatter plot → relation entre 2 variables numériques | **VRAI** | |
| Régression → variable cible continue | **VRAI** | |
| Train/test split → estimer la généralisation | **VRAI** | |
| Regression trees → bons pour relations linéaires | **FAUX** | Ils capturent des relations NON-linéaires |
| Precision = vrais positifs parmi tous les prédit positifs | **VRAI** | |
| Recall = vrais positifs parmi tous les réels positifs | **VRAI** | |
| K de KNN = K de K-means | **FAUX** | KNN = nb voisins, K-means = nb clusters |
| KNN utilisable en classification ET régression | **VRAI** | |
| Logistic Regression ne peut pas classifier | **FAUX** | Elle retourne une proba convertie en classe |
| PCA maximise la séparation entre classes | **FAUX** | PCA maximise la **variance**, pas la séparation |
| PCA est supervisé | **FAUX** | PCA est **non-supervisé** |
| LDA est non-supervisé | **FAUX** | LDA est **supervisé** (utilise les étiquettes) |
| Hierarchical clustering agglomératif = bottom-up | **VRAI** | Part de chaque point seul, fusionne |

---

## TYPES DE MACHINE LEARNING

| Type | Définition | Exemples |
|---|---|---|
| **Supervisé** | Apprend à prédire $y$ à partir de $(x, y)$ labelisés | Régression, Classification |
| **Non-supervisé** | Trouve des patterns dans $x$ sans labels | Clustering, PCA |
| **Renforcement** | Apprend par interactions avec l'environnement (reward) | Jeux, robots |

## TYPE DE PROBLÈME

| Scénario | Type | Variable cible |
|---|---|---|
| Prédire un **nombre** (temps, prix, score) | **Régression** | continue |
| Prédire une **catégorie** binaire (spam/pas spam) | **Classification binaire** | 0/1 |
| Prédire parmi **3+ catégories** (mold/pollen/dust) | **Classification multinomiale** | catégorielle |
| **Grouper** sans étiquettes | **Clustering (non-supervisé)** | aucune |
| Réduire le nb de variables | **Réduction de dimension** | aucune |

**Pour un problème supervisé:** identifier $n$ (nb d'observations) et $p$ (nb de variables indépendantes, sans la cible).

## TYPES DE VARIABLES

| Type | Sous-type | Exemple |
|---|---|---|
| **Quantitative continue** | — | Température, prix, poids |
| **Quantitative discrète** | — | Nb de tickets, nb de clients |
| **Qualitative nominale** | Catégories sans ordre | ZIP code, genre, couleur |
| **Qualitative ordinale** | Catégories **avec ordre** | Rating: poor/fair/good/excellent |

---

## VISUALISATION — MATPLOTLIB

### Bases
```python
import matplotlib.pyplot as plt

plt.plot(x, y, color='blue', label='label', marker='o', linestyle='--')  # ligne
plt.scatter(x, y, alpha=0.7, c=colors, s=sizes, cmap='coolwarm')         # scatter
plt.bar(grade, freq)          # barres verticales
plt.barh(grade, freq)         # barres horizontales
plt.hist(data, bins=20)       # histogramme
plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=(0.1,0,0,0),
        shadow=True, startangle=140)    # pie chart
plt.axis('equal')             # cercle parfait pour pie

plt.title('Titre')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.xticks(rotation=45)
plt.yticks([])                # masquer les ticks Y
plt.grid(True)
plt.colorbar()                # échelle de couleurs (avec c=...)
plt.figure(figsize=(10, 5))   # taille du graphique
plt.savefig("nom.png")
plt.show()
```

### Styles
```python
plt.style.use('ggplot')        # thème ggplot
plt.style.use('dark_background')
plt.style.use('default')       # reset
print(plt.style.available)     # lister les styles dispo
```

### Line styles & markers courants
| Linestyle | Code | Marker | Code |
|---|---|---|---|
| solide | `'-'` | cercle | `'o'` |
| tirets | `'--'` | carré | `'s'` |
| pointillés | `':'` | triangle | `'^'` |
| tiret-point | `'-.'` | croix | `'x'` |

### Subplots
```python
fig, axes = plt.subplots(nrows, ncols, figsize=(w, h))

# Exemples :
fig, axes = plt.subplots(1, 2, figsize=(12, 4))          # 1 ligne 2 cols
fig, axes = plt.subplots(2, 3)                            # 2 lignes 3 cols
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))    # déstructuré

# Accès aux axes :
axes[0].plot(...)            # si 1D
axes[0, 1].plot(...)         # si 2D
axes.flat                    # itérer sur tous : zip(axes.flat, items)

# Propriétés axes :
ax.set_title('...')
ax.set_xlabel('...')
ax.set_ylabel('...')

# sharex partagé :
fig, axes = plt.subplots(2, 1, sharex=True)

plt.tight_layout()           # évite chevauchement
plt.subplots_adjust(wspace=0.1, hspace=0.2)  # espace manuel entre subplots
```

### Bar chart Pandas
```python
df.plot.bar(color=['red','blue','green'])           # barres normales
df.plot.bar(stacked=True)                           # barres empilées
df.plot.barh()                                      # barres horizontales
series.plot(kind='bar', ax=axes[0])                 # dans un subplot
```

### Ligne plot avec markers
```python
plt.plot(x, y, marker='o')
```

### Dates
```python
df['col'] = pd.to_datetime(df['col'])   # convertir en datetime
plt.xticks(rotation=45)
```

---

## VISUALISATION — SEABORN

```python
import seaborn as sns
```

### Scatter plot
```python
sns.scatterplot(
    data=df,
    x='col_x', y='col_y',
    hue='categorie',       # couleur par catégorie
    style='col_style',     # forme du marker
    size='col_size',       # taille du marker
    edgecolor='black',
    ax=axes[0]             # subplot cible
)
```

### Histogramme
```python
sns.histplot(data=df, x='col', bins=15, kde=True, hue='cat', stat="density")
# stat="density" → affiche la densité (pas les counts)
```

### Boxplot
```python
sns.boxplot(data=df, x='cat', y='valeur', hue='cat2')
```

### Pairplot
```python
sns.pairplot(data=df[['A','B','C','cat']], hue='cat', height=3)
```

### Heatmap de corrélation
```python
corr = df.select_dtypes(include='number').corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
```

### Density plot (KDE)
```python
df['col'].plot(kind='kde', color='red', alpha=0.5)   # via Pandas
sns.histplot(df['col'], kde=True, stat='density')     # via Seaborn (combiné)
```

### Faceted plots
```python
# relplot : scatter/line facetté
sns.relplot(data=df, x='X', y='Y', hue='species', col='sex')

# catplot : box/bar/etc. facetté
sns.catplot(x='day', y='total_bill', hue='smoker', col='time',
            kind='bar', data=df, height=4, aspect=1)
sns.catplot(x='day', y='total_bill', hue='time', col='smoker',
            kind='box', data=df, height=4, aspect=.7)

# FacetGrid (manuel)
g = sns.FacetGrid(df, col='time', hue='smoker')
g.map(sns.scatterplot, 'x_col', 'y_col')
g.add_legend()
```

### Color palettes Seaborn
| Type | Exemples | Usage |
|---|---|---|
| Qualitative | `'Set1'`, `'Set2'`, `'tab10'`, `'husl'` | Données catégorielles |
| Séquentielle | `'Blues'`, `'viridis'`, `'plasma'` | Données continues |
| Divergente | `'coolwarm'`, `'RdBu'` | Données avec centre neutre |

### Grouped bar chart Pandas
```python
avg = df.groupby(['cat1', 'cat2'])['val'].mean().unstack()
avg.plot(kind='bar', ax=ax)
```

---

## NETTOYAGE DE DONNÉES

### Valeurs manquantes
```python
df.isnull().sum()                       # nb de NaN par colonne
df.isnull().mean()                      # % de NaN par colonne
df.isnull().any()                       # bool par colonne

# Supprimer colonnes > 70% NaN :
df = df.loc[:, df.isnull().mean() <= 0.7]

# Colonnes avec NaN :
mask = df.isnull().any()
missing_cols = df.columns[mask]

# Visualisation :
import missingno as msno
msno.matrix(df)
plt.show()
```

### Imputation simple (fillna)
```python
# Numérique : moyenne ou médiane
df['col'] = df['col'].fillna(df['col'].mean())
df['col'] = df['col'].fillna(df['col'].median())

# Catégorielle : mode
df['col'] = df['col'].fillna(df['col'].mode()[0])

# Auto (général) :
num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(exclude='number').columns

for col in missing_cols:
    if col in num_cols:
        df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])
```

### SimpleImputer (sklearn)
```python
from sklearn.impute import SimpleImputer

median_imputer = SimpleImputer(strategy='median')
mode_imputer   = SimpleImputer(strategy='most_frequent')

df[['age']] = median_imputer.fit_transform(df[['age']]).round().astype(int)
df[cat_cols] = mode_imputer.fit_transform(df[cat_cols])
```

### KNNImputer (sklearn)
```python
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=5)
df_imputed = pd.DataFrame(
    knn_imputer.fit_transform(df_combined),
    columns=df_combined.columns
)
```

### OneHotEncoder (pour KNN imputation)
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df[['col']])
encoder.get_feature_names_out(['col'])    # noms des colonnes encodées
encoder.inverse_transform(encoded)        # decoder
```

---

## MACHINE LEARNING — PIPELINE GÉNÉRAL

```python
from sklearn.model_selection import train_test_split

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=4610
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

---

## FORMULES DES MODÈLES

### Régression linéaire
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p + \epsilon$$
- $\beta_0$ = intercept, $\beta_1 \dots \beta_p$ = slopes, $\epsilon$ = bruit (erreur)

### Régression polynomiale
$$y = \beta_0 + \beta_1 x + \beta_2 x^2 + \cdots + \beta_n x^n$$

### Logistic Regression (sigmoid)
$$P(y=1 \mid x_1, \dots, x_n) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n)}}$$
→ Si $P \geq 0.5$ → classe 1, sinon classe 0

---

## RÉGRESSION LINÉAIRE

### Formule OLS (matrix form)
$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

```python
# OLS manuel avec NumPy :
X_design = np.c_[np.ones((x.shape[0], 1)), x]   # ajouter colonne de 1s
y_vec = y.reshape(-1, 1)
beta_hat = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y_vec
# beta_hat[0,0] = intercept,  beta_hat[1,0] = slope

# Avec sklearn :
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
model.intercept_   # β₀
model.coef_        # β₁, β₂, ...
```

### Régression polynomiale
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)   # fit ET transform sur train
X_test_poly  = poly.transform(X_test)         # SEULEMENT transform sur test

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)
poly_model.predict(X_test_poly)
```

> ⚠️ `fit_transform` sur train, `transform` seulement sur test (évite data leakage)

---

## MÉTRIQUES DE RÉGRESSION

| Métrique | Formule | Objectif | Code |
|---|---|---|---|
| MAE | $\frac{1}{n}\sum|y_i - \hat{y}_i|$ | **Bas** | `mean_absolute_error(y, y_pred)` |
| MSE | $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$ | **Bas** | `mean_squared_error(y, y_pred)` |
| R² | $1 - \frac{SS_{res}}{SS_{tot}}$ | **Haut** (max=1) | `r2_score(y, y_pred)` |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)
```

---

## KNN — K-NEAREST NEIGHBORS

### Principe
- **Classification** → prédire la **classe majoritaire** parmi les k voisins
- **Régression** → prédire la **moyenne** des k voisins

### Distance Euclidienne
$$d = \sqrt{(x_1 - q_1)^2 + (x_2 - q_2)^2}$$

```python
# Manuel (classification) :
df['distance'] = np.sqrt((df['x1'] - qx)**2 + (df['x2'] - qy)**2)
sorted_df = df.sort_values('distance').reset_index(drop=True)
predicted_class = sorted_df.head(k)['label'].mode().iloc[0]

# Manuel (régression, 1D) :
df['distance'] = (df['x'] - x_new).abs()
sorted_df = df.sort_values('distance')
prediction = sorted_df.head(k)['y'].mean()

# Avec sklearn :
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn.predict(X_test)
```

---

## LOGISTIC REGRESSION

```python
from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression(max_iter=10000)   # max_iter souvent nécessaire
log_reg.fit(X_train, y_train)
log_reg.predict(X_test)
```
> Retourne une probabilité → convertie en classe. Fonctionne pour multi-classes.

---

## DECISION TREE

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

dt_clf = DecisionTreeClassifier(random_state=4610)
dt_reg = DecisionTreeRegressor(random_state=4610)

dt_clf.fit(X_train, y_train)
dt_reg.fit(X_train, y_train)
```
> Capture des relations **non-linéaires**. Peut sur-apprendre (overfitting) facilement.

---

## MÉTRIQUES DE CLASSIFICATION

| Métrique | Formule | Quand l'utiliser |
|---|---|---|
| **Accuracy** | $\frac{TP+TN}{total}$ | En général |
| **Precision** | $\frac{TP}{TP+FP}$ | Quand les faux positifs coûtent cher (fraude) |
| **Recall** | $\frac{TP}{TP+FN}$ | Quand les faux négatifs coûtent cher (maladie) |

- **Precision haute** → peu de fausses alertes (chaque alerte est fiable)
- **Recall haut** → on rate peu de cas réels (on attrape tout)

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay

accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred, average='macro', zero_division=0)
recall_score(y_test, y_pred, average='macro', zero_division=0)

# Confusion matrix :
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap='Blues')
plt.show()

# Ou manuel :
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=target_names)
disp.plot(ax=ax, cmap='Blues', colorbar=False)
```

---

## TABLEAU RÉCAPITULATIF DES MODÈLES

```python
# Pattern général pour comparer plusieurs modèles :
results = []
for name, model in [("Linear Reg", lr), ("Decision Tree", dt)]:
    y_pred = model.predict(X_test)
    results.append({
        "Model": name,
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "R-squared": r2_score(y_test, y_pred),
    })
pd.DataFrame(results).sort_values('R-squared', ascending=False)
```

---

## K-MEANS CLUSTERING

### Principe
- Algorithme itératif qui assigne chaque point au centroïde le plus proche
- Minimise l'inertie (variance intra-cluster)

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Choisir k avec Silhouette Score & Davies-Bouldin Index :
rows = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=4610)
    kmeans.fit(X_train)
    labels = kmeans.predict(X_test)
    rows.append({
        'k': k,
        'Silhouette Score': silhouette_score(X_test, labels),
        'Davies-Bouldin Index': davies_bouldin_score(X_test, labels),
    })
eval_df = pd.DataFrame(rows)

# Meilleur k : Silhouette Score HAUT + Davies-Bouldin FAIBLE
best_k = ...

# Fit final :
best_kmeans = KMeans(n_clusters=best_k, random_state=4610)
best_kmeans.fit(X)
df['cluster'] = best_kmeans.labels_

# Centroides :
best_kmeans.cluster_centers_   # shape (k, n_features)
```

### Métriques de clustering

| Métrique | Objectif | Formule |
|---|---|---|
| **Silhouette Score** | **Haut** (entre -1 et 1) | $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$ |
| **Davies-Bouldin Index** | **Bas** (≥ 0) | $DB = \frac{1}{k}\sum_{i}\max_{j \neq i}\frac{s_i + s_j}{d_{ij}}$ |

- $a(i)$ = distance moyenne à son propre cluster
- $b(i)$ = distance moyenne minimale aux autres clusters
- $s_i$ = dispersion intra-cluster $i$, $d_{ij}$ = distance entre centroïdes $i$ et $j$

### Visualiser les clusters
```python
for label in sorted(df['cluster'].unique()):
    pts = df[df['cluster'] == label]
    plt.scatter(pts['x1'], pts['x2'], label=f'Cluster {label}', alpha=0.7)

plt.scatter(best_kmeans.cluster_centers_[:,0], best_kmeans.cluster_centers_[:,1],
            c='black', marker='x', s=150, linewidths=2, label='Centroids')
plt.legend()
```

### Pourquoi pas trop petit/grand k ?
- **k trop petit** → fusionne des groupes distincts
- **k trop grand** → découpe des groupes naturels artificiellement

---

## CLUSTERING HIÉRARCHIQUE (Agglomératif)

```python
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

methods = ['single', 'complete', 'average', 'ward']

# Linkage matrices (pour dendrogrammes) :
linkage_matrices = {}
for method in methods:
    linkage_matrices[method] = linkage(X_points, method=method)

# Dendrogrammes :
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, method in zip(axes.flat, methods):
    dendrogram(linkage_matrices[method], labels=labels, ax=ax)
    ax.set_title(f'{method.capitalize()} Linkage')

# Fit AgglomerativeClustering :
model = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = model.fit_predict(X_points)
```

### Méthodes de linkage

| Méthode | Distance entre clusters | Commentaire |
|---|---|---|
| **single** | min des distances entre points | Sensible aux outliers, forme des "chaînes" |
| **complete** | max des distances entre points | Clusters compacts |
| **average** | moyenne des distances | Compromis |
| **ward** | minimise la variance intra-cluster | Résultats souvent similaires à complete/average |

> **Complete, average, et Ward** donnent généralement les groupements les plus similaires.

---

## PCA — ANALYSE EN COMPOSANTES PRINCIPALES

### Principe
- Réduit la dimension en trouvant les axes de **variance maximale**
- **Non-supervisé** (n'utilise pas les étiquettes)
- Transformation linéaire : $Z = XW$ où $W$ contient les composantes principales
- **PCA ≠ LDA** : LDA (Linear Discriminant Analysis) est **supervisé** et maximise la séparation entre classes

### Formule : Explained Variance Ratio
$$\text{Explained Variance Ratio}_j = \frac{\lambda_j}{\sum_{k=1}^{p} \lambda_k}$$
- $\lambda_j$ = valeur propre de la composante $j$ — **plus c'est grand, plus la composante est importante**

```python
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# Garder 95% de la variance :
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train)   # fit ET transform sur train
X_test_pca  = pca.transform(X_test)         # seulement transform sur test

print('Dim originale:', X_train.shape[1])
print('Dim réduite:', X_train_pca.shape[1])
print('Variance expliquée:', pca.explained_variance_ratio_.sum())

# Trouver le nb minimum de composantes pour 95% :
pca_all = PCA()
pca_all.fit(X)
cumulative = np.cumsum(pca_all.explained_variance_ratio_)
n_components = np.argmax(cumulative >= 0.95) + 1   # +1 car indexing part de 0

# Scree plot (variance expliquée par composante) :
plt.bar(range(1, len(pca_all.explained_variance_ratio_)+1),
        pca_all.explained_variance_ratio_, label='Individuelle')
plt.plot(range(1, len(pca_all.explained_variance_ratio_)+1),
         np.cumsum(pca_all.explained_variance_ratio_), 'ro-', label='Cumulative')
plt.xlabel('Composante'); plt.ylabel('Variance Ratio')
plt.legend()

# Visualisation 2D :
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X)
scatter = plt.scatter(X_2d[:,0], X_2d[:,1], c=y, cmap='viridis', alpha=0.7, s=20)
plt.colorbar(scatter, label='Classe')
plt.title(f'PCA 2D — Variance expliquée: {pca_2d.explained_variance_ratio_.sum():.2%}')
plt.xlabel('PC1'); plt.ylabel('PC2')

# LDA (supervisé, pour comparaison) :
lda = LDA(n_components=2)
X_lda = lda.fit_transform(X, y)    # utilise les labels y
```

> Même si PCA ne préserve pas 100% de la variance, une projection 2D reste utile pour **visualiser la structure** des données.

---

## CLASSIFICATION REPORT

```python
from sklearn.metrics import classification_report

# Rapport complet (precision, recall, f1-score par classe) :
print(classification_report(y_test, y_pred))

# model.score() = raccourci pour accuracy_score :
model.score(X_test, y_test)   # équivalent à accuracy_score(y_test, model.predict(X_test))
```

---

## PATTERNS DE CODE FRÉQUENTS

### Charger des datasets sklearn
```python
from sklearn.datasets import load_diabetes, load_wine, load_iris, load_digits, make_blobs

dataset = load_diabetes(as_frame=True)
df = dataset.frame
X = df.drop('target', axis=1)
y = df['target']

# make_blobs (données synthétiques) :
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.35,
                        center_box=(-3.5, 3.5), random_state=4610)
```

### Charger seaborn dataset
```python
from seaborn import load_dataset
df = load_dataset('titanic')   # ou 'penguins', 'iris', etc.
```

### Imputer un plot de subplots + métriques
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(df['k'], df['Silhouette Score'], marker='o')
axes[0].set_title('Silhouette Score vs. k')
axes[0].set_xlabel('k'); axes[0].set_ylabel('Silhouette Score')
axes[0].grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

### Sélectionner colonnes par type
```python
num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(exclude='number').columns
# ou :
cat_cols = df.select_dtypes(include=['object', 'category']).columns
```

### Reformater un array NumPy
```python
x.reshape(-1, 1)          # colonne vecteur (n, 1)
np.c_[np.ones((n, 1)), x] # ajouter colonne de 1s
np.linalg.inv(M)           # inverse de matrice
A.T                        # transposée
A @ B                      # produit matriciel
np.cumsum(arr)             # cumul
np.argmax(arr)             # index du max
```

### Images (digits dataset)
```python
img = X.iloc[i].to_numpy().reshape(8, 8)
ax.imshow(img, cmap='gray')
ax.set_title(f'Label: {int(y.iloc[i])}')
ax.axis('off')
```

---

## AUTRES DATASETS SKLEARN

```python
from sklearn.datasets import (
    load_diabetes,          # régression, 442 patients, 10 features, target=progression maladie
    load_wine,              # classification, 178 vins, 13 features, 3 classes
    load_iris,              # classification, 150 iris, 4 features, 3 classes
    load_digits,            # classification, 1797 images 8x8, target=chiffre 0-9
    load_breast_cancer,     # classification binaire, cancer bénin/malin
    make_blobs,             # clustering synthétique, clusters gaussiens
    make_classification,    # classification synthétique
)
```

---

## IMPORTS COMPLETS (à copier)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report,
    silhouette_score, davies_bouldin_score,
)
from sklearn.datasets import (
    load_diabetes, load_wine, load_iris, load_digits,
    load_breast_cancer, make_blobs, make_classification,
)
from scipy.cluster.hierarchy import dendrogram, linkage
```

---

## RÉSUMÉ : QUAND UTILISER QUOI

| Objectif | Méthode | Supervisé ? |
|---|---|---|
| Prédire un nombre | Linear Regression, Poly Reg, Decision Tree Reg | ✅ |
| Classer en catégories | Logistic Reg, KNN, Decision Tree Clf | ✅ |
| Grouper sans labels | K-Means, Agglomerative Clustering | ❌ |
| Réduire dimensions (sans labels) | PCA | ❌ |
| Réduire dimensions (avec labels) | LDA | ✅ |
| Imputer des NaN | SimpleImputer, KNNImputer | — |

## MATPLOTLIB vs SEABORN

| | Matplotlib | Seaborn |
|---|---|---|
| **Niveau** | Bas niveau (contrôle total) | Haut niveau (simplifié) |
| **Relation** | Bibliothèque de base | Construit sur Matplotlib |
| **Meilleur pour** | Plots custom, publication | Exploration stat, DataFrames |
| **Données catég.** | Manuel | Intégré (`hue`, `style`, `col`) |
| **Style par défaut** | Basique | Attrayant |

---

