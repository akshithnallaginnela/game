"""Model training utilities."""

import pandas as pd
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os


class ModelTrainer:
    """Train and manage cryptographic algorithm identification models."""
    
    def __init__(self, model_dir: str = 'models'):
        """Initialize model trainer."""
        self.model_dir = model_dir
        self.models = {}
        os.makedirs(model_dir, exist_ok=True)
    
    def train_random_forest(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_estimators: int = 100,
        max_depth: int = 15,
        random_state: int = 42
    ) -> RandomForestClassifier:
        """Train Random Forest classifier."""
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        self.models['random_forest'] = model
        return model
    
    def train_svm(self, X_train: pd.DataFrame, y_train: pd.Series) -> SVC:
        """Train SVM classifier."""
        model = SVC(kernel='rbf', probability=True)
        model.fit(X_train, y_train)
        self.models['svm'] = model
        return model
    
    def train_neural_network(self, X_train: pd.DataFrame, y_train: pd.Series) -> MLPClassifier:
        """Train Neural Network classifier."""
        model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000)
        model.fit(X_train, y_train)
        self.models['neural_network'] = model
        return model
    
    def evaluate(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """Evaluate model performance."""
        y_pred = model.predict(X_test)
        return {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'predictions': y_pred
        }
    
    def save_model(self, model, model_name: str) -> str:
        """Save trained model to disk."""
        filepath = os.path.join(self.model_dir, f'{model_name}.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        return filepath
    
    def load_model(self, model_name: str):
        """Load model from disk."""
        filepath = os.path.join(self.model_dir, f'{model_name}.pkl')
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        return model
    
    def train_ensemble(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict:
        """Train all models for ensemble."""
        return {
            'random_forest': self.train_random_forest(X_train, y_train),
            'svm': self.train_svm(X_train, y_train),
            'neural_network': self.train_neural_network(X_train, y_train)
        }
