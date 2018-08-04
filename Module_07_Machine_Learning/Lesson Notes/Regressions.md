
Continuous Supervised Learning

LinearRegression


```python
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(ages_train, net_worths_train)

# requires a list of values
pred = reg.predict()

# slope and y intercept.  Must have underscore!!
reg.coef_
reg.intercept_

#r-squared.  The higher r-squared, the better it is
reg.score()
```

Linear Regression Errors

error = actual value - predicted value

The best regression is the one that minimizes:
Sum of (actual - predicted)^2

Algorithms:
Ordinary least squares (used by sklearn linear regression)
Gradient descent

r-squared


Classification vs. Regression

Property          Supervised Classification     Regression

Output Type       diescret (class labels)       continuous variable

Trying to Find    decision boundary             best fit line

Evaluation        accuracy                      r^2
