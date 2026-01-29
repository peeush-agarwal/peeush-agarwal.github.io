# Neural Networks Basics

Neural networks are a class of machine learning models inspired by the structure and function of the human brain. They consist of layers of interconnected nodes (neurons) that process input data to learn patterns and make predictions. This section provides an introduction to the fundamental concepts of neural networks, including their architecture, activation functions, and the processes of forward and backward propagation.

## Perceptron: The Basic Unit

The perceptron is the simplest type of neural network, consisting of a single neuron. It takes multiple binary inputs, applies weights to them, sums them up, and passes the result through an activation function to produce a binary output.

![Perceptron Diagram](https://media.geeksforgeeks.org/wp-content/uploads/20251209120638608023/bhu.webp)

### How does a Perceptron work?

1. **Inputs and Weights**: Each input feature is assigned a weight that signifies its importance.
2. **Weighted Sum**: The perceptron computes the weighted sum of the inputs.
3. **Activation Function**: The weighted sum is passed through an activation function (e.g., step function) to determine the output (0 or 1).

### Example

Consider a perceptron with two inputs (x1, x2), weights (w1, w2), and a bias (b). The output (y) is computed as follows:
$$y = f(w1*x1 + w2*x2 + b)$$

where f is the activation function.

## Architecture of Neural Networks

Neural networks are typically organized into layers:
1. **Input Layer**: The first layer that receives the input data.
2. **Hidden Layers**: Intermediate layers that perform computations and extract features.
3. **Output Layer**: The final layer that produces the output predictions.

![Neural Network Architecture](https://ik.imagekit.io/upgrad1/abroad-images/imageCompo/images/ChatGPT_Image_Nov_20_2025_03_47_56_PMTT18DE.png)

## Activation Functions

Activation functions introduce non-linearity into the network, allowing it to learn complex patterns. Common activation functions include:
- **Sigmoid**: Outputs values between 0 and 1.
- **ReLU (Rectified Linear Unit)**: Outputs the input directly if it is positive; otherwise, it outputs zero.
- **Tanh**: Outputs values between -1 and 1.

## Forward Propagation

Forward propagation is the process of passing input data through the network to obtain an output. Each neuron computes a weighted sum of its inputs, applies the activation function, and passes the result to the next layer. 

```python
def forward_propagation(inputs, weights, bias, activation_function):
    weighted_sum = sum(i * w for i, w in zip(inputs, weights)) + bias
    output = activation_function(weighted_sum)
    return output
```

## Backward Propagation

Backward propagation is the process of updating the weights of the network based on the error in the output. It involves calculating the gradient of the loss function with respect to each weight and adjusting the weights to minimize the loss. This is typically done using optimization algorithms like Gradient Descent.

```python
def backward_propagation(weights, learning_rate, error, inputs):
    for i in range(len(weights)):
        weights[i] -= learning_rate * error * inputs[i]
    return weights
```

![Forward and Backward Propagation](https://miro.medium.com/v2/resize:fit:1400/1*SCz0aTETjTYC864Bqjt6Og.png)

## Summary

Neural networks are powerful models capable of learning complex patterns from data. Understanding their architecture, activation functions, and the processes of forward and backward propagation is essential for building and training effective neural networks.

[Back to Deep Learning Concepts](index.md) | [Back to Home](../index.md)
