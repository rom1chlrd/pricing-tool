# ESI 4610 — Exam 3 Cheat Sheet

---

## KEY CONCEPTS (True / False)

| Statement | Answer | Note |
|---|---|---|
| Seaborn is separate from Matplotlib | **FALSE** | Seaborn is built *on top of* Matplotlib |
| Scatter plot → relationship between 2 numerical variables | **TRUE** | |
| Regression → continuous target variable | **TRUE** | |
| Train/test split → estimate how well model generalizes | **TRUE** | |
| Regression trees work best for linear relationships | **FALSE** | They capture **non-linear** relationships |
| Precision = true positives among all predicted positives | **TRUE** | |
| Recall = true positives among all actual positives | **TRUE** | |
| K in KNN = K in K-means | **FALSE** | KNN = # neighbors, K-means = # clusters |
| KNN works for both classification and regression | **TRUE** | |
| Logistic Regression cannot classify | **FALSE** | It outputs a probability converted to a class |
| PCA maximizes class separation | **FALSE** | PCA maximizes **variance**, not separation |
| PCA is supervised | **FALSE** | PCA is **unsupervised**; LDA is supervised |
| Agglomerative hierarchical clustering = bottom-up | **TRUE** | Starts with each point alone, then merges |

---

## TYPES OF MACHINE LEARNING

| Type | Definition | Examples |
|---|---|---|
| **Supervised** | Learns to predict $y$ from labeled $(x, y)$ pairs | Regression, Classification |
| **Unsupervised** | Finds patterns in $x$ without labels | Clustering, PCA |
| **Reinforcement** | Learns by interacting with an environment (reward) | Games, robotics |

## PROBLEM TYPE

| Scenario | Type | Target variable |
|---|---|---|
| Predict a **number** (time, price, score) | **Regression** | continuous |
| Predict a **binary category** (spam / not spam) | **Binary Classification** | 0 / 1 |
| Predict among **3+ categories** (mold/pollen/dust) | **Multinomial Classification** | categorical |
| **Group** without labels | **Clustering (unsupervised)** | none |
| Reduce number of variables | **Dimensionality Reduction** | none |

**For supervised problems:** identify $n$ (number of observations) and $p$ (number of independent variables, excluding the target).

## VARIABLE TYPES

| Type | Sub-type | Example |
|---|---|---|
| **Quantitative continuous** | — | Temperature, price, weight |
| **Quantitative discrete** | — | Number of tickets, number of customers |
| **Qualitative nominal** | Categories **without** order | ZIP code, gender, color |
| **Qualitative ordinal** | Categories **with** order | Rating: poor / fair / good / excellent |

---

## MODEL FORMULAS

### Linear Regression
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p + \epsilon$$
- $\beta_0$ = intercept, $\beta_1 \dots \beta_p$ = slopes, $\epsilon$ = noise (error term)

### Polynomial Regression
$$y = \beta_0 + \beta_1 x + \beta_2 x^2 + \cdots + \beta_n x^n$$

### Logistic Regression (sigmoid)
$$P(y=1 \mid x_1, \dots, x_n) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n)}}$$
→ Predict class 1 if $P \geq 0.5$, otherwise class 0

---

## VISUALIZATION — MATPLOTLIB

### Basic plots
```python
import matplotlib.pyplot as plt

plt.plot(x, y, color='blue', label='label', marker='o', linestyle='--')  # line plot
plt.scatter(x, y, alpha=0.7, c=colors, s=sizes, cmap='coolwarm')         # scatter
plt.bar(categories, values)          # vertical bar chart
plt.barh(categories, values)         # horizontal bar chart
plt.hist(data, bins=20)              # histogram
plt.pie(sizes, labels=labels, autopct='%1.1f%%', explode=(0.1,0,0,0),
        shadow=True, startangle=140) # pie chart
plt.axis('equal')                    # ensures circular pie

plt.title('Title')
plt.xlabel('X'); plt.ylabel('Y')
plt.legend()
plt.xticks(rotation=45)
plt.yticks([])                       # hide y-axis ticks
plt.grid(True)
plt.colorbar()                       # color scale (when using c=...)
plt.figure(figsize=(10, 5))
plt.savefig("filename.png")
plt.show()
```

