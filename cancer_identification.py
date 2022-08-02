# -*- coding: utf-8 -*-
"""Cancer_Identification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/NSBBala/CapstoneProject/blob/main/Cancer_Identification.ipynb

Machine Learning Foundation 

Dialog Data Science Academy 

Capstone Project 

Niroshan Balasuriya

# Loading Libraries
"""

import numpy as np
import pandas as pd

from matplotlib import pyplot
import seaborn as sns

import numpy as np
import pandas as pd

# Data visualization
import matplotlib.pyplot as plt
from matplotlib import cm # Colomaps
import seaborn as sns

# Classifier algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#train test split
from sklearn.model_selection import train_test_split

# Model evaluation
from sklearn import metrics

"""# Mount Google Drive for Testing Purpose"""

from google.colab import drive
drive.mount('/content/drive')

"""# Load Data"""

# From URL (GitHub raw file link)
# file_path_url= 'https://raw.githubusercontent.com/'

# From Google Drive
file_path_ws = '/content/drive/My Drive/Data/dataR2.csv' 

# Load CSV File

#data = pd.read_csv(file_path_url)
data = pd.read_csv(file_path_ws)
data.sample(20)

"""# Pre-process Data for Training"""

# check width (number of columns) and height (number of rows)
data.shape

# Check Columns and thier Data Types
data.dtypes

# Data Frame Info (Row count, Columns, Non-Null Count, Data Types)
data.info()

#list down the columns 
data.columns

data.describe(include='all').transpose()

# Finding the missing values
#print(data.isna())
print(data.isna().all())

# Finding the null values
#print(data.isnull())
print(data.isnull().all())

# Data Set selected is not having any missing data or data that needs to be corrected.

cormat = data.corr()
round(cormat,2)

import seaborn as sns
sns.heatmap(cormat)

"""## Create ID Column"""

data['id'] = data.index+1
data

"""# Age as a Variable"""

data['Classification'].value_counts()

#data.groupby(by='Age')['id'].count()
data.groupby(by=['Classification']).agg({'Age': ['min', 'max', 'mean', 'std']})

data['Age'].unique()

data.columns

X_variables = ['Age',  'BMI', 'Glucose', 'Insulin', 'HOMA', 'Leptin', 'Adiponectin', 'Resistin', 'MCP.1']
data[X_variables].head()

y_varibale = 'Classification'
data[y_varibale].head()

X = data[X_variables].values

y = data[y_varibale].values
y

"""# Data Pre-processing Function"""

def pre_processing(data):    
    data['id'] = data.index+1

    
    # Select Columns
    X_variables = ['Age',  'BMI', 'Glucose', 'Insulin', 'HOMA', 'Leptin', 'Adiponectin', 'Resistin', 'MCP.1']
    
    # Assign 0 to missing columns
    for x in list(set(X_variables) - set(data.columns)):
        data[x] = 0
        
    return data[X_variables]

"""# Train Test Split"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(F"Train sample size = {len(X_train)}")
print(F"Test sample size  = {len(X_test)}")

"""# Model Training"""

#Training Function 
#Prediction also included
def model_train(model, model_name, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)

    #Prediction
    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    test_result = pd.DataFrame(data={'y_act':y_test, 'y_pred':y_pred, 'y_pred_prob':y_pred_prob})
    #test_result.sample(10)

    #Model Evaluation
    accuracy = metrics.accuracy_score(test_result['y_act'], test_result['y_pred']) 
    precision = metrics.precision_score(test_result['y_act'], test_result['y_pred'], average='binary', pos_label=1)
    f1_score = metrics.f1_score(test_result['y_act'], test_result['y_pred'], average='weighted')  #weighted accounts for label imbalance.
    roc_auc = metrics.roc_auc_score(test_result['y_act'], test_result['y_pred_prob'])

    return ({'model_name':model_name, 
                   'model':model, 
                   'accuracy':accuracy, 
                   'precision':precision,
                  'f1_score':f1_score,
                  'roc_auc':roc_auc,
                  'test':test_result.sample(10),
                  })

