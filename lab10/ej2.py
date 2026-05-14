import os
import numpy as np
import tensorflow as tf

# 1. Configuración para evitar alertas innecesarias de CUDA (GPU)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 2. Datos de entrenamiento (Y = 3X + 2)
x_train = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
y_train = np.array([-1.0, 2.0, 5.0, 8.0, 11.0, 14.0], dtype=float)

# 3. Construcción del Modelo (Ejercicio 2: Más capas y neuronas)
model = tf.keras.Sequential([
    # Capa de entrada con 10 neuronas y activación ReLU
    tf.keras.layers.Dense(units=10, activation='relu', input_shape=[1]),
    # Capa oculta adicional con 5 neuronas
    tf.keras.layers.Dense(units=5, activation='relu'),
    # Capa de salida (1 sola neurona para el resultado numérico)
    tf.keras.layers.Dense(units=1)
])

# 4. Compilación del Modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# 5. Entrenamiento
print("Entrenando la red neuronal...")
model.fit(x_train, y_train, epochs=500, verbose=0)
print("Entrenamiento completado.\n")

# 6. Predicción (Corregido con np.array para evitar el error de tipos)
x_test = np.array([[5.0], [3.3]], dtype=float)
predictions = model.predict(x_test)


print("-" * 30)
print(f"Resultado para X=5:   {predictions[0][0]:.4f} (Esperado: 17)")
print(f"Resultado para X=3.3: {predictions[1][0]:.4f} (Esperado: 11.9)")
print("-" * 30)