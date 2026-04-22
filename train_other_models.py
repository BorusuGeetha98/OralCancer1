import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.applications import DenseNet169
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Directory configuration for dataset
BASE_DIR = 'dataset'
TRAIN_DIR = os.path.join(BASE_DIR, 'train')
VAL_DIR = os.path.join(BASE_DIR, 'validation')

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

def get_data_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='binary'
    )
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='binary'
    )
    return train_generator, val_generator

def build_densenet_model():
    print(f"\n--- Building DenseNet-164 (using DenseNet169 proxy) ---")
    base_model = DenseNet169(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def build_lenet_model():
    print("\n--- Building LeNet-5 Model ---")
    model = Sequential([
        Conv2D(6, kernel_size=(5, 5), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(16, kernel_size=(5, 5), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(120, activation='relu'),
        Dense(84, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_and_evaluate(model, model_name, train_gen, val_gen):
    print(f"\n--- Training {model_name} ---")
    
    checkpoint = ModelCheckpoint(f'oral_cancer_{model_name.lower()}.h5', 
                                 monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    
    history = model.fit(
        train_gen,
        steps_per_epoch=max(1, train_gen.samples // BATCH_SIZE),
        epochs=EPOCHS,
        validation_data=val_gen,
        validation_steps=max(1, val_gen.samples // BATCH_SIZE),
        callbacks=[checkpoint, early_stop]
    )
    
    print(f"Finished training {model_name}. Model saved as oral_cancer_{model_name.lower()}.h5")
    return history

def main():
    print("Preparing generators...")
    train_gen, val_gen = get_data_generators()
    
    results = {}
    
    # Train DenseNet
    densenet_model = build_densenet_model()
    history_mdl = train_and_evaluate(densenet_model, 'DenseNet164', train_gen, val_gen)
    results['DenseNet164'] = max(history_mdl.history['val_accuracy'])
    
    # Train LeNet
    lenet_model = build_lenet_model()
    history_lenet = train_and_evaluate(lenet_model, 'LeNet5', train_gen, val_gen)
    results['LeNet5'] = max(history_lenet.history['val_accuracy'])
        
    print("\n\n=== FINAL MODEL COMPARISON ===")
    for name, acc in results.items():
        print(f"{name} Max Validation Accuracy: {acc*100:.2f}%")
        
if __name__ == '__main__':
    main()
