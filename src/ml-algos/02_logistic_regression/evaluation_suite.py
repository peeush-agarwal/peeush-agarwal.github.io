"""
Comprehensive Evaluation Suite for Logistic Regression

This module provides a complete evaluation framework for logistic regression models
including ROC curves, Precision-Recall curves, calibration plots, cross-validation,
statistical significance testing, and confidence intervals.

Features:
- ROC and Precision-Recall curve analysis
- Calibration plots and reliability diagrams
- Bootstrap confidence intervals
- Cross-validation with multiple metrics
- Statistical significance testing
- Model comparison frameworks
- Learning curves for diagnosis

Author: Peeush Agarwal
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, KFold, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc,
    precision_recall_curve,
    brier_score_loss,
    log_loss,
    confusion_matrix,
    classification_report,
)
from sklearn.calibration import calibration_curve
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class LogisticRegressionEvaluator:
    """
    Comprehensive evaluation suite for logistic regression models
    """

    def __init__(self, model, model_name="Logistic Regression"):
        """
        Initialize the evaluator

        Parameters:
        -----------
        model : object
            Trained logistic regression model with predict and predict_proba methods
        model_name : str
            Name of the model for display purposes
        """
        self.model = model
        self.model_name = model_name
        self.evaluation_results = {}

    def evaluate_model(self, X_test, y_test, X_train=None, y_train=None):
        """
        Comprehensive model evaluation

        Parameters:
        -----------
        X_test : array-like, shape (n_samples, n_features)
            Test features
        y_test : array-like, shape (n_samples,)
            Test labels
        X_train : array-like, optional
            Training features for learning curves
        y_train : array-like, optional
            Training labels for learning curves

        Returns:
        --------
        dict
            Comprehensive evaluation results
        """
        # Predictions
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)

        # Handle sklearn format (n_samples, 2) vs our format (n_samples,)
        if len(y_proba.shape) > 1 and y_proba.shape[1] > 1:
            y_proba = y_proba[:, 1]

        # Basic metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        # Probabilistic metrics
        try:
            logloss = log_loss(y_test, y_proba)
        except Exception:
            logloss = np.nan

        try:
            brier_score = brier_score_loss(y_test, y_proba)
        except Exception:
            brier_score = np.nan

        # ROC metrics
        fpr, tpr, roc_thresholds = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)

        # Precision-Recall metrics
        precision_curve, recall_curve, pr_thresholds = precision_recall_curve(
            y_test, y_proba
        )
        pr_auc = auc(recall_curve, precision_curve)

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        # Calibration
        fraction_of_positives, mean_predicted_value = calibration_curve(
            y_test, y_proba, n_bins=10, strategy="uniform"
        )

        # Store results
        self.evaluation_results = {
            "predictions": {"y_pred": y_pred, "y_proba": y_proba, "y_test": y_test},
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "log_loss": logloss,
                "brier_score": brier_score,
                "roc_auc": roc_auc,
                "pr_auc": pr_auc,
            },
            "curves": {
                "roc": {"fpr": fpr, "tpr": tpr, "thresholds": roc_thresholds},
                "pr": {
                    "precision": precision_curve,
                    "recall": recall_curve,
                    "thresholds": pr_thresholds,
                },
            },
            "confusion_matrix": cm,
            "calibration": {
                "fraction_of_positives": fraction_of_positives,
                "mean_predicted_value": mean_predicted_value,
            },
        }

        # Learning curves if training data provided
        if X_train is not None and y_train is not None:
            self._compute_learning_curves(X_train, y_train)

        return self.evaluation_results

    def _compute_learning_curves(self, X_train, y_train):
        """Compute learning curves"""
        try:
            train_sizes, train_scores, val_scores = learning_curve(
                self.model,
                X_train,
                y_train,
                cv=5,
                n_jobs=-1,
                train_sizes=np.linspace(0.1, 1.0, 10),
                scoring="roc_auc",
                random_state=42,
            )

            self.evaluation_results["learning_curves"] = {
                "train_sizes": train_sizes,
                "train_scores": train_scores,
                "val_scores": val_scores,
            }
        except Exception as e:
            print(f"Could not compute learning curves: {e}")

    def print_evaluation_report(self):
        """Print comprehensive evaluation report"""
        if not self.evaluation_results:
            print("No evaluation results available. Run evaluate_model first.")
            return

        metrics = self.evaluation_results["metrics"]
        cm = self.evaluation_results["confusion_matrix"]

        print(f"\n{'=' * 60}")
        print(f"EVALUATION REPORT: {self.model_name}")
        print(f"{'=' * 60}")

        print("\nCLASSIFICATION METRICS:")
        print("-" * 30)
        print(f"Accuracy:      {metrics['accuracy']:.4f}")
        print(f"Precision:     {metrics['precision']:.4f}")
        print(f"Recall:        {metrics['recall']:.4f}")
        print(f"F1-Score:      {metrics['f1_score']:.4f}")

        print("\nPROBABILISTIC METRICS:")
        print("-" * 30)
        print(f"ROC AUC:       {metrics['roc_auc']:.4f}")
        print(f"PR AUC:        {metrics['pr_auc']:.4f}")
        print(f"Log Loss:      {metrics['log_loss']:.4f}")
        print(f"Brier Score:   {metrics['brier_score']:.4f}")

        print("\nCONFUSION MATRIX:")
        print("-" * 30)
        print(f"True Neg:  {cm[0, 0]:<8} False Pos: {cm[0, 1]}")
        print(f"False Neg: {cm[1, 0]:<8} True Pos:  {cm[1, 1]}")

        # Classification report
        y_test = self.evaluation_results["predictions"]["y_test"]
        y_pred = self.evaluation_results["predictions"]["y_pred"]
        print("\nDETAILED CLASSIFICATION REPORT:")
        print("-" * 30)
        print(classification_report(y_test, y_pred))

    def plot_evaluation_dashboard(self, figsize=(16, 12)):
        """
        Create comprehensive evaluation dashboard

        Parameters:
        -----------
        figsize : tuple
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if not self.evaluation_results:
            print("No evaluation results available. Run evaluate_model first.")
            return None

        fig, axes = plt.subplots(3, 3, figsize=figsize)
        fig.suptitle(
            f"Evaluation Dashboard: {self.model_name}", fontsize=16, fontweight="bold"
        )

        # 1. ROC Curve
        ax = axes[0, 0]
        roc_data = self.evaluation_results["curves"]["roc"]
        ax.plot(
            roc_data["fpr"],
            roc_data["tpr"],
            linewidth=2,
            label=f"ROC (AUC = {self.evaluation_results['metrics']['roc_auc']:.3f})",
        )
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Precision-Recall Curve
        ax = axes[0, 1]
        pr_data = self.evaluation_results["curves"]["pr"]
        ax.plot(
            pr_data["recall"],
            pr_data["precision"],
            linewidth=2,
            label=f"PR (AUC = {self.evaluation_results['metrics']['pr_auc']:.3f})",
        )
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 3. Calibration Plot
        ax = axes[0, 2]
        cal_data = self.evaluation_results["calibration"]
        ax.plot(
            cal_data["mean_predicted_value"],
            cal_data["fraction_of_positives"],
            marker="o",
            linewidth=2,
            label="Model",
        )
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfectly Calibrated")
        ax.set_xlabel("Mean Predicted Probability")
        ax.set_ylabel("Fraction of Positives")
        ax.set_title("Calibration Plot")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 4. Confusion Matrix Heatmap
        ax = axes[1, 0]
        cm = self.evaluation_results["confusion_matrix"]
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax,
            xticklabels=["Negative", "Positive"],
            yticklabels=["Negative", "Positive"],
        )
        ax.set_title("Confusion Matrix")
        ax.set_ylabel("True Label")
        ax.set_xlabel("Predicted Label")

        # 5. Metrics Bar Plot
        ax = axes[1, 1]
        metrics = self.evaluation_results["metrics"]
        metric_names = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC AUC"]
        metric_values = [
            metrics["accuracy"],
            metrics["precision"],
            metrics["recall"],
            metrics["f1_score"],
            metrics["roc_auc"],
        ]

        bars = ax.bar(metric_names, metric_values, alpha=0.7, color="skyblue")
        ax.set_ylabel("Score")
        ax.set_title("Performance Metrics")
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)

        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.01,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        # 6. Threshold Analysis
        ax = axes[1, 2]
        thresholds = roc_data["thresholds"]

        # Calculate metrics for different thresholds
        threshold_metrics = self._calculate_threshold_metrics(thresholds)

        ax.plot(
            thresholds, threshold_metrics["precision"], label="Precision", linewidth=2
        )
        ax.plot(thresholds, threshold_metrics["recall"], label="Recall", linewidth=2)
        ax.plot(thresholds, threshold_metrics["f1"], label="F1-Score", linewidth=2)
        ax.axvline(x=0.5, color="red", linestyle="--", alpha=0.7, label="Default (0.5)")

        ax.set_xlabel("Threshold")
        ax.set_ylabel("Score")
        ax.set_title("Threshold Analysis")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 7. Probability Distribution
        ax = axes[2, 0]
        y_test = self.evaluation_results["predictions"]["y_test"]
        y_proba = self.evaluation_results["predictions"]["y_proba"]

        ax.hist(
            y_proba[y_test == 0],
            bins=30,
            alpha=0.7,
            label="Class 0",
            color="skyblue",
            density=True,
        )
        ax.hist(
            y_proba[y_test == 1],
            bins=30,
            alpha=0.7,
            label="Class 1",
            color="lightcoral",
            density=True,
        )
        ax.axvline(x=0.5, color="red", linestyle="--", alpha=0.7, label="Threshold")
        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("Density")
        ax.set_title("Probability Distribution by Class")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 8. Learning Curves (if available)
        ax = axes[2, 1]
        if "learning_curves" in self.evaluation_results:
            lc_data = self.evaluation_results["learning_curves"]
            train_sizes = lc_data["train_sizes"]
            train_scores_mean = np.mean(lc_data["train_scores"], axis=1)
            train_scores_std = np.std(lc_data["train_scores"], axis=1)
            val_scores_mean = np.mean(lc_data["val_scores"], axis=1)
            val_scores_std = np.std(lc_data["val_scores"], axis=1)

            ax.plot(
                train_sizes,
                train_scores_mean,
                "o-",
                label="Training Score",
                linewidth=2,
            )
            ax.fill_between(
                train_sizes,
                train_scores_mean - train_scores_std,
                train_scores_mean + train_scores_std,
                alpha=0.1,
            )

            ax.plot(
                train_sizes,
                val_scores_mean,
                "o-",
                label="Validation Score",
                linewidth=2,
            )
            ax.fill_between(
                train_sizes,
                val_scores_mean - val_scores_std,
                val_scores_mean + val_scores_std,
                alpha=0.1,
            )

            ax.set_xlabel("Training Set Size")
            ax.set_ylabel("ROC AUC Score")
            ax.set_title("Learning Curves")
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            ax.text(
                0.5,
                0.5,
                "Learning Curves\nNot Available\n(Training data required)",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=12,
            )
            ax.set_title("Learning Curves")

        # 9. Error Analysis
        ax = axes[2, 2]

        # Calculate prediction errors by probability ranges
        prob_ranges = [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]
        error_rates = []
        range_labels = []

        for i, (low, high) in enumerate(prob_ranges):
            mask = (y_proba >= low) & (y_proba < high)
            if i == len(prob_ranges) - 1:  # Last range includes upper bound
                mask = (y_proba >= low) & (y_proba <= high)

            if np.sum(mask) > 0:
                predictions_in_range = (y_proba[mask] >= 0.5).astype(int)
                true_labels_in_range = y_test[mask]
                error_rate = np.mean(predictions_in_range != true_labels_in_range)
                error_rates.append(error_rate)
                range_labels.append(f"{low:.1f}-{high:.1f}")
            else:
                error_rates.append(0)
                range_labels.append(f"{low:.1f}-{high:.1f}")

        bars = ax.bar(range_labels, error_rates, alpha=0.7, color="lightcoral")
        ax.set_xlabel("Predicted Probability Range")
        ax.set_ylabel("Error Rate")
        ax.set_title("Error Analysis by Probability Range")
        ax.grid(True, alpha=0.3)

        # Add value labels on bars
        for bar, value in zip(bars, error_rates):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.01,
                f"{value:.3f}",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        return fig

    def _calculate_threshold_metrics(self, thresholds):
        """Calculate precision, recall, F1 for different thresholds"""
        y_test = self.evaluation_results["predictions"]["y_test"]
        y_proba = self.evaluation_results["predictions"]["y_proba"]

        precisions = []
        recalls = []
        f1_scores = []

        for threshold in thresholds:
            y_pred_thresh = (y_proba >= threshold).astype(int)

            precision = precision_score(y_test, y_pred_thresh, zero_division=0)
            recall = recall_score(y_test, y_pred_thresh, zero_division=0)

            if precision + recall > 0:
                f1 = 2 * precision * recall / (precision + recall)
            else:
                f1 = 0

            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1)

        return {
            "precision": np.array(precisions),
            "recall": np.array(recalls),
            "f1": np.array(f1_scores),
        }


