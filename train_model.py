import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Directory configuration
# Make sure your dataset is organized as:
# dataset/
#   train/
#     cancer/ (3000 images)
#     non_cancer/ (3000 images)
#   validation/
#     cancer/
#     non_cancer/
BASE_DIR = 'dataset'
TRAIN_DIR = os.path.join(BASE_DIR, 'train')
VAL_DIR = os.path.join(BASE_DIR, 'validation')

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25

def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid') # Binary classification: Cancer (1) or Non-Cancer (0)
    ])
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    print("Preparing data generators...")
    # Data augmentation for training to prevent overfitting
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Validation data should only be rescaled
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    print("Building model...")
    model = build_model()
    model.summary()

    # Callbacks
    checkpoint = ModelCheckpoint(
        'oral_cancer_model.h5', 
        monitor='val_accuracy', 
        save_best_only=True, 
        mode='max', 
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True
    )

    print("Starting training...")
    history = model.fit(
       train_generator,
       epochs=EPOCHS,
       validation_data=val_generator,
       callbacks=[checkpoint, early_stop]
    )
    print("Training finished! Model saved as oral_cancer_model.h5")

if __name__ == '__main__':
    # Remove the comment below to train!
    main()
    print("Please organize your 6000 images in the 'dataset' folder first, then run main()")
