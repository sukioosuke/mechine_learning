import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

content = pd.read_csv('../../data/titanic/train.csv').dropna()
age_with_fares = content[
    (content['Age'] > 22) & (content['Fare'] < 400) & (content['Fare'] > 130)
    ]
sub_fare = age_with_fares['Fare']
sub_age = age_with_fares['Age']


def func(age, k, b):
    return k * age + b


def loss(y, yhat):
    # return np.mean(np.abs(y - yhat))
    return np.mean(np.square(y.real - yhat.real))


min_error_rate = float('inf')
loop_times = 10000
losses = []

khat = random.random() * 20 - 10
bhat = random.random() * 20 - 10

best_k, best_b = khat, bhat


# def derivate_k(y, yhat, x):
#     abs_values = [-1 if y_i > yhat_i else 1 for y_i, yhat_i in zip(y, yhat)]
#     return np.mean([a * x_i for a, x_i in zip(abs_values, x)])
def derivate_k(y, k, b, x):
    return np.mean([2 * np.square(x_i) * k + 2 * (b - y_i) * x_i for x_i, y_i in zip(x, y)])


# def derivate_b(y, yhat):
#     return np.mean([-1 if y_i > yhat_i else 1 for y_i, yhat_i in zip(y, yhat)])
def derivate_b(y, k, b, x):
    return np.mean([2 * k * x_i + 2 * b - 2 * y_i for x_i, y_i in zip(x, y)])


learning_rate = 1e-7

while loop_times > 0:
    # k_delta = -1 * learning_rate * derivate_k(sub_fare, func(sub_age, khat, bhat), sub_age)
    # b_delta = -1 * learning_rate * derivate_b(sub_fare, func(sub_age, khat, bhat))
    k_delta = -1 * learning_rate * derivate_k(sub_fare, khat, bhat, sub_age)
    b_delta = -1 * learning_rate * derivate_b(sub_fare, khat, bhat, sub_age)

    khat += k_delta
    bhat += b_delta

    estimate_fare = func(sub_age, khat, bhat)
    error_rate = loss(sub_fare, estimate_fare)

    if error_rate < min_error_rate:
        min_error_rate = error_rate
        best_k = khat
        best_b = bhat

    print('loop == {}'.format(loop_times))
    print('f(age) = {} * age + {}, with error rate: {}'.format(best_k, best_b, error_rate))

    losses.append(error_rate)
    loop_times -= 1

plt.plot(range(len(losses)), losses)
plt.show()
