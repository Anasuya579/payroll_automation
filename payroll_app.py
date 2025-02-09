import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def main():
    st.title("🔄 AI-Powered Payroll Automation System")
    
    # File upload
    st.subheader("Upload Payroll Data")
    uploaded_file = st.file_uploader("Choose your Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        
        # Display original data
        st.subheader("Original Data Preview")
        st.dataframe(df.head())
        
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
        
        if st.button("🛠️ Fix Common Errors"):
            # Create a copy of the dataframe
            fixed_df = df.copy()
            
            # Fix common errors
            # 1. Recalculate Net Salary
            fixed_df['Net Salary (INR)'] = fixed_df['Gross Salary (INR)'] - fixed_df['Tax Deduction (INR)']
            
            # 2. Flag unusual work hours
            fixed_df['Work Hours Flag'] = fixed_df['Work Hours (Monthly)'].apply(
                lambda x: 'Check Required' if x > 200 or x < 140 else 'OK'
            )
            
            # Display fixed data
            st.write("✅ Fixed Data Preview:")
            st.dataframe(fixed_df)
            
            # Download option for fixed data
            st.download_button(
                label="📥 Download Fixed Data",
                data=fixed_df.to_csv(index=False).encode('utf-8'),
                file_name=f'fixed_payroll_data_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )
        
        if st.button("📊 Generate Report"):
            # Create report
            st.subheader("📑 Payroll Processing Report")
            
            # Summary statistics
            st.write("Summary Statistics:")
            summary_stats = {
                "Total Employees": len(df),
                "Total Salary Payout": f"₹{df['Gross Salary (INR)'].sum():,.2f}",
                "Average Salary": f"₹{df['Gross Salary (INR)'].mean():,.2f}",
                "Total Tax Deductions": f"₹{df['Tax Deduction (INR)'].sum():,.2f}",
                "Average Resolution Time": f"{df['Query Resolution Time (hrs)'].mean():.2f} hours"
            }
            
            for key, value in summary_stats.items():
                st.write(f"**{key}:** {value}")
            
            # Department-wise summary
            st.write("\nDepartment-wise Summary:")
            dept_summary = df.groupby('Department').agg({
                'Employee ID': 'count',
                'Gross Salary (INR)': 'sum',
                'Tax Deduction (INR)': 'sum'
            })
            st.dataframe(dept_summary)
            
            # Generate downloadable report
            report_df = pd.DataFrame(summary_stats.items(), columns=['Metric', 'Value'])
            st.download_button(
                label="📥 Download Report",
                data=report_df.to_csv(index=False).encode('utf-8'),
                file_name=f'payroll_report_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()
