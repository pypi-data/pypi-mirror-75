# data-complexity
The Data Complexity Measures in Python


## Install
```bash
$ pip install data-complexity
```


## How it works
### Maximum Fisher's Discriminant Ratio (F1)
```python
from dcm import dcm
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
y = iris.target

index, F1 = dcm.F1(X, y)
```

### Fraction of Borderline Points (N1)
```python
from dcm import dcm
from sklearn import datasets

bc = datasets.load_breast_cancer(as_frame=True)
X = bc.data.values
y = bc.target.values

N1 = dcm.N1(X, y)
```

### Entropy of Class Proportions (C1) and Imbalance Ratio (C2)
```python
from dcm import dcm
from sklearn import datasets

bc = datasets.load_breast_cancer(as_frame=True)
X = bc.data.values
y = bc.target.values

C1, C2 = dcm.C12(X, y)
```

### Other Measures
Coming soon...


## References
[1] How Complex is your classification problem? A survey on measuring classification complexity, https://arxiv.org/abs/1808.03591

[2] The Extended Complexity Library (ECoL), https://github.com/lpfgarcia/ECoL
