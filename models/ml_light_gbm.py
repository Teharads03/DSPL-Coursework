# -*- coding: utf-8 -*-
"""ML_Light_GBM-4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LERhiklI9onfIPwxfC9e-_M_3d_3vSyy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder,label_binarize
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error
from sklearn.metrics import roc_curve, auc

from google.colab import drive
drive.mount('/content/drive')

# Load the dataset
df = pd.read_csv('/content/Scaled_Train_data.csv')
print("Dataset Loaded Successfully!\n")

# Display basic info
display(df.head())
display(df.info())
display(df.describe())

# Define X and Y variables
X = df[['luxury_sales','fresh_sales','dry_sales','outlet_city_encoded']] # Change x to X
y = df['cluster_catgeory']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Import necessary libraries
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder

# ... (your existing code) ...

# Create a LabelEncoder object
encoder = LabelEncoder()

# Fit the encoder to the 'outlet_city' column in the training data and transform it
X_train['outlet_city_encoded'] = encoder.fit_transform(X_train['outlet_city_encoded'])

# Transform the 'outlet_city' column in the testing data using the trained encoder
X_test['outlet_city_encoded'] = encoder.transform(X_test['outlet_city_encoded'])

# Initialize and train LightGBM model
model = lgb.LGBMRegressor(objective='regression', num_leaves=31, learning_rate=0.05, n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Function to make predictions
def predict_new_data(new_data):
    new_data = pd.DataFrame([new_data], columns=X.columns)  # Ensure correct format
    new_data = scaler.transform(new_data)  # Scale features
    prediction = model.predict(new_data)
    return prediction

def evaluate_model():
    # Define is_classification here based on your model type
    is_classification = False  # Set to True if using a classification model, otherwise False

    if is_classification:
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
        print("Accuracy:", accuracy_score(y_test, y_pred))
    else:
        print("\nRegression Performance:")
        print("MAE:", mean_absolute_error(y_test, y_pred))
        print("MSE:", mean_squared_error(y_test, y_pred))
        print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

        # Import r2_score
        from sklearn.metrics import r2_score

        print("R^2 Score:", r2_score(y_test, y_pred))

# Call the evaluation function
evaluate_model()

# Convert regression predictions into categorical bins
num_bins = 5  # Define number of bins for classification
y_pred_class = pd.qcut(y_pred, num_bins, labels=False)  # Discretizing into bins
print("\nPredictions Converted to Class Table:")
print(pd.DataFrame({'Actual': y_test.values, 'Predicted Continuous': y_pred, 'Predicted Class': y_pred_class}))

# Determine Model Type (Classification or Regression)
is_classification = len(np.unique(y)) <= 10  # Assuming classification if target has ≤10 unique values

# Import confusion_matrix here
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

if is_classification:
    # LightGBM Classifier with Regularization to Prevent Overfitting
    model = lgb.LGBMClassifier(num_leaves=8, learning_rate=0.01, n_estimators=30, reg_alpha=0.1, reg_lambda=0.1, random_state=42)
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate accuracy
    train_accuracy = round(accuracy_score(y_train, y_train_pred), 3)
    test_accuracy = round(accuracy_score(y_test, y_test_pred), 3)

    print("\n=== Training Classification Report ===")
    print(classification_report(y_train, y_train_pred))
    print("\n=== Testing Classification Report ===")
    print(classification_report(y_test, y_test_pred))

    print("\n=== Training Confusion Matrix ===")
    print(confusion_matrix(y_train, y_train_pred))
    print("\n=== Testing Confusion Matrix ===")
    print(confusion_matrix(y_test, y_test_pred))

    print(f"\nTraining Accuracy: {train_accuracy}, Testing Accuracy: {test_accuracy}")

    if train_accuracy > test_accuracy:
        print("\nThe model might be overfitting.")
    elif train_accuracy < test_accuracy:
        print("\nThe model might be underfitting.")
    else:
        print("\nThe model appears to be well-fitted.")

else:
    # LightGBM Regressor
    # You can add code here for the regression case if needed
    pass  # This 'pass' statement will prevent the SyntaxError

# Import necessary libraries
from sklearn.metrics import confusion_matrix

# Generate confusion matrix if using a classification model
if is_classification:

    # Generate confusion matrix for the test set
    test_cm_gb = confusion_matrix(y_test, y_test_pred)


# Plot confusion matrix for test set (only if using a classification model)
if is_classification:
    plt.subplot(1, 2, 2)
    sns.heatmap(test_cm_gb, annot=True, fmt="d", cmap="Blues", xticklabels=np.unique(y), yticklabels=np.unique(y))
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix - Test Set")

    plt.show()

# Get feature importances from the model
importances = model.feature_importances_

# Create a DataFrame for feature importances
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

# Sort the DataFrame by importance
importance_df = importance_df.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
plt.title('Feature Importance - LightGBM')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.show()

# Compute correlation matrix
corr_matrix = df.select_dtypes(include=np.number).corr()

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

from sklearn.metrics import accuracy_score

# Assuming 'model' is already trained

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Accuracy scores
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Print accuracies
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Load the scaled test data (replace with your actual file path if different)
test_data = pd.read_csv('/content/Scaled_Test_data.csv')

# Instead of assuming 'Customer_ID', create a sequence for it
# if 'Customer_ID' is not in your test_data columns
if 'Customer_ID' not in test_data.columns:
    Customer_ID = pd.Series(range(1, len(test_data) + 1), name='Customer_ID')
else:
    Customer_ID = test_data['Customer_ID']

# Drop 'Customer_ID' to keep only features for prediction
X_test = test_data.drop(columns=['Customer_ID'], errors='ignore') # Ignore if 'Customer_ID' not found

# Ensure you have a trained LightGBM model object named 'model'
predictions = model.predict(X_test)

# Create a DataFrame with required format
output_df = pd.DataFrame({
    'Customer_ID': Customer_ID,
    'cluster_category': predictions
})

# Save the output to the specified file path
output_file_path = '/content/sample_data/Light_GBM_Predictions.CSV'
output_df.to_csv(output_file_path, index=False)

print(f"Predictions saved successfully to {output_file_path}")

from google.colab import files
files.download('/content/sample_data/Light_GBM_Predictions.CSV')

