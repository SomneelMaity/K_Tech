import streamlit as st

st.title("Streamlit Text Example")
name = st.text_input("Enter your name:")
age = st.slider("Select your age:", 0, 100, 25)
st.write(f"You are {age} years old.")
options = ['Python', 'JavaScript', 'C++', 'Java']
choice = st.selectbox("Select your favorite programming language:", options)
st.write(f"You selected: {choice}")
if name:
    st.write(f"Hello, {name}!")
    
import pandas as pd
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
    "City": ["New York", "Los Angeles", "Chicago", "Houston"]
}

df = pd.DataFrame(data)
st.write(df)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        if df_uploaded.empty:
            st.warning("The uploaded CSV file is empty. Please upload a file with data.")
        else:
            st.write(df_uploaded)
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or has no columns. Please upload a valid CSV file with data.")
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")