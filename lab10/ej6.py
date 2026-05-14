import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. Cargar el dataset 
df = pd.read_csv('Clustering.csv')

# 2. Seleccionar las columnas y limpiar NaNs
new_dataset = df[['x', 'y']].dropna()
scaler = StandardScaler()
scaled_data = scaler.fit_transform(new_dataset)

# 3. Método del Codo (Elbow Method)
inercia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(scaled_data)
    inercia.append(kmeans.inertia_)

plt.figure(figsize=(8,4))
plt.plot(range(1, 11), inercia, 'bx-')
plt.title('Método del Codo (Determinando K óptimo)')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inercia')
plt.show()

# 4. COMPARACIÓN: K óptimo vs K arbitrario 
def plot_kmeans(k, data, title):
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = model.fit_predict(data)
    plt.scatter(new_dataset['x'], new_dataset['y'], c=labels, cmap='viridis')
    plt.title(title)
    plt.show()

plot_kmeans(3, scaled_data, "Resultado con K=3 (Basado en el Codo)")
plot_kmeans(6, scaled_data, "Resultado con K=6 (Número Arbitrario)")

# 5. Aplicar PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data) 
print(f"Varianza explicada por PCA: {pca.explained_variance_ratio_.sum():.2%}")

