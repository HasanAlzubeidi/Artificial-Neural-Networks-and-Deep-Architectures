import numpy as np

class DoubleLayerNN:

    def __init__(self, input_nodes=3, nr_of_hidden_nodes=5, learning_rate=0.001):
        self.trained = False
        self.input_nodes = input_nodes
        self.hidden_nodes = nr_of_hidden_nodes
        self.output_nodes = 1
        self.W_hidden = np.random.normal(0, 1, (self.hidden_nodes, self.input_nodes))
        self.W_output = np.random.normal(0, 1, (self.output_nodes, self.hidden_nodes))
        self.learning_rate = learning_rate
        self.alpha = 0.9

        
    def predict(self, X):
        H_1 = self.W_hidden @ X
        A_1 = self.activation(H_1)
        O = self.W_output @ A_1

        return O

    def forward_pass(self, X):
        H_1 = self.W_hidden @ X
        A_1 = self.activation(H_1)
        O = self.W_output @ A_1
        
        return H_1, A_1, O


    def fit_data(self, X, Y, iterations=10000):
        assert X.shape[0] == self.input_nodes, 'dimension of input data is incorrect'
        assert Y.shape[1] == X.shape[1], 'dimensions of input and output do not match up'

        mse = []
        # For the momentum
        prev_dW_hidden = np.zeros((self.hidden_nodes, self.input_nodes))
        prev_dW_output = np.zeros((self.output_nodes, self.hidden_nodes))
        for i in range(iterations):
            # Forward pass
            H_1, A_1, O = self.forward_pass(X)
            # Backwards pass
            dW_hidden, dW_output = self.compute_gradients(A_1, O, X, Y, prev_dW_hidden, prev_dW_output)
            # Update weights
            self.W_hidden = self.W_hidden - self.learning_rate * dW_hidden
            self.W_output = self.W_output - self.learning_rate * dW_output
            # calculate mse
            current_mse = self.calculate_mse(Y, O)
            mse.append(current_mse)
            # Set previous gradients as current
            prev_dW_hidden = dW_hidden
            prev_dW_output = dW_output

        return mse

    def compute_gradients(self, A_1, O, X, T, prev_dW_hidden, prev_dW_output):
        dA_output = (O - T)
        dW_output = dA_output @ A_1.T
        dW_output = (1 - self.alpha) * dW_output + self.alpha * prev_dW_output

        dA_hidden = self.W_output.T @ (dA_output)
        dW_hidden = (dA_hidden * self.sigmoid_derivative(A_1)) @ X.T
        dW_hidden = (1 - self.alpha) * dW_hidden + self.alpha * prev_dW_hidden

        return dW_hidden, dW_output
    
 
    def calculate_mse(self, targets, predictions):
        return np.sum(1/targets.shape[1] * (predictions - targets)**2)


    def activation(self, Y):
        return 2/(1 + np.exp(-Y)) - 1


    def sigmoid_derivative(self, sigmoid_values):
        return ((1 + sigmoid_values) * (1 - sigmoid_values)) / 2


