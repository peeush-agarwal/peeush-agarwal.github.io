"""
Regularized Logistic Regression Implementation

This module provides comprehensive implementations of regularized logistic regression
variants including L1 (Lasso), L2 (Ridge), and Elastic Net regularization.

Features:
- L1 Regularization (Lasso) with coordinate descent
- L2 Regularization (Ridge) with gradient descent
- Elastic Net combining L1 and L2
- Automatic hyperparameter tuning with cross-validation
- Feature selection capabilities
- Comprehensive evaluation and visualization

Author: Peeush Agarwal
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class RegularizedLogisticRegression:
    """
    Regularized Logistic Regression with L1, L2, and Elastic Net penalties
    """

    def __init__(
        self,
        regularization="l2",
        lambda_reg=0.01,
        l1_ratio=0.5,
        learning_rate=0.01,
        max_iterations=1000,
        tolerance=1e-6,
        verbose=False,
    ):
        """
        Initialize the Regularized Logistic Regression model

        Parameters:
        -----------
        regularization : str, default='l2'
            Type of regularization: 'l1', 'l2', or 'elastic_net'
        lambda_reg : float, default=0.01
            Regularization strength
        l1_ratio : float, default=0.5
            Ratio of L1 penalty in Elastic Net (0 = pure L2, 1 = pure L1)
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        max_iterations : int, default=1000
            Maximum number of iterations
        tolerance : float, default=1e-6
            Convergence tolerance
        verbose : bool, default=False
            Whether to print training progress
        """
        self.regularization = regularization
        self.lambda_reg = lambda_reg
        self.l1_ratio = l1_ratio
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.verbose = verbose

        # Model parameters
        self.weights = None
        self.bias = None
        self.cost_history = []
        self.converged = False
        self.n_iterations = 0
        self.feature_importance_ = None

    def _sigmoid(self, z):
        """Sigmoid activation function with numerical stability"""
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _compute_cost(self, h, y, weights):
        """
        Compute regularized cross-entropy cost

        Parameters:
        -----------
        h : array-like
            Predicted probabilities
        y : array-like
            True labels
        weights : array-like
            Model weights (excluding bias)

        Returns:
        --------
        float
            Regularized cost
        """
        # Base cross-entropy cost
        epsilon = 1e-15
        h = np.clip(h, epsilon, 1 - epsilon)
        base_cost = -np.mean(y * np.log(h) + (1 - y) * np.log(1 - h))

        # Regularization term
        reg_term = 0
        if self.regularization == "l1":
            reg_term = self.lambda_reg * np.sum(np.abs(weights))
        elif self.regularization == "l2":
            reg_term = self.lambda_reg * np.sum(weights**2)
        elif self.regularization == "elastic_net":
            l1_term = self.l1_ratio * np.sum(np.abs(weights))
            l2_term = (1 - self.l1_ratio) * np.sum(weights**2)
            reg_term = self.lambda_reg * (l1_term + l2_term)

        return base_cost + reg_term

    def _soft_threshold(self, x, threshold):
        """Soft thresholding function for L1 regularization"""
        return np.sign(x) * np.maximum(np.abs(x) - threshold, 0)

    def _coordinate_descent_l1(self, X, y):
        """
        Coordinate descent algorithm for L1 regularization

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target labels
        """
        m, n = X.shape

        # Initialize weights
        self.weights = np.random.normal(0, 0.01, n)
        self.bias = 0.0
        self.cost_history = []

        if self.verbose:
            print("Training with L1 regularization (Coordinate Descent)...")

        for iteration in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights) + self.bias
            h = self._sigmoid(z)

            # Store old weights for convergence check
            old_weights = self.weights.copy()
            old_bias = self.bias

            # Update bias
            gradient_bias = np.mean(h - y)
            self.bias -= self.learning_rate * gradient_bias

            # Update weights using coordinate descent
            for j in range(n):
                # Compute partial residual
                z_partial = X.dot(self.weights) + self.bias - self.weights[j] * X[:, j]
                h_partial = self._sigmoid(z_partial)

                # Gradient without regularization
                gradient_j = np.mean((h_partial - y) * X[:, j])

                # Coordinate descent update with soft thresholding
                weight_update = self.weights[j] - self.learning_rate * gradient_j
                self.weights[j] = self._soft_threshold(
                    weight_update, self.learning_rate * self.lambda_reg
                )

            # Compute cost
            cost = self._compute_cost(h, y, self.weights)
            self.cost_history.append(cost)

            # Check convergence
            weight_change = np.linalg.norm(self.weights - old_weights)
            bias_change = abs(self.bias - old_bias)

            if weight_change + bias_change < self.tolerance:
                self.converged = True
                self.n_iterations = iteration + 1
                if self.verbose:
                    print(f"Converged after {iteration + 1} iterations")
                break

            if self.verbose and (iteration + 1) % 100 == 0:
                print(
                    f"Iteration {iteration + 1}, Cost: {cost:.6f}, Active features: {np.sum(np.abs(self.weights) > 1e-6)}"
                )

        if not self.converged:
            self.n_iterations = self.max_iterations

        # Calculate feature importance
        self.feature_importance_ = np.abs(self.weights)

    def _gradient_descent_l2(self, X, y):
        """
        Gradient descent for L2 regularization

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target labels
        """
        m, n = X.shape

        # Initialize weights
        self.weights = np.random.normal(0, 0.01, n)
        self.bias = 0.0
        self.cost_history = []

        if self.verbose:
            print("Training with L2 regularization (Gradient Descent)...")

        for iteration in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights) + self.bias
            h = self._sigmoid(z)

            # Compute gradients
            gradient_weights = (1 / m) * X.T.dot(
                h - y
            ) + 2 * self.lambda_reg * self.weights
            gradient_bias = np.mean(h - y)

            # Store old parameters
            old_weights = self.weights.copy()
            old_bias = self.bias

            # Update parameters
            self.weights -= self.learning_rate * gradient_weights
            self.bias -= self.learning_rate * gradient_bias

            # Compute cost
            cost = self._compute_cost(h, y, self.weights)
            self.cost_history.append(cost)

            # Check convergence
            weight_change = np.linalg.norm(self.weights - old_weights)
            bias_change = abs(self.bias - old_bias)

            if weight_change + bias_change < self.tolerance:
                self.converged = True
                self.n_iterations = iteration + 1
                if self.verbose:
                    print(f"Converged after {iteration + 1} iterations")
                break

            if self.verbose and (iteration + 1) % 100 == 0:
                print(f"Iteration {iteration + 1}, Cost: {cost:.6f}")

        if not self.converged:
            self.n_iterations = self.max_iterations

        # Calculate feature importance
        self.feature_importance_ = np.abs(self.weights)

    def _elastic_net_gradient_descent(self, X, y):
        """
        Gradient descent for Elastic Net regularization

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target labels
        """
        m, n = X.shape

        # Initialize weights
        self.weights = np.random.normal(0, 0.01, n)
        self.bias = 0.0
        self.cost_history = []

        if self.verbose:
            print("Training with Elastic Net regularization...")

        for iteration in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights) + self.bias
            h = self._sigmoid(z)

            # Compute gradients
            base_gradient = (1 / m) * X.T.dot(h - y)
            l1_gradient = self.lambda_reg * self.l1_ratio * np.sign(self.weights)
            l2_gradient = self.lambda_reg * (1 - self.l1_ratio) * 2 * self.weights

            gradient_weights = base_gradient + l1_gradient + l2_gradient
            gradient_bias = np.mean(h - y)

            # Store old parameters
            old_weights = self.weights.copy()
            old_bias = self.bias

            # Update parameters
            self.weights -= self.learning_rate * gradient_weights
            self.bias -= self.learning_rate * gradient_bias

            # Compute cost
            cost = self._compute_cost(h, y, self.weights)
            self.cost_history.append(cost)

            # Check convergence
            weight_change = np.linalg.norm(self.weights - old_weights)
            bias_change = abs(self.bias - old_bias)

            if weight_change + bias_change < self.tolerance:
                self.converged = True
                self.n_iterations = iteration + 1
                if self.verbose:
                    print(f"Converged after {iteration + 1} iterations")
                break

            if self.verbose and (iteration + 1) % 100 == 0:
                print(f"Iteration {iteration + 1}, Cost: {cost:.6f}")

        if not self.converged:
            self.n_iterations = self.max_iterations

        # Calculate feature importance
        self.feature_importance_ = np.abs(self.weights)

    def fit(self, X, y):
        """
        Fit the regularized logistic regression model

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values (0 or 1)
        """
        X = np.array(X)
        y = np.array(y)

        # Choose optimization method based on regularization type
        if self.regularization == "l1":
            self._coordinate_descent_l1(X, y)
        elif self.regularization == "l2":
            self._gradient_descent_l2(X, y)
        elif self.regularization == "elastic_net":
            self._elastic_net_gradient_descent(X, y)
        else:
            raise ValueError("regularization must be 'l1', 'l2', or 'elastic_net'")

    def predict_proba(self, X):
        """Predict class probabilities"""
        X = np.array(X)
        z = X.dot(self.weights) + self.bias
        return self._sigmoid(z)

    def predict(self, X, threshold=0.5):
        """Make binary predictions"""
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)

    def get_feature_importance(self):
        """Get feature importance scores"""
        return self.feature_importance_

    def get_selected_features(self, threshold=1e-6):
        """Get indices of selected features (for L1 regularization)"""
        if self.feature_importance_ is None:
            return None
        return np.where(self.feature_importance_ > threshold)[0]


class RegularizationPathAnalyzer:
    """
    Analyze regularization path and perform hyperparameter tuning
    """

    def __init__(self, regularization="l2", lambda_values=None, cv_folds=5):
        """
        Initialize the analyzer

        Parameters:
        -----------
        regularization : str
            Type of regularization
        lambda_values : array-like, optional
            Lambda values to test
        cv_folds : int
            Number of cross-validation folds
        """
        self.regularization = regularization
        self.lambda_values = lambda_values or np.logspace(-4, 2, 20)
        self.cv_folds = cv_folds
        self.cv_scores_ = None
        self.best_lambda_ = None
        self.models_ = None

    def cross_validate(self, X, y):
        """
        Perform cross-validation to find best lambda

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels

        Returns:
        --------
        dict
            Cross-validation results
        """
        X = np.array(X)
        y = np.array(y)

        kfold = KFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
        cv_scores = []
        models = []

        print(
            f"Performing {self.cv_folds}-fold cross-validation for {len(self.lambda_values)} lambda values..."
        )

        for i, lambda_val in enumerate(self.lambda_values):
            fold_scores = []

            for train_idx, val_idx in kfold.split(X):
                X_train, X_val = X[train_idx], X[val_idx]
                y_train, y_val = y[train_idx], y[val_idx]

                # Train model
                model = RegularizedLogisticRegression(
                    regularization=self.regularization,
                    lambda_reg=lambda_val,
                    max_iterations=1000,
                    verbose=False,
                )
                model.fit(X_train, y_train)

                # Evaluate
                y_pred_proba = model.predict_proba(X_val)
                score = roc_auc_score(y_val, y_pred_proba)
                fold_scores.append(score)

            avg_score = np.mean(fold_scores)
            std_score = np.std(fold_scores)
            cv_scores.append(
                {"lambda": lambda_val, "mean_score": avg_score, "std_score": std_score}
            )

            # Train final model on full data for this lambda
            final_model = RegularizedLogisticRegression(
                regularization=self.regularization,
                lambda_reg=lambda_val,
                max_iterations=1000,
                verbose=False,
            )
            final_model.fit(X, y)
            models.append(final_model)

            if i % 5 == 0:
                print(
                    f"Lambda {lambda_val:.4f}: ROC-AUC = {avg_score:.4f} ± {std_score:.4f}"
                )

        self.cv_scores_ = cv_scores
        self.models_ = models

        # Find best lambda
        best_idx = np.argmax([score["mean_score"] for score in cv_scores])
        self.best_lambda_ = self.lambda_values[best_idx]

        print(f"\nBest lambda: {self.best_lambda_:.4f}")
        print(
            f"Best CV score: {cv_scores[best_idx]['mean_score']:.4f} ± {cv_scores[best_idx]['std_score']:.4f}"
        )

        return {
            "cv_scores": cv_scores,
            "best_lambda": self.best_lambda_,
            "best_model": models[best_idx],
        }

    def plot_regularization_path(self, feature_names=None, figsize=(12, 8)):
        """
        Plot regularization path showing coefficient values vs lambda

        Parameters:
        -----------
        feature_names : list, optional
            Names of features
        figsize : tuple
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if self.models_ is None:
            print("Run cross_validate first")
            return None

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(
            f"{self.regularization.upper()} Regularization Path Analysis",
            fontsize=16,
            fontweight="bold",
        )

        # 1. Coefficient paths
        ax = axes[0, 0]
        coefficients = np.array([model.weights for model in self.models_])

        for i in range(coefficients.shape[1]):
            label = (
                feature_names[i]
                if feature_names and i < len(feature_names)
                else f"Feature {i}"
            )
            ax.plot(
                self.lambda_values,
                coefficients[:, i],
                marker="o",
                label=label,
                linewidth=2,
            )

        ax.set_xscale("log")
        ax.set_xlabel("Lambda (regularization strength)")
        ax.set_ylabel("Coefficient Value")
        ax.set_title("Coefficient Paths")
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax.grid(True, alpha=0.3)

        # 2. Cross-validation scores
        ax = axes[0, 1]
        mean_scores = [score["mean_score"] for score in self.cv_scores_]
        std_scores = [score["std_score"] for score in self.cv_scores_]

        ax.errorbar(
            self.lambda_values,
            mean_scores,
            yerr=std_scores,
            marker="o",
            capsize=5,
            linewidth=2,
        )
        ax.axvline(
            x=self.best_lambda_,
            color="red",
            linestyle="--",
            label=f"Best λ = {self.best_lambda_:.4f}",
        )

        ax.set_xscale("log")
        ax.set_xlabel("Lambda (regularization strength)")
        ax.set_ylabel("Cross-Validation ROC-AUC")
        ax.set_title("Cross-Validation Performance")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 3. Number of selected features (for L1)
        ax = axes[1, 0]
        if self.regularization == "l1":
            n_selected = [
                np.sum(np.abs(model.weights) > 1e-6) for model in self.models_
            ]
            ax.plot(
                self.lambda_values, n_selected, marker="o", linewidth=2, color="green"
            )
            ax.axvline(
                x=self.best_lambda_,
                color="red",
                linestyle="--",
                label=f"Best λ = {self.best_lambda_:.4f}",
            )
            ax.set_xscale("log")
            ax.set_xlabel("Lambda (regularization strength)")
            ax.set_ylabel("Number of Selected Features")
            ax.set_title("Feature Selection (L1 Regularization)")
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            # Feature importance at best lambda
            best_idx = np.argmax([score["mean_score"] for score in self.cv_scores_])
            importance = self.models_[best_idx].get_feature_importance()

            x_pos = np.arange(len(importance))
            bars = ax.bar(x_pos, importance, alpha=0.7)
            ax.set_xlabel("Feature Index")
            ax.set_ylabel("Feature Importance")
            ax.set_title("Feature Importance at Best Lambda")
            ax.set_xticks(x_pos)

            if feature_names:
                ax.set_xticklabels(
                    feature_names[: len(importance)], rotation=45, ha="right"
                )

            ax.grid(True, alpha=0.3)

        # 4. Training cost for best model
        ax = axes[1, 1]
        best_idx = np.argmax([score["mean_score"] for score in self.cv_scores_])
        best_model = self.models_[best_idx]

        if best_model.cost_history:
            ax.plot(best_model.cost_history, linewidth=2, color="blue")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Regularized Cost")
            ax.set_title(f"Training Cost (Best λ = {self.best_lambda_:.4f})")
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


