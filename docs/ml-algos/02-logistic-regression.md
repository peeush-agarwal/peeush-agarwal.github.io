# Logistic Regression: A Comprehensive Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Mathematical Foundation](#mathematical-foundation)
3. [Types of Logistic Regression](#types-of-logistic-regression)
4. [Algorithm Implementation](#algorithm-implementation)
5. [Assumptions](#assumptions)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Advantages and Disadvantages](#advantages-and-disadvantages)
8. [Common Interview Questions](#common-interview-questions)
9. [Practical Considerations](#practical-considerations)
10. [Code Examples](#code-examples)

## Introduction

Logistic Regression is a fundamental statistical method used for binary and multiclass classification problems. Despite its name containing "regression," it is actually a classification algorithm that models the probability of class membership using the logistic (sigmoid) function. It serves as a cornerstone in machine learning and provides an excellent foundation for understanding more complex classification algorithms.

**Key Concepts:**
- **Supervised Learning**: Uses labeled training data for classification
- **Classification Task**: Predicts discrete categorical outcomes
- **Probabilistic Model**: Outputs probabilities rather than hard classifications
- **Linear Decision Boundary**: Creates linear separating hyperplanes
- **Generalized Linear Model**: Extension of linear regression using link functions

## Mathematical Foundation

### Binary Logistic Regression

The logistic regression model uses the **sigmoid (logistic) function** to map any real-valued input to a value between 0 and 1:

$$P(Y=1|X) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n)}}$$

Or more compactly:

$$P(Y=1|X) = \frac{1}{1 + e^{-\mathbf{X}\boldsymbol{\beta}}}$$

Where:
- $P(Y=1|X)$ = probability of positive class given features
- $\mathbf{X}$ = feature matrix (including bias term)
- $\boldsymbol{\beta}$ = coefficient vector
- $e$ = Euler's number (≈ 2.718)

### Sigmoid Function Properties

The sigmoid function $\sigma(z) = \frac{1}{1 + e^{-z}}$ has several important properties:

- **Range**: $(0, 1)$ - perfect for probabilities
- **Monotonic**: Always increasing
- **Differentiable**: Smooth gradient everywhere
- **S-shaped**: Sigmoid curve
- **Symmetric**: Around point $(0, 0.5)$

$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$

### Odds and Log-Odds (Logit)

**Odds**: The ratio of probability of success to probability of failure:

$$\text{Odds} = \frac{P(Y=1|X)}{P(Y=0|X)} = \frac{P(Y=1|X)}{1 - P(Y=1|X)}$$

**Log-Odds (Logit)**: The natural logarithm of odds:

$$\text{logit}(P) = \ln\left(\frac{P}{1-P}\right) = \mathbf{X}\boldsymbol{\beta}$$

This is the **linear component** of logistic regression, showing that logistic regression models the log-odds as a linear function of the features.

### Maximum Likelihood Estimation

Unlike linear regression, logistic regression cannot be solved analytically. We use **Maximum Likelihood Estimation (MLE)** to find optimal parameters.

**Likelihood Function**: For binary classification:

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{m} P(Y=y^{(i)}|X^{(i)})$$

$$L(\boldsymbol{\beta}) = \prod_{i=1}^{m} [h_{\boldsymbol{\beta}}(x^{(i)})]^{y^{(i)}} [1 - h_{\boldsymbol{\beta}}(x^{(i)})]^{1-y^{(i)}}$$

**Log-Likelihood**: Taking the natural log for easier optimization:

$$\ell(\boldsymbol{\beta}) = \sum_{i=1}^{m} [y^{(i)} \log(h_{\boldsymbol{\beta}}(x^{(i)})) + (1-y^{(i)}) \log(1 - h_{\boldsymbol{\beta}}(x^{(i)}))]$$

### Cost Function (Cross-Entropy Loss)

The negative log-likelihood gives us the **cross-entropy loss**:

$$J(\boldsymbol{\beta}) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(h_{\boldsymbol{\beta}}(x^{(i)})) + (1-y^{(i)}) \log(1 - h_{\boldsymbol{\beta}}(x^{(i)}))]$$

**Gradient**: The partial derivatives for gradient descent:

$$\frac{\partial J}{\partial \beta_j} = \frac{1}{m} \sum_{i=1}^{m} (h_{\boldsymbol{\beta}}(x^{(i)}) - y^{(i)}) x_j^{(i)}$$

In matrix form:

$$\nabla J = \frac{1}{m} \mathbf{X}^T (h_{\boldsymbol{\beta}}(\mathbf{X}) - \mathbf{y})$$

### Multiclass Logistic Regression

For multiple classes, we extend to **multinomial logistic regression** using the **softmax function**:

$$P(Y=k|X) = \frac{e^{\mathbf{X}\boldsymbol{\beta}_k}}{\sum_{j=1}^{K} e^{\mathbf{X}\boldsymbol{\beta}_j}}$$

Where $K$ is the number of classes and $\boldsymbol{\beta}_k$ is the coefficient vector for class $k$.

## Types of Logistic Regression

### 1. Binary Logistic Regression
- **Use case**: Two-class problems (0/1, Yes/No, Success/Failure)
- **Output**: Single probability $P(Y=1|X)$
- **Decision boundary**: Linear hyperplane
- **Examples**: Email spam detection, medical diagnosis, customer churn

### 2. Multinomial Logistic Regression
- **Use case**: Multiple unordered classes (>2)
- **Output**: Probability distribution over all classes
- **Extension**: Uses softmax function
- **Examples**: Image classification, sentiment analysis (positive/negative/neutral)

### 3. Ordinal Logistic Regression
- **Use case**: Ordered categorical outcomes
- **Characteristic**: Respects natural ordering of classes
- **Examples**: Survey ratings (1-5 stars), severity levels (mild/moderate/severe)
- **Method**: Cumulative link models

### 4. Regularized Logistic Regression

#### L1 Regularization (Lasso)
$$J(\boldsymbol{\beta}) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(h_{\boldsymbol{\beta}}(x^{(i)})) + (1-y^{(i)}) \log(1 - h_{\boldsymbol{\beta}}(x^{(i)}))] + \lambda \sum_{j=1}^{n} |\beta_j|$$

#### L2 Regularization (Ridge)
$$J(\boldsymbol{\beta}) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(h_{\boldsymbol{\beta}}(x^{(i)})) + (1-y^{(i)}) \log(1 - h_{\boldsymbol{\beta}}(x^{(i)}))] + \lambda \sum_{j=1}^{n} \beta_j^2$$

