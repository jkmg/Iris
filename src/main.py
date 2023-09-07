import streamlit as st
import st_aggrid
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from streamlit_ace import st_ace
import pandas as pd
import numpy as np
<<<<<<< HEAD
import joblib
from joblib import load

st.write(""" ### Determination of STD NMR Binding Epitopes using the Reduced Dataset Approach from STD factors at 2 saturation times """)

st.sidebar.header('Reduced Dataset Approach')

# Collects user input features into dataframe
uploaded_file1 = st.sidebar.file_uploader("**Upload a CSV File (without column headers) containing 3 columns, the first with the proton names, then the experimental STD factors at short (typically 0.5, 0.75 or 1 s; 0.75 s is recommended) and large (typically 6 or 8 s) saturation times**", type=["csv"])
tsat_short = st.sidebar.number_input("**Enter the Short Saturation Time, in seconds**", value = 0.75, min_value=0.50, max_value=1.00)
if uploaded_file1 is not None:
    df = pd.read_csv(uploaded_file1, header = None)
    df.columns=['Proton', 'STD_short_tsat', 'STD_long_tsat']
    df['ksat'] = (- np.log((df.STD_long_tsat - df.STD_short_tsat)/df.STD_long_tsat))/tsat_short
    df['STD0'] = df.ksat*df.STD_long_tsat
    df['Epitope'] = df.STD0/(np.max(df.STD0))*100
    df.drop(['STD_short_tsat', 'STD_long_tsat'], inplace=True, axis=1)
else:
    num_rows = st.number_input("Number of Ligand Protons for which you are going to input STD factors", 1, 50, 5)
    def aggrid_interactive_table(num_rows):
        data = pd.DataFrame(columns=["Proton_Name", "STD_short_tsat", "STD_long_tsat"], index=range(num_rows))
        # Create grid options for interactive table
        options = GridOptionsBuilder.from_dataframe(data, enableRowGroup=True, enableValue=True, enablePivot=True)
        options.configure_side_bar()
        #grid_options = options.build()
        options.configure_selection("single")
        selection = AgGrid(data, enable_enterprise_modules=True, gridOptions=options.build(), theme="material", update_mode=GridUpdateMode.MODEL_CHANGED, allow_unsafe_jscode=True, key='table')
        if selection.get("table"):
            data = pd.DataFrame(selection["table"])
            table = pd.read_json(selection["table"])
            st.write(table)
        #table = st_ace(value=data, language="json", key="my_table")
        #if table:
        #    data = pd.read_json(table)
        st.write(data)
        

    selection = aggrid_interactive_table(num_rows)
    #if selection:
    #    st.write("You selected:")
    #    st.json(selection["selected_rows"])


        # Display the interactive table
        #grid_response = AgGrid(data, gridOptions=grid_options, key="table")

        # Update the DataFrame with the user-entered values


        #st.write(data)

    #user_input_features(num_rows)
=======
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
>>>>>>> 19f5e920fca6c54fb61054d4ab75aee2a05038b4

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