### Styles
```python
plt.style.use('ggplot')          # apply a theme
plt.style.use('dark_background')
plt.style.use('default')         # reset to default
print(plt.style.available)       # list all available styles
```

### Common linestyles & markers
| Linestyle | Code | Marker | Code |
|---|---|---|---|
| solid | `'-'` | circle | `'o'` |
| dashed | `'--'` | square | `'s'` |
| dotted | `':'` | triangle | `'^'` |
| dash-dot | `'-.'` | cross | `'x'` |

### Subplots
```python
fig, axes = plt.subplots(nrows, ncols, figsize=(w, h))

# Examples:
fig, axes = plt.subplots(1, 2, figsize=(12, 4))          # 1 row, 2 cols
fig, axes = plt.subplots(2, 3)                            # 2 rows, 3 cols
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))    # destructured

# Accessing axes:
axes[0].plot(...)            # 1D array of axes
axes[0, 1].plot(...)         # 2D array of axes
axes.flat                    # iterate over all: zip(axes.flat, items)

# Axis properties:
ax.set_title('...')
ax.set_xlabel('...')
ax.set_ylabel('...')

# Shared x-axis:
fig, axes = plt.subplots(2, 1, sharex=True)

plt.tight_layout()                           # prevent overlapping
plt.subplots_adjust(wspace=0.1, hspace=0.2) # manual spacing between subplots
```

### Pandas plots
```python
df.plot.bar(color=['red', 'blue', 'green'])  # bar chart
df.plot.bar(stacked=True)                    # stacked bar chart
df.plot.barh()                               # horizontal bar chart
series.plot(kind='bar', ax=axes[0])          # in a specific subplot
series.plot(kind='hist', bins=20)
series.plot(kind='kde')                      # density / KDE plot
```

### Dates on x-axis
```python
df['col'] = pd.to_datetime(df['col'])
plt.xticks(rotation=45)
```

---

## VISUALIZATION — SEABORN

```python
import seaborn as sns
```

### Scatter plot
```python
sns.scatterplot(
    data=df,
    x='col_x', y='col_y',
    hue='category',      # color by category
    style='col_style',   # marker shape by category
    size='col_size',     # marker size by numeric column
    edgecolor='black',
    ax=axes[0]           # target subplot
)
```

### Histogram
```python
sns.histplot(data=df, x='col', bins=15, kde=True, hue='cat', stat="density")
# stat="density" → shows density instead of counts
```

### Boxplot
```python
sns.boxplot(data=df, x='cat', y='value', hue='cat2')
```

### Pairplot
```python
sns.pairplot(data=df[['A', 'B', 'C', 'cat']], hue='cat', height=3)
```

### Correlation heatmap
```python
corr = df.select_dtypes(include='number').corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
```

### Density plot (KDE)
```python
df['col'].plot(kind='kde', color='red', alpha=0.5)  # via Pandas
sns.histplot(df['col'], kde=True, stat='density')    # via Seaborn (combined)
```

### Faceted plots
```python
# relplot: faceted scatter / line
sns.relplot(data=df, x='X', y='Y', hue='species', col='sex')

# catplot: faceted box / bar / etc.
sns.catplot(x='day', y='total_bill', hue='smoker', col='time',
            kind='bar', data=df, height=4, aspect=1)
sns.catplot(x='day', y='total_bill', hue='time', col='smoker',
            kind='box', data=df, height=4, aspect=.7)

# FacetGrid (manual)
g = sns.FacetGrid(df, col='time', hue='smoker')
g.map(sns.scatterplot, 'x_col', 'y_col')
g.add_legend()
```

### Color palettes
| Type | Examples | Use for |
|---|---|---|
| Qualitative | `'Set1'`, `'Set2'`, `'tab10'`, `'husl'` | Categorical data |
| Sequential | `'Blues'`, `'viridis'`, `'plasma'` | Continuous data |
| Diverging | `'coolwarm'`, `'RdBu'` | Data with a meaningful center |

### Grouped bar chart (Pandas)
```python
avg = df.groupby(['cat1', 'cat2'])['val'].mean().unstack()
avg.plot(kind='bar', ax=ax)
```

---

## DATA CLEANING

