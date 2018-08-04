
Adding a new feature:
- use intuition
- code up a new feature
- visualize
- repeat


```python
#compare author email address to list of known poi email
if from_emails:
        ctr = 0
        if from_emails[ctr] in poi_email_list:
            from_poi = True
            ctr += 1 
```


```python
# If a feature is unnecessary, get rid of it
# more features != more information

# Select only the top 10% features that will give good information
from sklearn.feature_selection nimport SelectPercentile
selector = SelectPercentile(percentile=10)
selector.fit()

vectorizer = TfidVectorizer(sublinear_tf=True, max_df=0.5,
                           stop_words='english')
# max_df = document frequency.  If a word appears in more 
# than 50% of the documents, it will be removed.
```
High Bias                         High Variance
Little attention to data          Too much attention to data
High error on training set        High error on test set
Few features used                 Carefully minimized SSE

Sweet spot:
Few Features
Large r-squared
low SSE
Regularization = automatic feature selection to limit the number of features used

Lasso Regression:
Minimizes: SSE + penalty parameter * |coef of regression|
Calculates the tradeoff of smaller errors with a simpler fit
Figures out what features have the most import effect on the regression model.  Sets the coef. of a feature to zero.


```python
# using Lasso Regression
from sklearn.linear_model import Lasso
features, labels = GetMyData()
regression = Lasso()
regression.fit(features, labels)

# predict regression coefficient
regression.predict([[2,4]])
# print regression coefficient
print (regression.coef_)

```
