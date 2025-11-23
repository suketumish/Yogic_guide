"""
Yoga Pose Image Classification Model Training
Uses Transfer Learning with MobileNetV2 for efficient, accurate pose detection
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import json

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_PHASE1 = 15  # Feature extraction
EPOCHS_PHASE2 = 30  # Fine-tuning
LEARNING_RATE_PHASE1 = 1e-3
LEARNING_RATE_PHASE2 = 1e-5
DATA_DIR = 'data'

class YogaImageClassifier:
    def __init__(self, num_classes, img_size=224):
        self.num_classes = num_classes
        self.img_size = img_size
        self.model = None
        self.history = {'phase1': None, 'phase2': None}
        self.class_names = None
        
    def create_data_generators(self):
        """Create augmented data generators for training"""
        # Training data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest'
        )
        
        # Validation/Test: only rescaling
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Load datasets
        train_generator = train_datagen.flow_from_directory(
            os.path.join(DATA_DIR, 'train'),
            target_size=(self.img_size, self.img_size),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        val_generator = val_datagen.flow_from_directory(
            os.path.join(DATA_DIR, 'validate'),
            target_size=(self.img_size, self.img_size),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        test_generator = val_datagen.flow_from_directory(
            os.path.join(DATA_DIR, 'test'),
            target_size=(self.img_size, self.img_size),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )
        
        self.class_names = list(train_generator.class_indices.keys())
        print(f"Classes found: {self.class_names}")
        
        return train_generator, val_generator, test_generator
    
    def build_model(self):
        """Build transfer learning model with MobileNetV2"""
        # Load pretrained base model
        base_model = MobileNetV2(
            input_shape=(self.img_size, self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model for phase 1
        base_model.trainable = False
        
        # Build classification head
        inputs = keras.Input(shape=(self.img_size, self.img_size, 3))
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        print("Model architecture created")
        return self.model
    
    def train_phase1(self, train_gen, val_gen):
        """Phase 1: Train only the classification head"""
        print("\n=== PHASE 1: Feature Extraction ===")
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE_PHASE1),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top3_acc')]
        )
        
        callbacks = [
            ModelCheckpoint('models/yoga_model_phase1.h5', save_best_only=True, monitor='val_accuracy'),
            EarlyStopping(patience=5, restore_best_weights=True, monitor='val_accuracy'),
            ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-6, monitor='val_loss')
        ]
        
        history = self.model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS_PHASE1,
            callbacks=callbacks
        )
        
        self.history['phase1'] = history.history
        return history
    
    def train_phase2(self, train_gen, val_gen):
        """Phase 2: Fine-tune the base model"""
        print("\n=== PHASE 2: Fine-Tuning ===")
        
        # Unfreeze the base model
        base_model = self.model.layers[1]
        base_model.trainable = True
        
        # Freeze early layers, fine-tune later layers
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE_PHASE2),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top3_acc')]
        )
        
        callbacks = [
            ModelCheckpoint('models/yoga_model_final.h5', save_best_only=True, monitor='val_accuracy'),
            EarlyStopping(patience=8, restore_best_weights=True, monitor='val_accuracy'),
            ReduceLROnPlateau(factor=0.5, patience=4, min_lr=1e-7, monitor='val_loss')
        ]
        
        history = self.model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS_PHASE2,
            callbacks=callbacks
        )
        
        self.history['phase2'] = history.history
        return history
    
    def evaluate(self, test_gen):
        """Evaluate model on test set"""
        print("\n=== Evaluation on Test Set ===")
        
        # Get predictions
        test_gen.reset()
        predictions = self.model.predict(test_gen)
        y_pred = np.argmax(predictions, axis=1)
        y_true = test_gen.classes
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, target_names=self.class_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('models/confusion_matrix.png')
        print("Confusion matrix saved to models/confusion_matrix.png")
        
        # Calculate per-class accuracy
        class_accuracy = cm.diagonal() / cm.sum(axis=1)
        for i, acc in enumerate(class_accuracy):
            print(f"{self.class_names[i]}: {acc:.3f}")
        
        return predictions, y_true, y_pred
    
    def plot_training_history(self):
        """Plot training curves"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Phase 1
        if self.history['phase1']:
            axes[0, 0].plot(self.history['phase1']['accuracy'], label='Train')
            axes[0, 0].plot(self.history['phase1']['val_accuracy'], label='Val')
            axes[0, 0].set_title('Phase 1: Accuracy')
            axes[0, 0].legend()
            
            axes[0, 1].plot(self.history['phase1']['loss'], label='Train')
            axes[0, 1].plot(self.history['phase1']['val_loss'], label='Val')
            axes[0, 1].set_title('Phase 1: Loss')
            axes[0, 1].legend()
        
        # Phase 2
        if self.history['phase2']:
            axes[1, 0].plot(self.history['phase2']['accuracy'], label='Train')
            axes[1, 0].plot(self.history['phase2']['val_accuracy'], label='Val')
            axes[1, 0].set_title('Phase 2: Accuracy')
            axes[1, 0].legend()
            
            axes[1, 1].plot(self.history['phase2']['loss'], label='Train')
            axes[1, 1].plot(self.history['phase2']['val_loss'], label='Val')
            axes[1, 1].set_title('Phase 2: Loss')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig('models/training_history.png')
        print("Training history saved to models/training_history.png")
    
    def convert_to_tflite(self, output_path='models/yoga_model.tflite'):
        """Convert model to TFLite for mobile deployment"""
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        print(f"TFLite model saved to {output_path}")
        
        # Save class names
        with open('models/class_names.json', 'w') as f:
            json.dump(self.class_names, f)
    
    def save_model_info(self):
        """Save model metadata"""
        info = {
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'img_size': self.img_size,
            'architecture': 'MobileNetV2',
            'phase1_epochs': EPOCHS_PHASE1,
            'phase2_epochs': EPOCHS_PHASE2
        }
        
        with open('models/model_info.json', 'w') as f:
            json.dump(info, f, indent=2)


def main():
    """Main training pipeline"""
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Initialize classifier
    classifier = YogaImageClassifier(num_classes=12)  # Adjust based on your dataset
    
    # Create data generators
    train_gen, val_gen, test_gen = classifier.create_data_generators()
    
    # Update num_classes based on actual data
    classifier.num_classes = len(classifier.class_names)
    
    # Build model
    classifier.build_model()
    print(classifier.model.summary())
    
    # Phase 1: Feature extraction
    classifier.train_phase1(train_gen, val_gen)
    
    # Phase 2: Fine-tuning
    classifier.train_phase2(train_gen, val_gen)
    
    # Evaluate
    classifier.evaluate(test_gen)
    
    # Plot training history
    classifier.plot_training_history()
    
    # Convert to TFLite
    classifier.convert_to_tflite()
    
    # Save metadata
    classifier.save_model_info()
    
    print("\n✅ Training complete! Models saved in 'models/' directory")


if __name__ == '__main__':
    main()
