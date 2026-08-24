import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

## Load the LSTM Model
model = load_model('next_word_lstm.h5')

## Load the Tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

## Function to predict the next word
def predict_next_word(model, tokenizer, text, max_sequence_len):
    token_list = tokenizer.texts_to_sequences([text])[0]    ## Convert the input text to a sequence of integers
    if len(token_list) >= max_sequence_len:
        token_list = token_list[-(max_sequence_len-1):]    ## If the input text is longer than the maximum sequence length, truncate it to the last max_sequence_len-1 tokens

    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')    ## Pad the sequence to the maximum length
    predicted = model.predict(token_list, verbose=0)    ## Predict the next word
    predicted_word_index = np.argmax(predicted, axis=-1)    ## Get the index of the predicted word
    for word, index in tokenizer.word_index.items():
        if index == predicted_word_index:
            return word
    return None

## Streamlit App
st.title("Next Word Prediction using LSTM") 
input_text = st.text_input("Enter a phrase:", "to be or not to be")    ## Input text from the user
if st.button("Predict Next Word"):    ## Button to trigger the prediction
    max_sequence_len = model.input_shape[1] + 1    ## Get the maximum sequence length from the model input shape
    next_word = predict_next_word(model, tokenizer, input_text, max_sequence_len)    ## Predict the next word
    st.write(f"Predicted Next Word: {next_word}")