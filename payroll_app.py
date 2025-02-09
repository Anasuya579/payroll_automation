if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Display original data
    st.subheader("Original Data Preview")
    st.dataframe(df.head())
    
    # Check column names
    st.write("Column Names in the Uploaded File:")
    st.write(list(df.columns))  # Display all column names for debugging
    
    # Ensure required columns exist
    required_columns = ['Payroll Errors', 'Compliance Issue', 'Department', 'Gross Salary (INR)',
                        'Query Resolution Time (hrs)', 'Payroll Query Type', 'Tax Deduction (INR)', 
                        'Work Hours (Monthly)']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"The following required columns are missing: {', '.join(missing_columns)}")
    else:
        # Analysis and Automation Options
        st.subheader("Select Automation Tasks")
        
        if st.button("🔍 Analyze Payroll Data"):
            # Error Detection
            error_records = df[df['Payroll Errors'] == 'Y']
            compliance_issues = df[df['Compliance Issue'] == 'Y']
            
            # Display Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Error Rate", f"{(len(error_records)/len(df))*100:.1f}%")
            with col3:
                st.metric("Compliance Issues", f"{(len(compliance_issues)/len(df))*100:.1f}%")
            
            # Detailed Analysis
            st.subheader("📊 Detailed Analysis")
            
            # Department-wise analysis
            st.write("Department-wise Statistics:")
            dept_analysis = df.groupby('Department').agg({
                'Gross Salary (INR)': 'mean',
                'Payroll Errors': lambda x: (x == 'Y').mean() * 100,
                'Query Resolution Time (hrs)': 'mean'
            }).round(2)
            dept_analysis.columns = ['Avg Salary', 'Error Rate %', 'Avg Resolution Time (hrs)']
            st.dataframe(dept_analysis)
            
            # Error Analysis
            if len(error_records) > 0:
                st.write("🚨 Records with Errors:")
                st.dataframe(error_records)
            
            # Query Analysis
            st.write("📝 Query Type Analysis:")
            query_analysis = df['Payroll Query Type'].value_counts()
            st.write(query_analysis)
