import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb
import re  

st. title(":red[Exploratory Data Analysis of Banking and Finance]")

st.write("This Web app gives the banking and finance sector insight on the loan applicants which makes it easier for them to apprve of their loan. This App aims to identify patterns that indicate if an applicant will repay their instalments which may be used for taking further actions such as denying the loan, reducing the amount of loan, lending at a higher interest rate, etc.")


# Upload Data in txt, csv or pdf formats
st.sidebar.title("EDA of Banking and Finance")
user_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "csv"], accept_multiple_files=False)

# When the file gets uploaded 
if user_file is not None:
    #Read file type csv pdf and txt only  loan.csv
    #splitting 
    ext = user_file.name.split(".")[-1]
    #st.write(ext)

    st.header(" Dataframe  ")
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
    null = (df.isnull().sum()/len(df)*100).sort_values(ascending = False)
    #st.write(null.values)
    # columns with more than 30% of null values
    null = null[null.values>30]
    null_list = list(null.index.values)
    #st.write(null_list)
    
    # Remove all the columns with null values greater than 30%
    df = df.drop(labels = null_list, axis=1) 
    #df = df[df.loc[:, (df!=0).all(axis=1)]]
    
    # Removing Unwanted columns
    df = df.drop(["delinq_2yrs","pub_rec","initial_list_status","out_prncp","out_prncp_inv","collections_12_mths_ex_med","policy_code","acc_now_delinq","chargeoff_within_12_mths","delinq_amnt","pub_rec_bankruptcies","tax_liens"], axis = 1)
    
    # replacing the rest of columns with less than 30 % null values with mode.
    cols = ["emp_title", "title", "revol_util","last_pymnt_d","last_credit_pull_d","emp_length"]
    df[cols]=df[cols].fillna(df.mode().iloc[0])

    # Converting Interest rate column from strig to numeric data
    df['int_rate'] = df['int_rate'].str.rstrip("%").astype(float)    
    #df = df.sample(100)
    df = df.reset_index()
    v2 = st.write(df) 
    
    v3 = st.write("Total Number of data present ")
    v4 = st.write(df.shape)
    
    # On pressing the Show Statistical Info Button
    if st.sidebar.button("Show EDA"):
        
        #st.header("Pandas profiling of the data")
        s_info = st.write(df.info())
        

        # Statistical information of the dataframe 
        st.header("Statistacal information of the dataframe")
        stat = st.write(df.describe())
        
        cl1, cl2 = st.columns(2)
        with cl1:
        #Listing all the variables
            st.header("Variables")
            var = st.write(df.columns.values)   
        with cl2:
            # Get unique values of purpose coumn
            #st.header("Purpose ")
            #st.write(df['purpose'].value_counts())
         
         # All fully paid loans / Current /Defaulters
        
            df_fully_paid = df[df["loan_status"]=="Fully Paid"]
            df_current = df[df["loan_status"]=="Current"]
            df_defaulters = df[df["loan_status"]=="Charged Off"]
        #st.dataframe(df_fully_paid)
        #st.write(df_fully_paid.shape[0])0
        #st.dataframe(df_current)
        #st.write(df_current.shape[0])
        #st.dataframe(df_defaulters)
        #st.write(df_defaulters.shape[0])
        
        #st.write(df['home_ownership'].value_counts())
        # Employment title 
        #df_fully_paid_emp = df_fully_paid[df_fully_paid["emp_title"]==""]


        t1,t2 = st.tabs(["**Univariate Analysis**", "**Bivariate Analysis**"], )
                
        with t1:
            #
            st.header("Outliers")
           
            
            
            red_circle = dict(markerfacecolor="red", marker = "o")
            green_circle = dict(markerfacecolor="green", marker = "o")
            fig = plt.figure()

            plt.rcParams['font.size'] = 10
            df["annual_inc"].plot(kind="box",title = "Annual income of the loan lenders", figsize = (3,3), flierprops = red_circle)
            plt.semilogy()
            st.pyplot(fig)

            fig = plt.figure()
            plt.rcParams['font.size'] = 10
            df["int_rate"].plot(kind="box",title = "Interest Rate", figsize = (3,3), flierprops = green_circle)
            st.pyplot(fig)
            
            fig = plt.figure()
            plt.rcParams['font.size'] = 18
            df["loan_amnt"].plot(kind="box",title = "Loan amount Sanctioned", figsize = (3,3), flierprops = red_circle)
            st.pyplot(fig)
            
            fig = plt.figure()
            plt.rcParams['font.size'] = 18
            df["installment"].plot(kind="box",title = "Installment", figsize = (3,3), flierprops = green_circle)
            st.pyplot(fig)

            #df1 = df.head(100)
            fig,ax = plt.subplots()
            plt.rcParams['font.size'] = 18
            fig = plt.figure(figsize= (5,5))
        
            plt.bar(df["loan_amnt"], df.index, color = "red")
            plt.xlabel("Loan Amount") 
            plt.rcParams['font.size'] = 18
            plt.title("No.of times a particular loan amount is sanctioned")
            st.pyplot(fig)

            st.header("Insights:")
            st.text("The above plots infer that there are a lot of outliers, and lower loan amounts are sanction for high interest rate, which may also lead to high risk of default.")
            
            x = ["Fully_paid", "Current","Defaulters"]
            y =[df_fully_paid.shape[0], df_current.shape[0], df_defaulters.shape[0]]
            fig,ax = plt.subplots()
            
            plt.rcParams['font.size'] = 10
            fig = plt.figure(figsize= (5,5))
            plt.bar(x, y, width = 0.2)
            plt.title("Loan Status")
            plt.xlabel('Loan status')
            plt.ylabel("Number")        
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            st.write("The above figure indicates that there are about 14.16% of defaulters who did not pay the loan back.")

    
        
        with t2:
            #Cross tab method to find the relation between the annual income and loan status
            st.markdown(":red[Relation between the annual income and loan status]")
            a = pd.crosstab(df["annual_inc"], df["loan_status"])
            st.write(a)
            st.write("**Insight:**")
            st.write("From the above tableit can be concluded that clients with annual income from 15000 to 50000, are likely to be defaulters")

            ##Cross tab method to find the relation between the house ownership and loan status
            st.markdown(":red[Relation between the House ownership and loan status]")
            b = pd.crosstab(df["home_ownership"], df["loan_status"])
            st.write(b)
            st.write("Insight:")
            st.write("From the above table, we can get the insight that the clients living for rent are likely to be defaulters.")

            # Fully paid loans with purpose debt_consolidation
            df_fp_dc = df_fully_paid[df_fully_paid["purpose"]=="debt_consolidation"]
            df_fp_dc.reset_index()
            # Fully paid loans with purpose credit card
            df_fp_cd = df_fully_paid[df_fully_paid["purpose"]=="credit_card"]
            df_fp_cd.reset_index()
            # Fully paid loans with purpose other
            df_fp_ot = df_fully_paid[df_fully_paid["purpose"]=="other"]
            df_fp_ot.reset_index()
            # Fully paid loans with purpose home_improvement &house loan
            df_fp_home1 = df_fully_paid[df_fully_paid["purpose"]=="home_improvement"]
            df_fp_home2 = df_fully_paid[df_fully_paid["purpose"]=="house"]
            df_fp_house = pd.concat([df_fp_home1,df_fp_home2])
            df_fp_house.reset_index()
            #Fully paid loans with purpose major_purchase
            df_fp_mp = df_fully_paid[df_fully_paid["purpose"]=="major_purchase"]
            df_fp_mp.reset_index()
            # Fully paid loans with purpose small_business
            df_fp_sb = df_fully_paid[df_fully_paid["purpose"]=="small_business"]
            df_fp_sb.reset_index()
            # Fully paid loans with purpose car
            df_fp_car = df_fully_paid[df_fully_paid["purpose"]=="car"]
            df_fp_car.reset_index()
            # Fully paid loans with purpose wedding
            df_fp_wed = df_fully_paid[df_fully_paid["purpose"]=="wedding"]
            df_fp_wed.reset_index()
            # Fully paid loans with purpose moving
            df_fp_mov = df_fully_paid[df_fully_paid["purpose"]=="moving"]
            df_fp_mov.reset_index()
            # Fully paid loans with purpose medical
            df_fp_med = df_fully_paid[df_fully_paid["purpose"]=="medical"]
            df_fp_med.reset_index()
            # Fully paid loans with purpose vacation
            df_fp_vc = df_fully_paid[df_fully_paid["purpose"]=="vacation"]
            df_fp_vc.reset_index()
            # Fully paid loans with purpose educational
            df_fp_edu = df_fully_paid[df_fully_paid["purpose"]=="educational"]
            df_fp_edu.reset_index()
            # Fully paid loans with purpose renewable_energy
            df_fp_ren = df_fully_paid[df_fully_paid["purpose"]=="renewable_energy"]
            df_fp_ren.reset_index()


            # Current loans with purpose debt_consolidation
            df_ct_dc = df_current[df_current["purpose"]=="debt_consolidation"]
            df_ct_dc.reset_index()
            #   Current loans with purpose credit card
            df_ct_cd = df_current[df_current["purpose"]=="credit_card"]
            df_ct_cd.reset_index()
            # Current loans with purpose other
            df_ct_ot = df_current[df_current["purpose"]=="other"]
            df_ct_ot.reset_index()
            # Current loans with purpose home_improvement
            df_ct_home1 = df_current[df_current["purpose"]=="home_improvement"]
            df_ct_home2 = df_current[df_current["purpose"]=="house"]
            df_ct_house = pd.concat([df_ct_home1,df_ct_home2])
            df_ct_house.reset_index()
            # Current loans with purpose major_purchase
            df_ct_mp = df_current[df_current["purpose"]=="major_purchase"]
            df_ct_mp.reset_index()
            # Current loans with purpose small_business
            df_ct_sb = df_current[df_current["purpose"]=="small_business"]
            df_ct_sb.reset_index()
            # Current loans with purpose car
            df_ct_car = df_current[df_current["purpose"]=="car"]
            df_ct_car.reset_index()
             # Current loans with purpose wedding
            df_ct_wed = df_current[df_current["purpose"]=="wedding"]
            df_ct_wed.reset_index()
            # Current loans with purpose moving
            df_ct_mov = df_current[df_current["purpose"]=="moving"]
            df_ct_mov.reset_index()
            # Current loans with purpose medical
            df_ct_med = df_current[df_current["purpose"]=="medical"]
            df_ct_med.reset_index()
            # Current loans with purpose vacation
            df_ct_vc = df_current[df_current["purpose"]=="vacation"]
            df_ct_vc.reset_index()
            # Currentloans with purpose educational
            df_ct_edu = df_current[df_current["purpose"]=="educational"]
            df_ct_edu.reset_index()
            # Current loans with purpose renewable_energy
            df_ct_ren = df_current[df_current["purpose"]=="renewable_energy"]
            df_ct_ren.reset_index()

            
       
            # Defaulters loans with purpose debt_consolidation
            df_df_dc = df_defaulters[df_defaulters["purpose"]=="debt_consolidation"]
            # Defaulters loans with purpose credit card
            df_df_cd = df_defaulters[df_defaulters["purpose"]=="credit_card"]
            # Defaulters loans with purpose other
            df_df_ot = df_defaulters[df_defaulters["purpose"]=="other"]
            # Defaulters loans with purpose home_improvement
            df_df_home1 = df_defaulters[df_defaulters["purpose"]=="home_improvement"]
            df_df_home2 = df_defaulters[df_defaulters["purpose"]=="house"]
            df_df_house = pd.concat([df_df_home1,df_df_home2])
            df_df_house.reset_index()
            # Defaulters loans with purpose major_purchase
            df_df_mp = df_defaulters[df_defaulters["purpose"]=="major_purchase"] 
            # Defaulters loans with purpose small_business
            df_df_sb = df_defaulters[df_defaulters["purpose"]=="small_business"]
            df_df_sb.reset_index() 
            # Defaulters loans with purpose car
            df_df_car = df_defaulters[df_defaulters["purpose"]=="car"]
            df_df_car.reset_index()   
            # Defaulters loans with purpose wedding
            df_df_wed = df_defaulters[df_defaulters["purpose"]=="wedding"]
            df_df_wed.reset_index()
            # Defaulters loans with purpose moving
            df_df_mov = df_defaulters[df_defaulters["purpose"]=="moving"]
            df_df_mov.reset_index()
            # Defaulters loans with purpose medical
            df_df_med = df_defaulters[df_defaulters["purpose"]=="medical"]
            df_df_med.reset_index()
            # Defaulters loans with purpose vacation
            df_df_vc = df_defaulters[df_defaulters["purpose"]=="vacation"]
            df_df_vc.reset_index()
            # Defaulters loans with purpose educational
            df_df_edu = df_defaulters[df_defaulters["purpose"]=="educational"]
            df_df_edu.reset_index()
            # Defaulters loans with purpose renewable_energy
            df_df_ren = df_defaulters[df_defaulters["purpose"]=="renewable_energy"]
            df_df_ren.reset_index()
 
            