def compare_regularization_methods(X_train, X_test, y_train, y_test, lambda_reg=0.01):
    """
    Compare different regularization methods

    Parameters:
    -----------
    X_train, X_test : array-like
        Training and test features
    y_train, y_test : array-like
        Training and test labels
    lambda_reg : float
        Regularization strength to use for comparison

    Returns:
    --------
    dict
        Comparison results
    """
    print("Comparing Regularization Methods")
    print("=" * 50)

    methods = ["l1", "l2", "elastic_net"]
    results = {}
    models = {}

    for method in methods:
        print(f"\nTraining {method.upper()} regularized model...")

        model = RegularizedLogisticRegression(
            regularization=method,
            lambda_reg=lambda_reg,
            l1_ratio=0.5,  # For elastic net
            max_iterations=2000,
            verbose=True,
        )

        model.fit(X_train, y_train)
        models[method] = model

        # Evaluate
        y_pred_proba = model.predict_proba(X_test)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        logloss = log_loss(y_test, y_pred_proba)

        # Feature selection (for L1)
        n_selected = np.sum(np.abs(model.weights) > 1e-6)

        results[method] = {
            "accuracy": accuracy,
            "roc_auc": roc_auc,
            "log_loss": logloss,
            "n_selected_features": n_selected,
            "converged": model.converged,
            "n_iterations": model.n_iterations,
        }

        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        print(f"  Log Loss: {logloss:.4f}")
        print(f"  Selected Features: {n_selected}")

    # Comparison table
    print("\n" + "=" * 70)
    print("REGULARIZATION COMPARISON SUMMARY")
    print("=" * 70)
    print(f"{'Metric':<20} {'L1 (Lasso)':<15} {'L2 (Ridge)':<15} {'Elastic Net':<15}")
    print("-" * 70)

    metrics = ["accuracy", "roc_auc", "log_loss", "n_selected_features"]
    for metric in metrics:
        l1_val = results["l1"][metric]
        l2_val = results["l2"][metric]
        en_val = results["elastic_net"][metric]
        print(f"{metric:<20} {l1_val:<15.4f} {l2_val:<15.4f} {en_val:<15.4f}")

    return results, models


