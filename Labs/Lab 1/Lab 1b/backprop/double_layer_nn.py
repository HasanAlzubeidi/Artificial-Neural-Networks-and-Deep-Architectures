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

        
    def predict(self, X):
        H_1 = self.W_hidden @ X
        A_1 = self.activation(H_1)
        Y_1 = self.W_output @ A_1
        O = self.activation(Y_1)

        O[O >= 0] = 1
        O[O < 0] = -1

        return O

    def forward_pass(self, X):
        H_1 = self.W_hidden @ X
        A_1 = self.activation(H_1)
        Y_1 = self.W_output @ A_1
        O = self.activation(Y_1)
        
        return H_1, A_1, Y_1, O


    def fit_data(self, X, Y, iterations=10000, val_X=None, val_Y=None):
        assert X.shape[0] == self.input_nodes, 'dimension of input data is incorrect'
        assert Y.shape[1] == X.shape[1], 'dimensions of input and output do not match up'

        train_mse = []
        val_mse = []
        for i in range(iterations):
            # Forward pass
            H_1, A_1, Y_1, O = self.forward_pass(X)
            # Backwards pass
            dW_hidden, dW_output = self.compute_gradients(A_1, O, X, Y)
            # Update weights
            self.W_hidden = self.W_hidden - self.learning_rate * dW_hidden
            self.W_output = self.W_output - self.learning_rate * dW_output
            # calculate mse
            current_mse = self.calculate_mse(Y, O)
            train_mse.append(current_mse)
            # calculate mse for validation_data
            if not val_X is None:
                O_val = self.predict(val_X)
                current_val_mse = self.calculate_mse(val_Y, O_val)
                val_mse.append(current_val_mse) 

        if val_X is None:
            return train_mse

        return train_mse, val_mse

    def compute_gradients(self, A_1, O, X, T):
        dA_output = (O - T) * self.sigmoid_derivative(O)
        dW_output = dA_output @ A_1.T

        dA_hidden = self.W_output.T @ (dA_output)
        dW_hidden = (dA_hidden * self.sigmoid_derivative(A_1)) @ X.T

        return dW_hidden, dW_output
    

    def accuracy(self, X, Y):
        predictions = self.predict(X)
        return np.sum(Y == predictions) / X.shape[1]
    
 
    def calculate_mse(self, targets, predictions):
        return np.sum(1/targets.shape[1] * (predictions - targets)**2)


    def activation(self, Y):
        return 2/(1 + np.exp(-Y)) - 1


    def sigmoid_derivative(self, sigmoid_values):
        return ((1 + sigmoid_values) * (1 - sigmoid_values)) / 2