#### Elastic Net
$$J(\boldsymbol{\beta}) = \text{Cross-entropy} + \lambda_1 \sum_{j=1}^{n} |\beta_j| + \lambda_2 \sum_{j=1}^{n} \beta_j^2$$

## Algorithm Implementation

### Gradient Descent Algorithm

```pseudocode
ALGORITHM: Logistic Regression with Gradient Descent

INPUT: 
  - Training data: X (m × n), y (m × 1) with y ∈ {0,1}
  - Learning rate: α
  - Number of iterations: max_iter
  - Convergence threshold: ε

OUTPUT: Optimal parameters β

PROCEDURE:
1. Initialize β randomly (small values near zero)
2. Add bias column to X (column of ones)
3. FOR iteration = 1 to max_iter:
   a. Compute linear combination: z = X × β
   b. Compute predictions: ŷ = sigmoid(z) = 1/(1 + exp(-z))
   c. Compute cost: J = -(1/m) × [y^T × log(ŷ) + (1-y)^T × log(1-ŷ)]
   d. Compute gradients: ∇J = (1/m) × X^T × (ŷ - y)
   e. Update parameters: β = β - α × ∇J
   f. IF ||∇J|| < ε: BREAK (convergence)
4. RETURN β

COMPLEXITY:
- Time: O(max_iter × m × n)
- Space: O(m × n)
```

### Newton-Raphson Method

