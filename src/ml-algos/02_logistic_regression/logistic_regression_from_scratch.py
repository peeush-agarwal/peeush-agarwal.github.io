"""
Logistic Regression Implementation from Scratch

This module provides a comprehensive implementation of logistic regression
from scratch, including both gradient descent and Newton-Raphson optimization methods.

Features:
- Binary logistic regression
- Gradient descent optimization
- Newton-Raphson optimization
- Comprehensive evaluation metrics
- Visualization capabilities

Author: Peeush Agarwal
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")

OUTPUTS_DIR = "../../../outputs/ml-algos/02_logistic_regression"

# Ensure output directory exists
os.makedirs(OUTPUTS_DIR, exist_ok=True)


class LogisticRegressionScratch:
    """
    Logistic Regression implementation from scratch with multiple optimization methods
    """

    def __init__(
        self,
        learning_rate=0.01,
        max_iterations=1000,
        tolerance=1e-6,
        method="gradient_descent",
        verbose=False,
        regularization=None,
        C=1.0,
        fit_intercept=True,
        adaptive_lr=True,
        momentum=0.0,
    ):
        """
        Initialize the Logistic Regression model

        Parameters:
        -----------
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        max_iterations : int, default=1000
            Maximum number of iterations for optimization
        tolerance : float, default=1e-6
            Convergence tolerance for optimization
        method : str, default='gradient_descent'
            Optimization method: 'gradient_descent' or 'newton_raphson'
        verbose : bool, default=False
            Whether to print training progress
        regularization : str, default=None
            Type of regularization: None, 'l1', 'l2', or 'elastic'
        C : float, default=1.0
            Inverse of regularization strength (higher C = less regularization)
        fit_intercept : bool, default=True
            Whether to fit intercept (bias) term
        adaptive_lr : bool, default=True
            Whether to use adaptive learning rate
        momentum : float, default=0.0
            Momentum factor for gradient descent (0.0 to 1.0)
        """
        self.learning_rate = learning_rate
        self.initial_learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.method = method
        self.verbose = verbose
        self.regularization = regularization
        self.C = C
        self.fit_intercept = fit_intercept
        self.adaptive_lr = adaptive_lr
        self.momentum = momentum

        # Model parameters
        self.weights = None
        self.bias = None
        self.cost_history = []
        self.gradient_norms = []
        self.converged = False
        self.n_iterations = 0

        # For momentum
        self.velocity_weights = None
        self.velocity_bias = None

    def _initialize_weights(self, n_features):
        """
        Initialize weights using Xavier/Glorot initialization

        Parameters:
        -----------
        n_features : int
            Number of features
        """
        # Xavier initialization: weights ~ N(0, sqrt(2/(n_in + n_out)))
        # For logistic regression: n_in = n_features, n_out = 1
        limit = np.sqrt(2.0 / (n_features + 1))
        self.weights = np.random.uniform(-limit, limit, n_features)

        if self.fit_intercept:
            self.bias = 0.0
        else:
            self.bias = 0.0

        # Initialize momentum velocities
        if self.momentum > 0:
            self.velocity_weights = np.zeros_like(self.weights)
            if self.fit_intercept:
                self.velocity_bias = 0.0

    def _add_bias(self, X):
        """Add bias term to feature matrix"""
        return np.column_stack([np.ones(X.shape[0]), X])

    def _sigmoid(self, z):
        """
        Sigmoid activation function with numerical stability

        Parameters:
        -----------
        z : array-like
            Linear combination of features and weights

        Returns:
        --------
        array-like
            Sigmoid transformation of z
        """
        # Clip z to prevent overflow
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _compute_cost(self, h, y):
        """
        Compute cross-entropy cost function with regularization

        Parameters:
        -----------
        h : array-like
            Predicted probabilities
        y : array-like
            True labels

        Returns:
        --------
        float
            Cross-entropy cost with regularization
        """
        # Add small epsilon to prevent log(0)
        epsilon = 1e-15
        h = np.clip(h, epsilon, 1 - epsilon)

        # Cross-entropy cost
        cost = -np.mean(y * np.log(h) + (1 - y) * np.log(1 - h))

        # Add regularization
        if self.regularization == "l1":
            # L1 regularization
            l1_penalty = np.sum(np.abs(self.weights))
            cost += l1_penalty / (2 * self.C * len(y))
        elif self.regularization == "l2":
            # L2 regularization
            l2_penalty = np.sum(self.weights**2)
            cost += l2_penalty / (2 * self.C * len(y))
        elif self.regularization == "elastic":
            # Elastic net (L1 + L2)
            l1_penalty = np.sum(np.abs(self.weights))
            l2_penalty = np.sum(self.weights**2)
            cost += (0.5 * l1_penalty + 0.5 * l2_penalty) / (2 * self.C * len(y))

        return cost

    def _compute_gradients(self, X, h, y):
        """
        Compute gradients for gradient descent with regularization

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        h : array-like, shape (n_samples,)
            Predicted probabilities
        y : array-like, shape (n_samples,)
            True labels

        Returns:
        --------
        tuple
            (weight_gradients, bias_gradient)
        """
        m = X.shape[0]

        # Basic gradients
        dw = (1 / m) * X.T.dot(h - y)
        db = (1 / m) * np.sum(h - y) if self.fit_intercept else 0

        # Add regularization to weight gradients (not bias)
        if self.regularization == "l1":
            # L1 regularization: add sign of weights
            dw += np.sign(self.weights) / (self.C * m)
        elif self.regularization == "l2":
            # L2 regularization: add weights
            dw += self.weights / (self.C * m)
        elif self.regularization == "elastic":
            # Elastic net: combine L1 and L2
            dw += (0.5 * np.sign(self.weights) + 0.5 * self.weights) / (self.C * m)

        return dw, db

    def _compute_hessian(self, X, h):
        """
        Compute Hessian matrix for Newton-Raphson method

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features + 1)
            Feature matrix with bias term
        h : array-like, shape (n_samples,)
            Predicted probabilities

        Returns:
        --------
        array-like, shape (n_features + 1, n_features + 1)
            Hessian matrix
        """
        m = X.shape[0]
        # Diagonal matrix of h(1-h)
        W = np.diag(h * (1 - h))
        # Hessian = (1/m) * X^T * W * X
        hessian = (1 / m) * X.T.dot(W).dot(X)
        return hessian

    def fit(self, X, y):
        """
        Fit the logistic regression model with improved convergence

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values (0 or 1)
        """
        # Convert to numpy arrays
        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64)

        m, n_features = X.shape

        # Initialize parameters
        self._initialize_weights(n_features)
        self.cost_history = []
        self.gradient_norms = []

        # Reset learning rate
        self.learning_rate = self.initial_learning_rate

        if self.verbose:
            print(f"Training with {self.method}...")
            print(f"Dataset shape: {X.shape}")
            print(f"Regularization: {self.regularization}, C: {self.C}")
            print(f"Learning rate: {self.learning_rate}, Momentum: {self.momentum}")

        # Early stopping variables
        best_cost = float("inf")
        patience_counter = 0
        patience = min(50, self.max_iterations // 10)  # Adaptive patience

        # Training loop
        for i in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights)
            if self.fit_intercept:
                z += self.bias
            h = self._sigmoid(z)

            # Compute cost
            cost = self._compute_cost(h, y)
            self.cost_history.append(cost)

            # Compute gradients
            dw, db = self._compute_gradients(X, h, y)

            # Compute gradient norm for convergence checking
            if self.fit_intercept:
                grad_norm = np.sqrt(np.sum(dw**2) + db**2)
            else:
                grad_norm = np.sqrt(np.sum(dw**2))
            self.gradient_norms.append(grad_norm)

            if self.method == "gradient_descent":
                # Apply momentum
                if self.momentum > 0:
                    if i == 0:
                        # Initialize velocity
                        self.velocity_weights = np.zeros_like(self.weights)
                        if self.fit_intercept:
                            self.velocity_bias = 0.0

                    # Update velocities
                    self.velocity_weights = (
                        self.momentum * self.velocity_weights - self.learning_rate * dw
                    )
                    if self.fit_intercept:
                        self.velocity_bias = (
                            self.momentum * self.velocity_bias - self.learning_rate * db
                        )

                    # Update parameters
                    self.weights += self.velocity_weights
                    if self.fit_intercept:
                        self.bias += self.velocity_bias
                else:
                    # Standard gradient descent
                    self.weights -= self.learning_rate * dw
                    if self.fit_intercept:
                        self.bias -= self.learning_rate * db

                # Adaptive learning rate
                if self.adaptive_lr and i > 10:
                    if i > 0 and cost > self.cost_history[-2]:
                        # Cost increased, reduce learning rate
                        self.learning_rate *= 0.95
                    elif i > 5 and all(
                        self.cost_history[-5:][j] > self.cost_history[-5:][j + 1]
                        for j in range(4)
                    ):
                        # Cost consistently decreasing, increase learning rate slightly
                        self.learning_rate *= 1.01

            elif self.method == "newton_raphson":
                # Newton-Raphson update (simplified for now)
                hessian = self._compute_hessian_simplified(X, h)

                # Add regularization and small diagonal for stability
                hessian += np.eye(len(dw)) * (
                    1e-8 + 1 / (self.C * m) if self.regularization else 1e-8
                )

                try:
                    # Newton update
                    hessian_inv = np.linalg.inv(hessian)
                    weight_update = hessian_inv.dot(dw)
                    self.weights -= weight_update

                    if self.fit_intercept:
                        self.bias -= (
                            self.learning_rate * db
                        )  # Use gradient descent for bias in Newton method

                except np.linalg.LinAlgError:
                    # Fallback to gradient descent
                    if self.verbose:
                        print(
                            f"Singular Hessian at iteration {i + 1}, using gradient descent"
                        )
                    self.weights -= self.learning_rate * dw
                    if self.fit_intercept:
                        self.bias -= self.learning_rate * db

            # Check convergence criteria
            converged = False

            # 1. Gradient norm convergence (primary criterion)
            if grad_norm < self.tolerance:
                converged = True
                if self.verbose:
                    print(
                        f"Converged: gradient norm {grad_norm:.2e} < tolerance {self.tolerance:.2e}"
                    )

            # 2. Cost change convergence
            if i > 5:
                recent_cost_change = abs(self.cost_history[-6] - cost)
                if recent_cost_change < self.tolerance * 10:
                    converged = True
                    if self.verbose:
                        print(
                            f"Converged: cost change {recent_cost_change:.2e} is small"
                        )

            # Early stopping based on cost improvement
            if cost < best_cost - 1e-8:
                best_cost = cost
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience and i > 100:
                if self.verbose:
                    print(f"Early stopping: no improvement for {patience} iterations")
                converged = True

            if converged:
                self.converged = True
                self.n_iterations = i + 1
                if self.verbose:
                    print(f"Converged after {i + 1} iterations")
                    print(f"Final cost: {cost:.6f}")
                    print(f"Final gradient norm: {grad_norm:.2e}")
                break

            # Progress reporting
            if self.verbose and (i + 1) % 100 == 0:
                print(
                    f"Iteration {i + 1:4d}, Cost: {cost:.6f}, Grad norm: {grad_norm:.2e}, LR: {self.learning_rate:.4f}"
                )

        if not self.converged:
            self.n_iterations = self.max_iterations
            if self.verbose:
                print(f"Did not converge after {self.max_iterations} iterations")
                print(f"Final cost: {cost:.6f}")
                print(f"Final gradient norm: {grad_norm:.2e}")

    def _compute_hessian_simplified(self, X, h):
        """
        Compute simplified Hessian matrix for weights only
        """
        m = X.shape[0]
        W = np.diag(h * (1 - h))
        hessian = (1 / m) * X.T.dot(W).dot(X)
        return hessian

    def predict_proba(self, X):
        """
        Predict class probabilities

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Test data

        Returns:
        --------
        array-like, shape (n_samples,)
            Predicted probabilities for positive class
        """
        X = np.array(X, dtype=np.float64)
        z = X.dot(self.weights)
        if self.fit_intercept:
            z += self.bias
        return self._sigmoid(z)

    def predict(self, X, threshold=0.5):
        """
        Make binary predictions

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Test data
        threshold : float, default=0.5
            Decision threshold

        Returns:
        --------
        array-like, shape (n_samples,)
            Binary predictions (0 or 1)
        """
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)

    def get_params(self):
        """Get model parameters"""
        return {
            "weights": self.weights,
            "bias": self.bias,
            "converged": self.converged,
            "n_iterations": self.n_iterations,
            "final_cost": self.cost_history[-1] if self.cost_history else None,
            "final_gradient_norm": self.gradient_norms[-1]
            if self.gradient_norms
            else None,
            "regularization": self.regularization,
            "C": self.C,
            "learning_rate": self.learning_rate,
        }

    def plot_cost_history(self, figsize=(10, 6)):
        """
        Plot the cost function history during training

        Parameters:
        -----------
        figsize : tuple, default=(10, 6)
            Figure size for the plot
        """
        if not self.cost_history:
            print("No cost history available. Train the model first.")
            return

        plt.figure(figsize=figsize)
        plt.plot(self.cost_history, linewidth=2)
        plt.title(f"Cost Function History - {self.method.title().replace('_', ' ')}")
        plt.xlabel("Iteration")
        plt.ylabel("Cross-Entropy Cost")
        plt.grid(True, alpha=0.3)

        # Add convergence indicator
        if self.converged:
            plt.axvline(
                x=self.n_iterations - 1,
                color="red",
                linestyle="--",
                label=f"Converged at iteration {self.n_iterations}",
            )
            plt.legend()

        plt.tight_layout()
        return plt.gcf()


def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Comprehensive evaluation of a logistic regression model

    Parameters:
    -----------
    model : LogisticRegressionScratch or sklearn model
        Trained model
    X_test : array-like
        Test features
    y_test : array-like
        Test labels
    model_name : str
        Name for display purposes

    Returns:
    --------
    dict
        Dictionary containing all evaluation metrics
    """
    # Predictions
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)
        if len(y_proba.shape) > 1:  # sklearn returns (n_samples, 2)
            y_proba = y_proba[:, 1]
    else:
        y_proba = model.predict_proba(X_test)

    y_pred = (y_proba >= 0.5).astype(int)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    # ROC AUC
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)

    # PR AUC
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall_curve, precision_curve)

    # Log Loss
    epsilon = 1e-15
    y_proba_clipped = np.clip(y_proba, epsilon, 1 - epsilon)
    log_loss = -np.mean(
        y_test * np.log(y_proba_clipped) + (1 - y_test) * np.log(1 - y_proba_clipped)
    )

    results = {
        "model_name": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "log_loss": log_loss,
        "fpr": fpr,
        "tpr": tpr,
        "precision_curve": precision_curve,
        "recall_curve": recall_curve,
        "y_proba": y_proba,
        "y_pred": y_pred,
    }

    # Print results
    print(f"\n{model_name} Evaluation Results:")
    print("-" * 40)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC AUC:   {roc_auc:.4f}")
    print(f"PR AUC:    {pr_auc:.4f}")
    print(f"Log Loss:  {log_loss:.4f}")

    return results