### Missing values
```python
df.isnull().sum()                        # count NaN per column
df.isnull().mean()                       # % NaN per column
df.isnull().any()                        # boolean per column

# Drop columns with > 70% NaN:
df = df.loc[:, df.isnull().mean() <= 0.7]

# Get columns that have NaN:
mask = df.isnull().any()
missing_cols = df.columns[mask]

# Visualize:
import missingno as msno
msno.matrix(df)
plt.show()
```

### Manual imputation (fillna)
```python
# Numeric → mean or median
df['col'] = df['col'].fillna(df['col'].mean())
df['col'] = df['col'].fillna(df['col'].median())

# Categorical → mode
df['col'] = df['col'].fillna(df['col'].mode()[0])

# General auto-imputation:
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

### OneHotEncoder (for KNN imputation pipeline)
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df[['col']])
encoder.get_feature_names_out(['col'])   # column names of encoded output
encoder.inverse_transform(encoded)       # decode back to original
```

---

## ML GENERAL PIPELINE

```python
from sklearn.model_selection import train_test_split

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=4610
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
model.score(X_test, y_test)   # shortcut for accuracy_score
```

---

## LINEAR REGRESSION

### OLS — Ordinary Least Squares (matrix form)
$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

```python
# Manual OLS with NumPy:
X_design = np.c_[np.ones((x.shape[0], 1)), x]   # add column of ones
y_vec = y.reshape(-1, 1)
beta_hat = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y_vec
# beta_hat[0, 0] = intercept,  beta_hat[1, 0] = slope

# With sklearn:
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
model.intercept_   # β₀
model.coef_        # β₁, β₂, ...
```

### Polynomial Regression
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)   # fit AND transform on train
X_test_poly  = poly.transform(X_test)         # transform ONLY on test

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)
poly_model.predict(X_test_poly)
```

> ⚠️ Always `fit_transform` on train, `transform` only on test — prevents data leakage.

---

## REGRESSION METRICS

| Metric | Formula | Goal | Code |
|---|---|---|---|
| MAE | $\frac{1}{n}\sum\|y_i - \hat{y}_i\|$ | **Low** | `mean_absolute_error(y, y_pred)` |
| MSE | $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$ | **Low** | `mean_squared_error(y, y_pred)` |
| R² | $1 - \frac{SS_{res}}{SS_{tot}}$ | **High** (max = 1) | `r2_score(y, y_pred)` |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)
```

---

## KNN — K-NEAREST NEIGHBORS

### How it works
- **Classification** → predict the **majority class** among the k nearest neighbors
- **Regression** → predict the **average** of the k nearest neighbors' values

### Euclidean Distance
$$d = \sqrt{(x_1 - q_1)^2 + (x_2 - q_2)^2}$$

```python
# Manual (classification):
df['distance'] = np.sqrt((df['x1'] - qx)**2 + (df['x2'] - qy)**2)
sorted_df = df.sort_values('distance').reset_index(drop=True)
predicted_class = sorted_df.head(k)['label'].mode().iloc[0]

# Manual (regression, 1D):
df['distance'] = (df['x'] - x_new).abs()
sorted_df = df.sort_values('distance')
prediction = sorted_df.head(k)['y'].mean()

# With sklearn:
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn.predict(X_test)
```

---

## LOGISTIC REGRESSION

```python
from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression(max_iter=10000)   # max_iter often needed
log_reg.fit(X_train, y_train)
log_reg.predict(X_test)
```
> Outputs a probability → converted to a class. Works for multi-class problems too.

---

## DECISION TREE

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

dt_clf = DecisionTreeClassifier(random_state=4610)
dt_reg = DecisionTreeRegressor(random_state=4610)

dt_clf.fit(X_train, y_train)
dt_reg.fit(X_train, y_train)
```
> Captures **non-linear** relationships. Prone to **overfitting**.

---

## CLASSIFICATION METRICS

| Metric | Formula | When to prioritize |
|---|---|---|
| **Accuracy** | $\frac{TP+TN}{\text{total}}$ | General overall performance |
| **Precision** | $\frac{TP}{TP+FP}$ | When false positives are costly (e.g. fraud) |
| **Recall** | $\frac{TP}{TP+FN}$ | When false negatives are costly (e.g. disease) |

- **High Precision** → few false alarms (every alert is reliable)
- **High Recall** → very few real cases missed (catch everything)

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              confusion_matrix, ConfusionMatrixDisplay, classification_report)

accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred, average='macro', zero_division=0)
recall_score(y_test, y_pred, average='macro', zero_division=0)
print(classification_report(y_test, y_pred))   # full report: precision, recall, f1

# Confusion matrix:
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap='Blues')
plt.show()

# Or manually:
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=target_names)
disp.plot(ax=ax, cmap='Blues', colorbar=False)
```

