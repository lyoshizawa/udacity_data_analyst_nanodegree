
PCA creates a new coordinate sytem by moving and rotating the axis.  It finds the axis and tells you how important the axis is.

Composite features - reduce the number of features and condensing them together.

Example: Square footage + number of rooms -> Size of the house

Variance = the spread of data distribution

Create new axis along the direction of maximum variance because it retains the maximum amount of information in the original data.  It minimizes the distance from the points to the axis, minimizing the information loss.

more variance = the higher the PC is ranked

PCA can take a group of features, and pick out the first principal component, and second principal component, which are aggregates of other components.

The maximum number of principal components = number of features



```python
def doPCA():
    from sklearn.decomposition import PCA
    pca = PCA(n_components =2)
    pca.fit(data)
    return pca

pca = doPCA
print pca.explained_variance_ratio_
first_pc = pca.components_[0]
second_pc = pca.components_[1]
```

When to use PCA
- access to latent features driving the patterns in data
- dimensionality reduction
     - visualizes high dimensional data
     - reduce noise
     - used as preprocessing for other algorithms that need fewer inputs
     
     
Facial recognition
- pictures of faces have high input dimensionality
- faces have general patterns that can be condensed into a smaller number of dimensions
