# -*- coding: utf-8 -*-
"""Feature scaling Test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O3Tj8ROzxMJPMwREl3KItvJI5f-Ernhc

Importing necessary libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Load the Datasets"""

test_path = '/content/processed_Test_data.csv'
test_df = pd.read_csv(test_path)

print("Test Dataset")
display(test_df.head())

"""Visualize Test Data Before Log Transformation"""

# Select numerical columns
num_cols = ["luxury_sales", "fresh_sales", "dry_sales"]

# Create subplots for visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, col in enumerate(num_cols):
    sns.histplot(test_df[col], bins=30, kde=True, ax=axes[i])
    axes[i].set_title(f"Before Log Transformation: {col}")

plt.tight_layout()
plt.show()

"""Log Transformation"""

test_df[num_cols] = test_df[num_cols].apply(lambda x: np.log1p(x))

"""Visualize Test Data After Log Transformation"""

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, col in enumerate(num_cols):
    sns.histplot(test_df[col], bins=30, kde=True, ax=axes[i])
    axes[i].set_title(f"After Log Transformation: {col}")

plt.tight_layout()
plt.show()

"""Feature scaling"""

from sklearn.preprocessing import MinMaxScaler

# Select numerical columns to scale
features_to_scale = ['luxury_sales', 'fresh_sales', 'dry_sales']

# Initialize MinMaxScaler
scaler = MinMaxScaler()

# Fit on training data and transform both train & test sets
test_df[features_to_scale] = scaler.fit_transform(test_df[features_to_scale])

print("Feature Scaling Completed!")

# Preview first few rows of the scaled test dataset
print("\nPreview of Scaled Test Data:")
print(test_df.head())

"""Prepare Data for Model Training"""

test_df.drop(columns=['outlet_city'], inplace=True)

# Save the scaled dataset
output_path = "/content/Scaled_Test_data.csv"
test_df.to_csv(output_path, index=False)