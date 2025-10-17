"""
Visualization Suite for Logistic Regression

This module provides comprehensive visualization tools for logistic regression models
including decision boundaries, coefficient plots, learning curves, feature importance,
residual analysis, and probability distribution visualizations.

Features:
- Decision boundary visualization (2D and 3D)
- Coefficient importance and evolution plots
- Learning curves and validation curves
- Feature effect visualizations
- Residual and diagnostic plots
- Probability distribution analysis
- Interactive plotting capabilities

Author: Peeush Agarwal
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, validation_curve, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.decomposition import PCA
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class LogisticRegressionVisualizer:
    """
    Comprehensive visualization suite for logistic regression models
    """

    def __init__(self, model, feature_names=None):
        """
        Initialize the visualizer

        Parameters:
        -----------
        model : object
            Trained logistic regression model
        feature_names : list, optional
            Names of features for labeling plots
        """
        self.model = model
        self.feature_names = feature_names
        self.is_fitted = hasattr(model, "coef_")

        if not self.is_fitted:
            raise ValueError("Model must be fitted before visualization")

    def plot_decision_boundary_2d(
        self, X, y, features=[0, 1], resolution=100, figsize=(10, 8), alpha=0.8
    ):
        """
        Plot 2D decision boundary

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target labels
        features : list, default [0, 1]
            Indices of two features to plot
        resolution : int, default 100
            Resolution of the decision boundary mesh
        figsize : tuple, default (10, 8)
            Figure size
        alpha : float, default 0.8
            Transparency of data points

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if X.shape[1] < 2:
            raise ValueError("Need at least 2 features for 2D decision boundary")

        # Extract the two features
        X_2d = X[:, features]

        # Create a temporary model for 2D data
        temp_model = LogisticRegression(random_state=42, max_iter=1000)
        temp_model.fit(X_2d, y)

        # Create mesh
        h = (X_2d[:, 0].max() - X_2d[:, 0].min()) / resolution
        xx, yy = np.meshgrid(
            np.arange(X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1, h),
            np.arange(X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1, h),
        )

        # Predict on mesh
        mesh_points = np.c_[xx.ravel(), yy.ravel()]
        Z = temp_model.predict_proba(mesh_points)[:, 1]
        Z = Z.reshape(xx.shape)

        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Plot 1: Decision boundary with probability contours
        contour = ax1.contourf(xx, yy, Z, levels=50, alpha=0.6, cmap="RdYlBu")
        ax1.contour(
            xx, yy, Z, levels=[0.5], colors="black", linestyles="--", linewidths=2
        )

        # Plot data points
        scatter = ax1.scatter(
            X_2d[:, 0],
            X_2d[:, 1],
            c=y,
            cmap="RdYlBu",
            alpha=alpha,
            edgecolors="black",
            linewidth=0.5,
        )

        # Labels and title
        feat1_name = (
            f"Feature {features[0]}"
            if self.feature_names is None
            else self.feature_names[features[0]]
        )
        feat2_name = (
            f"Feature {features[1]}"
            if self.feature_names is None
            else self.feature_names[features[1]]
        )

        ax1.set_xlabel(feat1_name)
        ax1.set_ylabel(feat2_name)
        ax1.set_title("Decision Boundary with Probability Contours")

        # Add colorbar
        cbar = plt.colorbar(contour, ax=ax1)
        cbar.set_label("Predicted Probability (Class 1)")

        # Plot 2: Decision regions
        ax2.contourf(xx, yy, Z > 0.5, levels=1, alpha=0.3, colors=["blue", "red"])
        ax2.contour(
            xx, yy, Z, levels=[0.5], colors="black", linestyles="--", linewidths=2
        )

        # Plot data points
        ax2.scatter(
            X_2d[:, 0],
            X_2d[:, 1],
            c=y,
            cmap="RdYlBu",
            alpha=alpha,
            edgecolors="black",
            linewidth=0.5,
        )

        ax2.set_xlabel(feat1_name)
        ax2.set_ylabel(feat2_name)
        ax2.set_title("Decision Regions")

        plt.tight_layout()
        return fig

    def plot_coefficient_importance(self, figsize=(12, 8), top_k=None):
        """
        Plot coefficient importance and statistics

        Parameters:
        -----------
        figsize : tuple, default (12, 8)
            Figure size
        top_k : int, optional
            Show only top k most important features

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        # Get coefficients
        if hasattr(self.model, "coef_"):
            coef = (
                self.model.coef_[0] if self.model.coef_.ndim > 1 else self.model.coef_
            )
        else:
            raise ValueError("Model does not have coefficients")

        # Feature names
        if self.feature_names is not None:
            feature_names = self.feature_names
        else:
            feature_names = [f"Feature_{i}" for i in range(len(coef))]

        # Sort by absolute coefficient value
        abs_coef = np.abs(coef)
        sorted_idx = np.argsort(abs_coef)[::-1]

        if top_k is not None:
            sorted_idx = sorted_idx[:top_k]

        sorted_coef = coef[sorted_idx]
        sorted_names = [feature_names[i] for i in sorted_idx]
        sorted_abs_coef = abs_coef[sorted_idx]

        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle("Coefficient Analysis", fontsize=16, fontweight="bold")

        # 1. Coefficient values (horizontal bar plot)
        ax = axes[0, 0]
        colors = ["red" if c < 0 else "blue" for c in sorted_coef]
        bars = ax.barh(range(len(sorted_coef)), sorted_coef, color=colors, alpha=0.7)
        ax.set_yticks(range(len(sorted_coef)))
        ax.set_yticklabels(sorted_names)
        ax.set_xlabel("Coefficient Value")
        ax.set_title("Feature Coefficients")
        ax.axvline(x=0, color="black", linestyle="-", alpha=0.3)
        ax.grid(True, alpha=0.3)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, sorted_coef)):
            width = bar.get_width()
            ax.text(
                width + 0.01 if width >= 0 else width - 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="left" if width >= 0 else "right",
                va="center",
            )

        # 2. Absolute coefficient importance
        ax = axes[0, 1]
        bars = ax.bar(
            range(len(sorted_abs_coef)), sorted_abs_coef, color="skyblue", alpha=0.7
        )
        ax.set_xticks(range(len(sorted_abs_coef)))
        ax.set_xticklabels(sorted_names, rotation=45, ha="right")
        ax.set_ylabel("Absolute Coefficient Value")
        ax.set_title("Feature Importance (|Coefficient|)")
        ax.grid(True, alpha=0.3)

        # Add value labels
        for bar, value in zip(bars, sorted_abs_coef):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.01,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )

        # 3. Coefficient distribution
        ax = axes[1, 0]
        ax.hist(coef, bins=20, alpha=0.7, color="lightgreen", edgecolor="black")
        ax.axvline(x=0, color="red", linestyle="--", alpha=0.7, label="Zero")
        ax.axvline(
            x=np.mean(coef), color="blue", linestyle="-", alpha=0.7, label="Mean"
        )
        ax.set_xlabel("Coefficient Value")
        ax.set_ylabel("Frequency")
        ax.set_title("Coefficient Distribution")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 4. Odds ratio (exp(coefficient))
        ax = axes[1, 1]
        odds_ratios = np.exp(sorted_coef)
        colors = ["red" if or_val < 1 else "blue" for or_val in odds_ratios]
        bars = ax.barh(range(len(odds_ratios)), odds_ratios, color=colors, alpha=0.7)
        ax.set_yticks(range(len(odds_ratios)))
        ax.set_yticklabels(sorted_names)
        ax.set_xlabel("Odds Ratio (exp(coefficient))")
        ax.set_title("Odds Ratios")
        ax.axvline(x=1, color="black", linestyle="-", alpha=0.3, label="No Effect")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, odds_ratios)):
            width = bar.get_width()
            ax.text(
                width + 0.01 if width >= 1 else width - 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="left" if width >= 1 else "right",
                va="center",
            )

        plt.tight_layout()
        return fig

    def plot_learning_curves(
        self, X, y, cv=5, train_sizes=None, scoring="roc_auc", figsize=(12, 8)
    ):
        """
        Plot learning curves to diagnose bias/variance

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        cv : int, default 5
            Number of cross-validation folds
        train_sizes : array-like, optional
            Training set sizes to use
        scoring : str, default 'roc_auc'
            Scoring metric
        figsize : tuple, default (12, 8)
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if train_sizes is None:
            train_sizes = np.linspace(0.1, 1.0, 10)

        # Compute learning curves
        train_sizes_abs, train_scores, val_scores = learning_curve(
            self.model,
            X,
            y,
            cv=cv,
            n_jobs=-1,
            train_sizes=train_sizes,
            scoring=scoring,
            random_state=42,
        )

        # Calculate means and standard deviations
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)

        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle("Learning Curve Analysis", fontsize=16, fontweight="bold")

        # 1. Learning curves
        ax = axes[0, 0]
        ax.plot(train_sizes_abs, train_mean, "o-", color="blue", label="Training Score")
        ax.fill_between(
            train_sizes_abs,
            train_mean - train_std,
            train_mean + train_std,
            alpha=0.1,
            color="blue",
        )

        ax.plot(train_sizes_abs, val_mean, "o-", color="red", label="Validation Score")
        ax.fill_between(
            train_sizes_abs,
            val_mean - val_std,
            val_mean + val_std,
            alpha=0.1,
            color="red",
        )

        ax.set_xlabel("Training Set Size")
        ax.set_ylabel(f"{scoring.upper()} Score")
        ax.set_title("Learning Curves")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Gap analysis
        ax = axes[0, 1]
        gap = train_mean - val_mean
        ax.plot(train_sizes_abs, gap, "o-", color="green", linewidth=2)
        ax.fill_between(
            train_sizes_abs,
            gap - (train_std + val_std),
            gap + (train_std + val_std),
            alpha=0.2,
            color="green",
        )
        ax.set_xlabel("Training Set Size")
        ax.set_ylabel(f"Training - Validation {scoring.upper()}")
        ax.set_title("Bias-Variance Gap")
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color="black", linestyle="--", alpha=0.5)

        # 3. Convergence analysis
        ax = axes[1, 0]
        # Calculate convergence (change in validation score)
        val_changes = np.abs(np.diff(val_mean))
        ax.plot(train_sizes_abs[1:], val_changes, "o-", color="purple", linewidth=2)
        ax.set_xlabel("Training Set Size")
        ax.set_ylabel(f"|Δ Validation {scoring.upper()}|")
        ax.set_title("Validation Score Convergence")
        ax.grid(True, alpha=0.3)

        # 4. Score statistics
        ax = axes[1, 1]
        x_pos = [1, 2]
        final_train_scores = train_scores[-1]
        final_val_scores = val_scores[-1]

        bp = ax.boxplot(
            [final_train_scores, final_val_scores],
            labels=["Training", "Validation"],
            patch_artist=True,
        )
        bp["boxes"][0].set_facecolor("lightblue")
        bp["boxes"][1].set_facecolor("lightcoral")

        ax.set_ylabel(f"{scoring.upper()} Score")
        ax.set_title("Final Score Distribution")
        ax.grid(True, alpha=0.3)

        # Add mean values as text
        ax.text(
            1,
            np.mean(final_train_scores),
            f"μ={np.mean(final_train_scores):.3f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
        ax.text(
            2,
            np.mean(final_val_scores),
            f"μ={np.mean(final_val_scores):.3f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

        plt.tight_layout()
        return fig

    def plot_validation_curves(
        self, X, y, param_name, param_range, cv=5, scoring="roc_auc", figsize=(10, 6)
    ):
        """
        Plot validation curves for hyperparameter tuning

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        param_name : str
            Name of parameter to vary
        param_range : array-like
            Range of parameter values
        cv : int, default 5
            Number of cross-validation folds
        scoring : str, default 'roc_auc'
            Scoring metric
        figsize : tuple, default (10, 6)
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        # Compute validation curves
        train_scores, val_scores = validation_curve(
            self.model,
            X,
            y,
            param_name=param_name,
            param_range=param_range,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )

        # Calculate means and standard deviations
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)

        # Create plot
        fig, ax = plt.subplots(figsize=figsize)

        # Plot curves
        ax.plot(param_range, train_mean, "o-", color="blue", label="Training Score")
        ax.fill_between(
            param_range,
            train_mean - train_std,
            train_mean + train_std,
            alpha=0.1,
            color="blue",
        )

        ax.plot(param_range, val_mean, "o-", color="red", label="Validation Score")
        ax.fill_between(
            param_range, val_mean - val_std, val_mean + val_std, alpha=0.1, color="red"
        )

        # Find best parameter
        best_idx = np.argmax(val_mean)
        best_param = param_range[best_idx]
        best_score = val_mean[best_idx]

        ax.axvline(
            x=best_param,
            color="green",
            linestyle="--",
            alpha=0.7,
            label=f"Best {param_name}={best_param:.3f}",
        )
        ax.scatter([best_param], [best_score], color="green", s=100, zorder=5)

        ax.set_xlabel(param_name)
        ax.set_ylabel(f"{scoring.upper()} Score")
        ax.set_title(f"Validation Curve: {param_name}")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Log scale for C parameter
        if param_name.lower() == "c":
            ax.set_xscale("log")

        return fig

    def plot_feature_effects(
        self, X, y, feature_idx=None, n_points=100, figsize=(12, 8)
    ):
        """
        Plot individual feature effects on predictions

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        feature_idx : int or list, optional
            Feature indices to plot (plots all if None)
        n_points : int, default 100
            Number of points for effect curves
        figsize : tuple, default (12, 8)
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        n_features = X.shape[1]

        if feature_idx is None:
            feature_idx = list(range(min(n_features, 9)))  # Limit to 9 features max
        elif isinstance(feature_idx, int):
            feature_idx = [feature_idx]

        # Calculate grid size
        n_plots = len(feature_idx)
        n_cols = min(3, n_plots)
        n_rows = (n_plots + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_plots == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes.reshape(1, -1)

        fig.suptitle("Individual Feature Effects", fontsize=16, fontweight="bold")

        for i, feat_idx in enumerate(feature_idx):
            row = i // n_cols
            col = i % n_cols
            ax = axes[row, col] if n_rows > 1 else axes[col]

            # Create feature range
            feat_min, feat_max = X[:, feat_idx].min(), X[:, feat_idx].max()
            feat_range = np.linspace(feat_min, feat_max, n_points)

            # Create baseline sample (median values for other features)
            baseline = np.median(X, axis=0)

            # Calculate predictions for different values of this feature
            predictions = []
            for feat_val in feat_range:
                sample = baseline.copy()
                sample[feat_idx] = feat_val
                pred_proba = self.model.predict_proba(sample.reshape(1, -1))[0, 1]
                predictions.append(pred_proba)

            # Plot feature effect
            ax.plot(feat_range, predictions, linewidth=2, color="blue")

            # Plot data distribution
            ax2 = ax.twinx()
            ax2.hist(
                X[y == 0, feat_idx],
                bins=20,
                alpha=0.3,
                color="red",
                density=True,
                label="Class 0",
            )
            ax2.hist(
                X[y == 1, feat_idx],
                bins=20,
                alpha=0.3,
                color="blue",
                density=True,
                label="Class 1",
            )
            ax2.set_ylabel("Density", alpha=0.7)
            ax2.tick_params(axis="y", alpha=0.7)

            # Labels
            feat_name = (
                f"Feature {feat_idx}"
                if self.feature_names is None
                else self.feature_names[feat_idx]
            )
            ax.set_xlabel(feat_name)
            ax.set_ylabel("Predicted Probability (Class 1)")
            ax.set_title(f"Effect of {feat_name}")
            ax.grid(True, alpha=0.3)

            # Add coefficient value as text
            if hasattr(self.model, "coef_"):
                coef_val = (
                    self.model.coef_[0, feat_idx]
                    if self.model.coef_.ndim > 1
                    else self.model.coef_[feat_idx]
                )
                ax.text(
                    0.05,
                    0.95,
                    f"Coef: {coef_val:.3f}",
                    transform=ax.transAxes,
                    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
                    verticalalignment="top",
                )

        # Hide empty subplots
        for i in range(n_plots, n_rows * n_cols):
            row = i // n_cols
            col = i % n_cols
            if n_rows > 1:
                axes[row, col].set_visible(False)
            else:
                axes[col].set_visible(False)

        plt.tight_layout()
        return fig

    def plot_residual_analysis(self, X, y, figsize=(12, 8)):
        """
        Plot residual analysis for logistic regression

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        figsize : tuple, default (12, 8)
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        # Get predictions and probabilities
        y_pred = self.model.predict(X)
        y_proba = self.model.predict_proba(X)[:, 1]

        # Calculate residuals (different types for logistic regression)
        # Pearson residuals
        pearson_residuals = (y - y_proba) / np.sqrt(y_proba * (1 - y_proba))

        # Deviance residuals
        deviance_residuals = np.sign(y - y_proba) * np.sqrt(
            -2 * (y * np.log(y_proba + 1e-15) + (1 - y) * np.log(1 - y_proba + 1e-15))
        )

        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle("Residual Analysis", fontsize=16, fontweight="bold")

        # 1. Pearson residuals vs fitted values
        ax = axes[0, 0]
        ax.scatter(y_proba, pearson_residuals, alpha=0.6, color="blue")
        ax.axhline(y=0, color="red", linestyle="--", alpha=0.7)
        ax.set_xlabel("Fitted Values (Predicted Probability)")
        ax.set_ylabel("Pearson Residuals")
        ax.set_title("Pearson Residuals vs Fitted Values")
        ax.grid(True, alpha=0.3)

        # Add LOWESS smooth line
        try:
            from scipy import signal

            # Simple moving average as approximation to LOWESS
            sorted_idx = np.argsort(y_proba)
            window_size = max(10, len(y_proba) // 20)
            smoothed = signal.savgol_filter(
                pearson_residuals[sorted_idx],
                window_size if window_size % 2 == 1 else window_size + 1,
                3,
            )
            ax.plot(y_proba[sorted_idx], smoothed, color="red", linewidth=2, alpha=0.8)
        except Exception:
            pass

        # 2. Q-Q plot of Pearson residuals
        ax = axes[0, 1]
        from scipy import stats

        stats.probplot(pearson_residuals, dist="norm", plot=ax)
        ax.set_title("Q-Q Plot: Pearson Residuals")
        ax.grid(True, alpha=0.3)

        # 3. Deviance residuals vs fitted values
        ax = axes[1, 0]
        ax.scatter(y_proba, deviance_residuals, alpha=0.6, color="green")
        ax.axhline(y=0, color="red", linestyle="--", alpha=0.7)
        ax.set_xlabel("Fitted Values (Predicted Probability)")
        ax.set_ylabel("Deviance Residuals")
        ax.set_title("Deviance Residuals vs Fitted Values")
        ax.grid(True, alpha=0.3)

        # 4. Residuals vs leverage (Cook's distance approximation)
        ax = axes[1, 1]

        # Calculate leverage (hat values) approximation
        # For logistic regression: h_i ≈ p_i(1-p_i) * x_i^T * (X^T * W * X)^(-1) * x_i
        # Simplified version: use predicted probabilities as leverage proxy
        leverage = y_proba * (1 - y_proba)

        # Plot residuals vs leverage
        colors = ["red" if abs(res) > 2 else "blue" for res in pearson_residuals]
        ax.scatter(leverage, pearson_residuals, alpha=0.6, c=colors)
        ax.axhline(y=0, color="red", linestyle="--", alpha=0.7)
        ax.axhline(
            y=2, color="orange", linestyle=":", alpha=0.7, label="|residual| = 2"
        )
        ax.axhline(y=-2, color="orange", linestyle=":", alpha=0.7)
        ax.set_xlabel("Leverage (approximation)")
        ax.set_ylabel("Pearson Residuals")
        ax.set_title("Residuals vs Leverage")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_probability_distributions(self, X, y, bins=30, figsize=(12, 8)):
        """
        Plot probability distribution analysis

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        bins : int, default 30
            Number of histogram bins
        figsize : tuple, default (12, 8)
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        y_proba = self.model.predict_proba(X)[:, 1]

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(
            "Probability Distribution Analysis", fontsize=16, fontweight="bold"
        )

        # 1. Probability distribution by class
        ax = axes[0, 0]
        ax.hist(
            y_proba[y == 0],
            bins=bins,
            alpha=0.7,
            label="Class 0 (Actual)",
            color="red",
            density=True,
        )
        ax.hist(
            y_proba[y == 1],
            bins=bins,
            alpha=0.7,
            label="Class 1 (Actual)",
            color="blue",
            density=True,
        )
        ax.axvline(
            x=0.5, color="black", linestyle="--", alpha=0.7, label="Decision Threshold"
        )
        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("Density")
        ax.set_title("Probability Distribution by True Class")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Calibration curve
        ax = axes[0, 1]
        from sklearn.calibration import calibration_curve

        fraction_of_positives, mean_predicted_value = calibration_curve(
            y, y_proba, n_bins=10, strategy="uniform"
        )

        ax.plot(
            mean_predicted_value,
            fraction_of_positives,
            marker="o",
            linewidth=2,
            label="Model",
            color="blue",
        )
        ax.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            color="gray",
            label="Perfectly Calibrated",
            alpha=0.7,
        )
        ax.set_xlabel("Mean Predicted Probability")
        ax.set_ylabel("Fraction of Positives")
        ax.set_title("Calibration Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 3. Confidence intervals
        ax = axes[1, 0]

        # Calculate confidence for each prediction
        confidence = np.maximum(y_proba, 1 - y_proba)

        # Bin by confidence levels
        conf_bins = np.linspace(0.5, 1.0, 6)
        accuracies = []
        bin_centers = []

        for i in range(len(conf_bins) - 1):
            mask = (confidence >= conf_bins[i]) & (confidence < conf_bins[i + 1])
            if np.sum(mask) > 0:
                y_pred_bin = (y_proba[mask] >= 0.5).astype(int)
                accuracy = np.mean(y_pred_bin == y[mask])
                accuracies.append(accuracy)
                bin_centers.append((conf_bins[i] + conf_bins[i + 1]) / 2)

        ax.bar(bin_centers, accuracies, width=0.08, alpha=0.7, color="skyblue")
        ax.set_xlabel("Confidence Level")
        ax.set_ylabel("Accuracy")
        ax.set_title("Accuracy vs Confidence")
        ax.grid(True, alpha=0.3)

        # Add value labels
        for x, y_val in zip(bin_centers, accuracies):
            ax.text(x, y_val + 0.01, f"{y_val:.3f}", ha="center", va="bottom")

        # 4. Prediction certainty analysis
        ax = axes[1, 1]

        # Categorize predictions
        very_certain = confidence > 0.9
        certain = (confidence > 0.7) & (confidence <= 0.9)
        uncertain = confidence <= 0.7

        categories = ["Uncertain\n(≤0.7)", "Certain\n(0.7-0.9)", "Very Certain\n(>0.9)"]
        counts = [np.sum(uncertain), np.sum(certain), np.sum(very_certain)]
        colors = ["red", "orange", "green"]

        bars = ax.bar(categories, counts, color=colors, alpha=0.7)
        ax.set_ylabel("Number of Predictions")
        ax.set_title("Distribution of Prediction Confidence")
        ax.grid(True, alpha=0.3)

        # Add percentage labels
        total = len(y_proba)
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            percentage = (count / total) * 100
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.01,
                f"{count}\n({percentage:.1f}%)",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        return fig


def create_comprehensive_visualization_dashboard(
    model, X_train, y_train, X_test, y_test, feature_names=None, figsize=(20, 24)
):
    """
    Create a comprehensive visualization dashboard

    Parameters:
    -----------
    model : object
        Trained logistic regression model
    X_train : array-like
        Training features
    y_train : array-like
        Training labels
    X_test : array-like
        Test features
    y_test : array-like
        Test labels
    feature_names : list, optional
        Feature names
    figsize : tuple, default (20, 24)
        Figure size

    Returns:
    --------
    dict
        Dictionary containing all generated figures
    """
    visualizer = LogisticRegressionVisualizer(model, feature_names)

    figures = {}

    print("Creating comprehensive visualization dashboard...")

    # 1. Decision boundary (if 2D or can be reduced to 2D)
    if X_test.shape[1] >= 2:
        print("- Decision boundary plot")
        try:
            figures["decision_boundary"] = visualizer.plot_decision_boundary_2d(
                X_test, y_test
            )
        except Exception as e:
            print(f"  Could not create decision boundary plot: {e}")

    # 2. Coefficient importance
    print("- Coefficient analysis")
    figures["coefficients"] = visualizer.plot_coefficient_importance()

    # 3. Learning curves
    print("- Learning curves")
    figures["learning_curves"] = visualizer.plot_learning_curves(X_train, y_train)

    # 4. Feature effects
    print("- Feature effects")
    figures["feature_effects"] = visualizer.plot_feature_effects(X_test, y_test)

    # 5. Residual analysis
    print("- Residual analysis")
    figures["residuals"] = visualizer.plot_residual_analysis(X_test, y_test)

    # 6. Probability distributions
    print("- Probability distributions")
    figures["probabilities"] = visualizer.plot_probability_distributions(X_test, y_test)

    # 7. Validation curves (for C parameter)
    print("- Validation curves")
    try:
        C_range = np.logspace(-4, 4, 9)
        figures["validation_curves"] = visualizer.plot_validation_curves(
            X_train, y_train, "C", C_range
        )
    except Exception as e:
        print(f"  Could not create validation curves: {e}")

    return figures


def save_all_figures(
    figures, output_dir="outputs/ml-algos/02_logistic_regression/", dpi=300
):
    """
    Save all figures to files

    Parameters:
    -----------
    figures : dict
        Dictionary of figure names and figure objects
    output_dir : str
        Output directory
    dpi : int
        Resolution for saved figures
    """
    import os

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    for name, fig in figures.items():
        if fig is not None:
            filename = f"{name}_visualization.png"
            filepath = os.path.join(output_dir, filename)
            fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
            print(f"Saved: {filepath}")


def main():
    """
    Main function to demonstrate the visualization suite
    """
    print("Logistic Regression Visualization Suite - Demonstration")
    print("=" * 60)

    # Generate synthetic dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=6,
        n_informative=4,
        n_redundant=1,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=1.5,
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Feature names
    feature_names = [f"Feature_{i + 1}" for i in range(X.shape[1])]

    print(f"Dataset: {X_train_scaled.shape}")
    print(f"Features: {feature_names}")

    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Evaluate model
    train_acc = accuracy_score(y_train, model.predict(X_train_scaled))
    test_acc = accuracy_score(y_test, model.predict(X_test_scaled))
    test_auc = roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:, 1])

    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test AUC: {test_auc:.4f}")

    # Create comprehensive dashboard
    figures = create_comprehensive_visualization_dashboard(
        model, X_train_scaled, y_train, X_test_scaled, y_test, feature_names
    )

    # Save all figures
    save_all_figures(figures)

    print(f"\n{'=' * 60}")
    print("VISUALIZATION SUITE DEMONSTRATION COMPLETE")
    print("=" * 60)
    print(f"Generated {len(figures)} visualization plots")
    print(
        "Check the outputs/ml-algos/02_logistic_regression/ directory for saved plots"
    )


if __name__ == "__main__":
    main()
