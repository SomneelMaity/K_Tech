import pandas as pd
import numpy as np
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

# Download NLTK data
print("Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load data
print("Loading data...")
df = pd.read_csv('spam.csv', encoding='latin-1')
print(f"Dataset shape: {df.shape}")

# Data Cleaning
df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True, errors='ignore')
df.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)

# Encode target
encoder = LabelEncoder()
df['target'] = encoder.fit_transform(df['target'])  # ham -> 0, spam -> 1

# Remove duplicates
df = df.drop_duplicates(keep='first')
print(f"Dataset after removing duplicates: {df.shape}")

# Train-test split (without preprocessing - let vectorizer handle it)
X = df['text']
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# TF-IDF Vectorization with preprocessing parameters
print("Vectorizing text...")
tfidf = TfidfVectorizer(
    max_features=3000,
    lowercase=True,
    stop_words='english',
    token_pattern=r'\b[a-zA-Z]+\b'  # Only keep alphanumeric tokens
)
print("Fitting vectorizer...")
X_train_tfidf = tfidf.fit_transform(X_train)
print(f"Vectorizer fitted. Vocabulary size: {len(tfidf.vocabulary_)}")
X_test_tfidf = tfidf.transform(X_test)

# Train model
print("Training MultinomialNB model...")
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Evaluate
train_accuracy = model.score(X_train_tfidf, y_train)
test_accuracy = model.score(X_test_tfidf, y_test)
print(f"Train Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Save model and vectorizer
print("Saving model and vectorizer...")
pickle.dump(tfidf, open('vectorizer.pkl', 'wb'))
pickle.dump(model, open('model.pkl', 'wb'))
print("✓ Model and vectorizer saved successfully!")
