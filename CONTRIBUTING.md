# Contributing to CryptoDetect

Thank you for your interest in contributing to CryptoDetect! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### 1. Report Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (Python version, OS, etc.)

### 2. Suggest Enhancements

Enhancement suggestions are welcome! Please include:
- Clear use case
- Proposed solution
- Alternative approaches you've considered

### 3. Submit Code Changes

#### Setup Development Environment

```bash
git clone https://github.com/akshithnallaginnela/algorithm_identifer.git
cd algorithm_identifer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

#### Make Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes with clear, descriptive commits
3. Follow PEP 8 style guidelines
4. Write/update tests for your changes
5. Run tests: `pytest tests/`
6. Format code: `black src/`
7. Lint code: `flake8 src/`

#### Commit Guidelines

- Use clear, descriptive commit messages
- Reference relevant issues: `Fixes #123` or `Related to #456`
- Keep commits focused and atomic
- Example: `Add SVM model training pipeline - Implements SVM classifier for algorithm detection`

#### Submit Pull Request

1. Push to your fork: `git push origin feature/your-feature-name`
2. Open a Pull Request with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes
   - Testing information
3. Respond to review feedback
4. Keep branch up to date with main

## Development Workflow

### Project Structure

```
algorithm_identifer/
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Data loading utilities
│   ├── feature_extractor.py    # Feature engineering
│   ├── model_trainer.py        # Model training pipeline
│   ├── predictor.py            # Prediction interface
│   └── utils.py                # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_feature_extractor.py
│   └── test_models.py
├── notebooks/
│   └── cryptography.ipynb      # Main analysis notebook
├── models/                     # Trained model artifacts
├── docs/                       # Documentation
└── web/                        # Web interface (future)
```

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints: `def process(data: pd.DataFrame) -> np.ndarray:`
- Write docstrings (Google style):

```python
def predict_algorithm(block_size: int, key_size: int) -> str:
    """Predict cryptographic algorithm from parameters.
    
    Args:
        block_size: Size of cipher block in bits
        key_size: Size of encryption key in bits
    
    Returns:
        Predicted algorithm name
    
    Raises:
        ValueError: If parameters are invalid
    """
```

### Testing

- Write tests for all new features
- Maintain >80% code coverage
- Run tests before submitting PR:

```bash
pytest tests/ --cov=src --cov-report=html
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions/classes
- Update docs/ folder for API changes
- Include examples in docstrings

## Areas for Contribution

### High Priority
- [ ] Implement SVM classifier
- [ ] Implement Neural Network classifier
- [ ] Create ensemble prediction method
- [ ] Web API with Flask
- [ ] Unit tests (target 80% coverage)

### Medium Priority
- [ ] Extended algorithm support (Elliptic Curve, ChaCha20)
- [ ] Performance optimization
- [ ] Docker containerization
- [ ] Documentation improvements
- [ ] Interactive web dashboard

### Low Priority
- [ ] Additional visualizations
- [ ] Kubernetes deployment
- [ ] Mobile application
- [ ] Real-time monitoring features

## Questions?

- Check [Discussions](https://github.com/akshithnallaginnela/algorithm_identifer/discussions)
- Open an [Issue](https://github.com/akshithnallaginnela/algorithm_identifer/issues)
- Email: akshith.nallaginnela@example.com

---

Thank you for contributing to CryptoDetect! 🙏
