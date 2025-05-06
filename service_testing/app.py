from flask import Flask, request, jsonify
import pickle
import re
import os

app = Flask(__name__)

# Load the model and vectorizer
model_path = os.path.join('..', 'Code', 'models', 'cyberbullying_model.pkl')
vectorizer_path = os.path.join('..', 'Code', 'models', 'tfidf_vectorizer.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Keep Hinglish words (Hindi written in English)
    # Remove only special characters but keep spaces and basic punctuation
    text = re.sub(r'[^a-zA-Z\s.,!?]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        cleaned_text = clean_text(text)
        
        # Transform the text using the vectorizer
        text_vectorized = vectorizer.transform([cleaned_text])
        
        # Get prediction probabilities
        probabilities = model.predict_proba(text_vectorized)[0]
        bullying_prob = probabilities[1]  # Probability of bullying class
        
        # Only classify as bullying if confidence is high (>0.7)
        is_bullying = bullying_prob > 0.7
        
        result = {
            'is_bullying': bool(is_bullying),
            'confidence': float(bullying_prob),
            'text': text,
            'cleaned_text': cleaned_text,
            'message': 'Message contains cyberbullying content' if is_bullying else 'Message is safe'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)