---

## COMPARING MULTIPLE MODELS

```python
# General pattern:
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

### How it works
- Iteratively assigns each point to the nearest centroid
- Minimizes within-cluster variance (inertia)

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Choose k using Silhouette Score & Davies-Bouldin Index:
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

# Best k: Silhouette Score HIGH + Davies-Bouldin LOW
best_kmeans = KMeans(n_clusters=best_k, random_state=4610)
best_kmeans.fit(X)
df['cluster'] = best_kmeans.labels_
best_kmeans.cluster_centers_   # shape (k, n_features)
```

### Clustering metrics

| Metric | Goal | Formula |
|---|---|---|
| **Silhouette Score** | **High** (−1 to 1) | $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$ |
| **Davies-Bouldin Index** | **Low** (≥ 0) | $DB = \frac{1}{k}\sum_{i}\max_{j \neq i}\frac{s_i + s_j}{d_{ij}}$ |

- $a(i)$ = average distance to points in own cluster
- $b(i)$ = minimum average distance to points in any other cluster
- $s_i$ = intra-cluster scatter, $d_{ij}$ = distance between centroids $i$ and $j$

### Visualizing clusters
```python
for label in sorted(df['cluster'].unique()):
    pts = df[df['cluster'] == label]
    plt.scatter(pts['x1'], pts['x2'], label=f'Cluster {label}', alpha=0.7)

plt.scatter(best_kmeans.cluster_centers_[:, 0], best_kmeans.cluster_centers_[:, 1],
            c='black', marker='x', s=150, linewidths=2, label='Centroids')
plt.legend()
```

### Why not too small / too large k?
- **k too small** → merges distinct groups together
- **k too large** → splits natural groups artificially

---

## HIERARCHICAL CLUSTERING (Agglomerative)

```python
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

methods = ['single', 'complete', 'average', 'ward']

# Compute linkage matrices (for dendrograms):
linkage_matrices = {}
for method in methods:
    linkage_matrices[method] = linkage(X_points, method=method)

# Plot dendrograms:
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, method in zip(axes.flat, methods):
    dendrogram(linkage_matrices[method], labels=labels, ax=ax)
    ax.set_title(f'{method.capitalize()} Linkage')

# Fit Agglomerative Clustering:
model = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = model.fit_predict(X_points)
```

### Linkage methods

| Method | Distance between clusters | Notes |
|---|---|---|
| **single** | min distance between any two points | Sensitive to outliers, forms "chains" |
| **complete** | max distance between any two points | Produces compact clusters |
| **average** | mean distance between all pairs | Good compromise |
| **ward** | minimizes intra-cluster variance | Often gives results similar to complete/average |

> **Complete, average, and Ward** typically produce the most similar groupings.

---

## PCA — PRINCIPAL COMPONENT ANALYSIS

### How it works
- Reduces dimensionality by finding directions of **maximum variance**
- **Unsupervised** (does not use labels)
- Linear transformation: $Z = XW$ where $W$ contains the principal components
- **PCA ≠ LDA**: LDA (Linear Discriminant Analysis) is **supervised** and maximizes class separation

### Explained Variance Ratio
$$\text{EVR}_j = \frac{\lambda_j}{\sum_{k=1}^{p} \lambda_k}$$
- $\lambda_j$ = eigenvalue of component $j$ — **larger = more important**

