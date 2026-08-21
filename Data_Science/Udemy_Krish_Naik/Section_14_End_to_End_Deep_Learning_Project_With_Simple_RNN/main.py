# Step 1: Import Libraries and Load the Model
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

#Load the word_index
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

# Load PreTrained Model
model = load_model('simple_rnn_imdb.h5')

## Step2: Helper Functions
## Function to decode reviews
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]    # 2 is for unknown words, 3 is for padding
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review

# ## Step 3: Prediction Function
# def predict_sentiment(review):
#     preprocessed_input = preprocess_text(review)
#     prediction = model.predict(preprocessed_input)
#     sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
#     return sentiment, prediction[0][0]

## Streamlit App
import streamlit as st
st.title("IMDB Movie Review Sentiment Analysis")
st.write('Enter a movie review below and click "Predict" to see the sentiment.')

## User Input
user_input = st.text_area("Movie Review")

if st.button("Classify"):
    preprocess_input = preprocess_text(user_input)

    ## Make Prediction
    prediction = model.predict(preprocess_input)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'

    ## Display Result
    st.write(f'Sentiment: {sentiment}')
    st.write(f'Prediction Score: {prediction[0][0]:.2f}')
else:
    st.write("Please enter a review and click 'Classify' to see the sentiment.")

