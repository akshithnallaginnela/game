"""Prediction utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class Predictor:
    """Make predictions using trained models."""
    
    def __init__(self, model):
        """Initialize predictor."""
        self.model = model
    
    def predict(self, block_size: int, key_size: int, return_confidence: bool = True) -> Dict:
        """Predict algorithm from parameters."""
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
    
    def predict_batch(self, data: pd.DataFrame, return_confidence: bool = True) -> pd.DataFrame:
        """Make batch predictions."""
        X = data[['block_size', 'key_size']]
        predictions = self.model.predict(X)
        
        result = data.copy()
        result['predicted_algorithm'] = predictions
        
        if return_confidence and hasattr(self.model, 'predict_proba'):
            probas = self.model.predict_proba(X)
            result['confidence'] = np.max(probas, axis=1)
        
        return result


class EnsemblePredictor:
    """Make predictions using ensemble of models."""
    
    def __init__(self, models: Dict):
        """Initialize ensemble predictor."""
        self.models = models
        self.predictors = {name: Predictor(model) for name, model in models.items()}
    
    def predict_majority_vote(self, block_size: int, key_size: int) -> Dict:
        """Predict using majority voting."""
        predictions = [
            predictor.predict(block_size, key_size, return_confidence=False)['algorithm']
            for predictor in self.predictors.values()
        ]
        
        from collections import Counter
        vote_counts = Counter(predictions)
        majority_pred = vote_counts.most_common(1)[0][0]
        
        return {
            'algorithm': majority_pred,
            'votes': dict(vote_counts),
        }
