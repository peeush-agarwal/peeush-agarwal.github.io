import numpy as np
from linear_regression_from_scratch import LinearRegression


class RidgeRegression(LinearRegression):
    def __init__(self, learning_rate=0.01, max_iter=1000, tol=1e-6, alpha=1.0):
        super().__init__(learning_rate, max_iter, tol)
        self.alpha = alpha

    def _gradient_descent(self, X, y):
        m, n = X.shape
        weights = np.random.normal(0, 0.01, n)

        for i in range(self.max_iter):
            predictions = X @ weights

            # Ridge cost function
            cost = np.mean((predictions - y) ** 2) / 2 + self.alpha * np.sum(
                weights[1:] ** 2
            )

            # Ridge gradients (don't regularize bias term)
            gradients = X.T @ (predictions - y) / m
            gradients[1:] += 2 * self.alpha * weights[1:]

            weights -= self.learning_rate * gradients

            if np.linalg.norm(gradients) < self.tol:
                print(f"Converged after {i + 1} iterations")
                break

        return weights


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    m = 100
    X = np.random.randn(m, 1)
    y = 4 + 3 * X.ravel() + np.random.randn(m) * 0.5

    # Fit model
    model = RidgeRegression(learning_rate=0.1, max_iter=1000, alpha=0.01)
    model.fit(X, y)

    # Make predictions
    y_pred = model.predict(X)

    # Evaluate
    r2_score = model.score(X, y)
    print(f"R² Score: {r2_score:.4f}")
    print(f"Weights: {model.weights}")
