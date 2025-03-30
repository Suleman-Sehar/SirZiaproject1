import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stapp{
    background-color: black;
    color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & description
st.title("Datasweeper Sterling Intgretor By Suleman Sehar")
st.write("Tranform your files between CSV and Excel format with built-in data cleaning and visualization Creating the project for quarter 3!")

# File uploader
uploaded_file = st.file_uploader("upload your files, CVS or Excel", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

#File Details
st.write("Preview the head of the Dataframe")
st.dataframe(df.head())

#Data Cleaning Option
st.subheader("Data Cleaning Options")
if st.checkbox(f"Clean data for {file.name}"):
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Remove duplicates from the file: {file.name}"):
            df.drop_duplicates(implace=True)
            st.write("Duplicates removed successfully!")
    with col2:
        if st.button(f"fill missing values in the file : {file.name}"):
            numeric_cols = df.select_dtypes(include=['number']).columns
            df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Missing values filled successfully!")

    st.subheader("Select Columns to keep")
    colmuns = st.multiselect(f"Select columns to keep from {file.name}", df.columns, default=df.columns)
    df = df[colmuns]


    #Data Visualization
    st.subheader("Data Visulization")
    if st.checkbox(f"Visualize data for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            )
            
st.success("Data Cleaning and Visulization complete successfully!")