"""Model training utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os


class ModelTrainer:
    """Train and manage cryptographic algorithm identification models."""
    
    def __init__(self, model_dir: str = 'models'):
        """Initialize model trainer.
        
        Args:
            model_dir: Directory to save trained models
        """
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
        """Train Random Forest classifier.
        
        Args:
            X_train: Training features
            y_train: Training targets
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            random_state: Random seed
        
        Returns:
            Trained RandomForestClassifier
        """
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        self.models['random_forest'] = model
        return model
    
    def train_svm(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        kernel: str = 'rbf',
        C: float = 1.0,
        random_state: int = 42
    ) -> SVC:
        """Train SVM classifier.
        
        Args:
            X_train: Training features
            y_train: Training targets
            kernel: SVM kernel type
            C: Regularization parameter
            random_state: Random seed
        
        Returns:
            Trained SVC model
        """
        model = SVC(kernel=kernel, C=C, random_state=random_state, probability=True)
        model.fit(X_train, y_train)
        self.models['svm'] = model
        return model
    
    def train_neural_network(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        hidden_layers: Tuple[int, ...] = (64, 32),
        max_iter: int = 1000,
        random_state: int = 42
    ) -> MLPClassifier:
        """Train Neural Network classifier.
        
        Args:
            X_train: Training features
            y_train: Training targets
            hidden_layers: Hidden layer sizes
            max_iter: Maximum iterations
            random_state: Random seed
        
        Returns:
            Trained MLPClassifier model
        """
        model = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            max_iter=max_iter,
            random_state=random_state,
            early_stopping=True
        )
        model.fit(X_train, y_train)
        self.models['neural_network'] = model
        return model
    
    def evaluate(
        self,
        model,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict:
        """Evaluate model performance.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test targets
        
        Returns:
            Dictionary with evaluation metrics
        """
        y_pred = model.predict(X_test)
        
        return {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'predictions': y_pred
        }
    
    def save_model(self, model, model_name: str) -> str:
        """Save trained model to disk.
        
        Args:
            model: Trained model to save
            model_name: Name for the model
        
        Returns:
            Path to saved model
        """
        filepath = os.path.join(self.model_dir, f'{model_name}.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        return filepath
    
    def load_model(self, model_name: str):
        """Load model from disk.
        
        Args:
            model_name: Name of the model
        
        Returns:
            Loaded model
        
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        filepath = os.path.join(self.model_dir, f'{model_name}.pkl')
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        return model
    
    def train_ensemble(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ) -> Dict:
        """Train all models for ensemble.
        
        Args:
            X_train: Training features
            y_train: Training targets
        
        Returns:
            Dictionary of trained models
        """
        models = {
            'random_forest': self.train_random_forest(X_train, y_train),
            'svm': self.train_svm(X_train, y_train),
            'neural_network': self.train_neural_network(X_train, y_train)
        }
        return models


def evaluate_models(
    models: Dict,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict:
    """Evaluate multiple models.
    
    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test targets
    
    Returns:
        Dictionary of evaluation results for each model
    """
    results = {}
    trainer = ModelTrainer()
    
    for model_name, model in models.items():
        results[model_name] = trainer.evaluate(model, X_test, y_test)
    
    return results
