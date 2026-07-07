"""Feature extraction utilities."""

import numpy as np
import pandas as pd
from typing import Dict, List


class FeatureExtractor:
    """Extract features from cryptographic data."""
    
    def __init__(self):
        """Initialize feature extractor."""
        self.features = {}
    
    def extract_basic_features(
        self,
        block_size: int,
        key_size: int
    ) -> Dict[str, float]:
        """Extract basic cryptographic features.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
        
        Returns:
            Dictionary of extracted features
        """
        return {
            'block_size': block_size,
            'key_size': key_size,
            'key_to_block_ratio': key_size / max(block_size, 1)
        }
    
    def extract_ciphertext_features(self, ciphertext: str) -> Dict[str, float]:
        """Extract features from ciphertext.
        
        Args:
            ciphertext: Hex or binary ciphertext string
        
        Returns:
            Dictionary of ciphertext features
        """
        # Convert hex to bytes if needed
        try:
            if ciphertext.startswith('0x'):
                cipher_bytes = bytes.fromhex(ciphertext[2:])
            else:
                cipher_bytes = ciphertext.encode()
        except:
            cipher_bytes = ciphertext.encode()
        
        # Calculate entropy
        byte_counts = np.bincount(np.frombuffer(cipher_bytes, dtype=np.uint8), minlength=256)
        entropy = -np.sum((byte_counts / len(cipher_bytes)) * np.log2(byte_counts / len(cipher_bytes) + 1e-10))
        
        # Byte frequency distribution
        byte_freq = byte_counts / len(cipher_bytes)
        
        return {
            'entropy': entropy,
            'ciphertext_length': len(cipher_bytes),
            'avg_byte_frequency': np.mean(byte_freq),
            'max_byte_frequency': np.max(byte_freq),
            'min_byte_frequency': np.min(byte_freq)
        }
    
    def extract_all_features(
        self,
        block_size: int,
        key_size: int,
        ciphertext: str = None
    ) -> Dict[str, float]:
        """Extract all available features.
        
        Args:
            block_size: Size of cipher block in bits
            key_size: Size of encryption key in bits
            ciphertext: Optional ciphertext for additional features
        
        Returns:
            Dictionary of all extracted features
        """
        features = self.extract_basic_features(block_size, key_size)
        
        if ciphertext:
            features.update(self.extract_ciphertext_features(ciphertext))
        
        return features
    
    def extract_from_dataframe(
        self,
        df: pd.DataFrame,
        feature_cols: List[str] = None
    ) -> pd.DataFrame:
        """Extract features from DataFrame.
        
        Args:
            df: Input DataFrame with algorithm data
            feature_cols: List of column names to use as features
        
        Returns:
            DataFrame with extracted features
        """
        if feature_cols is None:
            feature_cols = ['block_size', 'key_size']
        
        return df[feature_cols].copy()


def get_feature_names(include_ciphertext: bool = False) -> List[str]:
    """Get list of feature names.
    
    Args:
        include_ciphertext: Whether to include ciphertext features
    
    Returns:
        List of feature names
    """
    features = ['block_size', 'key_size', 'key_to_block_ratio']
    
    if include_ciphertext:
        features.extend([
            'entropy',
            'ciphertext_length',
            'avg_byte_frequency',
            'max_byte_frequency',
            'min_byte_frequency'
        ])
    
    return features