#Train the model & do the prediction
#RandomForest Classifier
model0 = model_train(RandomForestClassifier(n_estimators=500, max_depth=10, n_jobs=3, verbose=1), 'rf_new0', X_train, y_train, X_test, y_test)
#Print the output
model0

#DecisionTreeClassifier 
model1 = model_train(DecisionTreeClassifier(random_state=0, max_depth=10, min_samples_split=20), 'rf_new1', X_train, y_train, X_test, y_test)
model1

"""# Fitting Multipe Models with Different Hyperparamaters

## [A] Manualy explore hyperparameter space
"""

models = []
models.append(model_train(DecisionTreeClassifier(random_state=0, max_depth=5, min_samples_split=10), 'dt1', X_train, y_train, X_test, y_test))
models.append(model_train(DecisionTreeClassifier(random_state=0, max_depth=10, min_samples_split=20), 'dt2', X_train, y_train, X_test, y_test))
models.append(model_train(DecisionTreeClassifier(random_state=0, max_depth=20, min_samples_split=40), 'dt3', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=100, max_depth=None, n_jobs=3, verbose=1), 'rf1', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=None, n_jobs=3, verbose=1), 'rf2', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=10, n_jobs=3, verbose=1), 'rf3', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=20, n_jobs=3, verbose=1), 'rf4', X_train, y_train, X_test, y_test))
models = pd.DataFrame(models)
models

"""## [B] Use of Grid Search for RandomForestClassifier"""

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators': [100,500,1000], 'max_depth': [None, 10, 20]}
gs_model = GridSearchCV(RandomForestClassifier(), parameters, n_jobs=2, verbose=3, pre_dispatch=2)
gs_model.fit(X_train, y_train)

# Best Model Paramaters
print(gs_model.best_params_)

from sklearn.metrics import classification_report, confusion_matrix 

y_pred = gs_model.predict(X_test) 

print(classification_report(y_test, y_pred)) 
print(confusion_matrix(y_test, y_pred))

"""## [C] Use of Random Search for RandomForestClassifier"""

from sklearn.model_selection import RandomizedSearchCV
    
# Define Hyperparameter Grid
param_grid = {"n_estimators": [100,500,1000],
              "max_depth": [None, 10, 20],
             }
  
# Create model object
model = RandomForestClassifier()
  
# Create RandomizedSearchCV object
model_cv = RandomizedSearchCV(model, param_grid, cv=5, scoring='f1')
  
model_cv.fit(X_train, y_train)
  
# Print the tuned parameters and score
print("Tuned Model Parameters: {}".format(model_cv.best_params_))
print("Best model score: {}".format(model_cv.best_score_))

"""# Select Best Model"""

features_to_model = X_variables
#Get the best model from Grid Search
model = gs_model.best_estimator_

importance = model.feature_importances_
feature_profile = pd.DataFrame({"feature":features_to_model, "importance":importance})

print('\n')
print("feature_profile:\n", feature_profile.sort_values(by='importance', ascending=False))
#print("Model Parameters:\n", pd.Series(model.get_params()))

# Evaluate Model
#evaluate_model(model, X_test, features_to_model)

#Evaluate the best model from Random Search
model = model_cv.best_estimator_

# Feature importance/Coefficients
importance = model.feature_importances_
feature_profile = pd.DataFrame({"feature":features_to_model, "importance":importance})

print("Best model score: {}".format(model_cv.best_score_))
print('\n')
print("feature_profile:\n", feature_profile.sort_values(by='importance', ascending=False))
#print("Model Parameters:\n", pd.Series(model.get_params()))

"""# Fine Tunning the Model By Dropping the Least Importance Attributes"""

# As per the above feature profiles, dropping the least contributed three columns from the data set
# axis = 1 indicates columns (0 indicate index or rows)
data.drop(labels='Adiponectin', axis=1, inplace=True)
data.drop(labels='Insulin', axis=1, inplace=True)
data.drop(labels='MCP.1', axis=1, inplace=True)

# Select Columns
X_variables1 = ['Age',  'BMI', 'Glucose', 'HOMA', 'Leptin', 'Resistin']

