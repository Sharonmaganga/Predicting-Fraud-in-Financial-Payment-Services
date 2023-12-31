# -*- coding: utf-8 -*-
"""Online Payments Fraud Dectection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tMN3LAVkcgU6XUy5RVOWo7lJ9Jq0aKde

**Online Payments Fraud Detection with Machine Learning**

To identify online payment fraud with machine learning, we need to train a machine learning model for classifying fraudulent and non-fraudulent payments. For this, we need a dataset containing information about online payment fraud, so that we can understand what type of transactions lead to fraud. For this task, I collected a dataset from Kaggle, which contains historical information about fraudulent transactions which can be used to detect fraud in online payments. Below are all the columns from the dataset I’m using here:




1.  step: represents a unit of time where 1 step equals 1 hour
2.  type: type of online transaction
3.  amount: the amount of the transaction
4.  nameOrig: customer starting the transaction
5.  oldbalanceOrg: balance before the transaction
6.  newbalanceOrig: balance after the transaction
7.  nameDest: recipient of the transaction
8.  oldbalanceDest: initial balance of recipient before the transaction
9.  newbalanceDest: the new balance of recipient after the transaction
10. isFraud: fraud transaction
"""

#Start by importin the necesssary python librabries and dataset
import pandas as pd
import numpy as np
data = pd.read_csv("creditcard.csv")
print(data.head())

#Test if there any missing values in DataFrame. It turns out there are no obvious missing values but, as we will see below, this does not rule out proxies by a numerical value like 0.
data.dropna(inplace=True)
print(data.isnull().sum())

"""So this dataset does not have any null values. Before moving forward, now, let’s have a look at the type of transaction mentioned in the dataset:"""

# Exploring transaction type
print(data.type.value_counts())

type = data["type"].value_counts()
transactions = type.index
quantity = type.values

import plotly.express as px
figure = px.pie(data,
             values=quantity,
             names=transactions,hole = 0.5,
             title="Distribution of Transaction Type")
figure.show()

"""Now let’s have a look at the correlation between the features of the data with the isFraud column:"""

# Checking correlation
correlation =data.corr()
print(correlation["isFraud"].sort_values(ascending=False))

"""Now let’s transform the categorical features into numerical. Here I will also transform the values of the isFraud column into No Fraud and Fraud labels to have a better understanding of the output:"""

data["type"] = data["type"].map({"CASH_OUT": 1, "PAYMENT": 2,
                                 "CASH_IN": 3, "TRANSFER": 4,
                                 "DEBIT": 5})
data["isFraud"] = data["isFraud"].map({0: "No Fraud", 1: "Fraud"})
print(data.head())

"""**Online Payments Fraud Detection Model**

Now let’s train a classification model to classify fraud and non-fraud transactions. Before training the model, I will split the data into training and test sets:


"""

# splitting the data
from sklearn.model_selection import train_test_split
x = np.array(data[["type", "amount", "oldbalanceOrg", "newbalanceOrig"]])
y = np.array(data[["isFraud"]])

"""Now let’s train the online payments fraud detection model:"""

# training a machine learning model
from sklearn.tree import DecisionTreeClassifier
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.10, random_state=42)
model = DecisionTreeClassifier()
model.fit(xtrain, ytrain)
print(model.score(xtest, ytest))

"""Now let’s classify whether a transaction is a fraud or not by feeding about a transaction into the model:"""

# prediction
#features = [type, amount, oldbalanceOrg, newbalanceOrig]
features = np.array([[4, 9000.60, 9000.60, 0.0]])
print(model.predict(features))