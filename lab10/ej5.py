import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# 1. Cargar los datos de la imagen
data = {
    'cost': [750, 1245, 230, 533, 490, 1000, 190, 900, 600, 50, 1100, 930, 450, 330, 750],
    'card_purchases': [3, 1, 4, 3, 2, 1, 0, 3, 2, 1, 0, 4, 3, 2, 0]
}
df = pd.DataFrame(data)

# 2. FEATURE SCALING (Punto clave del ejercicio)
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

# 3. Aplicar K-Means
# Elegimos K=3 para identificar: Clientes Top, Clientes Promedio, Clientes Ocasionales
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_transform(df_scaled).argmin(axis=1) 

# 4. Visualización
plt.scatter(df['cost'], df['card_purchases'], c=df['cluster'], cmap='viridis', s=100)
plt.title('Segmentación de Clientes Vet Shop')
plt.xlabel('Costo de Compra (bs)')
plt.ylabel('Compras con Tarjeta')
plt.grid(True)
plt.show()

print(df.sort_values(by='cluster'))