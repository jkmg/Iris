import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression

st.write("""
# Iris plants Prediction App
This app predicts the type of iris plant ('Iris-setosa', 'Iris-versicolor' and 'Iris-virginica') from the paramters
sepal length, sepal width and petal width in cm. 
Data to generate the model were obtained from Kaggle (https://www.kaggle.com/uciml/iris).
""")

st.sidebar.header('User Input Features')

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        SepalLengthCm = st.sidebar.slider('Sepal length (cm)', 0.0,10.0,5.1)
        SepalWidthCm = st.sidebar.slider('Sepal width (cm)', 0.0,5.0,3.5)
        PetalWidthCm = st.sidebar.slider('Petal width (cm)', 0.0,5.0,0.2)
        data = {'SepalLengthCm': SepalLengthCm,
                'SepalWidthCm': SepalWidthCm,
                'PetalWidthCm': PetalWidthCm}
        features = pd.DataFrame(data, index=[0])
        return features
    input = user_input_features()

df = input[:1] # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Load Logistic Regression classification model
load_lr = pickle.load(open('iris_lr.pkl', 'rb'))
# Logistic Regression Prediction
prediction_lr = load_lr.predict(df)
prediction_proba_lr = load_lr.predict_proba(df)

st.subheader('Logistic Regression Prediction')
iris_species = np.array(['Iris-setosa','Iris-versicolor','Iris-virginica'])
st.write(iris_species[prediction_lr])

st.subheader('Logistic Regression Prediction Probability')
st.write(prediction_proba_lr)
