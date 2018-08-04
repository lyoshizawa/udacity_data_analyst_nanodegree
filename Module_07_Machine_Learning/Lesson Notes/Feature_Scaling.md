
Feature Scaling:

X' = (X - Xmin) / (Xmax - Xmin)

old weights [ 115, 140, 175]
Xmax = 174
Xmin = 115

X'(140) = (140 - 115) / (175 -115)
X'(140) = .416

0 < X' < 1 


```python
# Create a function that feature scales each value in an array
def featureScaling(arr):
    min_value = min(arr)
    max_value = max(arr)
    
    scaled = []
    for i, value in enumerate(arr):
        scaled.append(float(value - min_value) / float(max_value - min_value))
    return scaled

# tests of your feature scaler--line below is input data
data = [115, 140, 175]
print featureScaling(data)


```


```python
# Using sklearn MinMaxScaler to rescale data in an array
from sklearn.preprocessing import MinMaxScaler
import numpy

weights = numpy.array([[115.],[140.],[175.]])
scaler = MinMaxScaler()
rescaled = scaler.fit_transform(weights)
print rescaled
```

    [[ 0.        ]
     [ 0.41666667]
     [ 1.        ]]
    

SVM with RBF Kernel and K-Means Clustering is affected by feature rescaling
