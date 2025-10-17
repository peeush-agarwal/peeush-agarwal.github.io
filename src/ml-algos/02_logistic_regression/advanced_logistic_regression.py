"""
Advanced Logistic Regression Implementations

This module provides implementations of advanced logistic regression variants:
- Multinomial Logistic Regression for multiclass classification
- Ordinal Logistic Regression for ordered categorical outcomes
- Class Imbalance Handling techniques
- Online/Streaming Logistic Regression

Features:
- Softmax-based multinomial classification
- Proportional odds model for ordinal regression
- SMOTE, class weights, and threshold tuning for imbalance
- Stochastic gradient descent for online learning

Author: Peeush Agarwal
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class MultinomialLogisticRegression:
    """
    Multinomial Logistic Regression using softmax function
    """

    def __init__(
        self, learning_rate=0.01, max_iterations=1000, tolerance=1e-6, verbose=False
    ):
        """
        Initialize the Multinomial Logistic Regression model

        Parameters:
        -----------
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        max_iterations : int, default=1000
            Maximum number of iterations
        tolerance : float, default=1e-6
            Convergence tolerance
        verbose : bool, default=False
            Whether to print training progress
        """
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.verbose = verbose

        # Model parameters
        self.weights = None
        self.bias = None
        self.n_classes = None
        self.classes_ = None
        self.cost_history = []
        self.converged = False
        self.n_iterations = 0

    def _softmax(self, z):
        """
        Softmax activation function with numerical stability

        Parameters:
        -----------
        z : array-like, shape (n_samples, n_classes)
            Linear combination scores

        Returns:
        --------
        array-like, shape (n_samples, n_classes)
            Softmax probabilities
        """
        # Subtract max for numerical stability
        z_stable = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z_stable)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def _one_hot_encode(self, y):
        """Convert labels to one-hot encoding"""
        n_samples = len(y)
        one_hot = np.zeros((n_samples, self.n_classes))
        for i, label in enumerate(y):
            class_idx = np.where(self.classes_ == label)[0][0]
            one_hot[i, class_idx] = 1
        return one_hot

    def _compute_cost(self, h, y_one_hot):
        """
        Compute cross-entropy cost for multiclass classification

        Parameters:
        -----------
        h : array-like, shape (n_samples, n_classes)
            Predicted probabilities
        y_one_hot : array-like, shape (n_samples, n_classes)
            True labels in one-hot format

        Returns:
        --------
        float
            Cross-entropy cost
        """
        # Add small epsilon to prevent log(0)
        epsilon = 1e-15
        h = np.clip(h, epsilon, 1 - epsilon)

        cost = -np.mean(np.sum(y_one_hot * np.log(h), axis=1))
        return cost

    def fit(self, X, y):
        """
        Fit the multinomial logistic regression model

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target labels
        """
        X = np.array(X)
        y = np.array(y)

        # Determine classes and dimensions
        self.classes_ = np.unique(y)
        self.n_classes = len(self.classes_)
        n_samples, n_features = X.shape

        if self.n_classes < 2:
            raise ValueError("Need at least 2 classes for classification")

        # Initialize parameters
        # Shape: (n_features, n_classes)
        self.weights = np.random.normal(0, 0.01, (n_features, self.n_classes))
        self.bias = np.zeros(self.n_classes)

        # Convert labels to one-hot encoding
        y_one_hot = self._one_hot_encode(y)

        if self.verbose:
            print(f"Training multinomial logistic regression...")
            print(f"Classes: {self.classes_}")
            print(f"Dataset shape: {X.shape}")

        self.cost_history = []

        for iteration in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights) + self.bias  # Shape: (n_samples, n_classes)
            h = self._softmax(z)  # Shape: (n_samples, n_classes)

            # Compute cost
            cost = self._compute_cost(h, y_one_hot)
            self.cost_history.append(cost)

            # Compute gradients
            error = h - y_one_hot  # Shape: (n_samples, n_classes)
            grad_weights = (1 / n_samples) * X.T.dot(
                error
            )  # Shape: (n_features, n_classes)
            grad_bias = np.mean(error, axis=0)  # Shape: (n_classes,)

            # Store old parameters for convergence check
            old_weights = self.weights.copy()
            old_bias = self.bias.copy()

            # Update parameters
            self.weights -= self.learning_rate * grad_weights
            self.bias -= self.learning_rate * grad_bias

            # Check convergence
            weight_change = np.linalg.norm(self.weights - old_weights)
            bias_change = np.linalg.norm(self.bias - old_bias)

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
            if self.verbose:
                print(f"Did not converge after {self.max_iterations} iterations")

    def predict_proba(self, X):
        """
        Predict class probabilities

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Test data

        Returns:
        --------
        array-like, shape (n_samples, n_classes)
            Predicted probabilities for each class
        """
        X = np.array(X)
        z = X.dot(self.weights) + self.bias
        return self._softmax(z)

    def predict(self, X):
        """
        Make predictions

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Test data

        Returns:
        --------
        array-like, shape (n_samples,)
            Predicted class labels
        """
        probabilities = self.predict_proba(X)
        predicted_indices = np.argmax(probabilities, axis=1)
        return self.classes_[predicted_indices]


class OrdinalLogisticRegression:
    """
    Ordinal Logistic Regression using proportional odds model
    """

    def __init__(
        self, learning_rate=0.01, max_iterations=1000, tolerance=1e-6, verbose=False
    ):
        """
        Initialize the Ordinal Logistic Regression model

        Parameters:
        -----------
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        max_iterations : int, default=1000
            Maximum number of iterations
        tolerance : float, default=1e-6
            Convergence tolerance
        verbose : bool, default=False
            Whether to print training progress
        """
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.verbose = verbose

        # Model parameters
        self.weights = None
        self.thresholds = None
        self.n_classes = None
        self.classes_ = None
        self.cost_history = []
        self.converged = False
        self.n_iterations = 0

    def _sigmoid(self, z):
        """Sigmoid activation function with numerical stability"""
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _compute_cumulative_probabilities(self, X):
        """
        Compute cumulative probabilities P(Y <= k) for each threshold k

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix

        Returns:
        --------
        array-like, shape (n_samples, n_classes-1)
            Cumulative probabilities
        """
        linear_combo = X.dot(self.weights)  # Shape: (n_samples,)

        # Compute P(Y <= k) = sigmoid(threshold_k - X*beta)
        cum_probs = []
        for k in range(self.n_classes - 1):
            prob_k = self._sigmoid(self.thresholds[k] - linear_combo)
            cum_probs.append(prob_k)

        return np.column_stack(cum_probs)  # Shape: (n_samples, n_classes-1)

    def _compute_class_probabilities(self, cum_probs):
        """
        Convert cumulative probabilities to class probabilities

        Parameters:
        -----------
        cum_probs : array-like, shape (n_samples, n_classes-1)
            Cumulative probabilities

        Returns:
        --------
        array-like, shape (n_samples, n_classes)
            Class probabilities
        """
        n_samples = cum_probs.shape[0]
        class_probs = np.zeros((n_samples, self.n_classes))

        # P(Y = 1) = P(Y <= 1)
        class_probs[:, 0] = cum_probs[:, 0]

        # P(Y = k) = P(Y <= k) - P(Y <= k-1) for k = 2, ..., K-1
        for k in range(1, self.n_classes - 1):
            class_probs[:, k] = cum_probs[:, k] - cum_probs[:, k - 1]

        # P(Y = K) = 1 - P(Y <= K-1)
        class_probs[:, -1] = 1 - cum_probs[:, -1]

        return class_probs

    def _compute_cost(self, class_probs, y):
        """
        Compute negative log-likelihood for ordinal regression

        Parameters:
        -----------
        class_probs : array-like, shape (n_samples, n_classes)
            Predicted class probabilities
        y : array-like, shape (n_samples,)
            True class indices

        Returns:
        --------
        float
            Negative log-likelihood
        """
        epsilon = 1e-15
        class_probs = np.clip(class_probs, epsilon, 1 - epsilon)

        # Extract probabilities for true classes
        true_class_probs = class_probs[np.arange(len(y)), y]

        return -np.mean(np.log(true_class_probs))

    def fit(self, X, y):
        """
        Fit the ordinal logistic regression model

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Ordinal target labels (0, 1, 2, ...)
        """
        X = np.array(X)
        y = np.array(y)

        # Determine classes
        self.classes_ = np.unique(y)
        self.n_classes = len(self.classes_)

        if self.n_classes < 3:
            raise ValueError("Ordinal regression requires at least 3 classes")

        # Map labels to indices
        label_to_idx = {label: idx for idx, label in enumerate(self.classes_)}
        y_indexed = np.array([label_to_idx[label] for label in y])

        n_samples, n_features = X.shape

        # Initialize parameters
        self.weights = np.random.normal(0, 0.01, n_features)
        # Initialize thresholds in ascending order
        self.thresholds = np.linspace(-2, 2, self.n_classes - 1)

        if self.verbose:
            print(f"Training ordinal logistic regression...")
            print(f"Classes: {self.classes_}")
            print(f"Dataset shape: {X.shape}")

        self.cost_history = []

        for iteration in range(self.max_iterations):
            # Forward pass
            cum_probs = self._compute_cumulative_probabilities(X)
            class_probs = self._compute_class_probabilities(cum_probs)

            # Compute cost
            cost = self._compute_cost(class_probs, y_indexed)
            self.cost_history.append(cost)

            # Compute gradients (simplified version)
            # This is a simplified gradient computation for demonstration
            linear_combo = X.dot(self.weights)

            # Gradient for weights
            grad_weights = np.zeros_like(self.weights)
            for i in range(n_samples):
                true_class = y_indexed[i]

                # Contribution from each threshold
                for k in range(self.n_classes - 1):
                    sigmoid_val = self._sigmoid(self.thresholds[k] - linear_combo[i])

                    if true_class == 0 and k == 0:
                        # First class: gradient from P(Y <= 1)
                        grad_weights += -X[i] * sigmoid_val * (1 - sigmoid_val)
                    elif true_class == k + 1 and k < self.n_classes - 1:
                        # Middle classes: gradient from P(Y <= k+1) - P(Y <= k)
                        grad_weights += X[i] * sigmoid_val * (1 - sigmoid_val)
                    elif true_class > k + 1:
                        # Higher classes: gradient from 1 - P(Y <= k)
                        grad_weights += X[i] * sigmoid_val * (1 - sigmoid_val)

            grad_weights /= n_samples

            # Gradient for thresholds (simplified)
            grad_thresholds = np.zeros_like(self.thresholds)
            for k in range(self.n_classes - 1):
                for i in range(n_samples):
                    true_class = y_indexed[i]
                    sigmoid_val = self._sigmoid(self.thresholds[k] - linear_combo[i])

                    if true_class <= k:
                        grad_thresholds[k] += sigmoid_val * (1 - sigmoid_val)
                    else:
                        grad_thresholds[k] += -sigmoid_val * (1 - sigmoid_val)

                grad_thresholds[k] /= n_samples

            # Store old parameters
            old_weights = self.weights.copy()
            old_thresholds = self.thresholds.copy()

            # Update parameters
            self.weights -= self.learning_rate * grad_weights
            self.thresholds -= self.learning_rate * grad_thresholds

            # Ensure thresholds remain in ascending order
            self.thresholds = np.sort(self.thresholds)

            # Check convergence
            weight_change = np.linalg.norm(self.weights - old_weights)
            threshold_change = np.linalg.norm(self.thresholds - old_thresholds)

            if weight_change + threshold_change < self.tolerance:
                self.converged = True
                self.n_iterations = iteration + 1
                if self.verbose:
                    print(f"Converged after {iteration + 1} iterations")
                break

            if self.verbose and (iteration + 1) % 100 == 0:
                print(f"Iteration {iteration + 1}, Cost: {cost:.6f}")

        if not self.converged:
            self.n_iterations = self.max_iterations

    def predict_proba(self, X):
        """Predict class probabilities"""
        cum_probs = self._compute_cumulative_probabilities(X)
        return self._compute_class_probabilities(cum_probs)

    def predict(self, X):
        """Make predictions"""
        probabilities = self.predict_proba(X)
        predicted_indices = np.argmax(probabilities, axis=1)
        return self.classes_[predicted_indices]


class SMOTEOversampler:
    """
    Synthetic Minority Oversampling Technique (SMOTE) implementation
    """

    def __init__(self, k_neighbors=5, random_state=None):
        """
        Initialize SMOTE

        Parameters:
        -----------
        k_neighbors : int, default=5
            Number of nearest neighbors to use
        random_state : int, optional
            Random seed for reproducibility
        """
        self.k_neighbors = k_neighbors
        self.random_state = random_state
        if random_state is not None:
            np.random.seed(random_state)

    def _find_k_neighbors(self, X, sample_idx, k):
        """Find k nearest neighbors for a given sample"""
        distances = np.linalg.norm(X - X[sample_idx], axis=1)
        neighbor_indices = np.argsort(distances)[1 : k + 1]  # Exclude self
        return neighbor_indices

    def fit_resample(self, X, y):
        """
        Apply SMOTE to oversample minority classes

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target labels

        Returns:
        --------
        X_resampled, y_resampled : arrays
            Resampled data
        """
        X = np.array(X)
        y = np.array(y)

        # Count class frequencies
        class_counts = Counter(y)
        majority_count = max(class_counts.values())

        X_resampled = X.copy()
        y_resampled = y.copy()

        # Oversample each minority class
        for class_label, count in class_counts.items():
            if count < majority_count:
                # Number of synthetic samples to generate
                n_synthetic = majority_count - count

                # Get samples of this class
                class_indices = np.where(y == class_label)[0]
                class_samples = X[class_indices]

                # Generate synthetic samples
                synthetic_samples = []
                for _ in range(n_synthetic):
                    # Randomly select a sample from minority class
                    sample_idx = np.random.choice(len(class_samples))
                    sample = class_samples[sample_idx]

                    # Find k nearest neighbors
                    neighbor_indices = self._find_k_neighbors(
                        class_samples,
                        sample_idx,
                        min(self.k_neighbors, len(class_samples) - 1),
                    )

                    # Randomly select one neighbor
                    neighbor_idx = np.random.choice(neighbor_indices)
                    neighbor = class_samples[neighbor_idx]

                    # Generate synthetic sample
                    # S = S_i + rand(0,1) * (S_nn - S_i)
                    alpha = np.random.random()
                    synthetic_sample = sample + alpha * (neighbor - sample)
                    synthetic_samples.append(synthetic_sample)

                # Add synthetic samples
                if synthetic_samples:
                    synthetic_samples = np.array(synthetic_samples)
                    X_resampled = np.vstack([X_resampled, synthetic_samples])
                    y_resampled = np.hstack(
                        [y_resampled, np.full(len(synthetic_samples), class_label)]
                    )

        return X_resampled, y_resampled


class ImbalancedLogisticRegression:
    """
    Logistic Regression with techniques to handle class imbalance
    """

    def __init__(
        self,
        method="class_weights",
        learning_rate=0.01,
        max_iterations=1000,
        smote_k=5,
        verbose=False,
    ):
        """
        Initialize imbalanced logistic regression

        Parameters:
        -----------
        method : str, default='class_weights'
            Method to handle imbalance: 'class_weights', 'smote', 'threshold_tuning'
        learning_rate : float, default=0.01
            Learning rate for gradient descent
        max_iterations : int, default=1000
            Maximum number of iterations
        smote_k : int, default=5
            Number of neighbors for SMOTE
        verbose : bool, default=False
            Whether to print training progress
        """
        self.method = method
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.smote_k = smote_k
        self.verbose = verbose

        # Model parameters
        self.weights = None
        self.bias = None
        self.class_weights = None
        self.optimal_threshold = 0.5
        self.cost_history = []
        self.smote_sampler = None

    def _sigmoid(self, z):
        """Sigmoid activation function"""
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _compute_class_weights(self, y):
        """Compute class weights inversely proportional to class frequencies"""
        class_counts = Counter(y)
        total_samples = len(y)
        n_classes = len(class_counts)

        weights = {}
        for class_label, count in class_counts.items():
            weights[class_label] = total_samples / (n_classes * count)

        return weights

    def _compute_weighted_cost(self, h, y, sample_weights):
        """Compute weighted cross-entropy cost"""
        epsilon = 1e-15
        h = np.clip(h, epsilon, 1 - epsilon)

        cost = -np.mean(sample_weights * (y * np.log(h) + (1 - y) * np.log(1 - h)))
        return cost

    def _find_optimal_threshold(self, X_val, y_val):
        """Find optimal threshold using validation data"""
        y_proba = self.predict_proba(X_val)

        # Try different thresholds
        thresholds = np.linspace(0.01, 0.99, 100)
        best_f1 = 0
        best_threshold = 0.5

        for threshold in thresholds:
            y_pred = (y_proba >= threshold).astype(int)

            # Calculate F1 score
            tp = np.sum((y_pred == 1) & (y_val == 1))
            fp = np.sum((y_pred == 1) & (y_val == 0))
            fn = np.sum((y_pred == 0) & (y_val == 1))

            if tp + fp > 0 and tp + fn > 0:
                precision = tp / (tp + fp)
                recall = tp / (tp + fn)
                if precision + recall > 0:
                    f1 = 2 * precision * recall / (precision + recall)
                    if f1 > best_f1:
                        best_f1 = f1
                        best_threshold = threshold

        return best_threshold

    def fit(self, X, y, X_val=None, y_val=None):
        """
        Fit the imbalanced logistic regression model

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values (0 or 1)
        X_val : array-like, optional
            Validation data for threshold tuning
        y_val : array-like, optional
            Validation labels for threshold tuning
        """
        X = np.array(X)
        y = np.array(y)

        # Handle class imbalance
        if self.method == "smote":
            self.smote_sampler = SMOTEOversampler(
                k_neighbors=self.smote_k, random_state=42
            )
            X, y = self.smote_sampler.fit_resample(X, y)
            if self.verbose:
                print(f"SMOTE applied. New dataset shape: {X.shape}")

        elif self.method == "class_weights":
            self.class_weights = self._compute_class_weights(y)
            if self.verbose:
                print(f"Class weights: {self.class_weights}")

        # Initialize parameters
        n_features = X.shape[1]
        self.weights = np.random.normal(0, 0.01, n_features)
        self.bias = 0.0
        self.cost_history = []

        # Prepare sample weights
        if self.method == "class_weights":
            sample_weights = np.array([self.class_weights[label] for label in y])
        else:
            sample_weights = np.ones(len(y))

        if self.verbose:
            print(f"Training imbalanced logistic regression with {self.method}...")

        # Training loop
        for iteration in range(self.max_iterations):
            # Forward pass
            z = X.dot(self.weights) + self.bias
            h = self._sigmoid(z)

            # Compute cost
            if self.method == "class_weights":
                cost = self._compute_weighted_cost(h, y, sample_weights)
            else:
                epsilon = 1e-15
                h_clipped = np.clip(h, epsilon, 1 - epsilon)
                cost = -np.mean(y * np.log(h_clipped) + (1 - y) * np.log(1 - h_clipped))

            self.cost_history.append(cost)

            # Compute gradients
            if self.method == "class_weights":
                gradients_w = (1 / len(X)) * X.T.dot(sample_weights * (h - y))
                gradient_b = np.mean(sample_weights * (h - y))
            else:
                gradients_w = (1 / len(X)) * X.T.dot(h - y)
                gradient_b = np.mean(h - y)

            # Update parameters
            self.weights -= self.learning_rate * gradients_w
            self.bias -= self.learning_rate * gradient_b

            if self.verbose and (iteration + 1) % 100 == 0:
                print(f"Iteration {iteration + 1}, Cost: {cost:.6f}")

        # Threshold tuning
        if (
            self.method == "threshold_tuning"
            and X_val is not None
            and y_val is not None
        ):
            self.optimal_threshold = self._find_optimal_threshold(X_val, y_val)
            if self.verbose:
                print(f"Optimal threshold: {self.optimal_threshold:.4f}")

    def predict_proba(self, X):
        """Predict class probabilities"""
        X = np.array(X)
        z = X.dot(self.weights) + self.bias
        return self._sigmoid(z)

    def predict(self, X, threshold=None):
        """Make binary predictions"""
        if threshold is None:
            threshold = self.optimal_threshold

        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)


def demonstrate_multinomial_regression():
    """Demonstrate multinomial logistic regression"""
    print("Multinomial Logistic Regression Demonstration")
    print("=" * 50)

    # Generate multiclass dataset
    X, y = make_blobs(
        n_samples=1000, centers=4, n_features=2, random_state=42, cluster_std=1.5
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Dataset: {X_train_scaled.shape}, Classes: {np.unique(y_train)}")
    print(f"Class distribution: {dict(Counter(y_train))}")

    # Train model
    model = MultinomialLogisticRegression(
        learning_rate=0.1, max_iterations=1000, verbose=True
    )
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, (X_train_scaled, X_test_scaled, y_train, y_test)


def demonstrate_ordinal_regression():
    """Demonstrate ordinal logistic regression"""
    print("\nOrdinal Logistic Regression Demonstration")
    print("=" * 50)

    # Generate ordinal dataset (simulate ratings 1-5)
    np.random.seed(42)
    n_samples = 1000
    n_features = 3

    X = np.random.randn(n_samples, n_features)

    # Create ordinal target based on linear combination
    linear_combo = X.dot([1.5, -1.0, 0.8]) + np.random.normal(0, 0.5, n_samples)

    # Convert to ordinal scale (1-5)
    thresholds = [-2, -0.5, 0.5, 2]
    y = np.zeros(n_samples, dtype=int)
    for i, threshold in enumerate(thresholds):
        y[linear_combo > threshold] = i + 1

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Dataset: {X_train.shape}, Classes: {np.unique(y_train)}")
    print(f"Class distribution: {dict(Counter(y_train))}")

    # Train model
    model = OrdinalLogisticRegression(
        learning_rate=0.01, max_iterations=2000, verbose=True
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nTest Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model


def demonstrate_imbalanced_classification():
    """Demonstrate techniques for handling imbalanced datasets"""
    print("\nImbalanced Classification Demonstration")
    print("=" * 50)

    # Generate imbalanced dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_clusters_per_class=1,
        weights=[0.9, 0.1],
        flip_y=0.01,
        random_state=42,
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Further split train into train/val for threshold tuning
    X_train_sub, X_val, y_train_sub, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_sub_scaled = scaler.fit_transform(X_train_sub)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    print(f"Dataset: {X_train_sub_scaled.shape}")
    print(f"Original class distribution: {dict(Counter(y_train_sub))}")

    methods = ["class_weights", "smote", "threshold_tuning"]
    results = {}

    for method in methods:
        print(f"\n--- Testing {method.upper()} ---")

        model = ImbalancedLogisticRegression(
            method=method, learning_rate=0.01, max_iterations=1000, verbose=True
        )

        if method == "threshold_tuning":
            model.fit(X_train_sub_scaled, y_train_sub, X_val_scaled, y_val)
        else:
            model.fit(X_train_sub_scaled, y_train_sub)

        # Evaluate
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)

        accuracy = accuracy_score(y_test, y_pred)

        # Calculate precision, recall for minority class
        tp = np.sum((y_pred == 1) & (y_test == 1))
        fp = np.sum((y_pred == 1) & (y_test == 0))
        fn = np.sum((y_pred == 0) & (y_test == 1))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        results[method] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
        }

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")

    # Comparison
    print("\n" + "=" * 60)
    print("IMBALANCED CLASSIFICATION COMPARISON")
    print("=" * 60)
    print(f"{'Metric':<12} {'Class Weights':<15} {'SMOTE':<10} {'Threshold':<12}")
    print("-" * 60)

    for metric in ["accuracy", "precision", "recall", "f1_score"]:
        cw_val = results["class_weights"][metric]
        smote_val = results["smote"][metric]
        thresh_val = results["threshold_tuning"][metric]
        print(f"{metric:<12} {cw_val:<15.4f} {smote_val:<10.4f} {thresh_val:<12.4f}")

    return results


def main():
    """Main function to demonstrate advanced logistic regression techniques"""
    print("Advanced Logistic Regression Techniques - Demonstration")
    print("=" * 70)

    # 1. Multinomial Logistic Regression
    multinomial_model, multinomial_data = demonstrate_multinomial_regression()

    # 2. Ordinal Logistic Regression
    ordinal_model = demonstrate_ordinal_regression()

    # 3. Imbalanced Classification
    imbalanced_results = demonstrate_imbalanced_classification()

    print("\n" + "=" * 70)
    print("ADVANCED TECHNIQUES DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("Demonstrated:")
    print("1. Multinomial Logistic Regression for multiclass problems")
    print("2. Ordinal Logistic Regression for ordered categorical outcomes")
    print("3. Class imbalance handling techniques:")
    print("   - Class weighting")
    print("   - SMOTE oversampling")
    print("   - Threshold optimization")


if __name__ == "__main__":
    main()