def compare_implementations(X_train, X_test, y_train, y_test):
    """
    Compare our implementation with sklearn's implementation

    Parameters:
    -----------
    X_train, X_test : array-like
        Training and test features
    y_train, y_test : array-like
        Training and test labels

    Returns:
    --------
    dict
        Comparison results
    """
    print("Comparing Implementations")
    print("=" * 50)

    results = {}

    # Our implementation with Gradient Descent
    print("\n1. Training our implementation (Gradient Descent)...")
    model_gd = LogisticRegressionScratch(
        learning_rate=0.1,
        max_iterations=5000,
        tolerance=1e-8,
        method="gradient_descent",
        verbose=True,
        regularization="l2",
        C=1.0,
        adaptive_lr=True,
        momentum=0.9,
    )
    model_gd.fit(X_train, y_train)
    results["gradient_descent"] = evaluate_model(
        model_gd, X_test, y_test, "Our Implementation (GD)"
    )

    # Our implementation with Newton-Raphson
    print("\n2. Training our implementation (Newton-Raphson)...")
    model_nr = LogisticRegressionScratch(
        learning_rate=0.01,
        max_iterations=1000,
        tolerance=1e-8,
        method="newton_raphson",
        verbose=True,
        regularization="l2",
        C=1.0,
    )
    model_nr.fit(X_train, y_train)
    results["newton_raphson"] = evaluate_model(
        model_nr, X_test, y_test, "Our Implementation (NR)"
    )

    # Sklearn implementation
    print("\n3. Training sklearn implementation...")
    model_sklearn = SklearnLogisticRegression(max_iter=2000, random_state=42)
    model_sklearn.fit(X_train, y_train)
    results["sklearn"] = evaluate_model(
        model_sklearn, X_test, y_test, "Sklearn Implementation"
    )

    # Comparison table
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"{'Metric':<12} {'Our (GD)':<12} {'Our (NR)':<12} {'Sklearn':<12}")
    print("-" * 60)

    metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc", "log_loss"]
    for metric in metrics:
        gd_val = results["gradient_descent"][metric]
        nr_val = results["newton_raphson"][metric]
        sk_val = results["sklearn"][metric]
        print(f"{metric:<12} {gd_val:<12.4f} {nr_val:<12.4f} {sk_val:<12.4f}")

    return results, [model_gd, model_nr, model_sklearn]


