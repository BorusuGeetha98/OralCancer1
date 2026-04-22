import os
import tensorflow as tf
import numpy as np

def compress_model_svd(filepath='oral_cancer_model.h5', k=45):
    print("Loading original model...")
    orig_model = tf.keras.models.load_model(filepath, compile=False)
    
    # The layers we care about
    # 0: Conv2D, 1: MaxPool
    # 2: Conv2D, 3: MaxPool
    # 4: Conv2D, 5: MaxPool
    # 6: Flatten
    # 7: Dense(512)
    # 8: Dropout
    # 9: Dense(1)
    
    dense_layer = orig_model.layers[7]
    W, b = dense_layer.get_weights()
    print(f"Original Dense Weights Shape: {W.shape}") # (86528, 512)
    
    print("Performing SVD on dense weights to shrink size natively without retraining...")
    # W = U * S * V^T
    # We truncate to k components
    U, S, Vh = np.linalg.svd(W, full_matrices=False)
    
    U_k = U[:, :k]
    S_k = S[:k]
    Vh_k = Vh[:k, :]
    
    # U_scaled = U_k * S_k
    U_scaled = U_k * S_k[np.newaxis, :]
    W_k1 = U_scaled # shape (86528, k)
    W_k2 = Vh_k # shape (k, 512)
    
    print(f"Compressed Dense components: {W_k1.shape} and {W_k2.shape}")
    
    # Build new model
    new_model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(k, use_bias=False), # New compressed projection layer
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Transfer Weights
    for i in range(7): # Up to Flatten
        new_model.layers[i].set_weights(orig_model.layers[i].get_weights())
        
    # Set the split dense weights
    new_model.layers[7].set_weights([W_k1])
    new_model.layers[8].set_weights([W_k2, b])
    
    # Set final prediction layer
    new_model.layers[10].set_weights(orig_model.layers[9].get_weights())
    
    new_path = "compressed_SVD_model.h5"
    new_model.save(new_path, include_optimizer=False)
    
    orig_size = os.path.getsize(filepath) / (1024*1024)
    new_size = os.path.getsize(new_path) / (1024*1024)
    print(f"Original Size: {orig_size:.2f} MB")
    print(f"New Compressed Size: {new_size:.2f} MB")

if __name__ == "__main__":
    compress_model_svd()
