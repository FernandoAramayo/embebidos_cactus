import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np

# 1. Prepare the training data
x_train = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
y_train = np.array([-1.0, 2.0, 5.0, 8.0, 11.0, 14.0], dtype=float)

# 2. Define the Neural Network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

# 3. Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error')

# 4. Train the model (The "Learning" phase)
print("Training started...")
model.fit(x_train, y_train, epochs=500, verbose=0) 
print("Training finished!\n")

# 5. Predict for X = 5 and X = 3.3
x_test = np.array([5.0, 3.3], dtype=float)
predictions = model.predict(x_test)

print("-" * 30)
print(f"Prediction for X=5:   {predictions[0][0]:.4f} (Exact: 17)")
print(f"Prediction for X=3.3: {predictions[1][0]:.4f} (Exact: 11.9)")
print("-" * 30)