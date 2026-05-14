import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. Importar valores usando pandas
try:
    df = pd.read_csv('Clustering.csv')
except FileNotFoundError:
    print("Error: No se encontró 'Clustering.csv' en el directorio actual.")
    exit()

# 2. Filtrar valores NaN 
df = df.dropna(subset=['X', 'Y'])

# 3. Seleccionar X e Y
new_dataset = df[['X', 'Y']]

# 4. ELBOW METHOD para determinar el mejor K
inercia = []
K_range = range(1, 11)

for k in K_range:
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    model.fit(new_dataset)
    inercia.append(model.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(K_range, inercia, 'bx-')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inercia')
plt.title('Método del Codo para el Dataset Clustering')
plt.show()

# 5. Comparar resultados 
k_best = 3 
model_best = KMeans(n_clusters=k_best, n_init=10)
labels_best = model_best.fit_predict(new_dataset)

plt.scatter(new_dataset['X'], new_dataset['Y'], c=labels_best, cmap='viridis')
plt.title(f"Resultado con K={k_best} (Óptimo)")
plt.show()

# 6. Implementación de PCA
pca = PCA(n_components=1) 
pca_result = pca.fit_transform(new_dataset)
print(f"Varianza explicada por el componente principal: {pca.explained_variance_ratio_[0]:.2%}")