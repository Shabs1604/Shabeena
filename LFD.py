import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb
import re  

st. title(" Exploratory Data Analysis of Banking and Finance")

st.write("This Web app gives the banking and finance sector insight on the loan applicants which makes it easier for them to apprve of their loan")


# Upload Data in txt, csv or pdf formats
st.sidebar.title("EDA of Banking and Finance")
user_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "csv"], accept_multiple_files=False)

# When the file gets uploaded 
if user_file is not None:
    #Read file type csv pdf and txt only  loan.csv
    #splitting 
    ext = user_file.name.split(".")[-1]
    #st.write(ext)

    st.header(" The Data is shown below ")
    if ext == "csv":
        df = pd.read_csv(user_file)
  
    elif ext == "txt":
        df = pd.read_csv(user_file)
   
    elif ext =="pdf":
        df = pd.read_pdf(user_file)

    else:
        st.write("Error: upload the file in csv,txt or pdf format")       
       
    df = df.dropna(axis=1, how="all")
    #df = df.loc[(df!=0).all(axis=1)]
    
    
    # Columns with null values
    null = (df.isnull().sum()/len(df)*100).sort_values(ascending = False).head(50)
    #st.write(null.values)
    # columns with more than 30% of null values
    null = null[null.values>30]
    null_list = list(null.index.values)
    #st.write(null_list)
    # Remove all the columns with null values greater than 30%
    df = df.drop(labels = null_list, axis=1) 
    #df = df[df.loc[:, (df!=0).all(axis=1)]]
    df = df.drop(["delinq_2yrs","pub_rec","initial_list_status","out_prncp","out_prncp_inv","collections_12_mths_ex_med","policy_code","acc_now_delinq","chargeoff_within_12_mths","delinq_amnt","pub_rec_bankruptcies","tax_liens"], axis = 1)
    # replacing the rest of columns with less than 30 % null values with mode.
    
    
    v2 = st.write(df) 
    
    v3 = st.header("Total Number of data present ")
    v4 = st.title(df.shape)
    
    # On pressing the Show Statistical Info Button
    if st.sidebar.button("Show Statistical Info"):
        
        st.header("Pandas profiling of the data")
        s_info = st.write(df.info())

        # Statistical information of the dataframe 
        st.header("Statistacal information of the dataframe")
        stat = st.write(df.describe())
        
        #Listing all the variables
        st.title("Variables")
        var = st.write(df.columns.values)   
        df1 = df.head(50)
        st.header("Univariate Analysis")
        fig,ax = plt.subplots()
        fig = plt.figure(figsize= (5,5))
        plt.ylabel("Loan Amount") 
        plt.title("No.of times a particular loan amount is sanctioned")
        plt.scatter(df1.index, df1["loan_amnt"], c = "red")
        st.pyplot(fig)

        # Get unique values of purpose coumn
        st.write(df['purpose'].value_counts())

        
        # All fully paid loans / Current /Defaulters
        st.header("Loan Status")
        df_fully_paid = df[df["loan_status"]=="Fully Paid"]
        df_current = df[df["loan_status"]=="Current"]
        df_defaulters = df[df["loan_status"]=="Charged Off"]


     
        #st.dataframe(df_fully_paid)
        #st.write(df_fully_paid.shape[0])0
        #st.dataframe(df_current)
        ##st.write(df_current.shape[0])
        #st.dataframe(df_defaulters)
        #st.write(df_defaulters.shape[0])

        x = ["Fully_paid", "Current","Defaulters"]
        y =[df_fully_paid.shape[0], df_current.shape[0], df_defaulters.shape[0]]
                
        fig,ax = plt.subplots()
        fig = plt.figure(figsize= (5,5))
        plt.bar(x, y,width=0.2)
        plt.xlabel('Loan status')
        plt.ylabel("No. of loan_status")        
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.write("The above figure indicates that there are about 14.16% of defaulters who did not pay the loan back.")
                 
        st.header("Bivariate Analysis")

        # data processing for Loan Amount versus Interest rate
        df["loan_amnt"] = df["loan_amnt"].sort()
        for i in df["int_rate"]:
            p = re.split{}

        st.title("Loan Amount versus Interest rate")
        fig,ax = plt.subplots()
        fig = plt.figure(figsize= (5,5))
        plt.scatter(df["loan_amnt"].head(50), df["int_rate"].head(50))
        plt.xlabel('Loan Amount')
        plt.ylabel("Interest rate")        
        #plt.xticks(rotation = 'vertical')
        st.pyplot(fig)