# Plotting Group Bar chart1
            
            xg = ["debt_consolidation","credit_card", "other"]
            x_val = np.arange(len(xg))
            yg1 = [df_fp_dc.shape[0],df_fp_cd.shape[0],df_fp_ot.shape[0]]
            yg2 = [df_ct_dc.shape[0],df_ct_cd.shape[0],df_ct_ot.shape[0]]
            yg3 = [df_df_dc.shape[0],df_df_cd.shape[0],df_df_ot.shape[0]]           
            width = 0.25
            
            fig, ax = plt.subplots()
            plt.rcParams['font.size'] = 10
            
            plt.bar(x_val - width, yg1, width, color = "yellow")
            plt.bar(x_val, yg2, width, color = "cyan")
            plt.bar(x_val + width, yg3, width, color = "green")
            plt.xticks(x_val, ["debt_consolidation","credit_card", "other"])
            plt.xlabel("Purpose of loan")
            plt.ylabel("Values")
            plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            st.pyplot(fig)
# Plotting Group Bar chart2
            xg1 = ["house","major_purchase", "small_business"]
            x_val1 = np.arange(len(xg))
            yg11 = [df_fp_house.shape[0],df_fp_mp.shape[0],df_fp_sb.shape[0]]
            yg21 = [df_ct_house.shape[0],df_ct_mp.shape[0],df_ct_sb.shape[0]]
            yg31 = [df_df_house.shape[0],df_df_mp.shape[0],df_df_sb.shape[0]]           
            width = 0.25
            
            fig, ax = plt.subplots()
            plt.rcParams['font.size'] = 10
            plt.bar(x_val1 - width, yg11, width, color = "yellow")
            plt.bar(x_val1, yg21, width, color = "cyan")
            plt.bar(x_val1 + width, yg31, width, color = "green")
            plt.xticks(x_val1, ["house","major_purchase", "small_business"])
            plt.xlabel("Purpose of loan")
            plt.ylabel("Values")
            plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            st.pyplot(fig)
