# -*- coding: utf-8 -*-
"""EDA_before_preprocessingTrain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xl_Hohlp1-i7nvoERiI_HpNb0M00N47x
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

train_path = "/content/traincsv.csv"
train_df = pd.read_csv(train_path)

"""Univariate Analysis"""

#Histograms
sales_cols = ['luxury_sales', 'fresh_sales', 'dry_sales']
train_df[sales_cols] = train_df[sales_cols].apply(pd.to_numeric, errors='coerce')
numeric_cols = train_df.drop(columns=['Customer_ID']).select_dtypes(include=['number']).columns

train_df[numeric_cols].hist(figsize=(12, 8), bins=20)
plt.suptitle("Feature Distributions Before Filling Missing Values")
plt.show()

train_df['outlet_city'].unique()

train_df['cluster_catgeory'].unique()

# Count Plots for Categorical Variables
categorical_columns = train_df.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    plt.figure(figsize=(8, 4))
    sns.countplot(y=train_df[col], order=train_df[col].value_counts().index)
    plt.title(f"Count Plot of {col}")
    plt.show()

#Boxplots to Identify Outliers
# Ensure numeric columns
numeric_cols = ['luxury_sales', 'fresh_sales', 'dry_sales']

# Generate Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=train_df[numeric_cols])
plt.title("Boxplot of Numeric Features (Train Data)")
plt.xticks(rotation=45)
plt.show()

"""Bivariate Analysis"""

#Scatter Plot (for numerical features vs numerical features)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=train_df['luxury_sales'], y=train_df['fresh_sales'])
plt.title("Scatter Plot: Luxury Sales vs Fresh Sales")
plt.xlabel('Luxury Sales')
plt.ylabel('Fresh Sales')
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x=train_df['luxury_sales'], y=train_df['dry_sales'])
plt.title("Scatter Plot: Luxury Sales vs Dry Sales")
plt.xlabel('Luxury Sales')
plt.ylabel('Dry Sales')
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x=train_df['dry_sales'], y=train_df['fresh_sales'])
plt.title("Scatter Plot: dry Sales vs fresh Sales")
plt.xlabel('dry Sales')
plt.ylabel('fresh Sales')
plt.show()

#Barplot
# Melt the dataset to combine all sales columns into one for plotting
melted_df = train_df.melt(id_vars=['outlet_city'], value_vars=['luxury_sales', 'fresh_sales', 'dry_sales'],
                          var_name='sales_category', value_name='sales')

# Plot the average of each sales category by outlet city
plt.figure(figsize=(12, 6))
sns.barplot(x="outlet_city", y="sales", hue="sales_category", data=melted_df, estimator='mean',ci=None)
plt.title("Average Sales by Outlet City for Each Category")
plt.xticks(rotation=90, fontsize=10)
plt.show()

"""Multivariate Analysis"""

import seaborn as sns
import matplotlib.pyplot as plt

# Calculate correlation matrix
corr_matrix = train_df[['luxury_sales', 'fresh_sales', 'dry_sales']].corr()

# Create heatmap
plt.figure(figsize=(8, 6))  # Adjust figure size if needed
sns.heatmap(corr_matrix, annot=True, cmap='viridis', fmt=".2f")
plt.title("Correlation Heatmap Before")
plt.show()

for col in ['luxury_sales', 'fresh_sales', 'dry_sales']:
    plt.figure(figsize=(8,4))
    sns.boxplot(x='cluster_catgeory', y=col, data=train_df)
    plt.title(f'{col} by Cluster Before')
    plt.show()

# Group by cluster and calculate means for sales columns
cluster_summary = train_df.groupby('cluster_catgeory')[['luxury_sales', 'fresh_sales', 'dry_sales']].mean()

# Round for readability
cluster_summary = cluster_summary.round(2)
print(cluster_summary)

# Reset index to use cluster as x-axis
cluster_summary_plot = cluster_summary.reset_index().melt(id_vars='cluster_catgeory')

plt.figure(figsize=(10, 6))
sns.barplot(x='cluster_catgeory', y='value', hue='variable', ci=None,data=cluster_summary_plot)
plt.title('Average Spending per Category by Cluster')
plt.ylabel('Average Monthly Sales')
plt.xlabel('Cluster Category')
plt.legend(title='Category')
plt.show()