```pseudocode
ALGORITHM: Logistic Regression with Newton-Raphson

INPUT: 
  - Training data: X (m × n), y (m × 1)
  - Number of iterations: max_iter
  - Convergence threshold: ε

OUTPUT: Optimal parameters β

PROCEDURE:
1. Initialize β to small random values
2. Add bias column to X
3. FOR iteration = 1 to max_iter:
   a. Compute predictions: p = sigmoid(X × β)
   b. Compute gradient: g = X^T × (p - y)
   c. Compute Hessian: H = X^T × diag(p × (1-p)) × X
   d. Update: β = β - H^(-1) × g
   e. IF ||g|| < ε: BREAK
4. RETURN β

COMPLEXITY:
- Time: O(max_iter × n³) due to Hessian inversion
- Space: O(n²) for Hessian matrix
```

### Prediction Algorithm

```pseudocode
ALGORITHM: Logistic Regression Prediction

INPUT: 
  - Trained parameters: β
  - New data: X_new (k × n)
  - Decision threshold: τ (default = 0.5)

OUTPUT: Predictions and probabilities

PROCEDURE:
1. Add bias column to X_new
2. Compute linear combination: z = X_new × β
3. Compute probabilities: p = sigmoid(z)
4. Make predictions: ŷ = (p >= τ) ? 1 : 0
5. RETURN ŷ, p

COMPLEXITY:
- Time: O(k × n)
- Space: O(k)
```

## Assumptions

Logistic regression has fewer and more relaxed assumptions compared to linear regression, making it more robust in many scenarios.

### 1. Binary or Ordinal Target Variable

**Definition**: The dependent variable should be binary (0/1) for binary logistic regression, or ordinal/categorical for multinomial variants.

**Requirements**:
- Binary: Exactly two distinct outcomes
- Multinomial: More than two unordered categories
- Ordinal: Ordered categorical outcomes

**Consequences of Violation**:
- Inappropriate model choice
- Poor performance and interpretation
- Invalid probability estimates

**Solutions**:
- Binary: Ensure proper encoding (0/1, True/False)
- Continuous target: Use linear regression or discretize
- Multiple classes: Use multinomial logistic regression

### 2. Linear Relationship Between Features and Log-Odds

**Definition**: The log-odds (logit) of the target variable should be a linear combination of the independent variables.

**Mathematical Expression**:
$$\ln\left(\frac{P(Y=1|X)}{P(Y=0|X)}\right) = \beta_0 + \beta_1 x_1 + ... + \beta_n x_n$$

**Detailed Explanation**:
- The relationship is linear in the log-odds space, not probability space
- Non-linear relationships in feature space need transformation
- Feature engineering can address non-linearity

**Detection Methods**:
- **Box-Tidwell test**: Tests linearity in logit
- **Scatter plots**: Plot each feature vs. log-odds
- **Polynomial terms**: Test significance of higher-order terms

**Solutions when violated**:
- Polynomial features: $X^2, X^3, \sqrt{X}$
- Interaction terms: $X_1 \times X_2$
- Spline transformations
- Non-linear classifiers: Random Forest, SVM with kernels

### 3. Independence of Observations

**Definition**: Each observation should be independent of all others. No temporal or spatial correlation between residuals.

**Same as linear regression**: 
$$Cov(\epsilon_i, \epsilon_j) = 0 \text{ for all } i \neq j$$

**Common Violations**:
- Time series data with autocorrelation
- Clustered data (students in schools)
- Repeated measures on same subjects
- Spatial correlation in geographic data

**Detection Methods**:
- **Durbin-Watson test**: For autocorrelation
- **Residual plots**: Check for patterns
- **Domain knowledge**: Understand data collection process

**Solutions**:
- **Generalized Estimating Equations (GEE)**: For clustered data
- **Mixed-effects logistic regression**: Random effects for clusters
- **Time series methods**: Account for temporal correlation
- **Robust standard errors**: Cluster-robust estimates

### 4. No Severe Multicollinearity

**Definition**: Independent variables should not be highly correlated with each other, though logistic regression is more robust to multicollinearity than linear regression.

