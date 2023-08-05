### NEATLY HELPER FUNCTIONS ###
import numpy as np

# Sigmoid activation function "normalized" to range and domain of [-1, 1] and [-1, 1]
def sig(x):
    return (2 /(1+np.exp(-4.9*x)))-1

# Softmax function ripped from stackoverflow
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

# Caffe-esque Xavier weight initialization function
def xav(i_count):
    return np.random.normal(0, 1/np.sqrt(i_count), 1)[0]