# Plotting Group Bar chart3
            xg2 = ["car","wedding", "moving"]
            x_val2 = np.arange(len(xg2))
            yg12 = [df_fp_car.shape[0],df_fp_wed.shape[0],df_fp_mov.shape[0]]
            yg22 = [df_ct_car.shape[0],df_ct_wed.shape[0],df_ct_mov.shape[0]]
            yg32 = [df_df_car.shape[0],df_df_wed.shape[0],df_df_mov.shape[0]]           
            width = 0.25
            
            fig, ax = plt.subplots()
            plt.bar(x_val2 - width, yg12, width, color = "yellow")
            plt.bar(x_val2, yg22, width, color = "cyan")
            plt.bar(x_val2 + width, yg32, width, color = "green")
            plt.xticks(x_val1, ["car","wedding", "moving"])
            plt.xlabel("Purpose of loan")
            plt.ylabel("Values")
            plt.rcParams['font.size'] = 10
            plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            st.pyplot(fig)          
# Plotting Group Bar chart4
            xg3 = ["medical","vacation", "educational"]
            x_val3 = np.arange(len(xg3))
            yg13 = [df_fp_med.shape[0],df_fp_vc.shape[0],df_fp_edu.shape[0]]
            yg23 = [df_ct_med.shape[0],df_ct_vc.shape[0],df_ct_edu.shape[0]]
            yg33 = [df_df_med.shape[0],df_df_vc.shape[0],df_df_edu.shape[0]]           
            width = 0.25
            
            fig, ax = plt.subplots()
            plt.bar(x_val3 - width, yg13, width, color = "yellow")
            plt.bar(x_val3, yg23, width, color = "cyan")
            plt.bar(x_val3 + width, yg33, width, color = "green")
            plt.xticks(x_val3,  ["medical","vacation", "educational"])
            plt.xlabel("Purpose of loan")
            plt.ylabel("Values")
            plt.rcParams['font.size'] = 10
            plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            st.pyplot(fig)   

