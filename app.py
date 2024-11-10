# Required imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your dataset
df = pd.read_csv('supply_chain_data.csv')  # replace 'your_data.csv' with your actual data file

# Set the page configuration for Streamlit
st.set_page_config(page_title="Business Insights", layout="wide")

st.title("Business Insights Dashboard")
features = ['Overview', 'Product type', 'Customer demographics', 'Shipping carriers', 'Supplier name', 'Location', 'SKU', 'Transportation modes', 'Routes']
selected_feature = st.sidebar.selectbox("Choose a feature to analyze:", features)

# 0) Overview
if selected_feature == 'Overview':
    st.write('Overview of the Data')
    st.table(df.head())

    st.write('Statistics of the data')
    st.table(df.describe())

    st.write('Columns')
    st.table(df.columns)

    st.write('Correlation matrix')
    numeric_data = df.select_dtypes(include=['float64', 'int64'])  # Select only numeric columns
    if not numeric_data.empty:
        corr = numeric_data.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    

# 1) Product Type Analysis
if selected_feature == 'Product type':
    st.header("Product Type Analysis")
    st.subheader("Distribution of Product Types")

    # Distribution Pie Chart
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(df['Product type'].value_counts(), labels=df['Product type'].value_counts().index, autopct='%1.1f%%', pctdistance=0.85, colors=['teal', 'lightgreen', 'salmon'])
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title("Product Type")
    st.pyplot(fig)

    # Average Lead Time, Manufacturing Costs, and Defect Rate by Product Type
    st.subheader("Average Lead Time, Manufacturing Costs, and Defect Rate by Product Type")
    avg_lead_time = df.groupby('Product type')['Lead time'].mean().reset_index()
    avg_manufacturing_costs = df.groupby('Product type')['Manufacturing costs'].mean().reset_index()
    avg_defect_rate = df.groupby('Product type')['Defect rates'].mean().reset_index()
    result = pd.merge(avg_lead_time, avg_manufacturing_costs, on='Product type')
    result = pd.merge(result, avg_defect_rate, on='Product type')
    result.rename(columns={'Lead time': 'Average Lead Time', 'Manufacturing costs': 'Average Manufacturing Costs'}, inplace=True)
    st.write(result)

    # Barplots for each metric by Product Type
    metrics = {'Average Lead Time': 'Average Lead Time by Product Type', 
            'Average Manufacturing Costs': 'Average Manufacturing Costs by Product Type',
            'Defect rates': 'Defect Rate by Product Type'}

    for metric, title in metrics.items():
        fig, ax = plt.subplots()
        sns.barplot(data=result, x='Product type', y=metric, palette=['teal', 'lightgreen', 'salmon'], ax=ax)
        ax.set_title(title)
        st.pyplot(fig)

# 2) Customer Demographics Analysis
if selected_feature == 'Customer demographics':
    st.header("Customer Demographics Analysis")
    st.subheader("Customer Demographics Distribution")

    fig, ax = plt.subplots()
    sns.countplot(x='Customer demographics', data=df, palette=['lightgreen', 'salmon', 'teal', 'purple'], ax=ax)
    ax.set_title("Customer Demographics")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.countplot(x='Customer demographics', hue='Product type', data=df, palette=['salmon', 'teal', 'lightgreen'], ax=ax)
    ax.set_title("Product Type Distribution by Customer Demographics")
    ax.legend(title="Product Type")
    st.pyplot(fig)

# 3) Shipping Carrier Analysis
if selected_feature == 'Shipping carriers':
    st.header("Shipping Carrier Analysis")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(df['Shipping carriers'].value_counts(), labels=df['Shipping carriers'].value_counts().index, autopct='%1.1f%%', pctdistance=0.85, colors=['teal', 'lightgreen', 'salmon'])
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title("Shipping Carriers")
    st.pyplot(fig)

    # Revenue and Shipping Costs by Carrier
    revenue_by_carrier = df.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
    shipping_cost_by_carrier = df.groupby('Shipping carriers')['Shipping costs'].sum().reset_index()

    # Plot revenue and shipping costs
    fig, ax = plt.subplots()
    sns.barplot(data=revenue_by_carrier, x='Shipping carriers', y='Revenue generated', palette=['teal', 'lightgreen', 'salmon'], ax=ax)
    ax.set_title("Revenue by Shipping Carriers")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.barplot(data=shipping_cost_by_carrier, x='Shipping carriers', y='Shipping costs', palette=['teal', 'lightgreen', 'salmon'], ax=ax)
    ax.set_title("Shipping Costs by Carrier")
    st.pyplot(fig)

