# -*- coding: utf-8 -*-
"""LVADSUSR121_Regression_Lab1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BzrQfIEMDgo_CeG7zktRtmUS43GkgHoa
"""

#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
df1 = pd.read_csv('/content/drive/MyDrive/Predictive analytics Practice/Fare prediction.csv')
print(df1)

#Getting information about dataset
df1.info()

#Printing top 5 rows
df1.head()

#checking for null values
df1.isnull().sum()

# duplicate check
dup_no = df1.duplicated().sum()
print('Total number of duplicated records: ', dup_no)
# drop duplicates if exist
data1 = df1.drop_duplicates()

# outliers check
data_num = df1.drop(['pickup_datetime','key'],axis =1)
q1 = data_num.quantile(0.25)
q3 = data_num.quantile(0.75)
IQR = q3 - q1
threshold = 1.5
outliers = (data_num < (q1 - threshold * IQR)) | (data_num > (q3 + threshold * IQR))
data = data_num[~outliers.any(axis=1)]
print('Number of outliers removed: ', len(data_num) - len(data))

# Visualizing the distribution of the target variable 'fare_amount'
plt.figure(figsize=(8, 6))
sns.histplot(data['fare_amount'], bins=30, kde=True)
plt.title('Distribution of Fare Amount')
plt.xlabel('Fare Amount')
plt.ylabel('Frequency')
plt.show()

# Visualizing the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

numeric_columns = ['fare_amount', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']
plt.figure(figsize=(12, 8))
for i, column in enumerate(numeric_columns):
    plt.subplot(2, 3, i + 1)
    sns.histplot(data[column], kde=True)
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()

X = data[['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']]
y = data['fare_amount']

# Spliting the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = XGBRegressor()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
r2 = r2_score(y_test, y_pred)
print("R squared Error:", r2)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error (MAE):", mae)

"""From the above model for regression type problem, we found that, Mean squared 4.83, Mean absolute error of 1.557. so this gives transparent pricing to users and optimize earnings during peak and off-pear hours"""