"""
Breast Cancer Classification Using Supervised Machine Learning
Author: [Your Name]
Date: June 5, 2026

This script implements Logistic Regression and Random Forest classifiers
to predict whether a breast tumor is Malignant (M) or Benign (B).
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)

warnings.filterwarnings('ignore')

class BreastCancerClassifier:
    """Main class for breast cancer classification"""
    
    def __init__(self, data_path='data.csv'):
        """Initialize the classifier with data path"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X_train_scaled = None
        self.X_test_scaled = None
        self.scaler = None
        self.lr_model = None
        self.rf_model = None
        
    def load_data(self):
        """Load the dataset"""
        print("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Dataset loaded successfully!")
        print(f"Shape: {self.df.shape}")
        return self.df
    
    def explore_data(self):
        """Perform exploratory data analysis"""
        print("\n" + "="*60)
        print("DATA EXPLORATION")
        print("="*60)
        
        print(f"\nDataset Info:")
        print(f"Rows: {self.df.shape[0]}, Columns: {self.df.shape[1]}")
        
        print(f"\nMissing Values:")
        missing = self.df.isnull().sum().sum()
        print(f"Total missing values: {missing}")
        
        print(f"\nTarget Distribution:")
        print(self.df['diagnosis'].value_counts())
        
    def preprocess_data(self):
        """Preprocess the data"""
        print("\n" + "="*60)
        print("DATA PREPROCESSING")
        print("="*60)
        
        # Create a copy
        df_processed = self.df.copy()
        
        # Remove irrelevant columns
        columns_to_drop = [col for col in df_processed.columns 
                          if 'id' in col.lower() or 'unnamed' in col.lower()]
        if columns_to_drop:
            print(f"Dropping columns: {columns_to_drop}")
            df_processed = df_processed.drop(columns=columns_to_drop)
        
        # Encode diagnosis
        print("Encoding diagnosis: M→1, B→0")
        df_processed['diagnosis'] = df_processed['diagnosis'].map({'M': 1, 'B': 0})
        
        # Split features and target
        X = df_processed.drop('diagnosis', axis=1)
        y = df_processed['diagnosis']
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"\n✓ Train set: {self.X_train.shape[0]} samples")
        print(f"✓ Test set: {self.X_test.shape[0]} samples")
        
        # Feature scaling
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        print("✓ Feature scaling applied")
        
    def train_logistic_regression(self):
        """Train Logistic Regression model"""
        print("\n" + "="*60)
        print("TRAINING LOGISTIC REGRESSION")
        print("="*60)
        
        self.lr_model = LogisticRegression(random_state=42, max_iter=1000)
        self.lr_model.fit(self.X_train_scaled, self.y_train)
        print("✓ Logistic Regression trained successfully")
        
    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n" + "="*60)
        print("TRAINING RANDOM FOREST")
        print("="*60)
        
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.rf_model.fit(self.X_train_scaled, self.y_train)
        print("✓ Random Forest trained successfully")
        
    def evaluate_model(self, model, model_name):
        """Evaluate a given model"""
        print("\n" + "="*60)
        print(f"{model_name.upper()} - EVALUATION")
        print("="*60)
        
        # Predictions
        y_pred_train = model.predict(self.X_train_scaled)
        y_pred_test = model.predict(self.X_test_scaled)
        
        # Test set metrics
        accuracy = accuracy_score(self.y_test, y_pred_test)
        precision = precision_score(self.y_test, y_pred_test)
        recall = recall_score(self.y_test, y_pred_test)
        f1 = f1_score(self.y_test, y_pred_test)
        
        print(f"\nTest Set Performance:")
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        
        print(f"\nClassification Report:")
        print(classification_report(self.y_test, y_pred_test, 
                                   target_names=['Benign (0)', 'Malignant (1)']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'y_pred_test': y_pred_test
        }
    
    def compare_models(self, lr_results, rf_results):
        """Compare the two models"""
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        
        comparison = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Logistic Regression': [lr_results['accuracy'], lr_results['precision'], 
                                   lr_results['recall'], lr_results['f1_score']],
            'Random Forest': [rf_results['accuracy'], rf_results['precision'], 
                            rf_results['recall'], rf_results['f1_score']]
        })
        
        print("\n", comparison.to_string(index=False))
        
        # Determine winner
        lr_wins = sum([lr_results[metric] > rf_results[metric] 
                      for metric in ['accuracy', 'precision', 'recall', 'f1_score']])
        rf_wins = sum([rf_results[metric] > lr_results[metric] 
                      for metric in ['accuracy', 'precision', 'recall', 'f1_score']])
        
        print("\n" + "="*60)
        if rf_wins > lr_wins:
            print("WINNER: RANDOM FOREST")
        elif lr_wins > rf_wins:
            print("WINNER: LOGISTIC REGRESSION")
        else:
            print("RESULT: TIE")
        print("="*60)
        
    def run_full_pipeline(self):
        """Run the complete classification pipeline"""
        print("\n" + "="*70)
        print(" BREAST CANCER CLASSIFICATION - COMPLETE PIPELINE ")
        print("="*70)
        
        # Load data
        self.load_data()
        
        # Explore data
        self.explore_data()
        
        # Preprocess data
        self.preprocess_data()
        
        # Train models
        self.train_logistic_regression()
        self.train_random_forest()
        
        # Evaluate models
        lr_results = self.evaluate_model(self.lr_model, "Logistic Regression")
        rf_results = self.evaluate_model(self.rf_model, "Random Forest")
        
        # Compare models
        self.compare_models(lr_results, rf_results)
        
        print("\n✓ Pipeline completed successfully!")
        
        return lr_results, rf_results


def main():
    """Main function to run the classification"""
    # Create classifier instance
    classifier = BreastCancerClassifier('data.csv')
    
    # Run full pipeline
    lr_results, rf_results = classifier.run_full_pipeline()
    
    print("\n" + "="*70)
    print(" ASSIGNMENT COMPLETED SUCCESSFULLY! ")
    print("="*70)


if __name__ == "__main__":
    main()
