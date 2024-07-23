import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns

# Random seed
np.random.seed(0)
################################################## Define Functions ####################################################
# Define function to plot confusion matrix
def plot_confusion_matrix(y_var,y_predict):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_var, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix');
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()
########################################################################################################################

# URLs for the datasets
url_1 = r"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
url_2 = r"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"

# Read in the data
df = pd.read_csv(url_2)

# Audit the data
pd.set_option('display.max_columns', None)
print(df)
print(df.describe(include='all'))
for column in df.columns:
    print(f"Nulls in column {column}: {sum(df[column].isnull())}")
    print(f"Value Counts in column {column}:\n{df[column].value_counts()}\n")

# Convert dataframe to numpy array and standardize
x = np.asarray(df)
x = preprocessing.StandardScaler().fit(x).transform(x)

# Read target variable and convert to numpy array
df2 = pd.read_csv(url_1)
y = np.asarray(df2['Class'])

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)
print('Train set:', X_train.shape, y_train.shape)
print('Test set:', X_test.shape, y_test.shape)

# Create logistic regression object
lr = LogisticRegression()

# Define hyperparameters grid
parameters_lr = {
    'C': [0.01, 0.1, 1],
    'penalty': ['l2'],
    'solver': ['lbfgs']
}

# Use GridSearchCV to find the best hyperparameters
logreg_cv = GridSearchCV(estimator=lr, param_grid=parameters_lr, n_jobs=-1, cv=10)
logreg_cv.fit(X_train, y_train)

# Output the best parameters and accuracy
print("Best estimator: ", logreg_cv.best_estimator_)
print("Tuned hyperparameters (best parameters): ", logreg_cv.best_params_)

# Re-model with optimal parameters
yhat = logreg_cv.best_estimator_.predict(X_test)
print(f"Logistic regression best accuracy score: {logreg_cv.best_score_}\n")

##### Support Vector Machine #####
# Use an SVM with GridSearchCV to identify optimal parameters
from sklearn import svm
parameters_svm = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = svm.SVC()
svm_vc = GridSearchCV(estimator=svm, param_grid=parameters_svm, n_jobs=-1, cv=10)
svm_vc.fit(X_train, y_train)
print("Best estimator: ", svm_vc.best_estimator_)
print("Tuned hyperparameters (best parameters): ", svm_vc.best_params_)

# Re-model with optimal parameters
yhat = svm_vc.best_estimator_.predict(X_test)
print(f"Support Vector Machine best accuracy score: {svm_vc.best_score_}\n")

# Plot confusion matrix
yhat=svm_vc.predict(X_test)
plot_confusion_matrix(y_test,yhat)

##### Decision Tree #####
# Use a decision tree with GridSearchCV to identify optimal parameters
from sklearn.tree import DecisionTreeClassifier
parameters_tree = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(estimator=tree, param_grid=parameters_tree, n_jobs=-1, cv=10)
tree_cv.fit(X_train, y_train)
print("Best estimator: ", tree_cv.best_estimator_)
print("Tuned hyperparameters (best parameters): ", tree_cv.best_params_)

# Re-model with optimal parameters
yhat = tree_cv.best_estimator_.predict(X_test)
print(f"Decision Trees best accuracy score: {tree_cv.best_score_}\n")

# Plot confusion matrix
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

##### K Nearest #####
# Use a decision tree with GridSearchCV to identify optimal parameters
from sklearn.neighbors import KNeighborsClassifier
parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(estimator=knn, param_grid=parameters_knn, n_jobs=-1, cv=10)
knn_cv.fit(X_train, y_train)
print("Best estimator: ", knn_cv.best_estimator_)
print("Tuned hyperparameters (best parameters): ", knn_cv.best_params_)

# Re-model with optimal parameters
yhat = knn_cv.best_estimator_.predict(X_test)
print(f"Neasrest Neighbors best accuracy score: {knn_cv.best_score_}\n")

# Plot confusion matrix
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

# Print out accuracy scores for all models
print(f"Logistic regression best accuracy score: {logreg_cv.best_score_}")
print(f"Support Vector Machine best accuracy score: {svm_vc.best_score_}")
print(f"Decision Trees best accuracy score: {tree_cv.best_score_}")
print(f"Neasrest Neighbors best accuracy score: {knn_cv.best_score_}")