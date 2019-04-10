from sklearn.datasets import make_moons
from matplotlib import pyplot as plt
import numpy as np
from math import e
from math import log as log


def sigmoid(x):
    return 1 / (1 + e**(-x))


def loss(ytrue, ypred):
    return -((ytrue*np.log(ypred)) + ((1 - ytrue)*np.log(1 - ypred)))


def feed_forward(X, outer_weights, inner_weights):
    inner_prod = np.dot(X, inner_weights)
    hidden_out = sigmoid(inner_prod)
    hidden_out_wb = np.hstack([hidden_out, np.ones((hidden_out.shape[0], 1))])
    to_y = np.dot(hidden_out_wb, outer_weights)
    yh_sig = sigmoid(to_y)
    return hidden_out, hidden_out_wb, yh_sig


def der_sig(y):
    return sigmoid(y) * (1-sigmoid(y))


def single_prop(X, hidden_out, ypred, ytrue, outer_weights):
    y_loss = loss(ytrue, ypred)
    error = (ypred - ytrue) * loss(ytrue, ypred)
    grad_y = der_sig(ypred) * error
    LR = 0.18
    weights_delta = np.dot(-grad_y, hidden_out) * LR
    outer_weights = outer_weights.reshape(3)
    updated_weights = outer_weights + weights_delta
    return grad_y, updated_weights


def back_prop(inner_weights, outer_weights_new, grad_y, hidden_out_wb, Xc):
    outer_weights_rs = outer_weights.reshape(1, 3)
    grad_y_rs = grad_y.reshape(50, 1)
    right_h = np.dot(grad_y_rs, outer_weights_rs)
    grad_ho = hidden_out_wb * right_h
    grad_ho = grad_ho.reshape(3, 50)
    LR = 0.05
    delta_wi = np.dot(-grad_ho, Xc) * LR
    inner_weights = inner_weights + delta_wi
    return inner_weights


Xc, ytrue = make_moons(n_samples=50, noise=0.2, random_state=42)
X = np.hstack([Xc, np.ones((Xc.shape[0], 1))])
sig_x = sigmoid(X)


loss_plot = []
x = []
losses = []
for i in range(200):
    if i == 0:
        outer_weights = np.random.random(size=(3, 1))
        inner_weights = np.random.random(size=(3, 2))
        dec_loss = 30
    hidden_out, hidden_out_wb, ypred = feed_forward(X, outer_weights, inner_weights)
    ypred = ypred.reshape(50)
    grad_y, outer_weights = single_prop(X, hidden_out_wb, ypred, ytrue, outer_weights)
    inner_weights = back_prop(inner_weights, outer_weights, grad_y, hidden_out_wb, Xc)
    desc_loss = loss(ytrue, ypred).sum()
    x.append(i)
    print('The new loss is: ', desc_loss)
    print('new inner weights are: ', inner_weights)
    print('new outer weights are: ', outer_weights)
    print('iteration is: ', i)
    print('\n\n')
    losses.append(desc_loss)
    if i > 10:
        ypred[ypred >= 0.5] = 1
        ypred[ypred <= 0.5] = 0
        ypred = ypred.astype(int)
        plt.scatter(X[:, 0], X[:, 1], c=ypred)
        plt.show()
        if losses[-10] < losses[i]:
            break

# ypred[ypred >= 0.5] = 1
# ypred[ypred <= 0.5] = 0
# ypred = ypred.astype(int)
# plt.scatter(X[:, 0], X[:, 1], c=ypred)
# plt.show()
plt.plot(x, losses)
plt.show()