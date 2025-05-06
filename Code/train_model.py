import numpy as np
import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
import os

# Download required NLTK data
nltk.download('punkt', quiet=True)

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def train_model():
    # Read the dataset using the correct path
    dataset_path = os.path.join('..', 'Dataset', 'final_dataset_hinglish.csv')
    df = pd.read_csv(dataset_path)
    
    # Convert -1 labels to 1 (bullying)
    df['label'] = df['label'].replace(-1, 1)
    
    # Clean the text
    df['headline'] = df['headline'].apply(clean_text)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        df['headline'], df['label'], test_size=0.2, random_state=42
    )
    
    # Create and fit TF-IDF vectorizer
    tfidf = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    # Train the model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_tfidf, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join('..', 'Code', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save the model and vectorizer
    with open(os.path.join(models_dir, 'tfidf_vectorizer.pkl'), 'wb') as f:
        pickle.dump(tfidf, f)
    with open(os.path.join(models_dir, 'cyberbullying_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    print("\nModel and vectorizer saved successfully!")

if __name__ == "__main__":
    train_model() 