# Bar 5

            xg4 = ["renewable energy"]
            x_val4 = np.arange(len(xg4))
            yg33 = [df_fp_ren.shape[0],df_ct_ren.shape[0],df_df_ren.shape[0]]           
            width = 0.1
            fig, ax = plt.subplots()
            plt.bar(x_val4 - width, yg13, width, color = "yellow")
            plt.bar(x_val4, yg23, width, color = "cyan")
            plt.bar(x_val4 + width, yg33, width, color = "green")
            plt.xticks(x_val4, ["renewable energy"])
            plt.xlabel("Purpose of loan")
            plt.ylabel("Values")
            plt.rcParams['font.size'] = 10
            plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            st.pyplot(fig)  

            # House Ownership- Fully Paid
            
            df_fp_rent = df_fully_paid[df_fully_paid["home_ownership"]=="RENT"]
            df_fp_rent.reset_index()
            df_fp_mort = df_fully_paid[df_fully_paid["home_ownership"]=="MORTAGE"]
            df_fp_mort.reset_index()
            df_fp_own = df_fully_paid[df_fully_paid["home_ownership"]=="OWN"]
            df_fp_own.reset_index()
            df_fp_other = df_fully_paid[df_fully_paid["home_ownership"]=="OTHER"]
            df_fp_other.reset_index()
            df_fp_none = df_fully_paid[df_fully_paid["home_ownership"]=="NONE"]
            df_fp_none.reset_index()
        
            # House Ownership- Current
            
            df_ct_rent = df_current[df_current["home_ownership"]=="RENT"]
            df_ct_rent.reset_index()
            df_ct_mort = df_current[df_current["home_ownership"]=="MORTAGE"]
            df_ct_mort.reset_index()
            df_ct_own = df_current[df_current["home_ownership"]=="OWN"]
            df_ct_own.reset_index()
            df_ct_other = df_current[df_current["home_ownership"]=="OTHER"]
            df_ct_other.reset_index()
            df_ct_none = df_current[df_current["home_ownership"]=="NONE"]
            df_ct_none.reset_index()
            
            # House Ownership- Defaulters
            
            df_df_rent = df_defaulters[df_defaulters["home_ownership"]=="RENT"]
            df_df_rent.reset_index()
            df_df_mort = df_defaulters[df_defaulters["home_ownership"]=="MORTAGE"]
            df_df_mort.reset_index()
            df_df_own = df_defaulters[df_defaulters["home_ownership"]=="OWN"]
            df_df_own.reset_index()
            df_df_other = df_defaulters[df_defaulters["home_ownership"]=="OTHER"]
            df_df_other.reset_index()
            df_df_none = df_defaulters[df_defaulters["home_ownership"]=="NONE"]
            df_df_none.reset_index()
            
            # Plotting grouped bar chart

            
           # w = 0.2
            #x = ["RENT", "MORTAGE", "OWN","OTHER","NONE"]
            #xf = np.arange(len(x))
           # xc = [i+w for i in xf]
           # xd = [i+w for i in xc]
           # yf = [df_fp_rent,df_fp_mort,df_fp_own,df_fp_other,df_fp_none]
           #yc = [df_ct_rent,df_ct_mort,df_ct_own,df_ct_other,df_ct_none]
           # yd = [df_df_rent,df_df_mort,df_df_own,df_df_other,df_df_none]
            
            
            
            #fig, ax = plt.subplots()
            #plt.bar(xf, yf, w, color = "teal")  
            #plt.bar(xc, yc, w, color = "lightblue")
            #plt.bar(xd, yd, w, color = "lightgreen")
            #plt.xticks(x1,  ["RENT", "MORTAGE", "OWN","OTHER","NONE"])
            #plt.xlabel("Home_Ownershipn")
            #plt.ylabel("Values")
            #plt.rcParams['font.size'] = 10
            #plt.legend(["Fully Paid Loan","Current Loan","Defaulters"])
            #st.pyplot(fig)   
            

            #df1 = df[df["purpose"]=="debt_consolidation"]
            y1 = df["loan_amnt"].head(100)
            x1 = df["int_rate"].head(100)


            st.title("Loan Amount versus Interest rate")
            fig,ax = plt.subplots()
            fig = plt.figure(figsize= (3,2))

            plt.scatter(x1, y1)
            plt.xlabel('Loan Amount')
            plt.ylabel("Interest rate")  
            plt.rcParams['font.size'] = 10     
            #plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            st.header("Insights:")
            st.write("Most of the loans applied are for the debt consolidation. Clients applying for high and low credit,clients with home ownership on rent and clients with annual income betweem 15000/- to 50000/- are at high risk of default. ")
            #st.write(" And also since there is a huge imbalance in the data(i.e., uploaded data is not equally distributed among all the variables), it is difficult to conclude ")







