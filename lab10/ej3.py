import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- 1. Carga de datos ---
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, 'spam.csv')

try:
    df = pd.read_csv(file_path, encoding='latin-1')
except FileNotFoundError:
    print(f"Error: No se encontró 'spam.csv' en {dir_path}")
    exit()

df = df.iloc[:, [0, 1]] 
df.columns = ['label', 'text']

# --- 2. Preprocesamiento ---
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

vocab_size = 1000
max_length = 20
trunc_type = 'post'
padding_type = 'post'

tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])
padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

# --- 3. Modelo de Red Neuronal ---
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 16),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# --- 4. Entrenamiento ---
print("Entrenando el modelo...")
labels = np.array(df['label'])
model.fit(padded, labels, epochs=30, verbose=0)
print("Entrenamiento finalizado.\n")

# --- 5. Predicción ---
new_messages = ["Win a brand new car now!", "Hello, call me later."]
new_seq = tokenizer.texts_to_sequences(new_messages)
new_padded = pad_sequences(new_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)

predictions = model.predict(new_padded)

for i, msg in enumerate(new_messages):
    is_spam = "SPAM" if predictions[i] > 0.5 else "NORMAL"
    print(f"Mensaje: {msg} -> Resultado: {is_spam} ({predictions[i][0]:.4f})")