# Use below if inplace=True or not provided the parameter
#census_data = census_data.drop(labels='Unnamed: 0', axis=1)

data.head()

# Select Columns
X_variables1 = ['Age',  'BMI', 'Glucose', 'HOMA', 'Leptin', 'Resistin']

"""#Retraing the model to see the performance"""

#Trainning Split
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y, test_size=0.3, random_state=42)

print(F"Train sample size = {len(X_train1)}")
print(F"Test sample size  = {len(X_test1)}")

#Train the model & do the prediction
#RandomForest Classifier
model2 = model_train(RandomForestClassifier(n_estimators=500, max_depth=10, n_jobs=3, verbose=1), 'rf_new2', X_train1, y_train1, X_test1, y_test1)
#Print the output
model2

from sklearn.model_selection import RandomizedSearchCV
    
# Define Hyperparameter Grid
param_grid = {"n_estimators": [100,500,1000],
              "max_depth": [None, 10, 20],
             }
  
# Create model object
model = RandomForestClassifier()
  
# Create RandomizedSearchCV object
model_cv1 = RandomizedSearchCV(model, param_grid, cv=5, scoring='f1')
  
model_cv1.fit(X_train1, y_train1)
  
# Print the tuned parameters and score
print("Tuned Model Parameters: {}".format(model_cv1.best_params_))
print("Best model score: {}".format(model_cv1.best_score_))

#Evaluate the best model from Random Search
model = model_cv1.best_estimator_

# Feature importance/Coefficients
importance = model.feature_importances_
feature_profile = pd.DataFrame({"feature":features_to_model, "importance":importance})

print("Best model score: {}".format(model_cv.best_score_))
print('\n')
print("feature_profile:\n", feature_profile.sort_values(by='importance', ascending=False))

"""# Saving Best Model

## [A] Use Pickle
"""

import pickle

save_file = 'model_rf3_test.pickle'
pickle.dump(model, open(save_file, 'wb'))

# loading from file
model_ = pickle.load(open(save_file, 'rb'))
model_

"""## [B] Use Joblib (supports parallelization)"""

import joblib

save_file = 'model_rf3_test.joblib'
joblib.dump(model, open(save_file, 'wb'))

# loading from file
model_ = joblib.load(save_file)
model_

"""# Predict on a Sample Data"""

sample_input = data[['Age',  'BMI', 'Glucose', 'Insulin', 'HOMA', 'Leptin', 'Adiponectin', 'Resistin', 'MCP.1', 'Classification']].sample(10)
sample_input

pre_processing(sample_input)

model.predict_proba(pre_processing(sample_input))

"""# Score Function"""

def score(input_data, model):
    return model.predict_proba(input_data)

prediction = score(input_data=pre_processing(sample_input), model=model)
prediction

"""# Post-processing Function for Prediction"""

def post_processing(prediction):
    if len(prediction)==1:
        return prediction[:, 1][0]
    else:
        return prediction[:, 1]

output = post_processing(score(input_data=pre_processing(sample_input), model=model))
output

# Create new column in input dataset
sample_input['prediction'] = post_processing(model.predict_proba(pre_processing(sample_input)))
sample_input

# Output value 
sample_output = post_processing(score(input_data=pre_processing(sample_input), model=model))
sample_output

"""# Prediction Function for Application (Inference Pipeline)"""

def app_prediction_function(input_data, model):
    return post_processing(score(input_data=pre_processing(input_data), model=model))

input_data = data[['Age',  'BMI', 'Glucose', 'Insulin', 'HOMA', 'Leptin', 'Adiponectin', 'Resistin', 'MCP.1', 'Classification']].sample(1)
print(input_data)
app_prediction_function(input_data, model)

"""## Sample Input as dictionary"""

input_data = input_data.to_dict(orient='records')[0]
input_data

"""## Convert Input Data to DataFrame"""

input_data = pd.DataFrame([input_data])
input_data

"""## Get Prediction"""

app_prediction_function(input_data, model)

"""<hr>
Last update 2021-11-07 by Sumudu Tennakoon
"""