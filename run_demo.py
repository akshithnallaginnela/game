#!/usr/bin/env python3
"""
CryptoDetect - Quick Demo
Run this to see the ML pipeline in action
"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.model_trainer import ModelTrainer
from src.predictor import Predictor

print("\n" + "="*70)
print("  🔐 CryptoDetect - Cryptographic Algorithm Identification Demo")
print("="*70)

try:
    # Step 1: Load data
    print("\n📂 Step 1: Loading data...")
    loader = DataLoader('cryptographic_algorithms_large.csv')
    df = loader.load()
    print(f"   ✓ Loaded {len(df)} records")
    algorithms = [str(a) for a in df['algorithm'].unique()]
    print(f"   ✓ Algorithms: {', '.join(algorithms)}")
    
    # Step 2: Preprocess
    print("\n🔧 Step 2: Preprocessing data...")
    df = loader.preprocess()
    print(f"   ✓ Cleaned dataset: {len(df)} records")
    
    # Step 3: Get features
    print("\n📊 Step 3: Extracting features...")
    X, y = loader.get_features_and_target()
    print(f"   ✓ Features shape: {X.shape}")
    print(f"   ✓ Feature columns: {list(X.columns)}")
    
    # Step 4: Split data
    print("\n✂️  Step 4: Splitting data...")
    X_train, X_test, y_train, y_test = loader.split_data(X, y, test_size=0.3)
    print(f"   ✓ Training set: {len(X_train)} samples")
    print(f"   ✓ Test set: {len(X_test)} samples")
    
    # Step 5: Train model
    print("\n🤖 Step 5: Training Random Forest model...")
    trainer = ModelTrainer()
    model = trainer.train_random_forest(X_train, y_train, n_estimators=50)
    print("   ✓ Model trained successfully!")
    
    # Step 6: Evaluate
    print("\n📈 Step 6: Evaluating model...")
    results = trainer.evaluate(model, X_test, y_test)
    print(f"   ✓ Accuracy: {results['accuracy']:.2%}")
    print(f"\n   Classification Report:\n{results['classification_report']}")
    
    # Step 7: Make predictions
    print("\n🔍 Step 7: Making predictions...")
    predictor = Predictor(model)
    
    test_cases = [
        (128, 128, "AES (128-bit block, 128-bit key)"),
        (256, 256, "AES (256-bit block, 256-bit key)"),
        (2048, 2048, "RSA (2048-bit block, 2048-bit key)"),
    ]
    
    for block_size, key_size, description in test_cases:
        result = predictor.predict(block_size, key_size)
        print(f"\n   {description}")
        print(f"   → Predicted: {result['algorithm']}")
        print(f"   → Confidence: {result['confidence']:.2%}")
    
    # Step 8: Batch prediction
    print("\n📦 Step 8: Batch predictions...")
    batch_data = pd.DataFrame({
        'block_size': [128, 256, 2048, 128],
        'key_size': [128, 256, 2048, 128]
    })
    batch_results = predictor.predict_batch(batch_data)
    print(f"   ✓ Processed {len(batch_results)} predictions")
    print("\n   Results:")
    print(batch_results[['block_size', 'key_size', 'predicted_algorithm', 'confidence']].to_string())
    
    # Summary
    print("\n" + "="*70)
    print("✅ Demo completed successfully!")
    print("="*70)
    print("\n📚 Next steps:")
    print("   1. Check docs/QUICKSTART.md for more examples")
    print("   2. Read docs/API.md for complete API reference")
    print("   3. Review src/ modules for implementation details")
    print("   4. Run tests with: pytest tests/")
    print("\n🔐 Project is ready for development and deployment!")
    print()

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
