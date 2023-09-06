from sklearn.preprocessing import PolynomialFeatures
import streamlit as st
import st_aggrid
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from streamlit_ace import st_ace
import pandas as pd
import numpy as np
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

if uploaded_file1 is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded')

#st.sidebar.header('ML Approach')

# Collects user input features into dataframe
#uploaded_file2 = st.sidebar.file_uploader("Upload a CSV File (without column headers) containing 3 columns, the first with the proton names, then the experimental STD factors at 0.75s and finally the STD factros at 6s", type=["csv"])
#if uploaded_file2 is not None:
#    poly = joblib.load('/home/usuario/Documentos/Marie_Curie/Proyectos/STD_ML/Model_Deployment/polynomial_features_stdml_model')
#    model=joblib.load("/home/usuario/Documentos/Marie_Curie/Proyectos/STD_ML/Model_Deployment/extra_trees_best_sklearn_regressor")
#    df2 = pd.read_csv(uploaded_file2, header = None)
#    df2.rename(columns={0: 'Proton', 1: 'STD_0p75s', 2:'STD_6s'}, inplace=True)
#    df2["feature1"] = df2.STD_0p75s/df2.STD_6s
#    df2["feature2"] = np.exp(df2.STD_0p75s/df2.STD_6s)
#    dfval_poly = poly.transform(df2.loc[:,"STD_0p75s":"feature2"])
#    dfval_poly = pd.DataFrame(dfval_poly)
#    pred = model.predict(dfval_poly)
#    pred = pd.DataFrame(pred, columns=['STD0_ML'])
#    pred['Proton'] = df2.Proton.values
#    pred = pred.reindex(columns=['Proton', 'STD0_ML'])
#    pred['Epitope_ML'] = pred.STD0_ML/(np.max(pred.STD0_ML))*100

# Displays the user input features
#st.subheader('ML Approach')

#if uploaded_file2 is not None:
#    st.write(pred)
#else:
#    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
