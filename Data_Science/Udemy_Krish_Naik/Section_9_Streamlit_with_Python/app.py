import streamlit as st
import pandas as pd
import numpy as np

## Title of the application
st.title("Hello Streamlit")

## Display a simple text
st.write("This is a simple text.")

## Create a simple DataFrame
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40]
})

## Display the DataFrame
st.write("Here is a simple DataFrame:")
st.write(df)

## Create a simple line chart
st.write("Here is a simple line chart:")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)