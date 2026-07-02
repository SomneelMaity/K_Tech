import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

@st.cache_data   ## st.cache is used to cache the function output so that it doesn't need to be recomputed every time the app reruns.

def load_data():
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)   ## Creating a DataFrame from the iris dataset
    df['species'] = iris.target     ## Adding the target variable to the DataFrame
    return df, iris.target_names

df, target_names = load_data()
model = RandomForestClassifier()   ## Creating a Random Forest Classifier model
model.fit(df.iloc[:, :-1], df['species'])   ## Fitting the model on the features and target variable

# model.fit(X, y) - Trains the Random Forest model

# First argument: features (X) - the input data
# Second argument: target (y) - what you're trying to predict
# df.iloc[:, :-1] - Selects all feature columns (excluding species)

# iloc - integer-location based indexing
# : (before comma) - all rows
# :-1 (after comma) - all columns except the last one
# -1 means "last column"
# :-1 means "up to but not including the last"

st.sidebar.title("Input Features")
sepal_length = st.sidebar.slider("Sepal length", float(df['sepal length (cm)'].min()), float(df['sepal length (cm)'].max()))
sepal_width = st.sidebar.slider("Sepal width", float(df['sepal width (cm)'].min()), float(df['sepal width (cm)'].max()))
petal_length = st.sidebar.slider("Petal length", float(df['petal length (cm)'].min()), float(df['petal length (cm)'].max()))
petal_width = st.sidebar.slider("Petal width", float(df['petal width (cm)'].min()), float(df['petal width (cm)'].max()))

input_data = [[sepal_length, sepal_width, petal_length, petal_width]]

## Prediction
prediction = model.predict(input_data)
predicted_species = target_names[prediction[0]]
st.write("Prediction")
st.write(f"The predicted species is: {predicted_species}")