def create_comparison_plots(results, models, figsize=(15, 10)):
    """
    Create comprehensive comparison plots

    Parameters:
    -----------
    results : dict
        Results from compare_implementations
    models : list
        List of trained models
    figsize : tuple
        Figure size

    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle(
        "Logistic Regression Implementation Comparison", fontsize=16, fontweight="bold"
    )

    # 1. ROC Curves
    ax = axes[0, 0]
    colors = ["blue", "green", "red"]
    labels = ["Gradient Descent", "Newton-Raphson", "Sklearn"]

    for i, (key, result) in enumerate(results.items()):
        ax.plot(
            result["fpr"],
            result["tpr"],
            color=colors[i],
            label=f"{labels[i]} (AUC = {result['roc_auc']:.3f})",
            linewidth=2,
        )

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Precision-Recall Curves
    ax = axes[0, 1]
    for i, (key, result) in enumerate(results.items()):
        ax.plot(
            result["recall_curve"],
            result["precision_curve"],
            color=colors[i],
            label=f"{labels[i]} (AUC = {result['pr_auc']:.3f})",
            linewidth=2,
        )

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curves")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Cost History (for our implementations)
    ax = axes[0, 2]
    if models[0].cost_history:
        ax.plot(
            models[0].cost_history, label="Gradient Descent", color="blue", linewidth=2
        )
    if models[1].cost_history:
        ax.plot(
            models[1].cost_history, label="Newton-Raphson", color="green", linewidth=2
        )

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Cross-Entropy Cost")
    ax.set_title("Training Cost History")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Metrics Comparison Bar Plot
    ax = axes[1, 0]
    metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    x = np.arange(len(metrics))
    width = 0.25

    gd_values = [results["gradient_descent"][m] for m in metrics]
    nr_values = [results["newton_raphson"][m] for m in metrics]
    sk_values = [results["sklearn"][m] for m in metrics]

    ax.bar(
        x - width, gd_values, width, label="Gradient Descent", color="blue", alpha=0.7
    )
    ax.bar(x, nr_values, width, label="Newton-Raphson", color="green", alpha=0.7)
    ax.bar(x + width, sk_values, width, label="Sklearn", color="red", alpha=0.7)

    ax.set_xlabel("Metrics")
    ax.set_ylabel("Score")
    ax.set_title("Performance Metrics Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 5. Model Coefficients Comparison
    ax = axes[1, 1]

    # Get coefficients
    gd_coefs = np.concatenate([[models[0].bias], models[0].weights])
    nr_coefs = np.concatenate([[models[1].bias], models[1].weights])
    sk_coefs = np.concatenate([models[2].intercept_, models[2].coef_[0]])

    x = np.arange(len(gd_coefs))
    ax.bar(x - 0.25, gd_coefs, 0.25, label="Gradient Descent", alpha=0.7)
    ax.bar(x, nr_coefs, 0.25, label="Newton-Raphson", alpha=0.7)
    ax.bar(x + 0.25, sk_coefs, 0.25, label="Sklearn", alpha=0.7)

    ax.set_xlabel("Parameter Index")
    ax.set_ylabel("Coefficient Value")
    ax.set_title("Model Coefficients Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 6. Convergence Comparison
    ax = axes[1, 2]

    convergence_data = {
        "Gradient Descent": [models[0].n_iterations, models[0].converged],
        "Newton-Raphson": [models[1].n_iterations, models[1].converged],
        "Sklearn": ["N/A", "N/A"],
    }

    # Create a simple text-based comparison
    ax.axis("off")
    ax.text(0.1, 0.8, "Convergence Analysis:", fontsize=14, fontweight="bold")

    y_pos = 0.6
    for method, (iters, converged) in convergence_data.items():
        if iters != "N/A":
            status = "✓ Converged" if converged else "✗ Max iterations reached"
            ax.text(0.1, y_pos, f"{method}:", fontsize=12, fontweight="bold")
            ax.text(0.1, y_pos - 0.1, f"  Iterations: {iters}", fontsize=10)
            ax.text(0.1, y_pos - 0.15, f"  Status: {status}", fontsize=10)
        else:
            ax.text(0.1, y_pos, f"{method}: Uses different solver", fontsize=10)
        y_pos -= 0.25

    plt.tight_layout()
    return fig


def decision_boundary_plot(model, X, y, feature_names=None, figsize=(10, 8)):
    """
    Plot decision boundary for 2D data

    Parameters:
    -----------
    model : LogisticRegressionScratch
        Trained model
    X : array-like, shape (n_samples, 2)
        2D feature data
    y : array-like, shape (n_samples,)
        Labels
    feature_names : list, optional
        Names of the two features
    figsize : tuple
        Figure size
    """
    if X.shape[1] != 2:
        print("Decision boundary plot requires exactly 2 features")
        return

    plt.figure(figsize=figsize)

    # Create a mesh
    h = 0.01
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Make predictions on the mesh
    mesh_points = np.c_[xx.ravel(), yy.ravel()]
    Z = model.predict_proba(mesh_points)
    Z = Z.reshape(xx.shape)

    # Plot
    plt.contourf(xx, yy, Z, levels=50, alpha=0.6, cmap="RdYlBu")
    plt.colorbar(label="Predicted Probability")

    # Plot data points
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap="RdYlBu", edgecolors="black")
    plt.colorbar(scatter, label="True Class")

    # Plot decision boundary (probability = 0.5)
    plt.contour(xx, yy, Z, levels=[0.5], colors="black", linestyles="--", linewidths=2)

    # Labels
    if feature_names:
        plt.xlabel(feature_names[0])
        plt.ylabel(feature_names[1])
    else:
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")

    plt.title("Logistic Regression Decision Boundary")
    plt.grid(True, alpha=0.3)

    return plt.gcf()


def main():
    """
    Main function to demonstrate logistic regression implementation
    """
    print("Logistic Regression from Scratch - Demonstration")
    print("=" * 60)

    # Generate synthetic dataset
    print("\n1. Generating synthetic dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=4,
        n_redundant=0,
        n_informative=4,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=1.2,
    )

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Training set: {X_train_scaled.shape}")
    print(f"Test set: {X_test_scaled.shape}")
    print(f"Class distribution: {np.bincount(y_train)}")

    # Compare implementations
    results, models = compare_implementations(
        X_train_scaled, X_test_scaled, y_train, y_test
    )

    # Create comparison plots
    print("\n4. Creating comparison visualizations...")
    fig_comparison = create_comparison_plots(results, models)
    fig_comparison.savefig(
        os.path.join(OUTPUTS_DIR, "logistic_regression_comparison.png"),
        dpi=300,
        bbox_inches="tight",
    )
    print("Comparison plot saved as: logistic_regression_comparison.png")

    # Plot cost history for individual models
    print("\n5. Creating individual cost history plots...")
    fig_gd = models[0].plot_cost_history()
    if fig_gd:
        fig_gd.savefig(
            os.path.join(OUTPUTS_DIR, "gradient_descent_cost_history.png"),
            dpi=300,
            bbox_inches="tight",
        )
        print(
            "Gradient descent cost history saved as: gradient_descent_cost_history.png"
        )

    fig_nr = models[1].plot_cost_history()
    if fig_nr:
        fig_nr.savefig(
            os.path.join(OUTPUTS_DIR, "newton_raphson_cost_history.png"),
            dpi=300,
            bbox_inches="tight",
        )
        print("Newton-Raphson cost history saved as: newton_raphson_cost_history.png")

    # Decision boundary for 2D subset
    print("\n6. Creating decision boundary plot for 2D subset...")
    X_2d = X_train_scaled[:, :2]  # Use first 2 features
    y_2d = y_train

    # Train a model on 2D data
    model_2d = LogisticRegressionScratch(
        learning_rate=0.01,
        max_iterations=1000,
        method="gradient_descent",
        verbose=False,
    )
    model_2d.fit(X_2d, y_2d)

    fig_boundary = decision_boundary_plot(
        model_2d, X_2d, y_2d, feature_names=["Feature 1", "Feature 2"]
    )
    fig_boundary.savefig(
        os.path.join(OUTPUTS_DIR, "decision_boundary_2d.png"),
        dpi=300,
        bbox_inches="tight",
    )
    print("Decision boundary plot saved as: decision_boundary_2d.png")

    # Model parameters summary
    print("\n7. Model Parameters Summary:")
    print("=" * 40)

    for i, (name, model) in enumerate(
        [("Gradient Descent", models[0]), ("Newton-Raphson", models[1])]
    ):
        params = model.get_params()
        print(f"\n{name}:")
        print(f"  Converged: {params['converged']}")
        print(f"  Iterations: {params['n_iterations']}")
        print(f"  Final Cost: {params['final_cost']:.6f}")
        print(f"  Bias: {params['bias']:.4f}")
        print(f"  Weights: {params['weights']}")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Files generated:")
    print("- logistic_regression_comparison.png")
    print("- gradient_descent_cost_history.png")
    print("- newton_raphson_cost_history.png")
    print("- decision_boundary_2d.png")


if __name__ == "__main__":
    main()
