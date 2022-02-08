import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

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
        sepal_lenght_cm = st.sidebar.slider('Sepal length (cm)', 0.0,10.0,5.1)
        sepal_width_cm = st.sidebar.slider('Sepal width (cm)', 0.0,5.0,3.5)
        petal_width_cm = st.sidebar.slider('Petal length (cm)', 0.0,5.0,0.2)
        data = {'sepal_length_cm': sepal_lenght_cm,
                'sepal_width_cm': sepal_width_cm,
                'petal_width_cm': petal_width_cm}
        features = pd.DataFrame(data, index=[0])
        return features
    input = user_input_features()

# Combines user input features with entire Iris dataset. Useful for the encoding phase
#iris_raw = pd.read_csv("https://raw.githubusercontent.com/jkmg/Iris/main/Iris.csv", delimiter = ",")
#iris = iris_raw.drop(columns=['Id','PetalLengthCm','Species'], axis=1)
#df = pd.concat([input,iris],axis=0)

# Encoding of ordinal features
#encode = ['Species']
#for col in encode:
#    dummy = pd.get_dummies(df[col], prefix=col)
#    df = pd.concat([df,dummy], axis=1)
#    del df[col]
df = input[:1] # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_rf = pickle.load(open('iris_rf.pkl', 'rb'))

# Predict
prediction = load_rf.predict(df)
prediction_proba = load_rf.predict_proba(df)

st.subheader('Prediction')
iris_species = np.array(['Iris-setosa','Iris-versicolor','Iris-virginica'])
st.write(iris_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)
