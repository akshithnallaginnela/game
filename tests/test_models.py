"""Unit tests for CryptoDetect modules."""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.feature_extractor import FeatureExtractor
from src.model_trainer import ModelTrainer
from src.predictor import Predictor


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'block_size': [128, 256, 128, 2048],
        'key_size': [128, 256, 128, 2048],
        'algorithm': ['AES', 'AES', 'AES', 'RSA']
    })


@pytest.fixture
def sample_csv(tmp_path, sample_data):
    """Create temporary CSV file for testing."""
    filepath = tmp_path / "test_data.csv"
    sample_data.to_csv(filepath, index=False)
    return str(filepath)


class TestDataLoader:
    """Test DataLoader class."""
    
    def test_load_data(self, sample_csv):
        """Test data loading."""
        loader = DataLoader(sample_csv)
        df = loader.load()
        assert len(df) == 4
        assert 'algorithm' in df.columns
    
    def test_get_statistics(self, sample_csv):
        """Test dataset statistics."""
        loader = DataLoader(sample_csv)
        loader.load()
        stats = loader.get_statistics()
        assert stats['total_records'] == 4
        assert 'AES' in stats['algorithms']
        assert 'RSA' in stats['algorithms']


class TestFeatureExtractor:
    """Test FeatureExtractor class."""
    
    def test_extract_basic_features(self):
        """Test basic feature extraction."""
        extractor = FeatureExtractor()
        features = extractor.extract_basic_features(128, 128)
        assert features['block_size'] == 128
        assert features['key_size'] == 128
        assert 'key_to_block_ratio' in features
    
    def test_extract_ciphertext_features(self):
        """Test ciphertext feature extraction."""
        extractor = FeatureExtractor()
        ciphertext = '0x6d251e0e0e0e0e0e0e0e0e0e0e0e'
        features = extractor.extract_ciphertext_features(ciphertext)
        assert 'entropy' in features
        assert 'ciphertext_length' in features


class TestModelTrainer:
    """Test ModelTrainer class."""
    
    def test_train_random_forest(self, sample_data):
        """Test Random Forest training."""
        trainer = ModelTrainer()
        X = sample_data[['block_size', 'key_size']]
        y = sample_data['algorithm']
        
        model = trainer.train_random_forest(X, y, n_estimators=10)
        assert model is not None
        assert hasattr(model, 'predict')
    
    def test_evaluate(self, sample_data):
        """Test model evaluation."""
        trainer = ModelTrainer()
        X = sample_data[['block_size', 'key_size']]
        y = sample_data['algorithm']
        
        model = trainer.train_random_forest(X, y, n_estimators=10)
        results = trainer.evaluate(model, X, y)
        
        assert 'accuracy' in results
        assert 'classification_report' in results
        assert 'confusion_matrix' in results


class TestPredictor:
    """Test Predictor class."""
    
    def test_predict(self, sample_data):
        """Test prediction."""
        from sklearn.ensemble import RandomForestClassifier
        
        X = sample_data[['block_size', 'key_size']]
        y = sample_data['algorithm']
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        predictor = Predictor(model)
        result = predictor.predict(128, 128)
        
        assert 'algorithm' in result
        assert result['algorithm'] in y.unique()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
