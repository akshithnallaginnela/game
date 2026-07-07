# Quick Start Guide

## Installation

```bash
# Clone repository
git clone https://github.com/akshithnallaginnela/algorithm_identifer.git
cd algorithm_identifer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run the Jupyter Notebook

```bash
jupyter notebook cryptography.ipynb
```

## Quick Python Example

```python
import pandas as pd
from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer
from src.predictor import Predictor

# Load and prepare data
loader = DataLoader('cryptographic_algorithms_large.csv')
df = loader.load()
X, y = loader.get_features_and_target()
X_train, X_test, y_train, y_test = loader.split_data(X, y)

# Train model
trainer = ModelTrainer()
model = trainer.train_random_forest(X_train, y_train)
results = trainer.evaluate(model, X_test, y_test)
print(f"Accuracy: {results['accuracy']:.2%}")

# Make predictions
predictor = Predictor(model)
prediction = predictor.predict(block_size=128, key_size=128)
print(f"Algorithm: {prediction['algorithm']}")
print(f"Confidence: {prediction['confidence']:.2%}")
```

## Train All Models

```python
from src.model_trainer import ModelTrainer, evaluate_models

trainer = ModelTrainer()
models = trainer.train_ensemble(X_train, y_train)

# Evaluate all models
results = evaluate_models(models, X_test, y_test)
for model_name, metrics in results.items():
    print(f"{model_name}: {metrics['accuracy']:.2%}")
```

## Use Ensemble Predictions

```python
from src.predictor import EnsemblePredictor

ensemble = EnsemblePredictor(models)

# Majority voting
result = ensemble.predict_majority_vote(128, 128)
print(f"Algorithm: {result['algorithm']}")

# Weighted voting
weights = {'random_forest': 0.5, 'svm': 0.3, 'neural_network': 0.2}
result = ensemble.predict_weighted_average(128, 128, weights=weights)
print(f"Algorithm: {result['algorithm']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Run Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
pytest tests/ --cov=src  # With coverage
```

## Project Structure

```
algorithm_identifer/
├── README.md
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
├── cryptography.ipynb
├── cryptographic_algorithms_large.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── feature_extractor.py
│   ├── model_trainer.py
│   ├── predictor.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_models.py
├── models/
│   └── (trained model files)
├── docs/
│   ├── API.md
│   ├── DATASET.md
│   └── CONTRIBUTING.md
└── notebooks/
    └── (additional notebooks)
```

## Common Tasks

### Load and Explore Data
```python
from src.data_loader import DataLoader

loader = DataLoader('cryptographic_algorithms_large.csv')
df = loader.load()

stats = loader.get_statistics()
print(f"Total records: {stats['total_records']}")
print(f"Algorithms: {stats['algorithms']}")
```

### Feature Engineering
```python
from src.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()
features = extractor.extract_all_features(
    block_size=128,
    key_size=128,
    ciphertext='0x6d251e0e...'
)
```

### Save/Load Models
```python
trainer = ModelTrainer()

# Save model
trainer.save_model(model, 'my_model')

# Load model
loaded = trainer.load_model('my_model')
```

### Batch Predictions
```python
predictor = Predictor(model)

# Prepare batch data
batch_df = pd.DataFrame({
    'block_size': [128, 256, 2048],
    'key_size': [128, 256, 2048]
})

# Get predictions
results = predictor.predict_batch(batch_df)
print(results)
```

## Next Steps

1. Read [API.md](docs/API.md) for detailed API documentation
2. Check [DATASET.md](docs/DATASET.md) for dataset information
3. See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Explore [cryptography.ipynb](cryptography.ipynb) for analysis

## Troubleshooting

**Import Error: No module named 'src'**
- Ensure you're running from the project root directory
- Install with: `pip install -e .`

**Memory Error during Training**
- Reduce dataset size
- Use fewer features
- Enable garbage collection

**Low Accuracy**
- Check data preprocessing
- Review feature engineering
- Tune hyperparameters
- Try different models

## Support

- 📚 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/akshithnallaginnela/algorithm_identifer/issues)
- 💬 [Discussions](https://github.com/akshithnallaginnela/algorithm_identifer/discussions)
- 📧 Email: akshith.nallaginnela@example.com

---

**Ready to detect cryptographic algorithms?** 🔐
