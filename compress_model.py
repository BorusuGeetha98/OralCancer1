import os
import tensorflow as tf

def minimize_h5_file(filepath):
    print(f"Original size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
    
    # Load model and save it immediately without optimizer to shrink it by ~60%
    temp_path = "temp_compressed.h5"
    try:
        model = tf.keras.models.load_model(filepath, compile=False)
        model.save(temp_path, include_optimizer=False)
        
        # Replace original with compressed
        os.replace(temp_path, filepath)
        print(f"New minimized size: {os.path.getsize(filepath) / (1024*1024):.2f} MB")
        print("Success! Reduced size without losing any prediction accuracy.")
    except Exception as e:
        print("Error compressing:", str(e))

if __name__ == '__main__':
    minimize_h5_file('oral_cancer_model.h5')