**Impact on Logistic Regression**:
- Less severe than in linear regression
- Still causes unstable coefficient estimates
- Wide confidence intervals
- Difficulty in interpretation

**Detection Methods**:
- **Variance Inflation Factor (VIF)**: Same as linear regression
- **Correlation matrix**: Check pairwise correlations
- **Condition Index**: Measure of numerical stability

**Solutions**:
- Remove highly correlated features
- Principal Component Analysis (PCA)
- Regularization (L1/L2)
- Domain knowledge for feature selection

### 5. Large Sample Size

**Definition**: Logistic regression requires larger sample sizes than linear regression, especially for stable coefficient estimates and valid statistical inference.

**Guidelines**:
- **Minimum**: At least 10-20 observations per feature
- **Rule of thumb**: 10 events per variable (EPV) for each class
- **Stable estimates**: 50+ observations per feature recommended
- **Small samples**: Can lead to complete separation issues

**Consequences of Small Samples**:
- **Complete separation**: Perfect classification on training data
- **Quasi-complete separation**: Nearly perfect separation
- **Unstable estimates**: Large standard errors
- **Convergence issues**: Algorithm may not converge

**Solutions for Small Samples**:
- **Regularization**: L1/L2 penalties
- **Bayesian methods**: Prior distributions on coefficients
- **Exact logistic regression**: For very small samples
- **Feature reduction**: Reduce number of parameters

### 6. No Complete Separation

**Definition**: There should be no complete or quasi-complete separation in the data, where one or more features perfectly predict the outcome.

**Types of Separation**:
- **Complete separation**: A hyperplane perfectly separates classes
- **Quasi-complete separation**: Near-perfect separation with one misclassified point

**Consequences**:
- Infinite coefficient estimates
- Algorithm convergence failures
- Perfect training accuracy but poor generalization
- Unreliable standard errors and p-values

**Detection Methods**:
- Monitor coefficient magnitudes during training
- Check for perfect or near-perfect classification
- Examine extreme coefficient values (|β| > 10)

**Solutions**:
- **Regularization**: Add L1 or L2 penalties
- **Remove problematic features**: That cause separation
- **Data collection**: Gather more diverse samples
- **Bayesian methods**: Use informative priors
- **Penalized likelihood**: Firth's correction

### Assumption Validation

**Implementation Available**: [`src/ml-algos/02_logistic_regression/validate_assumptions.py`](../../src/ml-algos/02_logistic_regression/validate_assumptions.py)

This comprehensive module provides:
- **Box-Tidwell test** for linearity in logit
- **VIF calculation** for multicollinearity detection
- **Sample size adequacy** checks
- **Complete separation** detection algorithms
- **Independence tests** for clustered data
- **Visual diagnostics** with statistical plots

Example usage:
```python
from src.ml_algos.logistic_regression.validate_assumptions import LogisticRegressionAssumptions

# Create validator instance
validator = LogisticRegressionAssumptions()

# Check all assumptions
results = validator.check_all_assumptions(X, y)
validator.print_assumption_summary()

# Generate diagnostic plots
fig = validator.plot_assumption_diagnostics()
```

## Evaluation Metrics

### Classification Metrics

#### 1. Confusion Matrix
For binary classification:

$$\begin{bmatrix}
TN & FP \\
FN & TP
\end{bmatrix}$$

Where:
- **TP (True Positives)**: Correctly predicted positive cases
- **TN (True Negatives)**: Correctly predicted negative cases
- **FP (False Positives)**: Incorrectly predicted positive (Type I error)
- **FN (False Negatives)**: Incorrectly predicted negative (Type II error)

#### 2. Accuracy
$$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$

#### 3. Precision (Positive Predictive Value)
$$Precision = \frac{TP}{TP + FP}$$

#### 4. Recall (Sensitivity, True Positive Rate)
$$Recall = \frac{TP}{TP + FN}$$

#### 5. Specificity (True Negative Rate)
$$Specificity = \frac{TN}{TN + FP}$$

