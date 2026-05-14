import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 1. Cargar el dataset (usando tus nombres reales)
df = pd.read_csv('Clustering.csv')

# 2. Seleccionar las columnas correctas (minúsculas según tu imagen)
# Usamos .dropna() para eliminar cualquier fila con valores NaN
new_dataset = df[['x', 'y']].dropna()

# 3. Método del Codo (Elbow Method)
inercia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(new_dataset)
    inercia.append(kmeans.inertia_)

plt.plot(range(1, 11), inercia, 'bx-')
plt.title('Método del Codo')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inercia')
plt.show()

# 4. Aplicar PCA (Reducción de dimensiones)
# PCA ayuda a resumir la información de X, Y y Z en componentes principales
pca = PCA(n_components=2)
pca_data = pca.fit_transform(new_dataset) 
print(f"Varianza explicada por PCA: {pca.explained_variance_ratio_.sum():.2%}")