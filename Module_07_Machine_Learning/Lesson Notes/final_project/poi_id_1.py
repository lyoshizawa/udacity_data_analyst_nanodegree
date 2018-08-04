
# coding: utf-8
#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

import matplotlib.pyplot
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 
                      'bonus', 'restricted_stock_deferred', 'deferred_income', 
                      'total_stock_value', 'expenses', 'exercised_stock_options', 
                      'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
email_features = ['to_messages', 'from_poi_to_this_person',
                  'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']
poi_label =['poi']
features_list = poi_label + financial_features + email_features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Dataset Exploration
## Find total number of people
print ("Number of people in dataset: %i" % len(data_dict))

## Find number / percentage of persons of interest
poi_count = 0
for name in data_dict:
    if data_dict[name]['poi'] == 1:
        poi_count += 1
print ("Number of Persons of Interest ('POI'): %i " % poi_count)
print ("%% of Persons who are POIs: %f%%" % ((float(poi_count)/len(data_dict))*100))

## Find number of features in data_dict
for name, data in data_dict.iteritems():
    print ("Number of Features in Dataset: %i " % len(data))
    break

## Find the number of missing values for each feature
NaN_count = {}
for name, data in data_dict.iteritems():
    for key, value in data.iteritems():
        if value == 'NaN':
            if key in NaN_count:
                NaN_count[key] += 1
            else:
                NaN_count[key] = 1

## Sort the list of missing values descending, and print out the top 5
NaN_count = sorted(NaN_count.items(), key=lambda x:x[1], reverse=True)
print ("\nTop 5 features with missing values: ")
for i, data in enumerate(NaN_count):
    if i < 5:
        print "%s: %i" % (data[0], data[1])

### Task 2: Remove outliers
# Identify Outliers
## Create a function to identify outliers on a plot
def outlier_id(data_dict, feature1, feature2):
    features = [feature1, feature2]
    data = featureFormat(data_dict, features)

    for point in data:
        x = point[0]
        y = point[1]
        matplotlib.pyplot.scatter( x, y )

    matplotlib.pyplot.xlabel(feature1)
    matplotlib.pyplot.ylabel(feature2)
    matplotlib.pyplot.show()

outlier_id(data_dict, "salary", "exercised_stock_options")

## Identify the person with the min and max value for each feature.
## Create a dictionary of dictionaries containing feature name, min/max values, and min/max names
min_max_values = {}
for name, data in data_dict.iteritems():
    for feature, value in data.iteritems():
        if value != 'NaN' and isinstance(value, (int, float)):
            if feature in min_max_values:
                if value > min_max_values[feature]['max_value']:
                    min_max_values[feature]['max_value'] = value
                    min_max_values[feature]['max_name'] = name
                elif value < min_max_values[feature]['min_value']:
                    min_max_values[feature]['min_value'] = value
                    min_max_values[feature]['min_name'] = name
            else:
                #print feature, value, name
                min_max_values[feature] = {}
                min_max_values[feature]['min_name'] = name
                min_max_values[feature]['min_value'] = value
                min_max_values[feature]['max_name'] = name
                min_max_values[feature]['max_value'] = value      
                
print min_max_values['salary']['max_value'], min_max_values['salary']['max_name']
print ('Removing outlier: TOTAL')
data_dict.pop('TOTAL')  # remove the outlier TOTAL from the dataset
outlier_id(data_dict, "salary", "exercised_stock_options")

# Identify users and the number of missing (NaN) values and print out the top 5
person_NaN = {}
for person, data in data_dict.iteritems():
    for feature, value in data.iteritems():
        if value == 'NaN':
            if person in person_NaN:
                person_NaN[person] += 1
            else:
                person_NaN[person] = 1
person_NaN = sorted(person_NaN.items(), key=lambda x:x[1], reverse=True)
print ('\nTop 5 persons with missing features:')
for i, data in enumerate(person_NaN):
    if i < 5:
        if data[1] > 10:
            print ("%s: %i" % (data[0], data[1])) 