#### 6. F1-Score
$$F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall} = \frac{2TP}{2TP + FP + FN}$$

#### 7. F-Beta Score
$$F_\beta = (1 + \beta^2) \times \frac{Precision \times Recall}{\beta^2 \times Precision + Recall}$$

### Probabilistic Metrics

#### 8. Log-Loss (Cross-Entropy)
$$LogLoss = -\frac{1}{m} \sum_{i=1}^{m} [y_i \log(p_i) + (1-y_i) \log(1-p_i)]$$

#### 9. Brier Score
$$BS = \frac{1}{m} \sum_{i=1}^{m} (p_i - y_i)^2$$

#### 10. AUC-ROC (Area Under ROC Curve)
- **ROC Curve**: Plot of True Positive Rate vs. False Positive Rate
- **AUC**: Area under the ROC curve
- **Interpretation**: 
  - AUC = 0.5: Random classifier
  - AUC = 1.0: Perfect classifier
  - AUC > 0.7: Generally acceptable
  - AUC > 0.8: Good performance
  - AUC > 0.9: Excellent performance

#### 11. AUC-PR (Area Under Precision-Recall Curve)
- **PR Curve**: Plot of Precision vs. Recall
- **Better for imbalanced datasets** than ROC
- **Baseline**: Proportion of positive class

### Statistical Measures

#### 12. Likelihood Ratio Test
$$LR = -2 \ln\left(\frac{L_0}{L_1}\right)$$

Where $L_0$ is likelihood of null model and $L_1$ is likelihood of full model.

#### 13. Pseudo R-squared Measures

**McFadden's R²**:
$$R^2_{McFadden} = 1 - \frac{\ln(L_1)}{\ln(L_0)}$$

**Cox & Snell R²**:
$$R^2_{CS} = 1 - \left(\frac{L_0}{L_1}\right)^{2/m}$$

**Nagelkerke R²**:
$$R^2_{N} = \frac{R^2_{CS}}{1 - (L_0)^{2/m}}$$

#### 14. Hosmer-Lemeshow Test
Tests goodness of fit by comparing observed vs. expected frequencies across deciles of predicted probabilities.

## Advantages and Disadvantages

### Advantages

#### 1. **Probabilistic Output**
- Provides probability estimates, not just classifications
- Useful for ranking and uncertainty quantification
- Enables threshold tuning for different use cases

#### 2. **No Distributional Assumptions**
- Doesn't assume normality of features
- Robust to outliers in features (not target)
- Flexible with different data types

#### 3. **Interpretable Coefficients**
- Clear relationship between features and log-odds
- Odds ratios provide meaningful interpretations
- Statistical significance testing available

#### 4. **Computational Efficiency**
- Fast training and prediction
- Scales well to large datasets
- No hyperparameters in basic form

#### 5. **Baseline Model**
- Excellent starting point for classification
- Easy to implement and debug
- Well-understood statistical properties

#### 6. **Extension Flexibility**
- Easily extends to multiclass problems
- Regularization variants available
- Foundation for more complex models

### Disadvantages

#### 1. **Linear Decision Boundary**
- Cannot capture complex non-linear relationships
- Limited expressiveness for complex patterns
- May underfit complex datasets

#### 2. **Sensitive to Outliers in Target**
- Extreme values can influence coefficients significantly
- Complete separation issues with perfect predictors
- Requires careful data preprocessing

#### 3. **Feature Engineering Required**
- Manual creation of polynomial/interaction terms
- Need domain knowledge for effective features
- Scaling and normalization often necessary

#### 4. **Sample Size Requirements**
- Needs sufficient data for stable estimates
- Poor performance with very small datasets
- Class imbalance can be problematic

#### 5. **Multicollinearity Issues**
- Unstable coefficients with correlated features
- Difficult interpretation with high correlation
- Requires feature selection or regularization

#### 6. **Assumption Dependencies**
- Linear relationship assumption in log-odds space
- Independence assumption can be violated
- Convergence issues with problematic data

## Common Interview Questions

### Theoretical Questions