```python
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# Keep 95% of variance:
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train)   # fit AND transform on train
X_test_pca  = pca.transform(X_test)         # transform ONLY on test

print('Original dims:', X_train.shape[1])
print('Reduced dims:', X_train_pca.shape[1])
print('Variance retained:', pca.explained_variance_ratio_.sum())

# Find minimum components for 95%:
pca_all = PCA()
pca_all.fit(X)
n_components = np.argmax(np.cumsum(pca_all.explained_variance_ratio_) >= 0.95) + 1

# Scree plot:
plt.bar(range(1, len(pca_all.explained_variance_ratio_)+1),
        pca_all.explained_variance_ratio_, label='Individual')
plt.plot(range(1, len(pca_all.explained_variance_ratio_)+1),
         np.cumsum(pca_all.explained_variance_ratio_), 'ro-', label='Cumulative')
plt.xlabel('Component'); plt.ylabel('Variance Ratio'); plt.legend()

# 2D visualization:
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X)
scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap='viridis', alpha=0.7, s=20)
plt.colorbar(scatter, label='Class')
plt.title(f'PCA 2D — Variance: {pca_2d.explained_variance_ratio_.sum():.2%}')
plt.xlabel('PC1'); plt.ylabel('PC2')

# LDA (supervised, for comparison):
lda = LDA(n_components=2)
X_lda = lda.fit_transform(X, y)   # uses labels y
```

> Even if PCA does not preserve 100% of variance, a 2D projection is still useful to **visualize the structure** of the data.

---

## COMMON CODE PATTERNS

### Load sklearn datasets
```python
from sklearn.datasets import load_diabetes, load_wine, load_iris, load_digits, make_blobs

dataset = load_diabetes(as_frame=True)
df = dataset.frame
X = df.drop('target', axis=1)
y = df['target']

# Synthetic blobs (clustering):
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.35,
                        center_box=(-3.5, 3.5), random_state=4610)
```

### Load seaborn dataset
```python
from seaborn import load_dataset
df = load_dataset('titanic')   # also: 'penguins', 'tips', 'iris', etc.
```

### Subplot + metric plot pattern
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(df['k'], df['Silhouette Score'], marker='o')
axes[0].set_title('Silhouette Score vs. k')
axes[0].set_xlabel('k'); axes[0].set_ylabel('Silhouette Score')
axes[0].grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

### Select columns by type
```python
num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(exclude='number').columns
# or:
cat_cols = df.select_dtypes(include=['object', 'category']).columns
```

### Useful NumPy operations
```python
x.reshape(-1, 1)           # column vector (n, 1)
np.c_[np.ones((n, 1)), x]  # prepend column of ones
np.linalg.inv(M)            # matrix inverse
A.T                         # transpose
A @ B                       # matrix multiplication
np.cumsum(arr)              # cumulative sum
np.argmax(arr)              # index of maximum value
```

### Display digit images
```python
img = X.iloc[i].to_numpy().reshape(8, 8)
ax.imshow(img, cmap='gray')
ax.set_title(f'Label: {int(y.iloc[i])}')
ax.axis('off')
```

---

## SKLEARN DATASETS REFERENCE

```python
load_diabetes()      # regression — 442 patients, 10 features, target = disease progression
load_wine()          # classification — 178 wines, 13 features, 3 classes
load_iris()          # classification — 150 flowers, 4 features, 3 classes
load_digits()        # classification — 1797 images 8×8, target = digit 0–9
load_breast_cancer() # binary classification — benign / malignant
make_blobs()         # synthetic clustering — Gaussian clusters
make_classification()# synthetic classification dataset
```

---

## ALL IMPORTS

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

## QUICK REFERENCE: WHEN TO USE WHAT

| Goal | Method | Supervised? |
|---|---|---|
| Predict a number | Linear Regression, Polynomial Reg, Decision Tree Reg | ✅ |
| Classify into categories | Logistic Reg, KNN, Decision Tree Clf | ✅ |
| Group without labels | K-Means, Agglomerative Clustering | ❌ |
| Reduce dimensions (no labels) | PCA | ❌ |
| Reduce dimensions (with labels) | LDA | ✅ |
| Impute missing values | SimpleImputer, KNNImputer | — |

## MATPLOTLIB vs SEABORN

| | Matplotlib | Seaborn |
|---|---|---|
| **Level** | Low-level (full control) | High-level (simplified) |
| **Relationship** | Base library | Built on top of Matplotlib |
| **Best for** | Custom plots, publication figures | Statistical exploration, DataFrames |
| **Categorical data** | Manual | Built-in (`hue`, `style`, `col`) |
| **Default style** | Basic | Attractive |

---

*ESI 4610 — Spring 2026 | Based on HW6, HW7, HW8 and Exam 3 Review*
