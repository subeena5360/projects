# -*- coding: utf-8 -*-
"""Mobile_price_predition_project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T6xXtw6mRa_TpFjc7zHfH8-X7Bnp00eT

# **Mobile Price Range Classification**

**Problem Statement** : Market size of mobile phones if growing everyday and so is the competition.To capture the maximum market electronics companies try to make improvements in their products. However, sales of mobile phones depend on various factors like demand, technology, marketing, brand, availability, user experience, service, price, etc. As we understand that selling price makes a huge difference when it comes to sales and profits.
Estimating an optimal price for a new mobile phone can be a tricky task especially when you are new in the business or when you want to launch a new kind of mobile phone in the market.

As part of this exercise we will try to estimate the price range for a given mobile phone using given feature information. These details are collected from various similar companies.

## **Import Libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
# used to supress display of warnings
import warnings

# os is used to provide a way of using operating system dependent functionality
# We use it for setting working folder
import os

# Pandas is used for data manipulation and analysis
import pandas as pd

# Numpy is used for large, multi-dimensional arrays and matrices, along with mathematical operators on these arrays
import numpy as np

# Matplotlib is a data visualization library for 2D plots of arrays, built on NumPy arrays
# and designed to work with the broader SciPy stack
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib import pyplot
# Seaborn is based on matplotlib, which aids in drawing attractive and informative statistical graphics.
import seaborn as sns

"""## **Setting Options**"""

# suppress display of warnings
warnings.filterwarnings('ignore')

# display all dataframe columns
pd.options.display.max_columns = None

# to set the limit to 3 decimals
pd.options.display.float_format = '{:.7f}'.format

# display all dataframe rows
pd.options.display.max_rows = None

"""## **Read Data**"""

df =  pd.read_csv("/content/drive/MyDrive/Colab Notebooks/Mobile.csv")   # loading dataset

df.head()            # to display the top 5 rows of the dataframe

df.tail()                              # it gives last 5 rows of dataset

df.shape               # to display the dimension of the dataframe

"""## Dataframe has 21 columns and 2000 rows"""

# to display the column names of the dataframe
df.columns

# check the datatypes
df.dtypes

"""From the above output, we see that except for the columns of clock_speed and m_dep all our columns datatype is int64.


"""

df.info()                            # it gives data type and non_null count of each column

df.describe()                   # it give statistical information about numerical values

"""### The above output prints the important summary statistics of all the numeric variables like the mean, median (50%), minimum, and maximum values, along with the standard deviation."""

df[df.duplicated()]                    #This line shows that we are checking for the duplicated rows in the dataset

"""### There are no duplicate rows in this data set"""

df.isnull().sum()        # Checking if the dataset has any null values in it

"""### There are no missing values in the data."""

df.corr()

# To get a correlation matrix
# Ploting correlation plot
corr = df.corr()
plt.figure(figsize=(15, 5))

# plotting the heat map
# corr: give the correlation matrix
# cmap: colour code used for plotting
# vmax: gives maximum range of values for the chart
# vmin: gives minimum range of values for the chart

sns.heatmap(corr, cmap='YlGnBu', vmax=1.0, vmin=-1.0)

# specify name of the plot
plt.title('Correlation between features')
plt.show()

"""Observations

1. We can see that ram is highly correlated with price range
2. four_g and three_g also have some relationship
3. pc ( primary camera) and fc (front camera) are also related
4. Most of the features are not corelated to each other
5. Few features like clock_speed, m_dep, n_cores are not having much relationship with price range and can be dropped
"""

# Check Frequency count between price range and ram
pd.crosstab(df['ram'],df['price_range'])

"""### We can see that as 'RAM' increases the price also increases"""