def create_regularization_comparison_plot(results, models, figsize=(15, 10)):
    """
    Create comprehensive comparison plot for regularization methods

    Parameters:
    -----------
    results : dict
        Results from compare_regularization_methods
    models : dict
        Trained models
    figsize : tuple
        Figure size

    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Regularization Methods Comparison", fontsize=16, fontweight="bold")

    methods = ["l1", "l2", "elastic_net"]
    method_names = ["L1 (Lasso)", "L2 (Ridge)", "Elastic Net"]
    colors = ["blue", "green", "red"]

    # 1. Performance metrics comparison
    ax = axes[0, 0]
    metrics = ["accuracy", "roc_auc"]
    x = np.arange(len(metrics))
    width = 0.25

    for i, method in enumerate(methods):
        values = [results[method][metric] for metric in metrics]
        ax.bar(
            x + i * width,
            values,
            width,
            label=method_names[i],
            color=colors[i],
            alpha=0.7,
        )

    ax.set_xlabel("Metrics")
    ax.set_ylabel("Score")
    ax.set_title("Performance Metrics")
    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Feature selection
    ax = axes[0, 1]
    n_features = [results[method]["n_selected_features"] for method in methods]
    bars = ax.bar(method_names, n_features, color=colors, alpha=0.7)
    ax.set_ylabel("Number of Selected Features")
    ax.set_title("Feature Selection")
    ax.grid(True, alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    # 3. Coefficient comparison
    ax = axes[0, 2]
    for i, method in enumerate(methods):
        model = models[method]
        ax.plot(
            model.weights,
            marker="o",
            label=method_names[i],
            color=colors[i],
            linewidth=2,
        )

    ax.set_xlabel("Feature Index")
    ax.set_ylabel("Coefficient Value")
    ax.set_title("Coefficient Values")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Cost history comparison
    ax = axes[1, 0]
    for i, method in enumerate(methods):
        model = models[method]
        if model.cost_history:
            ax.plot(
                model.cost_history, label=method_names[i], color=colors[i], linewidth=2
            )

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Regularized Cost")
    ax.set_title("Training Cost History")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 5. Convergence analysis
    ax = axes[1, 1]
    ax.axis("off")
    ax.text(0.1, 0.8, "Convergence Analysis:", fontsize=14, fontweight="bold")

    y_pos = 0.6
    for i, method in enumerate(methods):
        model = models[method]
        status = "✓ Converged" if model.converged else "✗ Max iterations"
        ax.text(0.1, y_pos, f"{method_names[i]}:", fontsize=12, fontweight="bold")
        ax.text(0.1, y_pos - 0.1, f"  Iterations: {model.n_iterations}", fontsize=10)
        ax.text(0.1, y_pos - 0.15, f"  Status: {status}", fontsize=10)
        y_pos -= 0.25

    # 6. Feature importance (absolute values)
    ax = axes[1, 2]
    feature_importance = {}
    for method in methods:
        model = models[method]
        feature_importance[method] = np.abs(model.weights)

    x = np.arange(len(feature_importance["l1"]))
    width = 0.25

    for i, method in enumerate(methods):
        ax.bar(
            x + i * width,
            feature_importance[method],
            width,
            label=method_names[i],
            color=colors[i],
            alpha=0.7,
        )

    ax.set_xlabel("Feature Index")
    ax.set_ylabel("|Coefficient Value|")
    ax.set_title("Feature Importance (Absolute)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([f"F{i}" for i in range(len(x))])
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def main():
    """
    Main function to demonstrate regularized logistic regression
    """
    print("Regularized Logistic Regression - Demonstration")
    print("=" * 60)

    # Generate synthetic dataset with some irrelevant features
    print("\n1. Generating synthetic dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=5,
        n_redundant=5,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=1.0,
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

    # Compare regularization methods
    print("\n2. Comparing regularization methods...")
    results, models = compare_regularization_methods(
        X_train_scaled, X_test_scaled, y_train, y_test, lambda_reg=0.01
    )

    # Create comparison plot
    print("\n3. Creating comparison visualizations...")
    fig_comparison = create_regularization_comparison_plot(results, models)
    fig_comparison.savefig(
        "regularization_comparison.png", dpi=300, bbox_inches="tight"
    )
    print("Comparison plot saved as: regularization_comparison.png")

    # Regularization path analysis for L1
    print("\n4. Analyzing L1 regularization path...")
    analyzer_l1 = RegularizationPathAnalyzer(regularization="l1")
    cv_results_l1 = analyzer_l1.cross_validate(X_train_scaled, y_train)

    feature_names = [f"Feature_{i}" for i in range(X_train_scaled.shape[1])]
    fig_path_l1 = analyzer_l1.plot_regularization_path(feature_names)
    fig_path_l1.savefig("l1_regularization_path.png", dpi=300, bbox_inches="tight")
    print("L1 regularization path saved as: l1_regularization_path.png")

    # Regularization path analysis for L2
    print("\n5. Analyzing L2 regularization path...")
    analyzer_l2 = RegularizationPathAnalyzer(regularization="l2")
    cv_results_l2 = analyzer_l2.cross_validate(X_train_scaled, y_train)

    fig_path_l2 = analyzer_l2.plot_regularization_path(feature_names)
    fig_path_l2.savefig("l2_regularization_path.png", dpi=300, bbox_inches="tight")
    print("L2 regularization path saved as: l2_regularization_path.png")

    # Feature selection analysis
    print("\n6. Feature selection analysis...")
    best_l1_model = cv_results_l1["best_model"]
    selected_features = best_l1_model.get_selected_features()

    print(f"L1 regularization selected {len(selected_features)} features:")
    for idx in selected_features:
        print(f"  Feature {idx}: coefficient = {best_l1_model.weights[idx]:.4f}")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Files generated:")
    print("- regularization_comparison.png")
    print("- l1_regularization_path.png")
    print("- l2_regularization_path.png")


if __name__ == "__main__":
    main()
