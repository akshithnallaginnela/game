"""Prediction utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union
import warnings


class Predictor:
    """Make predictions using trained models."""
    
    def __init__(self, model, class_labels: Optional[list] = None):
        """Initialize predictor.
        
        Args:
            model: Trained classification model
            class_labels: List of algorithm class labels
        """
        self.model = model
        self.class_labels = class_labels
    
    def predict(
        self,
        block_size: int,
        key_size: int,
        return_confidence: bool = True
    ) -> Dict:
        """Predict algorithm from parameters.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
            return_confidence: Whether to return prediction confidence
        
        Returns:
            Dictionary with prediction and optionally confidence
        """
        X = pd.DataFrame({'block_size': [block_size], 'key_size': [key_size]})
        
        prediction = self.model.predict(X)[0]
        result = {'algorithm': str(prediction)}
        
        if return_confidence and hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(X)[0]
            result['confidence'] = float(np.max(proba))
            result['probabilities'] = {
                str(label): float(prob) 
                for label, prob in zip(self.model.classes_, proba)
            }
        
        return result
    
    def predict_batch(
        self,
        data: pd.DataFrame,
        return_confidence: bool = True
    ) -> pd.DataFrame:
        """Make batch predictions.
        
        Args:
            data: DataFrame with 'block_size' and 'key_size' columns
            return_confidence: Whether to include confidence scores
        
        Returns:
            DataFrame with predictions
        """
        if not all(col in data.columns for col in ['block_size', 'key_size']):
            raise ValueError("DataFrame must contain 'block_size' and 'key_size' columns")
        
        X = data[['block_size', 'key_size']]
        predictions = self.model.predict(X)
        
        result = data.copy()
        result['predicted_algorithm'] = predictions
        
        if return_confidence and hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)
            result['confidence'] = np.max(probas, axis=1)
        
        return result
    
    def predict_with_explanation(
        self,
        block_size: int,
        key_size: int
    ) -> Dict:
        """Predict with explanation.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
        
        Returns:
            Dictionary with prediction and explanation
        """
        prediction = self.predict(block_size, key_size, return_confidence=True)
        
        explanation = self._generate_explanation(block_size, key_size)
        prediction['explanation'] = explanation
        
        return prediction
    
    def _generate_explanation(self, block_size: int, key_size: int) -> str:
        """Generate explanation for prediction.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
        
        Returns:
            Explanation string
        """
        explanations = {
            'AES': "Advanced Encryption Standard (AES) detected. Block size: 128 bits, Key size: 128/192/256 bits.",
            'RSA': "RSA asymmetric encryption detected. Large key sizes (2048+ bits).",
            'DES': "Data Encryption Standard (DES) detected. Block size: 64 bits, Key size: 56 bits.",
            '3DES': "Triple DES detected. Block size: 64 bits, Key size: 168 bits.",
            'Blowfish': "Blowfish encryption detected. Block size: 64 bits, Key size: 32-448 bits."
        }
        
        if block_size == 128 and key_size in [128, 192, 256]:
            return explanations.get('AES', "Unknown algorithm")
        elif block_size >= 2048:
            return explanations.get('RSA', "Unknown algorithm")
        elif block_size == 64 and key_size == 56:
            return explanations.get('DES', "Unknown algorithm")
        elif block_size == 64 and key_size == 168:
            return explanations.get('3DES', "Unknown algorithm")
        elif block_size == 64 and 32 <= key_size <= 448:
            return explanations.get('Blowfish', "Unknown algorithm")
        
        return "Unable to determine algorithm from given parameters"
    
    def evaluate_prediction(
        self,
        block_size: int,
        key_size: int,
        actual_algorithm: str
    ) -> Dict:
        """Evaluate a single prediction against actual value.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
            actual_algorithm: True algorithm name
        
        Returns:
            Dictionary with evaluation results
        """
        prediction_result = self.predict(block_size, key_size, return_confidence=True)
        
        is_correct = prediction_result['algorithm'] == actual_algorithm
        
        return {
            'predicted': prediction_result['algorithm'],
            'actual': actual_algorithm,
            'correct': is_correct,
            'confidence': prediction_result.get('confidence', None)
        }


class EnsemblePredictor:
    """Make predictions using ensemble of models."""
    
    def __init__(self, models: Dict):
        """Initialize ensemble predictor.
        
        Args:
            models: Dictionary of trained models
        """
        self.models = models
        self.predictors = {
            name: Predictor(model) 
            for name, model in models.items()
        }
    
    def predict_majority_vote(
        self,
        block_size: int,
        key_size: int
    ) -> Dict:
        """Predict using majority voting.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
        
        Returns:
            Dictionary with ensemble prediction
        """
        predictions = []
        
        for model_name, predictor in self.predictors.items():
            pred = predictor.predict(block_size, key_size, return_confidence=False)
            predictions.append(pred['algorithm'])
        
        from collections import Counter
        vote_counts = Counter(predictions)
        majority_pred = vote_counts.most_common(1)[0][0]
        
        return {
            'algorithm': majority_pred,
            'votes': dict(vote_counts),
            'model_predictions': {
                name: pred['algorithm']
                for name, pred in zip(self.predictors.keys(),
                                      [self.predictors[n].predict(block_size, key_size, False) for n in self.predictors])
            }
        }
    
    def predict_weighted_average(
        self,
        block_size: int,
        key_size: int,
        weights: Optional[Dict] = None
    ) -> Dict:
        """Predict using weighted average of probabilities.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
            weights: Dictionary of model weights (must sum to 1)
        
        Returns:
            Dictionary with ensemble prediction
        """
        if weights is None:
            weights = {name: 1/len(self.models) for name in self.models.keys()}
        
        # Validate weights
        if not isinstance(weights, dict) or abs(sum(weights.values()) - 1.0) > 1e-6:
            raise ValueError("Weights must be a dictionary summing to 1.0")
        
        weighted_probs = {}
        
        for model_name, predictor in self.predictors.items():
            pred_result = predictor.predict(block_size, key_size, return_confidence=True)
            probs = pred_result.get('probabilities', {})
            
            for algorithm, prob in probs.items():
                weighted_probs[algorithm] = weighted_probs.get(algorithm, 0) + weights[model_name] * prob
        
        best_algorithm = max(weighted_probs, key=weighted_probs.get)
        
        return {
            'algorithm': best_algorithm,
            'confidence': weighted_probs[best_algorithm],
            'probabilities': weighted_probs
        }
