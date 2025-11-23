"""
Keypoint-based Yoga Pose Classifier
Trains an MLP classifier on extracted pose keypoints and angles
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

class KeypointClassifier:
    def __init__(self, model_type='mlp'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = None
        
    def load_data(self, csv_path='keypoints_dataset.csv'):
        """Load keypoint dataset"""
        df = pd.read_csv(csv_path)
        
        # Separate features and labels
        exclude_cols = ['image_path', 'split', 'label']
        self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        X = df[self.feature_columns].values
        y = df['label'].values
        splits = df['split'].values
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split by existing train/val/test
        X_train = X[splits == 'train']
        y_train = y_encoded[splits == 'train']
        
        X_val = X[splits == 'validate']
        y_val = y_encoded[splits == 'validate']
        
        X_test = X[splits == 'test']
        y_test = y_encoded[splits == 'test']
        
        print(f"Train samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        print(f"Test samples: {len(X_test)}")
        print(f"Features: {len(self.feature_columns)}")
        print(f"Classes: {len(self.label_encoder.classes_)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def build_mlp(self, input_dim, num_classes):
        """Build Multi-Layer Perceptron classifier"""
        model = MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            alpha=0.0001,
            batch_size=32,
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            verbose=True,
            random_state=42
        )
        return model
    
    def build_svm(self):
        """Build SVM classifier"""
        model = SVC(
            kernel='rbf',
            C=10.0,
            gamma='scale',
            probability=True,
            verbose=True,
            random_state=42
        )
        return model
    
    def train(self, X_train, y_train, X_val, y_val):
        """Train the keypoint classifier"""
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Build model
        if self.model_type == 'mlp':
            self.model = self.build_mlp(X_train.shape[1], len(self.label_encoder.classes_))
        elif self.model_type == 'svm':
            self.model = self.build_svm()
        
        print(f"\nTraining {self.model_type.upper()} classifier...")
        
        # Train
        self.model.fit(X_train_scaled, y_train)
        
        # Validation accuracy
        val_pred = self.model.predict(X_val_scaled)
        val_acc = accuracy_score(y_val, val_pred)
        print(f"Validation Accuracy: {val_acc:.4f}")
        
        return self.model
    
    def evaluate(self, X_test, y_test):
        """Evaluate on test set"""
        X_test_scaled = self.scaler.transform(X_test)
        y_pred = self.model.predict(X_test_scaled)
        
        print("\n=== Test Set Evaluation ===")
        print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred, 
            target_names=self.label_encoder.classes_
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=self.label_encoder.classes_,
            yticklabels=self.label_encoder.classes_
        )
        plt.title('Keypoint Model Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('models/keypoint_confusion_matrix.png')
        print("Confusion matrix saved")
        
        return y_pred
    
    def predict_with_confidence(self, X):
        """Predict with confidence scores"""
        X_scaled = self.scaler.transform(X)
        
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(X_scaled)
            pred_class = np.argmax(proba, axis=1)
            confidence = np.max(proba, axis=1)
        else:
            pred_class = self.model.predict(X_scaled)
            confidence = np.ones(len(pred_class))
        
        pred_labels = self.label_encoder.inverse_transform(pred_class)
        
        return pred_labels, confidence
    
    def save_model(self, prefix='keypoint'):
        """Save trained model and preprocessing objects"""
        joblib.dump(self.model, f'models/{prefix}_classifier.pkl')
        joblib.dump(self.scaler, f'models/{prefix}_scaler.pkl')
        joblib.dump(self.label_encoder, f'models/{prefix}_label_encoder.pkl')
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'num_features': len(self.feature_columns),
            'feature_columns': self.feature_columns,
            'classes': self.label_encoder.classes_.tolist()
        }
        
        with open(f'models/{prefix}_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Model saved to models/{prefix}_*.pkl")
    
    def load_model(self, prefix='keypoint'):
        """Load trained model"""
        self.model = joblib.load(f'models/{prefix}_classifier.pkl')
        self.scaler = joblib.load(f'models/{prefix}_scaler.pkl')
        self.label_encoder = joblib.load(f'models/{prefix}_label_encoder.pkl')
        
        with open(f'models/{prefix}_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        self.feature_columns = metadata['feature_columns']
        self.model_type = metadata['model_type']
        
        print(f"Model loaded: {self.model_type}")


def main():
    """Main training pipeline"""
    # Train MLP classifier
    print("=" * 50)
    print("Training MLP Classifier")
    print("=" * 50)
    
    mlp_classifier = KeypointClassifier(model_type='mlp')
    X_train, X_val, X_test, y_train, y_val, y_test = mlp_classifier.load_data()
    mlp_classifier.train(X_train, y_train, X_val, y_val)
    mlp_classifier.evaluate(X_test, y_test)
    mlp_classifier.save_model(prefix='keypoint_mlp')
    
    print("\n✅ Keypoint classifier training complete!")


if __name__ == '__main__':
    main()
