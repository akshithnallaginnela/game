"""Data loading and preprocessing utilities."""

import pandas as pd
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split


class DataLoader:
    """Load and preprocess cryptographic algorithm data."""
    
    def __init__(self, filepath: str):
        """Initialize data loader."""
        self.filepath = filepath
        self.df = None
    
    def load(self) -> pd.DataFrame:
        """Load data from CSV file."""
        self.df = pd.read_csv(self.filepath)
        return self.df
    
    def preprocess(self) -> pd.DataFrame:
        """Preprocess data for model training."""
        if self.df is None:
            self.load()
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna()
        return self.df
    
    def get_features_and_target(
        self, 
        feature_cols: Optional[list] = None,
        target_col: str = 'algorithm'
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Extract features and target variable."""
        if self.df is None:
            self.load()
        
        if feature_cols is None:
            feature_cols = ['block_size', 'key_size']
        
        X = self.df[feature_cols]
        y = self.df[target_col]
        return X, y
    
    def split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split data into training and testing sets."""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def get_statistics(self) -> dict:
        """Get dataset statistics."""
        if self.df is None:
            self.load()
        return {
            'total_records': len(self.df),
            'algorithms': self.df['algorithm'].unique().tolist(),
            'shape': self.df.shape
        }
