"""Utility functions."""

def get_algorithm_info(algorithm: str) -> Dict:
    """Get information about a cryptographic algorithm."""
    algorithms = {
        'AES': {'name': 'Advanced Encryption Standard', 'type': 'Symmetric', 'year': 2001},
        'RSA': {'name': 'Rivest-Shamir-Adleman', 'type': 'Asymmetric', 'year': 1978},
        'DES': {'name': 'Data Encryption Standard', 'type': 'Symmetric', 'year': 1977},
    }
    return algorithms.get(algorithm, {})
