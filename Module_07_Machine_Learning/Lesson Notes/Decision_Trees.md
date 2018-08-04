
Decision Trees

Utilizes linear decision to create a non-linear decision surface


```python
# Training a decision tree
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

# Making a prediction
pred = clf.predict(features_test)

# Check accuracy
from sklearn.metrics import accuracy_score
acc = accuracy_score(pred, labels_test)

```

min_samples_split -> The minimum value needed to split it
- Default = 2
- Smaller numbers create more complicated results


```python
#Create 2 decision tree classifiers that changes the minimum sample split

from sklearn import tree
from sklearn.metrics import accuracy_score

def decision(split_num):
    clf = tree.DecisionTreeClassifier(min_samples_split = split_num)
    clf = clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    acc = accuracy_score(pred, labels_test
    return acc
    
acc_min_samples_split_2 = decision(2)
acc_min_samples_split_50 = decision(50)

```

Entropy controls how a Decision Tree decides where to split the data.  It measure the impurity in a bunch of examples.

No impurities = Entropy 0
Half impurities = Entropy 1

Entropy = ∑i -(pi)log2(pi)
pi = fraction of examples

Speed: Slow Slow Fast Fast
Slow = .5
Fast = .5

slow = -.5 log2 (.5)
fast = -.5 log2 (.5)

Entropy = 1.0

Information Gain = Entropy(parent) - [Weighted Average] * entropy(children)
Grade     Speed     Speed Limit
Steep     Slow      Yes
Steep     Slow      Yes
Flat      Fast      No
Steep     Fast      No

Speed:
Slow Slow | Fast Fast

Grade:
Steep          |  Flat
Slow Slow Fast |  Fast

Slow: 2/3      |  Fast: 1/1
Fast: 1/3 
    


```python
# Calculate entropy of Steep Grade
import math
entropy = -.6666 * math.log(.6666, 2) - .3333*math.log(.3333,2)
print entropy
```

    0.918348266761
    


```python
# Calculate Information Gain if you split Speed on the Grade
ig = 1 - .75*(entropy)
print ig
```

    0.311238799929
    


```python
# Splitting based on speed limit:
# Perfect purity: Entropy = 0 & Information Gain = 1
e_sl = -1 * math.log(1, 2) - 1 * math.log(1, 2)
print e_sl

ig_sl = 1 - .5 * e_sl
print ig_sl
```

    0.0
    1.0
    
