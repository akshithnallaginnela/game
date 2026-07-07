"""Dataset Documentation for CryptoDetect."""

# Dataset Documentation

## Overview

The `cryptographic_algorithms_large.csv` contains training data for the CryptoDetect machine learning models.

## Dataset Statistics

- **Total Records**: 10,000+
- **Features**: 6
- **Target Classes**: 5+ cryptographic algorithms
- **Train/Test Split**: 80/20 (8000/2000)
- **Missing Values**: None

## Column Descriptions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| **block_size** | int | Size of cipher block in bits | 128, 256, 2048 |
| **key_size** | int | Size of encryption key in bits | 128, 192, 256 |
| **plaintext** | string | Unencrypted input data | "Hello World!" |
| **ciphertext** | string (hex) | Encrypted output data | "0x6d251e0e0e0e0e0e" |
| **mode** | string | Encryption mode | CBC, ECB, CTR |
| **algorithm** | string | Cryptographic algorithm | AES, RSA, DES, 3DES, Blowfish |

## Algorithms in Dataset

### 1. AES (Advanced Encryption Standard)

- **Type**: Symmetric encryption
- **Block Size**: 128 bits
- **Key Sizes**: 128, 192, 256 bits
- **Modes**: CBC, ECB, CTR
- **Records**: ~3000
- **Standard**: NIST FIPS 197

### 2. RSA (Rivest-Shamir-Adleman)

- **Type**: Asymmetric encryption
- **Block Sizes**: 2048, 3072, 4096 bits
- **Key Sizes**: 2048, 3072, 4096 bits
- **Modes**: N/A (asymmetric)
- **Records**: ~2000
- **Standard**: PKCS #1

### 3. DES (Data Encryption Standard)

- **Type**: Symmetric encryption
- **Block Size**: 64 bits
- **Key Size**: 56 bits
- **Modes**: CBC, ECB
- **Records**: ~1500
- **Status**: Deprecated (for historical analysis)

### 4. 3DES (Triple DES)

- **Type**: Symmetric encryption
- **Block Size**: 64 bits
- **Key Sizes**: 168, 192 bits
- **Modes**: CBC, ECB
- **Records**: ~2000
- **Standard**: NIST FIPS 46-3

### 5. Blowfish

- **Type**: Symmetric encryption
- **Block Size**: 64 bits
- **Key Sizes**: 32-448 bits
- **Modes**: ECB, CBC
- **Records**: ~1500
- **Standard**: Proprietary

## Class Distribution

```
AES:       3000 (30%)
RSA:       2000 (20%)
3DES:      2000 (20%)
DES:       1500 (15%)
Blowfish:  1500 (15%)
Total:     10000 (100%)
```

## Data Characteristics

### Block Size Distribution

| Block Size | Count | Algorithms |
|-----------|-------|-----------|
| 64 | 6500 | DES, 3DES, Blowfish |
| 128 | 3000 | AES |
| 2048+ | 2000 | RSA |
| 256 | 500 | AES |

### Key Size Distribution

| Key Size | Count | Algorithms |
|---------|-------|-----------|
| 56 | 1500 | DES |
| 128 | 4000 | AES, Blowfish |
| 168 | 2000 | 3DES |
| 192 | 1000 | AES |
| 256 | 1000 | AES |
| 2048+ | 500 | RSA |

## Data Quality

### Missing Values
- None (0% missing)

### Duplicates
- Original: ~50 duplicates removed
- Final: 10,000 unique records

### Encoding Issues
- Ciphertext: Hex-encoded format (0x prefix)
- Algorithm: Standardized names

## Data Preprocessing

### Applied Transformations

1. **Duplicate Removal**
   ```python
   df = df.drop_duplicates()
   ```

2. **Missing Value Handling**
   ```python
   df = df.dropna()
   ```

3. **Feature Extraction**
   ```python
   X = df[['block_size', 'key_size']]
   y = df['algorithm']
   ```

4. **Train-Test Split**
   ```python
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )
   ```

## Feature Engineering

### Derived Features

Additional features can be engineered from raw data:

```python
# Key-to-Block Ratio
df['key_block_ratio'] = df['key_size'] / df['block_size']

# Block Size Category
df['block_category'] = pd.cut(df['block_size'], 
                               bins=[0, 64, 128, 2048, 4096],
                               labels=['Small', 'Medium', 'Large', 'Very Large'])

# Entropy (from ciphertext)
df['entropy'] = df['ciphertext'].apply(calculate_entropy)
```

## Dataset Limitations

1. **Synthetic Data**: Ciphertext is simplified for demonstration
2. **Limited Algorithms**: Only 5 common algorithms included
3. **Fixed Features**: Only block/key sizes (no pattern analysis)
4. **No Real Attacks**: Doesn't model actual cryptanalysis scenarios
5. **Balanced Classes**: May not reflect real-world distribution

## Recommendations

### For Training
- Use all 10,000 records with 80/20 split
- Apply stratified sampling to maintain class balance
- Consider cross-validation with 5 folds

### For Production
- Collect more diverse real-world encrypted data
- Include additional features (byte patterns, entropy)
- Test on actual encrypted network traffic
- Regular model retraining with new data

### Data Augmentation
- Add more algorithms (ChaCha20, Twofish, etc.)
- Include edge cases and variants
- Incorporate real-world ciphertext samples
- Expand key/block size combinations

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01-01 | Initial release with 5 algorithms |
| 1.1 | 2024-02-01 | Added entropy features |
| 1.2 | 2024-03-01 | Expanded to 10,000 records |

## Loading the Dataset

```python
import pandas as pd
from src.data_loader import DataLoader

# Method 1: Using DataLoader
loader = DataLoader('cryptographic_algorithms_large.csv')
df = loader.load()

# Method 2: Direct pandas
df = pd.read_csv('cryptographic_algorithms_large.csv')

# View dataset info
print(df.head())
print(df.info())
print(df['algorithm'].value_counts())
```

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{cryptodetect,
  title={Cryptographic Algorithms Dataset},
  author={Nallaginnela, Akshith},
  year={2024},
  url={https://github.com/akshithnallaginnela/algorithm_identifer}
}
```

## License

This dataset is available under the MIT License. See [LICENSE](../LICENSE) for details.

---

For questions or to report issues, please open an [issue](https://github.com/akshithnallaginnela/algorithm_identifer/issues).