# Creating pairplot
sns.pairplot(df, vars=['battery_power', 'clock_speed', 'fc', 'int_memory', 'mobile_wt', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time'], hue='price_range', diag_kind='kde')
plt.show()

# Melt the DataFrame to long format for easier plotting
df_melted = pd.melt(df, id_vars=['price_range'], var_name='category', value_name='value')

# Plotting
plt.figure(figsize=(10, 6))
sns.countplot(data=df_melted, x='category', hue='value', hue_order=[1, 0], palette="Set2")
plt.title('Distribution of Categorical Variables Across Price Ranges')
plt.xlabel('Category')
plt.ylabel('Count')
plt.legend(title='Value', labels=['Yes', 'No'])
plt.xticks(rotation=45)
plt.show()

"""This bar plot showing the distribution of each categorical variable ('blue', 'dual_sim', 'four_g', 'three_g', 'touch_screen', 'wifi') across different price ranges based on the dataset."""

# Select numerical columns for box plots
numerical_columns = ['battery_power', 'clock_speed', 'fc', 'int_memory', 'm_dep', 'mobile_wt',
                     'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time']

# Plotting box plots for each numerical feature across different price ranges
plt.figure(figsize=(14, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(4, 4, i)
    sns.boxplot(x='price_range', y=column, data=df)
    plt.title(f'{column} vs Price Range')

plt.tight_layout()
plt.show()

# Select numerical columns for histograms
numerical_columns = ['battery_power', 'clock_speed', 'fc', 'int_memory', 'm_dep', 'mobile_wt',
                     'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time']

# Plot histograms for each numerical feature
plt.figure(figsize=(14, 10))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(4, 4, i)
    plt.hist(df[column], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'{column} Distribution')
    plt.grid(True)

plt.tight_layout()
plt.show()

"""**Importance of detecting an outlier**

One of the most important tasks from large data sets is to find an outlier, which is defined as a sample or event that is very inconsistent with the rest of the data set. The observation point or value would be distant from the other observations in the data set.

Recollect that one of the assumption of Logistic Regression is there should be no outliers
"""

# create a boxplot for all the continuous features
df.boxplot(column = ['battery_power', 'clock_speed', 'dual_sim', 'fc',
       'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height',
       'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time',
       'touch_screen', 'price_range'], figsize = (20,10))

df['px_height'].describe()

"""As we know that pixel height can be 1960. There are no outliers.

# **Logistic Regression**
"""

## Scikit-learn features various classification, regression and clustering algorithms
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import average_precision_score, confusion_matrix, accuracy_score, classification_report

# Select independent features for model building.
X = df.iloc[:,:20]

y = df['price_range']

# split data into train subset and test subset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# checking the dimensions of the train & test subset
# to print dimension of train set
print(X_train.shape)
# to print dimension of test set
print(X_test.shape)

# import logistic regression and train on tarining set
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(random_state=0)
model.fit(X_train, y_train)

# Predict price range of test data
y_pred = model.predict(X_test)
y_pred

# Let's measure the accuracy of this model's prediction
accuracy_score(y_test, y_pred)

# And some other metrics

print(classification_report(y_test, y_pred, digits=2))

# Display confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)
df_conf_mat = pd.DataFrame(conf_mat)
plt.figure(figsize = (10,7))
sns.heatmap(df_conf_mat, annot=True,cmap='Blues', fmt='g')

"""# **Standardize the data**"""

# import zscore for scaling the data
from scipy.stats import zscore

# Apply zscore on independent features
xtrainsc = X_train.apply(zscore)
xtestsc = X_test.apply(zscore)

# Fit the logistic regression model on scaled data

model1 = LogisticRegression(random_state=0)
model1.fit(xtrainsc, y_train)

model1.score(xtrainsc, y_train)

model1.score(xtestsc, y_test)

ypred = model1.predict(xtestsc)

conf_mat = confusion_matrix(y_test, ypred)
df_conf_mat = pd.DataFrame(conf_mat)
plt.figure(figsize = (10,7))
sns.heatmap(df_conf_mat, annot=True,cmap='Blues', fmt='g')

print(classification_report(y_test, ypred, digits=2))

model1.classes_

y_pred

classification = X_test.copy(deep=True)

classification['prediction']=y_pred

classification

"""# **Conclusion**

1. We are able to classify price range with an accuracy of 96%
2. 'RAM' seems to be highly correlated with the price range
3. 'battery power' is also an deciding factor of the price
4. Few features like clock_speed, m_dep, n_cross are not having much relationship with price range
5. Standardization of data improves accuracy drastically
6. Few cases were misclassified. However, there were zero misclassification in far classes ( like none of the low cost prices were predicted as high cost). Hence we can say that our model is good for production.
"""