class CrossValidationEvaluator:
    """
    Cross-validation evaluation with multiple metrics and statistical testing
    """

    def __init__(self, model_class, cv_folds=5, random_state=42):
        """
        Initialize cross-validation evaluator

        Parameters:
        -----------
        model_class : class
            Model class to evaluate
        cv_folds : int
            Number of cross-validation folds
        random_state : int
            Random seed for reproducibility
        """
        self.model_class = model_class
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.cv_results = None

    def cross_validate_model(self, X, y, model_params=None, scoring_metrics=None):
        """
        Perform cross-validation with multiple metrics

        Parameters:
        -----------
        X : array-like
            Feature matrix
        y : array-like
            Target labels
        model_params : dict, optional
            Parameters for model initialization
        scoring_metrics : list, optional
            List of metrics to compute

        Returns:
        --------
        dict
            Cross-validation results
        """
        if model_params is None:
            model_params = {}

        if scoring_metrics is None:
            scoring_metrics = [
                "accuracy",
                "precision",
                "recall",
                "f1",
                "roc_auc",
                "log_loss",
            ]

        kfold = KFold(
            n_splits=self.cv_folds, shuffle=True, random_state=self.random_state
        )

        # Store results for each fold
        fold_results = {metric: [] for metric in scoring_metrics}
        fold_predictions = []

        print(f"Performing {self.cv_folds}-fold cross-validation...")

        for fold, (train_idx, val_idx) in enumerate(kfold.split(X)):
            print(f"Fold {fold + 1}/{self.cv_folds}")

            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            # Train model
            model = self.model_class(**model_params)
            model.fit(X_train, y_train)

            # Predictions
            y_pred = model.predict(X_val)
            y_proba = model.predict_proba(X_val)

            # Handle sklearn format
            if len(y_proba.shape) > 1 and y_proba.shape[1] > 1:
                y_proba = y_proba[:, 1]

            # Calculate metrics
            if "accuracy" in scoring_metrics:
                fold_results["accuracy"].append(accuracy_score(y_val, y_pred))

            if "precision" in scoring_metrics:
                fold_results["precision"].append(
                    precision_score(y_val, y_pred, zero_division=0)
                )

            if "recall" in scoring_metrics:
                fold_results["recall"].append(
                    recall_score(y_val, y_pred, zero_division=0)
                )

            if "f1" in scoring_metrics:
                fold_results["f1"].append(f1_score(y_val, y_pred, zero_division=0))

            if "roc_auc" in scoring_metrics:
                try:
                    roc_auc = auc(*roc_curve(y_val, y_proba)[:2])
                    fold_results["roc_auc"].append(roc_auc)
                except Exception:
                    fold_results["roc_auc"].append(np.nan)

            if "log_loss" in scoring_metrics:
                try:
                    fold_results["log_loss"].append(log_loss(y_val, y_proba))
                except Exception:
                    fold_results["log_loss"].append(np.nan)

            # Store predictions for later analysis
            fold_predictions.append(
                {
                    "y_true": y_val,
                    "y_pred": y_pred,
                    "y_proba": y_proba,
                    "indices": val_idx,
                }
            )

        # Calculate statistics
        cv_stats = {}
        for metric in scoring_metrics:
            scores = np.array(fold_results[metric])
            scores = scores[~np.isnan(scores)]  # Remove NaN values

            cv_stats[metric] = {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": np.min(scores),
                "max": np.max(scores),
                "scores": scores,
            }

        self.cv_results = {
            "fold_results": fold_results,
            "cv_stats": cv_stats,
            "fold_predictions": fold_predictions,
            "cv_folds": self.cv_folds,
        }

        return self.cv_results

    def print_cv_report(self):
        """Print cross-validation report"""
        if self.cv_results is None:
            print("No CV results available. Run cross_validate_model first.")
            return

        cv_stats = self.cv_results["cv_stats"]

        print(f"\n{'=' * 60}")
        print(f"CROSS-VALIDATION REPORT ({self.cv_folds} folds)")
        print(f"{'=' * 60}")

        print(f"{'Metric':<12} {'Mean':<8} {'Std':<8} {'Min':<8} {'Max':<8}")
        print("-" * 60)

        for metric, stats in cv_stats.items():
            print(
                f"{metric:<12} {stats['mean']:<8.4f} {stats['std']:<8.4f} "
                f"{stats['min']:<8.4f} {stats['max']:<8.4f}"
            )

        # Statistical significance tests
        print(f"\n{'=' * 60}")
        print("STATISTICAL SIGNIFICANCE TESTS")
        print(f"{'=' * 60}")

        for metric, metric_stats in cv_stats.items():
            scores = metric_stats["scores"]
            if len(scores) > 1:
                # One-sample t-test against baseline (0.5 for most metrics)
                baseline = (
                    0.5 if metric != "log_loss" else 0.693
                )  # log(2) for random classifier
                from scipy import stats

                t_stat, p_value = stats.ttest_1samp(scores, baseline)

                print(f"{metric}:")
                print(f"  H0: μ = {baseline} (random performance)")
                print(f"  t-statistic: {t_stat:.4f}")
                print(f"  p-value: {p_value:.4f}")
                print(
                    f"  {'Significant' if p_value < 0.05 else 'Not significant'} at α = 0.05"
                )
                print()

    def plot_cv_results(self, figsize=(12, 8)):
        """
        Plot cross-validation results

        Parameters:
        -----------
        figsize : tuple
            Figure size

        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        if self.cv_results is None:
            print("No CV results available. Run cross_validate_model first.")
            return None

        cv_stats = self.cv_results["cv_stats"]
        fold_results = self.cv_results["fold_results"]

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(
            f"{self.cv_folds}-Fold Cross-Validation Results",
            fontsize=16,
            fontweight="bold",
        )

        # 1. Box plot of metrics
        ax = axes[0, 0]
        metrics_to_plot = [
            m
            for m in ["accuracy", "precision", "recall", "f1", "roc_auc"]
            if m in cv_stats
        ]

        data_to_plot = [fold_results[metric] for metric in metrics_to_plot]
        bp = ax.boxplot(data_to_plot, labels=metrics_to_plot, patch_artist=True)

        # Color the boxes
        colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow", "lightpink"]
        for patch, color in zip(bp["boxes"], colors[: len(bp["boxes"])]):
            patch.set_facecolor(color)

        ax.set_ylabel("Score")
        ax.set_title("Cross-Validation Score Distribution")
        ax.grid(True, alpha=0.3)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        # 2. Mean scores with error bars
        ax = axes[0, 1]
        means = [cv_stats[metric]["mean"] for metric in metrics_to_plot]
        stds = [cv_stats[metric]["std"] for metric in metrics_to_plot]

        bars = ax.bar(
            metrics_to_plot,
            means,
            yerr=stds,
            capsize=5,
            alpha=0.7,
            color=colors[: len(metrics_to_plot)],
        )
        ax.set_ylabel("Score")
        ax.set_title("Mean CV Scores with Standard Deviation")
        ax.grid(True, alpha=0.3)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        # Add value labels
        for bar, mean, std in zip(bars, means, stds):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + std + 0.01,
                f"{mean:.3f}±{std:.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

        # 3. Fold-wise performance
        ax = axes[1, 0]
        for metric in metrics_to_plot:
            ax.plot(
                range(1, self.cv_folds + 1),
                fold_results[metric],
                marker="o",
                label=metric,
                linewidth=2,
            )

        ax.set_xlabel("Fold")
        ax.set_ylabel("Score")
        ax.set_title("Performance Across Folds")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(1, self.cv_folds + 1))

        # 4. Prediction consistency analysis
        ax = axes[1, 1]

        # Calculate prediction variance across folds
        all_predictions = np.concatenate(
            [fold["y_proba"] for fold in self.cv_results["fold_predictions"]]
        )
        all_true = np.concatenate(
            [fold["y_true"] for fold in self.cv_results["fold_predictions"]]
        )

        # Histogram of prediction probabilities
        ax.hist(
            all_predictions[all_true == 0],
            bins=20,
            alpha=0.7,
            label="Class 0",
            color="skyblue",
            density=True,
        )
        ax.hist(
            all_predictions[all_true == 1],
            bins=20,
            alpha=0.7,
            label="Class 1",
            color="lightcoral",
            density=True,
        )

        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("Density")
        ax.set_title("Aggregated Prediction Distribution")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


class BootstrapEvaluator:
    """
    Bootstrap evaluation for confidence intervals and stability analysis
    """

    def __init__(self, model, n_bootstrap=1000, random_state=42):
        """
        Initialize bootstrap evaluator

        Parameters:
        -----------
        model : object
            Trained model
        n_bootstrap : int
            Number of bootstrap samples
        random_state : int
            Random seed
        """
        self.model = model
        self.n_bootstrap = n_bootstrap
        self.random_state = random_state
        self.bootstrap_results = None

    def bootstrap_evaluate(self, X_test, y_test, confidence_level=0.95):
        """
        Perform bootstrap evaluation

        Parameters:
        -----------
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        confidence_level : float
            Confidence level for intervals

        Returns:
        --------
        dict
            Bootstrap results with confidence intervals
        """
        np.random.seed(self.random_state)
        n_samples = len(X_test)

        bootstrap_scores = {
            "accuracy": [],
            "precision": [],
            "recall": [],
            "f1": [],
            "roc_auc": [],
        }

        print(f"Performing bootstrap evaluation with {self.n_bootstrap} samples...")

        for i in range(self.n_bootstrap):
            if (i + 1) % 100 == 0:
                print(f"Bootstrap sample {i + 1}/{self.n_bootstrap}")

            # Bootstrap sample
            indices = np.random.choice(n_samples, size=n_samples, replace=True)
            X_boot = X_test[indices]
            y_boot = y_test[indices]

            # Predictions
            y_pred = self.model.predict(X_boot)
            y_proba = self.model.predict_proba(X_boot)

            # Handle sklearn format
            if len(y_proba.shape) > 1 and y_proba.shape[1] > 1:
                y_proba = y_proba[:, 1]

            # Calculate metrics
            try:
                bootstrap_scores["accuracy"].append(accuracy_score(y_boot, y_pred))
                bootstrap_scores["precision"].append(
                    precision_score(y_boot, y_pred, zero_division=0)
                )
                bootstrap_scores["recall"].append(
                    recall_score(y_boot, y_pred, zero_division=0)
                )
                bootstrap_scores["f1"].append(f1_score(y_boot, y_pred, zero_division=0))

                fpr, tpr, _ = roc_curve(y_boot, y_proba)
                bootstrap_scores["roc_auc"].append(auc(fpr, tpr))
            except Exception:
                # Skip this bootstrap sample if there's an error
                continue

        # Calculate confidence intervals
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100

        confidence_intervals = {}
        for metric, scores in bootstrap_scores.items():
            scores = np.array(scores)
            scores = scores[~np.isnan(scores)]  # Remove NaN values

            confidence_intervals[metric] = {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "lower_ci": np.percentile(scores, lower_percentile),
                "upper_ci": np.percentile(scores, upper_percentile),
                "confidence_level": confidence_level,
                "scores": scores,
            }

        self.bootstrap_results = confidence_intervals
        return confidence_intervals

    def print_bootstrap_report(self):
        """Print bootstrap evaluation report"""
        if self.bootstrap_results is None:
            print("No bootstrap results available. Run bootstrap_evaluate first.")
            return

        print(f"\n{'=' * 70}")
        print(f"BOOTSTRAP EVALUATION REPORT ({self.n_bootstrap} samples)")
        print(f"{'=' * 70}")

        conf_level = list(self.bootstrap_results.values())[0]["confidence_level"]
        print(f"Confidence Level: {conf_level:.1%}")
        print()

        print(
            f"{'Metric':<12} {'Mean':<8} {'Std':<8} {'Lower CI':<10} {'Upper CI':<10}"
        )
        print("-" * 70)

        for metric, results in self.bootstrap_results.items():
            print(
                f"{metric:<12} {results['mean']:<8.4f} {results['std']:<8.4f} "
                f"{results['lower_ci']:<10.4f} {results['upper_ci']:<10.4f}"
            )


def compare_models_comprehensive(
    models_dict, X_test, y_test, X_train=None, y_train=None
):
    """
    Comprehensive comparison of multiple models

    Parameters:
    -----------
    models_dict : dict
        Dictionary of model_name: model pairs
    X_test : array-like
        Test features
    y_test : array-like
        Test labels
    X_train : array-like, optional
        Training features
    y_train : array-like, optional
        Training labels

    Returns:
    --------
    dict
        Comprehensive comparison results
    """
    print("Comprehensive Model Comparison")
    print("=" * 50)

    comparison_results = {}

    # Evaluate each model
    for model_name, model in models_dict.items():
        print(f"\nEvaluating {model_name}...")
        evaluator = LogisticRegressionEvaluator(model, model_name)
        results = evaluator.evaluate_model(X_test, y_test, X_train, y_train)
        comparison_results[model_name] = {"evaluator": evaluator, "results": results}

    # Create comparison plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Model Comparison Dashboard", fontsize=16, fontweight="bold")

    # 1. ROC Curves Comparison
    ax = axes[0, 0]
    for model_name, data in comparison_results.items():
        roc_data = data["results"]["curves"]["roc"]
        auc_score = data["results"]["metrics"]["roc_auc"]
        ax.plot(
            roc_data["fpr"],
            roc_data["tpr"],
            linewidth=2,
            label=f"{model_name} (AUC = {auc_score:.3f})",
        )

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Precision-Recall Curves Comparison
    ax = axes[0, 1]
    for model_name, data in comparison_results.items():
        pr_data = data["results"]["curves"]["pr"]
        pr_auc = data["results"]["metrics"]["pr_auc"]
        ax.plot(
            pr_data["recall"],
            pr_data["precision"],
            linewidth=2,
            label=f"{model_name} (AUC = {pr_auc:.3f})",
        )

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curves Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Metrics Comparison
    ax = axes[1, 0]
    metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc"]
    model_names = list(models_dict.keys())

    x = np.arange(len(metrics))
    width = 0.8 / len(model_names)

    for i, model_name in enumerate(model_names):
        values = [
            comparison_results[model_name]["results"]["metrics"][metric]
            for metric in metrics
        ]
        ax.bar(x + i * width, values, width, label=model_name, alpha=0.7)

    ax.set_xlabel("Metrics")
    ax.set_ylabel("Score")
    ax.set_title("Performance Metrics Comparison")
    ax.set_xticks(x + width * (len(model_names) - 1) / 2)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # 4. Calibration Comparison
    ax = axes[1, 1]
    for model_name, data in comparison_results.items():
        cal_data = data["results"]["calibration"]
        ax.plot(
            cal_data["mean_predicted_value"],
            cal_data["fraction_of_positives"],
            marker="o",
            linewidth=2,
            label=model_name,
        )

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect Calibration")
    ax.set_xlabel("Mean Predicted Probability")
    ax.set_ylabel("Fraction of Positives")
    ax.set_title("Calibration Comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Print comparison table
    print(f"\n{'=' * 80}")
    print("MODEL COMPARISON SUMMARY")
    print(f"{'=' * 80}")
    print(
        f"{'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'ROC AUC':<10}"
    )
    print("-" * 80)

    for model_name, data in comparison_results.items():
        metrics = data["results"]["metrics"]
        print(
            f"{model_name:<20} {metrics['accuracy']:<10.4f} {metrics['precision']:<10.4f} "
            f"{metrics['recall']:<10.4f} {metrics['f1_score']:<10.4f} {metrics['roc_auc']:<10.4f}"
        )

    return comparison_results, fig


def main():
    """
    Main function to demonstrate the evaluation suite
    """
    print("Logistic Regression Evaluation Suite - Demonstration")
    print("=" * 60)

    # Generate synthetic dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=1.0,
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Dataset: {X_train_scaled.shape}")
    print(f"Class distribution: {dict(Counter(y_train))}")

    # Train models for comparison
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "L1 Regularized": LogisticRegression(
            penalty="l1", solver="liblinear", random_state=42
        ),
        "L2 Regularized": LogisticRegression(
            penalty="l2", random_state=42, max_iter=1000
        ),
    }

    # Train models
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)

    # Comprehensive model comparison
    comparison_results, comparison_fig = compare_models_comprehensive(
        models, X_test_scaled, y_test, X_train_scaled, y_train
    )
    comparison_fig.savefig(
        "model_comparison_dashboard.png", dpi=300, bbox_inches="tight"
    )
    print("\nModel comparison dashboard saved as: model_comparison_dashboard.png")

    # Detailed evaluation of best model
    best_model = models["Logistic Regression"]
    evaluator = LogisticRegressionEvaluator(best_model, "Best Model")
    results = evaluator.evaluate_model(X_test_scaled, y_test, X_train_scaled, y_train)

    # Print detailed report
    evaluator.print_evaluation_report()

    # Create evaluation dashboard
    eval_fig = evaluator.plot_evaluation_dashboard()
    eval_fig.savefig("evaluation_dashboard.png", dpi=300, bbox_inches="tight")
    print("\nEvaluation dashboard saved as: evaluation_dashboard.png")

    # Cross-validation evaluation
    print("\n" + "=" * 60)
    print("CROSS-VALIDATION EVALUATION")
    print("=" * 60)

    cv_evaluator = CrossValidationEvaluator(LogisticRegression, cv_folds=5)
    cv_results = cv_evaluator.cross_validate_model(
        X_train_scaled, y_train, model_params={"random_state": 42, "max_iter": 1000}
    )
    cv_evaluator.print_cv_report()

    cv_fig = cv_evaluator.plot_cv_results()
    cv_fig.savefig("cross_validation_results.png", dpi=300, bbox_inches="tight")
    print("\nCross-validation results saved as: cross_validation_results.png")

    # Bootstrap evaluation
    print("\n" + "=" * 60)
    print("BOOTSTRAP EVALUATION")
    print("=" * 60)

    bootstrap_evaluator = BootstrapEvaluator(best_model, n_bootstrap=500)
    bootstrap_results = bootstrap_evaluator.bootstrap_evaluate(X_test_scaled, y_test)
    bootstrap_evaluator.print_bootstrap_report()

    print("\n" + "=" * 60)
    print("EVALUATION SUITE DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Files generated:")
    print("- model_comparison_dashboard.png")
    print("- evaluation_dashboard.png")
    print("- cross_validation_results.png")


if __name__ == "__main__":
    main()
