"""Feature extraction utilities."""

import numpy as np
import pandas as pd
from typing import Dict, List


class FeatureExtractor:
    """Extract features from cryptographic data."""
    
    def __init__(self):
        """Initialize feature extractor."""
        self.features = {}
    
    def extract_basic_features(self, block_size: int, key_size: int) -> Dict[str, float]:
        """Extract basic cryptographic features."""
        return {
            'block_size': block_size,
            'key_size': key_size,
            'key_to_block_ratio': key_size / max(block_size, 1)
        }
    
    def extract_from_dataframe(self, df: pd.DataFrame, feature_cols: List[str] = None) -> pd.DataFrame:
        """Extract features from DataFrame."""
        if feature_cols is None:
            feature_cols = ['block_size', 'key_size']
        return df[feature_cols].copy()


def get_feature_names() -> List[str]:
    """Get list of feature names."""
    return ['block_size', 'key_size', 'key_to_block_ratio']