1. **Q: Explain the difference between linear and logistic regression.**

   **A:** 
   - **Linear Regression**: Predicts continuous values, uses identity link function, minimizes MSE
   - **Logistic Regression**: Predicts probabilities for classification, uses logit link function, maximizes likelihood

2. **Q: Why can't we use linear regression for classification?**

   **A:** 
   - Linear regression can output values outside [0,1]
   - No inherent probability interpretation
   - Sensitive to outliers affecting decision boundary
   - Assumes constant variance (homoscedasticity)

3. **Q: What is the sigmoid function and why is it used?**

   **A:** 
   - $\sigma(z) = \frac{1}{1+e^{-z}}$ maps real numbers to (0,1)
   - Smooth and differentiable everywhere
   - Monotonic and S-shaped
   - Natural interpretation as probability

4. **Q: How do you interpret logistic regression coefficients?**

   **A:** 
   - Coefficient $\beta_j$ represents change in log-odds per unit change in $x_j$
   - $e^{\beta_j}$ gives the odds ratio
   - Positive $\beta_j$: increases probability of positive class
   - Negative $\beta_j$: decreases probability of positive class

5. **Q: What is the difference between odds and probability?**

   **A:** 
   - **Probability**: $P = \frac{\text{successes}}{\text{total}}$, range [0,1]
   - **Odds**: $\frac{P}{1-P} = \frac{\text{successes}}{\text{failures}}$, range [0,∞]
   - **Odds Ratio**: Compares odds between groups

### Technical Questions

6. **Q: Why use maximum likelihood instead of least squares?**

   **A:** 
   - MLE is more appropriate for binary outcomes
   - Provides better statistical properties
   - Naturally handles the probabilistic nature
   - Least squares can give invalid probabilities

7. **Q: How do you handle imbalanced datasets in logistic regression?**

   **A:** 
   - **Resampling**: SMOTE, undersampling, oversampling
   - **Class weights**: Inverse proportion weighting
   - **Threshold tuning**: Optimize for F1 or other metrics
   - **Cost-sensitive learning**: Different penalties for each class

8. **Q: What is complete separation and how do you handle it?**

   **A:** 
   - Perfect linear separation of classes
   - Causes infinite coefficient estimates
   - **Solutions**: Regularization, remove separating features, collect more data

9. **Q: Compare different regularization techniques for logistic regression.**

   **A:** 
   - **L1 (Lasso)**: Sparse solutions, automatic feature selection
   - **L2 (Ridge)**: Shrinks coefficients, handles multicollinearity
   - **Elastic Net**: Combines L1 and L2 benefits

### Coding Questions

10. **Q: Implement logistic regression from scratch**
11. **Q: How would you tune the decision threshold?**
12. **Q: Implement cross-validation for logistic regression**
13. **Q: How do you handle categorical features?**

### Performance Questions

14. **Q: When would you choose logistic regression over other classifiers?**

    **A:** 
    - Need probabilistic outputs
    - Interpretability is crucial
    - Linear decision boundary is sufficient
    - Fast training/prediction required
    - Baseline model for comparison

15. **Q: How do you evaluate logistic regression performance?**

    **A:** 
    - **Balanced data**: Accuracy, F1-score
    - **Imbalanced data**: Precision, Recall, AUC-PR
    - **Probabilistic**: Log-loss, Brier score, AUC-ROC
    - **Statistical**: Likelihood ratio test, pseudo R²

## Practical Considerations

### Data Preprocessing

#### 1. **Feature Scaling**
- **Standardization**: $z = \frac{x - \mu}{\sigma}$
- **Normalization**: $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$
- **Impact**: Helps convergence and coefficient interpretation

#### 2. **Handling Categorical Variables**
- **One-hot encoding**: Create binary dummy variables
- **Ordinal encoding**: For ordered categories
- **Target encoding**: Mean target value per category
- **Reference category**: Choose baseline for interpretation

#### 3. **Feature Engineering**
- **Polynomial features**: Capture non-linear relationships
- **Interaction terms**: Model feature combinations
- **Binning**: Convert continuous to categorical
- **Domain-specific transformations**: Log, square root, etc.

