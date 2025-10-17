import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
import warnings
import os

warnings.filterwarnings("ignore")

OUTPUTS_DIR = "../../../outputs/ml-algos/01_linear_regression"


def check_linear_regression_assumptions(X, y, graph_title: str, feature_names=None):
    """
    Comprehensive assumption checking for linear regression
    """
    # Fit the model
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    residuals = y - y_pred

    if feature_names is None:
        feature_names = [f"Feature_{i + 1}" for i in range(X.shape[1])]

    # Create subplots
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle(graph_title, fontsize=16, y=0.98)

    # 1. LINEARITY CHECK
    # Scatter plot of actual vs predicted
    axes[0, 0].scatter(y_pred, y, alpha=0.6, color="blue")
    axes[0, 0].plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
    axes[0, 0].set_xlabel("Predicted Values")
    axes[0, 0].set_ylabel("Actual Values")
    axes[0, 0].set_title("Linearity: Actual vs Predicted")
    axes[0, 0].grid(True, alpha=0.3)

    # Residuals vs fitted plot
    axes[0, 1].scatter(y_pred, residuals, alpha=0.6, color="green")
    axes[0, 1].axhline(y=0, color="red", linestyle="--")
    axes[0, 1].set_xlabel("Fitted Values")
    axes[0, 1].set_ylabel("Residuals")
    axes[0, 1].set_title("Linearity: Residuals vs Fitted")
    axes[0, 1].grid(True, alpha=0.3)

    # 2. INDEPENDENCE CHECK
    # Residuals vs observation order
    axes[0, 2].plot(residuals, marker="o", linestyle="-", alpha=0.6, color="purple")
    axes[0, 2].axhline(y=0, color="red", linestyle="--")
    axes[0, 2].set_xlabel("Observation Order")
    axes[0, 2].set_ylabel("Residuals")
    axes[0, 2].set_title("Independence: Residuals vs Order")
    axes[0, 2].grid(True, alpha=0.3)

    # Durbin-Watson test
    dw_stat = durbin_watson(residuals)
    axes[0, 2].text(
        0.05,
        0.95,
        f"Durbin-Watson: {dw_stat:.3f}\n(~2.0 is good)",
        transform=axes[0, 2].transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    # 3. HOMOSCEDASTICITY CHECK
    # Residuals vs fitted (repeated for emphasis)
    axes[1, 0].scatter(y_pred, np.abs(residuals), alpha=0.6, color="orange")
    axes[1, 0].set_xlabel("Fitted Values")
    axes[1, 0].set_ylabel("|Residuals|")
    axes[1, 0].set_title("Homoscedasticity: |Residuals| vs Fitted")
    axes[1, 0].grid(True, alpha=0.3)

    # Scale-Location plot
    standardized_residuals = residuals / np.std(residuals)
    axes[1, 1].scatter(
        y_pred, np.sqrt(np.abs(standardized_residuals)), alpha=0.6, color="brown"
    )
    axes[1, 1].set_xlabel("Fitted Values")
    axes[1, 1].set_ylabel("√|Standardized Residuals|")
    axes[1, 1].set_title("Scale-Location Plot")
    axes[1, 1].grid(True, alpha=0.3)

    # Breusch-Pagan test
    try:
        _, bp_pvalue, _, _ = het_breuschpagan(residuals, X)
        axes[1, 1].text(
            0.05,
            0.95,
            f"Breusch-Pagan p-value: {bp_pvalue:.4f}\n(>0.05 is good)",
            transform=axes[1, 1].transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )
    except Exception:
        axes[1, 1].text(
            0.05,
            0.95,
            "Breusch-Pagan test failed",
            transform=axes[1, 1].transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

    # 4. NORMALITY CHECK
    # Q-Q plot
    stats.probplot(residuals, dist="norm", plot=axes[1, 2])
    axes[1, 2].set_title("Normality: Q-Q Plot")
    axes[1, 2].grid(True, alpha=0.3)

    # Shapiro-Wilk test
    if len(residuals) <= 5000:  # Shapiro-Wilk has sample size limit
        _, sw_pvalue = stats.shapiro(residuals)
        axes[1, 2].text(
            0.05,
            0.95,
            f"Shapiro-Wilk p-value: {sw_pvalue:.4f}\n(>0.05 is good)",
            transform=axes[1, 2].transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

    # Histogram of residuals
    axes[2, 0].hist(
        residuals,
        bins=30,
        density=True,
        alpha=0.7,
        color="lightblue",
        edgecolor="black",
    )

    # Overlay normal distribution
    x_norm = np.linspace(residuals.min(), residuals.max(), 100)
    y_norm = stats.norm.pdf(x_norm, residuals.mean(), residuals.std())
    axes[2, 0].plot(x_norm, y_norm, "r-", linewidth=2, label="Normal Distribution")
    axes[2, 0].set_xlabel("Residuals")
    axes[2, 0].set_ylabel("Density")
    axes[2, 0].set_title("Normality: Histogram of Residuals")
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)

    # 5. MULTICOLLINEARITY CHECK
    if X.shape[1] > 1:
        # Correlation heatmap
        df_features = pd.DataFrame(X, columns=feature_names)
        corr_matrix = df_features.corr()

        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            center=0,
            square=True,
            ax=axes[2, 1],
            cbar_kws={"shrink": 0.8},
        )
        axes[2, 1].set_title("Multicollinearity: Correlation Matrix")

        # VIF calculation
        from statsmodels.stats.outliers_influence import variance_inflation_factor

        vif_data = pd.DataFrame()
        vif_data["Feature"] = feature_names
        vif_data["VIF"] = [variance_inflation_factor(X, i) for i in range(X.shape[1])]

        # VIF bar plot
        colors = [
            "red" if vif > 10 else "orange" if vif > 5 else "green"
            for vif in vif_data["VIF"]
        ]
        axes[2, 2].bar(range(len(vif_data)), vif_data["VIF"], color=colors, alpha=0.7)
        axes[2, 2].set_xlabel("Features")
        axes[2, 2].set_ylabel("VIF")
        axes[2, 2].set_title("Multicollinearity: VIF Values")
        axes[2, 2].set_xticks(range(len(feature_names)))
        axes[2, 2].set_xticklabels(feature_names, rotation=45)
        axes[2, 2].axhline(
            y=5, color="orange", linestyle="--", alpha=0.7, label="VIF=5"
        )
        axes[2, 2].axhline(y=10, color="red", linestyle="--", alpha=0.7, label="VIF=10")
        axes[2, 2].legend()
        axes[2, 2].grid(True, alpha=0.3)

        # Add VIF values as text
        for i, vif in enumerate(vif_data["VIF"]):
            axes[2, 2].text(i, vif + 0.1, f"{vif:.1f}", ha="center", va="bottom")
    else:
        axes[2, 1].text(
            0.5,
            0.5,
            "Single feature:\nNo multicollinearity check needed",
            transform=axes[2, 1].transAxes,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
        )
        axes[2, 1].set_title("Multicollinearity Check")

        axes[2, 2].text(
            0.5,
            0.5,
            "Single feature:\nNo VIF calculation needed",
            transform=axes[2, 2].transAxes,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
        )
        axes[2, 2].set_title("VIF Values")

    plt.tight_layout()

    # Create output directory if it doesn't exist
    output_dir = OUTPUTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure
    # Replace any characters that might be problematic in filenames
    safe_filename = "".join(
        c for c in graph_title if c.isalnum() or c in (" ", "-", "_")
    ).rstrip()
    safe_filename = safe_filename.replace(" ", "_")
    output_path = os.path.join(output_dir, f"{safe_filename}.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Graph saved to: {output_path}")

    # plt.show()

    # Print summary statistics
    print("=" * 60)
    print("LINEAR REGRESSION ASSUMPTIONS SUMMARY")
    print("=" * 60)

    print("1. LINEARITY:")
    r2_score = model.score(X, y)
    print(f"   - R² Score: {r2_score:.4f}")
    print("   - Visual check: See scatter plots above")

    print("\n2. INDEPENDENCE:")
    print(f"   - Durbin-Watson statistic: {dw_stat:.4f}")
    print("   - Interpretation: Values close to 2.0 indicate no autocorrelation")

    print("\n3. HOMOSCEDASTICITY:")
    try:
        _, bp_pvalue, _, _ = het_breuschpagan(residuals, X)
        print(f"   - Breusch-Pagan test p-value: {bp_pvalue:.4f}")
        print("   - Interpretation: p > 0.05 suggests homoscedasticity")
    except Exception:
        print("   - Breusch-Pagan test could not be performed")

    print("\n4. NORMALITY:")
    if len(residuals) <= 5000:
        _, sw_pvalue = stats.shapiro(residuals)
        print(f"   - Shapiro-Wilk test p-value: {sw_pvalue:.4f}")
        print("   - Interpretation: p > 0.05 suggests normality")
    else:
        print("   - Sample too large for Shapiro-Wilk test")

    print("\n5. MULTICOLLINEARITY:")
    if X.shape[1] > 1:
        vif_values = [variance_inflation_factor(X, i) for i in range(X.shape[1])]
        max_vif = max(vif_values)
        print(f"   - Maximum VIF: {max_vif:.2f}")
        print("   - Interpretation: VIF < 5 (good), 5-10 (moderate), >10 (high)")
        for i, (name, vif) in enumerate(zip(feature_names, vif_values)):
            status = "HIGH" if vif > 10 else "MODERATE" if vif > 5 else "LOW"
            print(f"     * {name}: {vif:.2f} ({status})")
    else:
        print("   - Single feature: No multicollinearity possible")


# Example usage with different scenarios
def demonstrate_assumptions():
    """
    Demonstrate assumption violations with example datasets
    """
    np.random.seed(42)
    n_samples = 200

    # Example 1: Well-behaved data (all assumptions satisfied)
    print("EXAMPLE 1: WELL-BEHAVED DATA")
    print("-" * 40)
    X1 = np.random.randn(n_samples, 3)
    y1 = (
        2
        + 3 * X1[:, 0]
        + 1.5 * X1[:, 1]
        - 2 * X1[:, 2]
        + np.random.randn(n_samples) * 0.5
    )

    check_linear_regression_assumptions(
        X1,
        y1,
        "01-Well behaved Data-Linear Regression Assumptions Validation",
        ["Age", "Income", "Education"],
    )

    # Example 2: Heteroscedasticity
    print("\n\nEXAMPLE 2: HETEROSCEDASTICITY VIOLATION")
    print("-" * 40)
    X2 = np.random.randn(n_samples, 2)
    # Variance increases with X values
    noise_var = 0.1 + 0.5 * np.abs(X2[:, 0])
    y2 = 1 + 2 * X2[:, 0] + X2[:, 1] + np.random.randn(n_samples) * noise_var

    check_linear_regression_assumptions(
        X2,
        y2,
        "02-Heteroscedasticity Violation-Linear Regression Assumptions Validation",
        ["Feature1", "Feature2"],
    )

    # Example 3: Non-linearity
    print("\n\nEXAMPLE 3: NON-LINEARITY VIOLATION")
    print("-" * 40)
    X3 = np.random.randn(n_samples, 2)
    # Non-linear relationship
    y3 = 1 + X3[:, 0] ** 2 + np.sin(X3[:, 1]) + np.random.randn(n_samples) * 0.3

    check_linear_regression_assumptions(
        X3,
        y3,
        "03-Non linearity Violation-Linear Regression Assumptions Validation",
        ["Feature1", "Feature2"],
    )


# Run the demonstration
if __name__ == "__main__":
    demonstrate_assumptions()
