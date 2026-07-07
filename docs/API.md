"""API Documentation for CryptoDetect."""

# CryptoDetect API Reference

## Overview

CryptoDetect provides a modular Python API for cryptographic algorithm identification using machine learning.

## Core Modules

### data_loader.py

Load and preprocess cryptographic algorithm data.

#### DataLoader Class

```python
from src.data_loader import DataLoader

# Initialize loader
loader = DataLoader('cryptographic_algorithms_large.csv')

# Load data
df = loader.load()

# Preprocess
df_clean = loader.preprocess()

# Get features and target
X, y = loader.get_features_and_target(
    feature_cols=['block_size', 'key_size'],
    target_col='algorithm'
)

# Split data
X_train, X_test, y_train, y_test = loader.split_data(X, y, test_size=0.2)

# Get statistics
stats = loader.get_statistics()
```

### feature_extractor.py

Extract features from cryptographic data.

#### FeatureExtractor Class

```python
from src.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()

# Extract basic features
features = extractor.extract_basic_features(block_size=128, key_size=128)

# Extract ciphertext features
cipher_features = extractor.extract_ciphertext_features(ciphertext='0x6d251e0e...')

# Extract all features
all_features = extractor.extract_all_features(
    block_size=128,
    key_size=128,
    ciphertext='0x6d251e0e...'
)

# Extract from DataFrame
feature_df = extractor.extract_from_dataframe(df)
```

### model_trainer.py

Train and manage machine learning models.

#### ModelTrainer Class

```python
from src.model_trainer import ModelTrainer

trainer = ModelTrainer(model_dir='models')

# Train Random Forest
rf_model = trainer.train_random_forest(X_train, y_train)

# Train SVM
svm_model = trainer.train_svm(X_train, y_train)

# Train Neural Network
nn_model = trainer.train_neural_network(X_train, y_train)

# Evaluate model
results = trainer.evaluate(rf_model, X_test, y_test)

# Save model
path = trainer.save_model(rf_model, 'random_forest_v1')

# Load model
loaded_model = trainer.load_model('random_forest_v1')

# Train ensemble
all_models = trainer.train_ensemble(X_train, y_train)
```

### predictor.py

Make predictions using trained models.

#### Predictor Class

```python
from src.predictor import Predictor

predictor = Predictor(model)

# Single prediction
result = predictor.predict(block_size=128, key_size=128)
# Returns: {'algorithm': 'AES', 'confidence': 0.95, 'probabilities': {...}}

# Batch predictions
batch_df = predictor.predict_batch(data_df)

# Prediction with explanation
explained = predictor.predict_with_explanation(block_size=128, key_size=128)

# Evaluate prediction
evaluation = predictor.evaluate_prediction(128, 128, actual_algorithm='AES')
```

#### EnsemblePredictor Class

```python
from src.predictor import EnsemblePredictor

ensemble = EnsemblePredictor({'rf': rf_model, 'svm': svm_model, 'nn': nn_model})

# Majority voting
result = ensemble.predict_majority_vote(block_size=128, key_size=128)

# Weighted average
weights = {'rf': 0.5, 'svm': 0.3, 'nn': 0.2}
result = ensemble.predict_weighted_average(block_size=128, key_size=128, weights=weights)
```

### utils.py

Utility functions for CryptoDetect.

```python
from src.utils import save_results, load_results, format_metrics, get_algorithm_info

# Save results
save_results(results, 'results.json')

# Load results
results = load_results('results.json')

# Format metrics
formatted = format_metrics(metrics)

# Get algorithm info
info = get_algorithm_info('AES')
```

## Complete Workflow Example

```python
from src.data_loader import DataLoader
from src.feature_extractor import FeatureExtractor
from src.model_trainer import ModelTrainer
from src.predictor import Predictor
from sklearn.metrics import classification_report

# Load and prepare data
loader = DataLoader('cryptographic_algorithms_large.csv')
df = loader.load()
df = loader.preprocess()

# Extract features
extractor = FeatureExtractor()
X, y = loader.get_features_and_target()

# Split data
X_train, X_test, y_train, y_test = loader.split_data(X, y)

# Train model
trainer = ModelTrainer()
model = trainer.train_random_forest(X_train, y_train)

# Evaluate
results = trainer.evaluate(model, X_test, y_test)
print(f"Accuracy: {results['accuracy']:.4f}")
print(results['classification_report'])

# Save model
trainer.save_model(model, 'production_model')

# Make predictions
predictor = Predictor(model)
prediction = predictor.predict(block_size=128, key_size=128)
print(f"Predicted algorithm: {prediction['algorithm']}")
print(f"Confidence: {prediction['confidence']:.2%}")
```

## Data Format

### Input CSV Format

```csv
block_size,key_size,plaintext,ciphertext,mode,algorithm
128,128,Hello World!,0x6d251e0e0e0e0e0e,CBC,AES
256,256,Hello World!,0x6d251e0e0e0e0e0e,CBC,AES
2048,2048,Hello World!,0x1234567890abcdef,ECB,RSA
```

### Prediction Output

```python
{
    'algorithm': 'AES',
    'confidence': 0.95,
    'probabilities': {
        'AES': 0.95,
        'DES': 0.03,
        'RSA': 0.02
    }
}
```

## Error Handling

All functions raise appropriate exceptions:

- `FileNotFoundError`: When data file doesn't exist
- `ValueError`: When input validation fails
- `KeyError`: When required columns are missing

```python
try:
    result = predictor.predict(128, 128)
except ValueError as e:
    print(f"Prediction error: {e}")
```

## Configuration

### Model Parameters

Adjust model hyperparameters during training:

```python
# Random Forest
rf = trainer.train_random_forest(
    X_train, y_train,
    n_estimators=200,
    max_depth=20
)

# SVM
svm = trainer.train_svm(
    X_train, y_train,
    kernel='rbf',
    C=10.0
)

# Neural Network
nn = trainer.train_neural_network(
    X_train, y_train,
    hidden_layers=(128, 64, 32),
    max_iter=2000
)
```

## Performance Tips

1. **Data Preprocessing**: Use `DataLoader.preprocess()` for consistency
2. **Feature Engineering**: Extract relevant features with `FeatureExtractor`
3. **Model Selection**: Compare all models and choose ensemble for best results
4. **Hyperparameter Tuning**: Use GridSearchCV for optimization
5. **Evaluation**: Always evaluate on held-out test set

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low accuracy | Increase training data, tune hyperparameters, check features |
| Slow training | Reduce dataset size, use fewer features, parallelize with n_jobs=-1 |
| Model not found | Check model_dir path and filename |
| Memory error | Reduce batch size, use data sampling |

---

For more information, see [README.md](../README.md) and [Dataset Documentation](DATASET.md).