#### 4. **Missing Value Treatment**
- **Imputation**: Mean, median, mode, or model-based
- **Indicator variables**: Flag missing values
- **Domain knowledge**: Understand missingness patterns

### Model Selection and Tuning

#### 1. **Regularization Parameter Selection**
- **Cross-validation**: K-fold CV for λ selection
- **Grid search**: Systematic parameter exploration
- **Random search**: More efficient for large spaces
- **Bayesian optimization**: Advanced hyperparameter tuning

#### 2. **Feature Selection**
- **Univariate**: Chi-square, mutual information
- **Recursive**: Recursive Feature Elimination (RFE)
- **Regularization-based**: L1 penalty for sparsity
- **Domain knowledge**: Subject matter expertise

#### 3. **Threshold Optimization**
- **ROC analysis**: Find optimal threshold from ROC curve
- **Precision-Recall**: Optimize for specific metric
- **Business constraints**: Cost considerations
- **Cross-validation**: Avoid overfitting to threshold

### Diagnostics and Validation

#### 1. **Model Assumptions**
- **Linearity**: Box-Tidwell test, residual plots
- **Independence**: Durbin-Watson, domain knowledge
- **Multicollinearity**: VIF, correlation analysis
- **Sample size**: Rules of thumb, power analysis

#### 2. **Goodness of Fit**
- **Hosmer-Lemeshow test**: Calibration assessment
- **Deviance residuals**: Check for patterns
- **Influential observations**: Cook's distance
- **Calibration plots**: Predicted vs. observed probabilities

#### 3. **Cross-Validation Strategies**
- **Stratified K-fold**: Maintain class proportions
- **Time series split**: For temporal data
- **Group K-fold**: For clustered data
- **Leave-one-out**: For very small datasets

### Deployment Considerations

#### 1. **Model Monitoring**
- **Performance metrics**: Track accuracy, AUC over time
- **Data drift**: Monitor feature distributions
- **Concept drift**: Track relationship changes
- **Prediction confidence**: Monitor probability distributions

#### 2. **Interpretability**
- **Coefficient analysis**: Feature importance
- **Odds ratios**: Business-friendly interpretation
- **Partial dependence**: Feature effect visualization
- **SHAP values**: Individual prediction explanations

#### 3. **Scalability**
- **Online learning**: Stochastic gradient descent
- **Batch prediction**: Efficient scoring
- **Feature store**: Consistent feature engineering
- **Model versioning**: Track changes and rollbacks

## Code Examples

### Python Implementation from Scratch

**Implementation Available**: [`src/ml-algos/02_logistic_regression/logistic_regression_from_scratch.py`](../../src/ml-algos/02_logistic_regression/logistic_regression_from_scratch.py)

This comprehensive implementation includes:
- **Binary logistic regression** with gradient descent optimization
- **Newton-Raphson method** for faster convergence
- **Regularized versions** (L1, L2, Elastic Net)
- **Comprehensive evaluation metrics** and comparison frameworks
- **Cross-validation implementation** with multiple scoring options
- **Feature engineering utilities** and preprocessing tools

Key features:
```python
from src.ml_algos.logistic_regression.logistic_regression_from_scratch import LogisticRegressionScratch

# Initialize with different optimizers
model_gd = LogisticRegressionScratch(optimizer='gradient_descent')
model_nr = LogisticRegressionScratch(optimizer='newton_raphson')

# Train and compare
model_gd.fit(X_train, y_train)
results = model_gd.compare_optimizers(X_test, y_test)
```

### Regularized Logistic Regression

**Implementation Available**: [`src/ml-algos/02_logistic_regression/regularized_logistic_regression.py`](../../src/ml-algos/02_logistic_regression/regularized_logistic_regression.py)

This module provides:
- **L1 regularization (Lasso)** with coordinate descent for feature selection
- **L2 regularization (Ridge)** for handling multicollinearity  
- **Elastic Net** combining L1 and L2 penalties
- **Regularization path analysis** for optimal hyperparameter selection
- **Cross-validation framework** for automated tuning