# Remove 'LOCKHART EUGENE E' from the dataset as all his data is 'NaN'
# Remove 'THE TRAVEL AGENCY IN THE PARK' from the dataset as this is not a person.
print ('\nRemoving outlier: LOCKHART EUGENE E')
print ('Removing outlier: THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

# Create feature: bonus_salary_ratio
for person, data in my_dataset.items():
    for feature, value in data.items():
        if feature == 'bonus': bonus_value = value 
        if feature == 'salary': salary_value = value 
            
    if bonus_value != 'NaN' and salary_value != 'NaN':
        my_dataset[person]['bonus_salary_ratio'] = float(bonus_value) / salary_value
    else:
        my_dataset[person]['bonus_salary_ratio'] = 0

# Create feature: emails_to_poi_ratio, emails_from_poi_ratio
for person, data in my_dataset.items():
    for feature, value in data.items():
        if feature == 'to_messages': 
            recd_emails = value if value != 'NaN' else 0
        if feature == 'from_messages': 
            sent_emails = value if value != 'NaN' else 0
        if feature == 'from_poi_to_this_person': 
            poi_sent = value if value != 'NaN' else 0
        if feature == 'from_this_person_to_poi': 
            poi_recd = value if value != 'NaN' else 0
    
    if sent_emails != 0:
        my_dataset[person]['emails_to_poi_ratio'] = float(poi_recd) / sent_emails
    else: 
        my_dataset[person]['emails_to_poi_ratio'] = 0
    if recd_emails != 0:
        my_dataset[person]['emails_from_poi_ratio'] = float(poi_sent) / recd_emails
    else: my_dataset[person]['emails_from_poi_ratio'] = 0

# Update features list
features_list = features_list + ['bonus_salary_ratio', 'emails_to_poi_ratio', 'emails_from_poi_ratio']

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Use SelectKBest to find the best features
no_features = 6
selector = SelectKBest(f_classif, k = no_features)
selector.fit_transform(features, labels)

# create an array with the features, scores, and bool value of if it is in the k best features
kbest = zip(features_list[1:],selector.scores_, selector.get_support())    
kbest = sorted(kbest, key=lambda x:x[1], reverse=True)

# create a new feature list with only the poi_label + 10 best features
new_feature_list = poi_label
print ("Features with their ANOVA F-values:")
for feature, score, boolean in kbest:
    print ("%s: %.04f" % (feature, score))
          
print ("\nSelecting top %i features..." % no_features)
for feature, score, boolean in kbest:
    if boolean == True:       
        new_feature_list.append(feature)
        print feature

### Re-extract features and labels from dataset for local testing
data = featureFormat(my_dataset, new_feature_list, sort_keys = True)
labels2, features2 = targetFeatureSplit(data)

# Normalize the data using a StandardScaler.
scaler = StandardScaler()
features2 = scaler.fit_transform(features2)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

clf_nb  =  GaussianNB()
clf_svc =  SVC()
clf_dt  =  DecisionTreeClassifier()
clf_ab  =  AdaBoostClassifier()
clf_lr  =  LogisticRegression()


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# optimize classifier parameters by using GridSearchCV
param_svc = {'C':range(1,1000,50), 'kernel':('rbf', 'poly', 'linear'), 'gamma':(1, .75, .5, .25, .1, .075, .05, .001, .0001, .00001)}
param_dt = {'min_samples_split': range(2,10,1), 'min_samples_leaf': range(1,10,1), 'splitter':('best', 'random')}
param_ab ={'n_estimators': range(10,100,5), 'learning_rate': (1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2), 'algorithm':('SAMME', 'SAMME.R') }
param_lr = {'C': (1000, 10000, 100000, 1000000), 'tol': (1, .1, .01, .001, .0001, .00001), 'penalty':('l1', 'l2')  }

optimize_clf = [(clf_svc, param_svc), (clf_dt, param_dt), (clf_ab, param_ab), (clf_lr, param_lr)]

def optimize_classifier (clf, params):
    grid = GridSearchCV(estimator=clf, param_grid=params, scoring='f1')
    grid.fit(features2,labels2)
    print grid.best_params_
    
for clf, params in optimize_clf:
    optimize_classifier(clf, params)

# Use the GridSearchCV results to optimize the paramaters for each classifier
clf_svc =  SVC(C=551, gamma=.001, kernel='rbf')
clf_dt  =  DecisionTreeClassifier(min_samples_split=2, splitter='random', min_samples_leaf=1)
clf_ab  =  AdaBoostClassifier(n_estimators=75, learning_rate=1.8, algorithm='SAMME')
clf_lr  =  LogisticRegression(penalty='l1', C=100000, tol=.1)

clf_list = {'Naive Bayes': 'nb', 'SVM': 'svc', 'Decision Tree': 'dt',
            'AdaBoost': 'ab','LogisticRegression': 'lr',}

# Test out each classifier on the test_classifier function
for name, classifier in clf_list.items():
    print ("Testing %s..." % name)
    clf = 'clf_'+classifier
    test_classifier(eval(clf), my_dataset, new_feature_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

# Selecting Naive Bayes as the classifier
clf = clf_nb

dump_classifier_and_data(clf, my_dataset, features_list)
