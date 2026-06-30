import tensorflow as tf
import numpy as np
from PIL import Image
import os

model = tf.keras.models.load_model('oral_cancer_model.h5', compile=False)

def test_image(path):
    if not os.path.exists(path):
        print(f"File {path} not found")
        return
    img = Image.open(path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array, verbose=0)[0][0]
    print(f"Image: {os.path.basename(path)} | Pred: {pred:.4f}")

print("Testing Cancer Images:")
test_image('media/predictions/aug_aug_C0235749-Mouth_cancer-SPL-20170511085515620.jpg')
test_image('media/predictions/aug_aug_aug_Tongue-cancer-symptoms.png')

print("\nTesting potentially Normal Images (low numbers usually):")
test_image('media/predictions/001.jpeg')
test_image('media/predictions/002.jpeg')