Usage example:
```python
from src.ml_algos.logistic_regression.regularized_logistic_regression import RegularizedLogisticRegression

# L1 regularization with feature selection
model_l1 = RegularizedLogisticRegression(penalty='l1', alpha=0.01)
model_l1.fit(X_train, y_train)

# Analyze regularization path
path_analyzer = RegularizationPathAnalyzer()
best_alpha = path_analyzer.find_optimal_alpha(X_train, y_train)
```

### Advanced Topics

**Implementation Available**: [`src/ml-algos/02_logistic_regression/advanced_logistic_regression.py`](../../src/ml-algos/02_logistic_regression/advanced_logistic_regression.py)

Advanced implementations include:
- **Multinomial logistic regression** for multiclass problems using softmax
- **Ordinal logistic regression** for ordered categorical outcomes
- **Class imbalance handling** with SMOTE, class weights, and threshold tuning
- **Online learning algorithms** for streaming data scenarios
- **Polynomial feature engineering** for capturing non-linear relationships

Key classes:
```python
from src.ml_algos.logistic_regression.advanced_logistic_regression import (
    MultinomialLogisticRegression,
    OrdinalLogisticRegression, 
    ImbalancedLogisticRegression
)

# Multiclass classification
multinomial_model = MultinomialLogisticRegression()
multinomial_model.fit(X_train, y_train_multiclass)

# Handle imbalanced data
imbalanced_model = ImbalancedLogisticRegression(strategy='smote')
imbalanced_model.fit(X_train_imbalanced, y_train_imbalanced)
```

### Evaluation and Diagnostics

**Implementation Available**: [`src/ml-algos/02_logistic_regression/evaluation_suite.py`](../../src/ml-algos/02_logistic_regression/evaluation_suite.py)

Comprehensive evaluation framework featuring:
- **ROC and Precision-Recall curves** with detailed analysis
- **Calibration plots and reliability diagrams** for probability assessment
- **Cross-validation with multiple metrics** and statistical significance testing
- **Bootstrap resampling** for confidence intervals and uncertainty quantification
- **Model comparison frameworks** with comprehensive dashboards

Key components:
```python
from src.ml_algos.logistic_regression.evaluation_suite import (
    LogisticRegressionEvaluator,
    CrossValidationEvaluator,
    BootstrapEvaluator
)

# Comprehensive evaluation
evaluator = LogisticRegressionEvaluator(model)
results = evaluator.evaluate_model(X_test, y_test)
evaluator.plot_evaluation_dashboard()

# Cross-validation analysis
cv_evaluator = CrossValidationEvaluator(LogisticRegression, cv_folds=5)
cv_results = cv_evaluator.cross_validate_model(X, y)
```

### Visualization Tools

**Implementation Available**: [`src/ml-algos/02_logistic_regression/visualization_suite.py`](../../src/ml-algos/02_logistic_regression/visualization_suite.py)

Comprehensive visualization toolkit including:
- **Decision boundary plots** for 2D and dimensionally-reduced data
- **Coefficient importance analysis** with odds ratios and statistical significance
- **Probability distribution analysis** by class with calibration assessment
- **Learning curves** for bias/variance diagnosis and convergence analysis
- **Residual analysis plots** for model diagnostic validation
- **Feature interaction visualizations** and partial dependence plots

Usage example:
```python
from src.ml_algos.logistic_regression.visualization_suite import LogisticRegressionVisualizer

# Create visualizer
visualizer = LogisticRegressionVisualizer(model, feature_names)

# Generate comprehensive dashboard
figures = create_comprehensive_visualization_dashboard(
    model, X_train, y_train, X_test, y_test, feature_names
)

# Individual plot types
visualizer.plot_decision_boundary_2d(X, y)
visualizer.plot_coefficient_importance()
visualizer.plot_learning_curves(X, y)
```

[Back to ML Algorithms](index.md) | [Back to Home](../index.md)