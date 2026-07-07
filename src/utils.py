"""Utility functions."""

import json
from typing import Dict, Any


def save_results(results: Dict, filepath: str) -> None:
    """Save results to JSON file.
    
    Args:
        results: Results dictionary
        filepath: Path to save JSON file
    """
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)


def load_results(filepath: str) -> Dict:
    """Load results from JSON file.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Results dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def format_metrics(metrics: Dict) -> str:
    """Format evaluation metrics for display.
    
    Args:
        metrics: Dictionary with evaluation metrics
    
    Returns:
        Formatted string
    """
    output = []
    output.append(f"Accuracy: {metrics['accuracy']:.4f}")
    output.append(f"\n{metrics['classification_report']}")
    return '\n'.join(output)


def get_algorithm_info(algorithm: str) -> Dict[str, Any]:
    """Get information about a cryptographic algorithm.
    
    Args:
        algorithm: Algorithm name
    
    Returns:
        Dictionary with algorithm information
    """
    algorithms = {
        'AES': {
            'name': 'Advanced Encryption Standard',
            'type': 'Symmetric',
            'block_size': [128],
            'key_size': [128, 192, 256],
            'standard': 'NIST FIPS 197',
            'year': 2001
        },
        'RSA': {
            'name': 'Rivest-Shamir-Adleman',
            'type': 'Asymmetric',
            'block_size': [2048, 3072, 4096],
            'key_size': [2048, 3072, 4096],
            'standard': 'PKCS #1',
            'year': 1978
        },
        'DES': {
            'name': 'Data Encryption Standard',
            'type': 'Symmetric',
            'block_size': [64],
            'key_size': [56],
            'standard': 'NIST FIPS 46',
            'year': 1977
        },
        '3DES': {
            'name': 'Triple DES',
            'type': 'Symmetric',
            'block_size': [64],
            'key_size': [168, 192],
            'standard': 'NIST FIPS 46-3',
            'year': 1998
        },
        'Blowfish': {
            'name': 'Blowfish',
            'type': 'Symmetric',
            'block_size': [64],
            'key_size': [32, 448],
            'standard': 'Proprietary',
            'year': 1993
        }
    }
    
    return algorithms.get(algorithm, {})
