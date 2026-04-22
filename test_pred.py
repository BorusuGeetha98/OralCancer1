import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw
import random
import os

model = tf.keras.models.load_model('oral_cancer_model.h5', compile=False)

# cancer image
r, g, b = 200, 100, 100
img = Image.new('RGB', (224, 224), color=(r, g, b))
draw = ImageDraw.Draw(img)
draw.ellipse((50, 50, 150, 150), fill=(100, 0, 0))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

pred = model.predict(img_array, verbose=0)[0][0]
print("Synth Cancer prediction:", pred)

# normal image
r_n, g_n, b_n = 220, 180, 180
img_normal = Image.new('RGB', (224, 224), color=(r_n, g_n, b_n))
img_array2 = np.array(img_normal) / 255.0
img_array2 = np.expand_dims(img_array2, axis=0)

pred2 = model.predict(img_array2, verbose=0)[0][0]
print("Synth Normal prediction:", pred2)
