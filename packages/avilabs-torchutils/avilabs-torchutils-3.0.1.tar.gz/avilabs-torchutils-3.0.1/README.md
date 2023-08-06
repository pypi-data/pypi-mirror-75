# torchutils

Convenience classes for training and hyperparameter tuning. These are just thin wrappers on top of PyTorch and Ax.

## Compatibility
Built using Python 3.7.

## Installation

```
pip install avilabs-torchutils
```

For full working examples see the `torchutils/examples` directory.

## PyTorch Gotchas

### Metric Functions
SciKit-Learn has some really good built-in metric functions that can be mostly reused. Most of these functions can work with `t.Tensor` without any need for detaching, etc. However, unlike PyTorch loss functions that take in the outputs followed by targets  `loss_fn(y_hat, y_true)`, scikit-learn metric functions take in the targets followed by the predictions `score(y_true, y_pred)`.

### Binary Classification
When doing binary classification we use the `BCELoss` function. This function wants *both* the targets and outputs to be of type `t.float32`, even though we might think of the targets as integers 0 or 1. Ensure that the Dataset does the neccessary conversions to make targets of type `t.float32`.

Ensure that the output of the model has the same shape as the targets. E.g., if the Dataset gives targets as a single dimensional array `(m,)` then care must be taken in the model to squeeze the output of the `t.nn.Linear(n, 1)` operator along the first dimension using `t.squeeze(t.nn.Linear(n, 1)(x), dim=1)`. This is because when the `t.nn.Linear(n, 1)` operator is applied to a 2 dimensional input of shape `(m, n)` it will output a tensor of shape `(m, 1)`. We need to convert it to a single dimensional array of size `(m,)`.

### Multiclass Classification
When doing multiclass classification we use the `CrossEntropyLoss` function. This function wants the targets as longs `t.int64` and the outputs as floats `t.float32`. Using shorter integer types will not work. Ensure that the Dataset does the neccessary conversions to make targets of type `t.int64`.

In most ML literature, the targets are in range [1, k] for k classes. But the `CrossEntropyLoss` function requires the targets to be in range [0, k-1].
