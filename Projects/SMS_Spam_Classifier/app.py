import streamlit as st
import pickle

try:
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
except FileNotFoundError as e:
    st.error(f"Model files not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.title("SMS Spam Classifier")
input_sms = st.text_area("Enter the message to classify it as spam or not spam")

if st.button('Predict'):
    # Vectorize (no separate preprocessing needed - vectorizer handles it)
    vectorized_sms = tfidf.transform([input_sms])
    # Predict
    prediction = model.predict(vectorized_sms)[0]
    # Display
    if prediction == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
