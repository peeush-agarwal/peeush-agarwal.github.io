import numpy as np
import matplotlib.pyplot as plt


class LinearRegression:
    def __init__(self, learning_rate=0.01, max_iter=1000, tol=1e-6):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol

    def fit(self, X, y, method="gradient_descent"):
        # Add bias column
        X_with_bias = np.column_stack([np.ones(X.shape[0]), X])

        if method == "normal_equation":
            self.weights = self._normal_equation(X_with_bias, y)
        else:
            self.weights = self._gradient_descent(X_with_bias, y)

        return self

    def _normal_equation(self, X, y):
        """Analytical solution using normal equation"""
        try:
            weights = np.linalg.inv(X.T @ X) @ X.T @ y
        except np.linalg.LinAlgError:
            # Use pseudo-inverse if matrix is singular
            weights = np.linalg.pinv(X.T @ X) @ X.T @ y
        return weights

    def _gradient_descent(self, X, y):
        """Iterative solution using gradient descent"""
        m, n = X.shape
        weights = np.random.normal(0, 0.01, n)

        for i in range(self.max_iter):
            # Forward pass
            predictions = X @ weights

            # Compute cost
            cost = np.mean((predictions - y) ** 2) / 2

            # Compute gradients
            gradients = X.T @ (predictions - y) / m

            # Update weights
            weights -= self.learning_rate * gradients

            # Check convergence
            if np.linalg.norm(gradients) < self.tol:
                print(f"Converged after {i + 1} iterations")
                break

        return weights

    def predict(self, X):
        X_with_bias = np.column_stack([np.ones(X.shape[0]), X])
        return X_with_bias @ self.weights

    def score(self, X, y):
        """Calculate R-squared score"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    m = 100
    X = np.random.randn(m, 1)
    y = 4 + 3 * X.ravel() + np.random.randn(m) * 0.5

    # Fit model
    model = LinearRegression(learning_rate=0.1, max_iter=1000)
    model.fit(X, y)

    # Make predictions
    y_pred = model.predict(X)

    # Evaluate
    r2_score = model.score(X, y)
    print(f"R² Score: {r2_score:.4f}")
    print(f"Weights: {model.weights}")
