

```python
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
```


```python
# write code that compares predictions to y_test, element-by-element
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(pred, labels_test)
```
Bayes Rule
Prior Probability x Test Evidence -> Posterior probability

Probability Cancer: 0.01 (1%)
Probability No Cancer: 0.99  (99%)

Probability Cancer w/ Pos Test: 0.9
Probability No Cancer w/ Pos Test: 0.1
Probability No Cancer w/ Neg Test: 0.9
Probability Cancer w/ Neg Test: 0.1

Prior:  
Probability you have cancer
P(C): 0.01
P(nC): 0.99

Test probabilities
P(Pos|C) = 0.9   (sensitivity)
P(Pos|nC) = 0.1
P(Neg|nC) = 0.9  (specificity)
P(Neg|C) = 0.1

Joint:   
P(C|Pos) = P(C) x P(Pos|C)
           0.01 x 0.9
           0.009
P(nC|Pos) = P(nC) x P(Pos|nC)  
            0.99 x .1
            0.099

What is the probaility a test will be positive?
Normalize:
P(Pos) = P(C|Pos) + P(nC|Pos) = .009 + .099 = .108

If you have a positive test, what is the probability you have cancer?
Posterior:
P(C|Pos) = .009 / .108 = .0833
P(nC|Pos) = .099 / .108 = .9166
             Chris
P(C|Love) = .1
P(C|Deal) = .8
P(C|Life) = .1

Sarah
P(S|Love) = .5
P(S|Deal) = .2
P(S|Life) = .3

Probability "Life Deal" will be said
P(C|Life Deal) = .8 x .1 = .08
P(S|Life Deal) = .3 x .2 = .06

Normalize = .08 + .06 = .14

Probability who wrote "Life Deal"
P(C|Life Deal) = .08/.14 = .5714
P(S|Life Deal) = .06/.14 = .4286
-----------
Probability "Love Deal" will be said
Chris = .1 x .8 = .08
Sarah = .5 x .2 = .1

Normalize = .08 + .1 = .18

Probability who wrote "Love Deal"
P(C|Love Deal) = .08 / .18 = .4444
P(S|Love Deal) = .10 / .18 = .5555
Naive Bayes looks at word frequency and length, but not the word order.  It also doesn't work well with multi-word phrases.