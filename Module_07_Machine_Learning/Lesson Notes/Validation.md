

```python
from sklearn.model_selection import train_test_split

#splitting iris data into training and testing data.
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size = 0.4, random_state=0)
```

Order of processes

TRAINING
pca.fit -> training features.
pca.transform -> training features
svc.train -> training features

TESTING
pca.transform -> test features
svc.predict -> test features

Cross validation
- Divide data set into 'k' bins
- run 'k' seperate testing experiments
    - pick testing set (k-1)
    - train
    - test on the remaining set
    - repeat k times
    - average the test results from the k experiments
- each bin is used for testing and training.


```python
# GridSearchCV
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
svr = svm.SVC()
clf = grid_search.GridSearchCV(svr, parameters)
clf.fit(iris.data, iris.target)
```