# 4) Supplier Analysis
if selected_feature == 'Supplier name':
    st.header("Supplier Analysis")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(df['Supplier name'].value_counts(), labels=df['Supplier name'].value_counts().index, autopct='%1.1f%%', pctdistance=0.85, colors=['teal', 'lightgreen', 'salmon', 'green', 'pink'])
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title("Supplier Name Distribution")
    st.pyplot(fig)

    revenue_by_supplier = df.groupby('Supplier name')['Revenue generated'].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=revenue_by_supplier, x='Supplier name', y='Revenue generated', palette=['teal', 'lightgreen', 'salmon', 'green', 'pink'], ax=ax)
    ax.set_title("Revenue by Supplier")
    st.pyplot(fig)

# 5) Location Analysis
if selected_feature == 'Location':
    st.header("Location Analysis")
    location_analysis = df.groupby('Location').agg({
        'Revenue generated': 'sum',
        'Order quantities': 'sum',
        'Defect rates': 'mean',
        'Lead time': 'mean',
        'Shipping costs': 'mean'
    }).reset_index()
    location_analysis.columns = ['Location', 'Total Revenue', 'Total Order Quantity', 'Average Defect Rate', 'Average Lead Time', 'Average Shipping Cost']
    st.write(location_analysis)

    # Plot each metric by Location
    metrics = {'Total Revenue': 'Total Revenue by Location',
            'Total Order Quantity': 'Total Order Quantity by Location',
            'Average Defect Rate': 'Average Defect Rate by Location',
            'Average Lead Time': 'Average Lead Time by Location',
            'Average Shipping Cost': 'Average Shipping Cost by Location'}

    for metric, title in metrics.items():
        fig, ax = plt.subplots()
        sns.barplot(data=location_analysis, x='Location', y=metric, palette=['teal', 'lightgreen', 'salmon', 'purple'], ax=ax)
        ax.set_title(title)
        st.pyplot(fig)

# 6) SKU Analysis
if selected_feature == 'SKU':
    st.header("SKU Analysis")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='SKU', y='Revenue generated', color='teal', ax=ax)
    ax.set_xticks(np.arange(0, len(df), step=5))
    ax.set_title("Revenue Generated by SKU")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='SKU', y='Stock levels', color='orange', ax=ax)
    ax.set_xticks(np.arange(0, len(df), step=5))
    ax.set_title("Stock Levels by SKU")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.barplot(data=df, x='SKU', y='Order quantities', color='salmon', ax=ax)
    ax.set_xticks(np.arange(0, len(df), step=5))
    ax.set_title("Order Quantities by SKU")
    st.pyplot(fig)

# 7) Transportation Model Analysis
if selected_feature == 'Transportation modes':
    st.header("Transportation Model Analysis")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(df['Transportation modes'].value_counts(), labels=df['Transportation modes'].value_counts().index, autopct='%1.1f%%', pctdistance=0.85, colors=['teal', 'lightgreen', 'salmon', 'gold'])
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title("Transportation Modes")
    st.pyplot(fig)

# 8) Routes Analysis
if selected_feature == 'Routes':
    st.header("Route Analysis")
    route_analysis = df.groupby('Routes').agg({
        'Revenue generated': 'sum',
        'Defect rates': 'mean',
        'Lead time': 'mean',
        'Shipping costs': 'mean'
    }).reset_index()

    route_analysis = route_analysis.rename(columns={
    'Revenue generated': 'Total Revenue',
    'Defect rates': 'Average Defect Rate',
    'Lead time': 'Average Lead Time',
    'Shipping costs': 'Average Shipping Cost'
    })

    # Total Revenue by Route
    fig = plt.figure(figsize=(8, 6))
    sns.barplot(data=route_analysis, x='Routes', y='Total Revenue', palette=['teal', 'lightgreen', 'salmon', 'purple'])
    plt.xlabel('Route')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue by Route')
    st.pyplot(fig)

    # Average Defect Rate by Route
    fig = plt.figure(figsize=(8, 6))
    sns.barplot(data=route_analysis, x='Routes', y='Average Defect Rate', palette=['teal', 'lightgreen', 'salmon', 'purple'])
    plt.xlabel('Route')
    plt.ylabel('Average Defect Rate')
    plt.title('Average Defect Rate by Route')
    plt.savefig('Average_Defect_Rate_by_Route.png')
    st.pyplot(fig)

    # Average Lead Time by Route
    fig = plt.figure(figsize=(8, 6))
    sns.barplot(data=route_analysis, x='Routes', y='Average Lead Time', palette=['teal', 'lightgreen', 'salmon', 'purple'])
    plt.xlabel('Route')
    plt.ylabel('Average Lead Time')
    plt.title('Average Lead Time by Route')
    plt.savefig('Average_Lead_Time_by_Route.png')
    st.pyplot(fig)

    # Average Shipping Cost by Route
    fig = plt.figure(figsize=(8, 6))
    sns.barplot(data=route_analysis, x='Routes', y='Average Shipping Cost', palette=['teal', 'lightgreen', 'salmon', 'purple'])
    plt.xlabel('Route')
    plt.ylabel('Average Shipping Cost')
    plt.title('Average Shipping Cost by Route')
    plt.savefig('Average_Shipping_Cost_by_Route.png')
    st.pyplot(fig)

