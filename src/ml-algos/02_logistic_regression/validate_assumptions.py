"""
Logistic Regression Assumptions Validation

This module provides comprehensive functions to validate the key assumptions
of logistic regression models with visualizations and statistical tests.

Key Assumptions Tested:
1. Binary/Categorical Target Variable
2. Linear Relationship Between Features and Log-Odds
3. Independence of Observations
4. No Severe Multicollinearity
5. Large Sample Size
6. No Complete Separation

Author: Peeush Agarwal
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report, confusion_matrix
import warnings

warnings.filterwarnings("ignore")

# Set style for better visualizations
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class LogisticRegressionAssumptions:
    """
    A comprehensive class for validating logistic regression assumptions
    """

    def __init__(self, X, y, feature_names=None):
        """
        Initialize with feature matrix and target variable

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix
        y : array-like, shape (n_samples,)
            Target variable (should be binary: 0/1)
        feature_names : list, optional
            Names of features for better visualization
        """
        self.X = np.array(X)
        self.y = np.array(y)
        self.n_samples, self.n_features = self.X.shape
        self.feature_names = feature_names or [
            f"Feature_{i}" for i in range(self.n_features)
        ]

        # Fit initial model for analysis
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(self.X, self.y)
        self.y_pred_proba = self.model.predict_proba(self.X)[:, 1]

    def check_target_variable(self):
        """
        Check if target variable is appropriate for logistic regression
        """
        print("=" * 60)
        print("ASSUMPTION 1: BINARY/CATEGORICAL TARGET VARIABLE")
        print("=" * 60)

        unique_values = np.unique(self.y)
        n_unique = len(unique_values)

        print(f"Number of unique values in target: {n_unique}")
        print(f"Unique values: {unique_values}")

        if n_unique == 2:
            print("✅ PASSED: Target variable has exactly 2 unique values (binary)")
            if set(unique_values) == {0, 1}:
                print("✅ PASSED: Target variable is properly encoded as 0/1")
            else:
                print("⚠️  WARNING: Target variable should be encoded as 0/1")
        elif n_unique > 2:
            print(
                "⚠️  WARNING: Target has more than 2 classes - consider multinomial logistic regression"
            )
        else:
            print("❌ FAILED: Target variable has only 1 unique value")

        # Check class distribution
        class_counts = np.bincount(self.y.astype(int))
        class_proportions = class_counts / len(self.y)

        print(f"\nClass distribution:")
        for i, (count, prop) in enumerate(zip(class_counts, class_proportions)):
            print(f"  Class {i}: {count} samples ({prop:.2%})")

        # Check for class imbalance
        min_class_prop = np.min(class_proportions)
        if min_class_prop < 0.1:
            print("⚠️  WARNING: Severe class imbalance detected (minority class < 10%)")
        elif min_class_prop < 0.2:
            print(
                "⚠️  WARNING: Moderate class imbalance detected (minority class < 20%)"
            )
        else:
            print("✅ PASSED: Classes are reasonably balanced")

    def box_tidwell_test(self, alpha=0.05):
        """
        Box-Tidwell test for linearity in logit
        Tests if log-odds are linear in the predictors
        """
        print("\n" + "=" * 60)
        print("ASSUMPTION 2: LINEAR RELATIONSHIP IN LOG-ODDS")
        print("=" * 60)

        # Create interaction terms with log of features (for positive features)
        results = []

        for i, feature_name in enumerate(self.feature_names):
            feature = self.X[:, i]

            # Skip if feature has non-positive values
            if np.any(feature <= 0):
                print(
                    f"⚠️  WARNING: {feature_name} has non-positive values, skipping Box-Tidwell test"
                )
                continue

            # Create interaction term: X * ln(X)
            interaction_term = feature * np.log(feature)

            # Create extended feature matrix
            X_extended = np.column_stack([self.X, interaction_term])

            # Fit logistic regression with interaction term
            model_extended = LogisticRegression(max_iter=1000)
            model_extended.fit(X_extended, self.y)

            # Test significance of interaction coefficient
            # Note: This is a simplified version; proper implementation would use
            # likelihood ratio test or Wald test
            interaction_coef = model_extended.coef_[0][-1]

            # Store results
            results.append(
                {
                    "feature": feature_name,
                    "interaction_coef": interaction_coef,
                    "abs_coef": abs(interaction_coef),
                }
            )

            # Simple heuristic for significance
            if abs(interaction_coef) > 0.1:
                print(
                    f"⚠️  WARNING: {feature_name} may violate linearity assumption (coef: {interaction_coef:.4f})"
                )
            else:
                print(
                    f"✅ PASSED: {feature_name} appears linear in log-odds (coef: {interaction_coef:.4f})"
                )

        return results

    def check_independence(self):
        """
        Check independence of observations
        """
        print("\n" + "=" * 60)
        print("ASSUMPTION 3: INDEPENDENCE OF OBSERVATIONS")
        print("=" * 60)

        # Durbin-Watson test for autocorrelation in residuals
        from scipy.stats import pearsonr

        # Calculate deviance residuals
        p = self.y_pred_proba
        deviance_residuals = np.sign(self.y - p) * np.sqrt(
            2
            * (
                self.y * np.log(np.maximum(p, 1e-10))
                + (1 - self.y) * np.log(np.maximum(1 - p, 1e-10))
            )
        )

        # Test for autocorrelation (simple version)
        if len(deviance_residuals) > 1:
            # Lag-1 autocorrelation
            autocorr, p_value = pearsonr(
                deviance_residuals[:-1], deviance_residuals[1:]
            )

            print(f"Lag-1 autocorrelation of residuals: {autocorr:.4f}")
            print(f"P-value: {p_value:.4f}")

            if abs(autocorr) > 0.1:
                print("⚠️  WARNING: Potential autocorrelation in residuals detected")
            else:
                print("✅ PASSED: No strong autocorrelation detected")

        print("\n📝 Note: Independence assumption is primarily checked through:")
        print("   - Study design and data collection method")
        print("   - Domain knowledge about data structure")
        print("   - Checking for temporal or spatial patterns")

    def check_multicollinearity(self, threshold=10):
        """
        Check for multicollinearity using VIF and correlation matrix
        """
        print("\n" + "=" * 60)
        print("ASSUMPTION 4: NO SEVERE MULTICOLLINEARITY")
        print("=" * 60)

        # Calculate correlation matrix
        corr_matrix = np.corrcoef(self.X.T)

        # Find highly correlated feature pairs
        high_corr_pairs = []
        for i in range(len(self.feature_names)):
            for j in range(i + 1, len(self.feature_names)):
                corr_val = corr_matrix[i, j]
                if abs(corr_val) > 0.8:
                    high_corr_pairs.append(
                        (self.feature_names[i], self.feature_names[j], corr_val)
                    )

        if high_corr_pairs:
            print("⚠️  WARNING: High correlations detected:")
            for feat1, feat2, corr in high_corr_pairs:
                print(f"   {feat1} - {feat2}: {corr:.3f}")
        else:
            print("✅ PASSED: No high correlations (>0.8) detected")

        # Calculate VIF (Variance Inflation Factor)
        print(f"\nVariance Inflation Factors:")
        print(f"{'Feature':<15} {'VIF':<8} {'Status'}")
        print("-" * 35)

        vif_values = []
        for i in range(self.n_features):
            # Calculate R² for feature i regressed on all other features
            if self.n_features > 1:
                X_others = np.delete(self.X, i, axis=1)
                y_feature = self.X[:, i]

                # Simple linear regression R²
                try:
                    from sklearn.linear_model import LinearRegression

                    reg = LinearRegression()
                    reg.fit(X_others, y_feature)
                    r2 = reg.score(X_others, y_feature)
                    vif = 1 / (1 - r2) if r2 < 0.99 else float("inf")
                except:
                    vif = 1.0
            else:
                vif = 1.0

            vif_values.append(vif)

            # Determine status
            if vif > threshold:
                status = "❌ HIGH"
            elif vif > 5:
                status = "⚠️  MODERATE"
            else:
                status = "✅ LOW"

            print(f"{self.feature_names[i]:<15} {vif:<8.2f} {status}")

        return vif_values

    def check_sample_size(self):
        """
        Check if sample size is adequate for logistic regression
        """
        print("\n" + "=" * 60)
        print("ASSUMPTION 5: ADEQUATE SAMPLE SIZE")
        print("=" * 60)

        # Events per variable (EPV) rule
        min_class_count = np.min(np.bincount(self.y.astype(int)))
        epv = min_class_count / self.n_features

        print(f"Total samples: {self.n_samples}")
        print(f"Number of features: {self.n_features}")
        print(f"Minority class size: {min_class_count}")
        print(f"Events per variable (EPV): {epv:.1f}")

        # Guidelines
        if epv >= 20:
            print("✅ EXCELLENT: EPV ≥ 20 (very stable estimates)")
        elif epv >= 10:
            print("✅ GOOD: EPV ≥ 10 (stable estimates)")
        elif epv >= 5:
            print("⚠️  WARNING: EPV < 10 (potentially unstable estimates)")
        else:
            print(
                "❌ CRITICAL: EPV < 5 (very unstable estimates, consider regularization)"
            )

        # Overall sample size check
        recommended_size = max(100, 10 * self.n_features)
        if self.n_samples >= recommended_size:
            print(
                f"✅ PASSED: Sample size adequate ({self.n_samples} ≥ {recommended_size})"
            )
        else:
            print(
                f"⚠️  WARNING: Sample size may be inadequate ({self.n_samples} < {recommended_size})"
            )

    def check_complete_separation(self):
        """
        Check for complete or quasi-complete separation
        """
        print("\n" + "=" * 60)
        print("ASSUMPTION 6: NO COMPLETE SEPARATION")
        print("=" * 60)

        # Check coefficient magnitudes
        coefficients = self.model.coef_[0]
        large_coef_threshold = 10

        print("Coefficient Analysis:")
        print(f"{'Feature':<15} {'Coefficient':<12} {'Magnitude':<10} {'Status'}")
        print("-" * 55)

        separation_issues = []
        for i, (coef, feature_name) in enumerate(zip(coefficients, self.feature_names)):
            magnitude = abs(coef)

            if magnitude > large_coef_threshold:
                status = "⚠️  LARGE"
                separation_issues.append(feature_name)
            elif magnitude > 5:
                status = "⚠️  MODERATE"
            else:
                status = "✅ NORMAL"

            print(f"{feature_name:<15} {coef:<12.4f} {magnitude:<10.2f} {status}")

        if separation_issues:
            print(
                f"\n⚠️  WARNING: Potential separation issues with: {', '.join(separation_issues)}"
            )
            print("   Consider regularization or removing these features")
        else:
            print("\n✅ PASSED: No signs of complete separation detected")

        # Check perfect classification
        y_pred = self.model.predict(self.X)
        accuracy = np.mean(y_pred == self.y)

        if accuracy == 1.0:
            print(
                "⚠️  WARNING: Perfect classification on training data - possible overfitting/separation"
            )
        else:
            print(f"✅ Training accuracy: {accuracy:.3f} (not perfect - good sign)")

    def create_visualizations(self, figsize=(20, 15)):
        """
        Create comprehensive visualization plots for assumption checking
        """
        fig, axes = plt.subplots(3, 3, figsize=figsize)
        fig.suptitle(
            "Logistic Regression Assumptions Validation", fontsize=16, fontweight="bold"
        )

        # 1. Target distribution
        ax = axes[0, 0]
        class_counts = np.bincount(self.y.astype(int))
        class_labels = [f"Class {i}" for i in range(len(class_counts))]
        bars = ax.bar(class_labels, class_counts, color=["skyblue", "lightcoral"])
        ax.set_title("Target Variable Distribution")
        ax.set_ylabel("Count")

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

        # 2. Correlation matrix heatmap
        ax = axes[0, 1]
        corr_matrix = np.corrcoef(self.X.T)
        im = ax.imshow(corr_matrix, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_title("Feature Correlation Matrix")
        ax.set_xticks(range(len(self.feature_names)))
        ax.set_yticks(range(len(self.feature_names)))
        ax.set_xticklabels(self.feature_names, rotation=45, ha="right")
        ax.set_yticklabels(self.feature_names)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label("Correlation")

        # 3. Predicted probabilities distribution
        ax = axes[0, 2]
        ax.hist(
            self.y_pred_proba[self.y == 0],
            bins=20,
            alpha=0.7,
            label="Class 0",
            color="skyblue",
            density=True,
        )
        ax.hist(
            self.y_pred_proba[self.y == 1],
            bins=20,
            alpha=0.7,
            label="Class 1",
            color="lightcoral",
            density=True,
        )
        ax.set_title("Predicted Probability Distribution")
        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("Density")
        ax.legend()

        # 4. Residual plots for first few features
        for i in range(min(3, self.n_features)):
            ax = axes[1, i]

            # Calculate deviance residuals
            p = self.y_pred_proba
            deviance_residuals = np.sign(self.y - p) * np.sqrt(
                2
                * (
                    self.y * np.log(np.maximum(p, 1e-10))
                    + (1 - self.y) * np.log(np.maximum(1 - p, 1e-10))
                )
            )

            ax.scatter(self.X[:, i], deviance_residuals, alpha=0.6)
            ax.axhline(y=0, color="red", linestyle="--")
            ax.set_title(f"Residuals vs {self.feature_names[i]}")
            ax.set_xlabel(self.feature_names[i])
            ax.set_ylabel("Deviance Residuals")

        # 5. Box plot of features by class
        for i in range(min(3, self.n_features)):
            ax = axes[2, i]

            data_class_0 = self.X[self.y == 0, i]
            data_class_1 = self.X[self.y == 1, i]

            box_data = [data_class_0, data_class_1]
            bp = ax.boxplot(box_data, labels=["Class 0", "Class 1"], patch_artist=True)
            bp["boxes"][0].set_facecolor("skyblue")
            bp["boxes"][1].set_facecolor("lightcoral")

            ax.set_title(f"{self.feature_names[i]} by Class")
            ax.set_ylabel(self.feature_names[i])

        plt.tight_layout()
        return fig

    def run_all_checks(self):
        """
        Run all assumption checks and create visualizations
        """
        print("LOGISTIC REGRESSION ASSUMPTIONS VALIDATION")
        print("=" * 80)

        # Run all checks
        self.check_target_variable()
        self.box_tidwell_test()
        self.check_independence()
        vif_values = self.check_multicollinearity()
        self.check_sample_size()
        self.check_complete_separation()

        # Create visualizations
        fig = self.create_visualizations()

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY AND RECOMMENDATIONS")
        print("=" * 60)
        print("1. Ensure target variable is properly encoded (0/1)")
        print("2. Consider polynomial/interaction terms if linearity is violated")
        print("3. Check data collection method for independence")
        print("4. Use regularization if multicollinearity is high (VIF > 10)")
        print("5. Collect more data if sample size is inadequate")
        print("6. Use regularization if separation issues detected")

        return fig


def generate_example_datasets():
    """
    Generate example datasets to demonstrate assumption violations
    """
    np.random.seed(42)

    datasets = {}

    # 1. Well-behaved dataset
    X_good, y_good = make_classification(
        n_samples=1000,
        n_features=4,
        n_redundant=0,
        n_informative=4,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=1.2,
    )
    datasets["well_behaved"] = (
        X_good,
        y_good,
        ["Feature_1", "Feature_2", "Feature_3", "Feature_4"],
    )

    # 2. Dataset with multicollinearity
    X_multi = np.random.randn(500, 4)
    X_multi[:, 1] = X_multi[:, 0] + 0.2 * np.random.randn(500)  # Highly correlated
    X_multi[:, 3] = 2 * X_multi[:, 2] + 0.1 * np.random.randn(
        500
    )  # Almost perfectly correlated
    y_multi = (X_multi[:, 0] + X_multi[:, 2] + np.random.randn(500) * 0.5 > 0).astype(
        int
    )
    datasets["multicollinearity"] = (
        X_multi,
        y_multi,
        ["X1", "X2_corr_X1", "X3", "X4_corr_X3"],
    )

    # 3. Small dataset
    X_small, y_small = make_classification(
        n_samples=50, n_features=8, n_redundant=0, n_informative=8, random_state=42
    )
    datasets["small_sample"] = (X_small, y_small, [f"Feature_{i}" for i in range(8)])

    # 4. Imbalanced dataset
    X_imbal, y_imbal = make_classification(
        n_samples=1000,
        n_features=4,
        n_redundant=0,
        n_informative=4,
        weights=[0.95, 0.05],
        random_state=42,
    )
    datasets["imbalanced"] = (
        X_imbal,
        y_imbal,
        ["Feature_1", "Feature_2", "Feature_3", "Feature_4"],
    )

    return datasets


def main():
    """
    Main function to demonstrate assumption validation
    """
    print("Logistic Regression Assumptions Validation Demo")
    print("=" * 50)

    # Generate example datasets
    datasets = generate_example_datasets()

    for name, (X, y, feature_names) in datasets.items():
        print(f"\n{'=' * 80}")
        print(f"ANALYZING DATASET: {name.upper()}")
        print(f"{'=' * 80}")

        # Create validator
        validator = LogisticRegressionAssumptions(X, y, feature_names)

        # Run all checks
        fig = validator.run_all_checks()

        # Save plot
        fig.savefig(f"assumptions_validation_{name}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

        print(f"\nPlot saved as: assumptions_validation_{name}.png")
        print("-" * 50)


if __name__ == "__main__":
    main()
