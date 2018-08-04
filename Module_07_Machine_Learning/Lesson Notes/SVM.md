
SVM = Support Vector Machine
Classifier built on giving linear 

Priority:
Classify correctly
Margins = Maximize distance to nearest point

If an outlier prevents a 100% correct decision boundary, it will do the best it can by ignoring the outliers while maximizing the margin.



```python
from sklearn.svm import SVC
clf = SVC(kernel="linear")

# Fit the classifier usint training features and labels
clf.fit(features_train, labels_train)

# List predictions
pred = clf.predict(features_test)

# Test accuracy
from sklearn.metrics import accuracy_score
acc = accuracy_score(pred, labels_test)

```

If SVM cannot linearly seperate the data, such as when the data is in a circle, you can add a new feature such as:

z = x^2 + y^2 

and plot X and Z.  This should make the data linearly separable.  

Kernel Trick

Changes input space from X,Y into a much larger input space.  Finds a linear separation, and then converts it back into X,Y.  

Parameters are arguments passed when you create your classifier

Parameters for a SVM:
- Kernel
- C: Controls the tradeoff between a smooth decision boundary and classifying training points correctly.  Higher values of C results in more squiggly lines.
- Gamma:  Defines how far the influence of a single training example reaches.  Low values weigh far points higher, while High values of Gamma weigh closer points more.

Overfitting: When the line is too complex when a simpler line can explain it
