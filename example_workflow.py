#!/usr/bin/env python3
"""
CryptoDetect - Complete Example Workflow

This script demonstrates the full machine learning pipeline for cryptographic
algorithm identification.

Usage:
    python example_workflow.py
"""

import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer, evaluate_models
from src.predictor import Predictor, EnsemblePredictor
from src.utils import format_metrics


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_basic_workflow():
    """Example 1: Basic Random Forest workflow."""
    print_section("Example 1: Basic Random Forest Workflow")
    
    # Load data
    print("\n1. Loading data...")
    loader = DataLoader('cryptographic_algorithms_large.csv')
    df = loader.load()
    print(f"   ✓ Loaded {len(df)} records")
    
    # Display statistics
    print("\n2. Dataset statistics:")
    stats = loader.get_statistics()
    print(f"   - Total records: {stats['total_records']}")
    print(f"   - Algorithms: {', '.join(stats['algorithms'])}")
    
    # Preprocess
    print("\n3. Preprocessing data...")
    df = loader.preprocess()
    print(f"   ✓ Cleaned dataset: {len(df)} records")
    
    # Get features
    print("\n4. Extracting features...")
    X, y = loader.get_features_and_target()
    print(f"   ✓ Features shape: {X.shape}")
    
    # Split data
    print("\n5. Splitting data...")
    X_train, X_test, y_train, y_test = loader.split_data(X, y)
    print(f"   - Train set: {len(X_train)} samples")
    print(f"   - Test set: {len(X_test)} samples")
    
    # Train model
    print("\n6. Training Random Forest...")
    trainer = ModelTrainer()
    model = trainer.train_random_forest(X_train, y_train)
    print("   ✓ Model trained successfully")
    
    # Evaluate
    print("\n7. Evaluating model...")
    results = trainer.evaluate(model, X_test, y_test)
    print(f"   ✓ Accuracy: {results['accuracy']:.2%}")
    
    # Make prediction
    print("\n8. Making prediction...")
    predictor = Predictor(model)
    prediction = predictor.predict(block_size=128, key_size=128)
    print(f"   ✓ Algorithm: {prediction['algorithm']}")
    print(f"   ✓ Confidence: {prediction['confidence']:.2%}")
    
    return model, X_test, y_test


def example_ensemble_workflow(X_test, y_test):
    """Example 2: Ensemble model workflow."""
    print_section("Example 2: Ensemble Model Workflow")
    
    # Load data for training
    print("\n1. Preparing data...")
    loader = DataLoader('cryptographic_algorithms_large.csv')
    df = loader.load()
    X, y = loader.get_features_and_target()
    X_train, _, y_train, _ = loader.split_data(X, y)
    print(f"   ✓ Training data ready: {len(X_train)} samples")
    
    # Train ensemble
    print("\n2. Training ensemble models...")
    trainer = ModelTrainer()
    models = trainer.train_ensemble(X_train, y_train)
    print(f"   ✓ Trained {len(models)} models:")
    for name in models.keys():
        print(f"     - {name}")
    
    # Evaluate all models
    print("\n3. Evaluating all models...")
    results = evaluate_models(models, X_test, y_test)
    
    for model_name, metrics in results.items():
        print(f"\n   {model_name.upper()}:")
        print(f"   - Accuracy: {metrics['accuracy']:.2%}")
    
    # Ensemble predictions
    print("\n4. Making ensemble predictions...")
    ensemble = EnsemblePredictor(models)
    
    # Majority voting
    print("\n   a) Majority Voting:")
    result_majority = ensemble.predict_majority_vote(128, 128)
    print(f"      - Algorithm: {result_majority['algorithm']}")
    print(f"      - Votes: {result_majority['votes']}")
    
    # Weighted average
    print("\n   b) Weighted Average:")
    weights = {'random_forest': 0.5, 'svm': 0.3, 'neural_network': 0.2}
    result_weighted = ensemble.predict_weighted_average(128, 128, weights=weights)
    print(f"      - Algorithm: {result_weighted['algorithm']}")
    print(f"      - Confidence: {result_weighted['confidence']:.2%}")


def example_batch_prediction(model):
    """Example 3: Batch prediction workflow."""
    print_section("Example 3: Batch Prediction")
    
    # Prepare batch data
    print("\n1. Preparing batch data...")
    batch_data = pd.DataFrame({
        'block_size': [128, 256, 128, 2048, 64],
        'key_size': [128, 256, 128, 2048, 56]
    })
    print(f"   ✓ Batch size: {len(batch_data)} samples")
    
    # Make predictions
    print("\n2. Making batch predictions...")
    predictor = Predictor(model)
    results = predictor.predict_batch(batch_data)
    
    # Display results
    print("\n3. Results:")
    print("\n   Block Size | Key Size | Predicted Algorithm | Confidence")
    print("   " + "-" * 60)
    for idx, row in results.iterrows():
        print(f"   {row['block_size']:>10} | {row['key_size']:>8} | "
              f"{row['predicted_algorithm']:>19} | {row['confidence']:>10.2%}")


def example_prediction_details(model):
    """Example 4: Detailed prediction with explanation."""
    print_section("Example 4: Prediction Details & Explanation")
    
    predictor = Predictor(model)
    
    print("\n1. AES (128-bit block, 128-bit key):")
    result = predictor.predict_with_explanation(128, 128)
    print(f"   - Algorithm: {result['algorithm']}")
    print(f"   - Confidence: {result['confidence']:.2%}")
    print(f"   - Explanation: {result['explanation']}")
    
    print("\n2. RSA (2048-bit block, 2048-bit key):")
    result = predictor.predict_with_explanation(2048, 2048)
    print(f"   - Algorithm: {result['algorithm']}")
    print(f"   - Confidence: {result['confidence']:.2%}")
    print(f"   - Explanation: {result['explanation']}")
    
    print("\n3. DES (64-bit block, 56-bit key):")
    result = predictor.predict_with_explanation(64, 56)
    print(f"   - Algorithm: {result['algorithm']}")
    print(f"   - Confidence: {result['confidence']:.2%}")
    print(f"   - Explanation: {result['explanation']}")


def main():
    """Run all examples."""
    print("\n" + "🔐" * 35)
    print("     CryptoDetect - Complete Workflow Examples")
    print("🔐" * 35)
    
    try:
        # Run examples
        model, X_test, y_test = example_basic_workflow()
        example_ensemble_workflow(X_test, y_test)
        example_batch_prediction(model)
        example_prediction_details(model)
        
        # Summary
        print_section("Summary")
        print("\n✓ All examples completed successfully!")
        print("\nYou now have:")
        print("  - Trained machine learning models")
        print("  - Individual model predictions")
        print("  - Ensemble predictions (voting & weighted)")
        print("  - Batch processing capability")
        print("  - Detailed prediction analysis")
        
        print("\nNext steps:")
        print("  1. Explore the src/ directory for more details")
        print("  2. Check docs/ for API and dataset documentation")
        print("  3. Run tests: pytest tests/")
        print("  4. Read CONTRIBUTING.md to contribute")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Please ensure 'cryptographic_algorithms_large.csv' exists in the project root")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
