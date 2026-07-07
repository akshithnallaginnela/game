"""Data loading and preprocessing utilities."""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class DataLoader:
    """Load and preprocess cryptographic algorithm data."""
    
    def __init__(self, filepath: str):
        """Initialize data loader.
        
        Args:
            filepath: Path to CSV file containing training data
        """
        self.filepath = filepath
        self.df = None
        self.label_encoder = LabelEncoder()
    
    def load(self) -> pd.DataFrame:
        """Load data from CSV file.
        
        Returns:
            DataFrame with cryptographic algorithm data
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        try:
            self.df = pd.read_csv(self.filepath)
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")
    
    def preprocess(self) -> pd.DataFrame:
        """Preprocess data for model training.
        
        Returns:
            Cleaned and preprocessed DataFrame
        """
        if self.df is None:
            self.load()
        
        # Remove duplicates
        self.df = self.df.drop_duplicates()
        
        # Handle missing values
        self.df = self.df.dropna()
        
        return self.df
    
    def get_features_and_target(
        self, 
        feature_cols: Optional[list] = None,
        target_col: str = 'algorithm'
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Extract features and target variable.
        
        Args:
            feature_cols: List of feature column names
            target_col: Name of target column
        
        Returns:
            Tuple of (features DataFrame, target Series)
        """
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
        """Split data into training and testing sets.
        
        Args:
            X: Features DataFrame
            y: Target Series
            test_size: Proportion of test set
            random_state: Random seed for reproducibility
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def get_statistics(self) -> dict:
        """Get dataset statistics.
        
        Returns:
            Dictionary with dataset statistics
        """
        if self.df is None:
            self.load()
        
        return {
            'total_records': len(self.df),
            'num_features': len(self.df.columns),
            'algorithms': self.df['algorithm'].unique().tolist(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'shape': self.df.shape
        }


def load_data(filepath: str) -> pd.DataFrame:
    """Convenience function to load data.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        DataFrame with cryptographic algorithm data
    """
    loader = DataLoader(filepath)
    return loader.load()
