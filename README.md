# Cyberbullying Detection in Hinglish Languages

## Overview
This project is a real-time chat application with built-in cyberbullying detection for Hinglish (Hindi written in English) text. It helps create a safer online environment by automatically detecting and preventing cyberbullying messages.

## Simple Explanation
Imagine a chat room where:
- Users can chat with each other in Hinglish (like "kaise ho" or "mast hai")
- Before any message is sent, it's checked for cyberbullying content
- If a message contains cyberbullying, it's blocked with a warning
- If the message is safe, it's sent to everyone in the chat

## Technical Architecture

### Components
1. **Machine Learning Model**
   - Trained on Hinglish text dataset
   - Uses TF-IDF vectorization for text processing
   - LinearSVC classifier for cyberbullying detection
   - Confidence threshold of 0.7 for predictions

2. **Chat Server**
   - Built with Flask and Socket.IO
   - Handles real-time message broadcasting
   - Manages user connections and disconnections
   - Integrates with the ML model for message screening

3. **Web Interface**
   - Modern, responsive design
   - Real-time message updates
   - User-friendly warning system
   - Username-based identification

### How It Works
1. **Text Processing**
   ```python
   def clean_text(text):
       text = text.lower()
       text = re.sub(r'[^a-zA-Z\s.,!?]', '', text)
       return ' '.join(text.split())
   ```

2. **Cyberbullying Detection**
   ```python
   def check_cyberbullying(text):
       cleaned_text = clean_text(text)
       text_vectorized = vectorizer.transform([cleaned_text])
       probabilities = model.predict_proba(text_vectorized)[0]
       return probabilities[1] > 0.7, float(probabilities[1])
   ```

3. **Real-time Message Handling**
   ```python
   @socketio.on('message')
   def handle_message(data):
       is_bullying, confidence = check_cyberbullying(data['text'])
       if is_bullying:
           emit('warning', {'message': 'Cyberbullying detected!'})
       else:
           emit('message', data, broadcast=True)
   ```

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git (for version control)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd CyberBullying-Detection-in-Hinglish-Languages-Using-Machine-Learning-
   ```

2. **Set up virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r Safe_Chat/requirements.txt
   ```

4. **Train the model:**
   ```bash
   cd Code
   python train_model.py
   ```

5. **Start the application:**
   ```bash
   cd Safe_Chat
   python app.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```


## Project Structure
```
CyberBullying-Detection-in-Hinglish-Languages-Using-Machine-Learning-/
├── Code/
│   ├── train_model.py          # Model training script
│   └── models/                 # Trained model files
├── Dataset/
│   └── final_dataset_hinglish.csv  # Training data
├── Safe_Chat/
│   ├── app.py                  # Main application
│   ├── templates/
│   │   └── index.html         # Web interface
│   └── requirements.txt        # Dependencies
└── service_testing/
    └── app.py                 # Prediction service
```

## Technical Details

### Machine Learning Model
- **Algorithm**: Linear Support Vector Classifier (LinearSVC)
- **Vectorization**: TF-IDF with custom vocabulary
- **Features**: 
  - Text preprocessing
  - Stop word removal
  - Character-level features
- **Performance Metrics**:
  - Accuracy
  - Precision
  - Recall
  - F1-score

### Web Technologies
- **Backend**: Flask + Socket.IO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Real-time Communication**: WebSocket
- **Styling**: Custom CSS with responsive design

### Security Features
- Message validation
- Input sanitization
- Confidence thresholding
- Real-time monitoring

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

### Testing
- Test the model with various Hinglish inputs
- Verify chat functionality
- Check error handling
- Test on different browsers


3. **Creating Pull Requests**:
   - Push your feature branch
   - Go to GitHub repository
   - Click "Compare & pull request"
   - Fill in the PR description
   - Request review from team members

## Future Improvements
1. Enhanced model accuracy
2. Support for more languages
3. User authentication
4. Message history
5. Admin dashboard
6. Custom warning messages
7. Message reporting system

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request







