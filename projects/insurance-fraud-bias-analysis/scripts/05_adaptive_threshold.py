import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("projects/insurance-fraud-bias-analysis/data/cleaned/featured_data.csv")

# -------------------------
# CREATE PRICE SEGMENTS
# -------------------------

bins = [0, 5000, 15000, 30000, 1000000]
labels = ['Budget', 'Mid-range', 'Premium', 'Luxury']

data['price_segment'] = pd.cut(data['Price'], bins=bins, labels=labels)

# -------------------------
# UNIFORM THRESHOLD (BASELINE)
# -------------------------

data['flagged_uniform'] = (data['price_cost_ratio'] > 20).astype(int)

# -------------------------
# ADAPTIVE THRESHOLDS
# -------------------------

thresholds = data.groupby('price_segment')['price_cost_ratio'].quantile(0.90)

print("\nAdaptive Thresholds:")
print(thresholds)

# Apply adaptive thresholds
data['flagged_adaptive'] = 0

for segment in thresholds.index:
    mask = data['price_segment'] == segment
    threshold = thresholds[segment]
    
    data.loc[mask, 'flagged_adaptive'] = (
        data.loc[mask, 'price_cost_ratio'] > threshold
    ).astype(int)

# -------------------------
# COMPARISON
# -------------------------

comparison = data.groupby('price_segment').agg(
    actual_fraud_rate=('anomaly_present', 'mean'),
    uniform_flagged=('flagged_uniform', 'mean'),
    adaptive_flagged=('flagged_adaptive', 'mean')
)

comparison = comparison * 100

print("\nComparison (Actual vs Uniform vs Adaptive):\n")
print(comparison.round(2))

from scipy import stats

# -------------------------
# CHI-SQUARE TEST (ADAPTIVE)
# -------------------------

contingency_adaptive = pd.crosstab(data['price_segment'], data['flagged_adaptive'])

chi2_a, p_value_a, dof_a, expected_a = stats.chi2_contingency(contingency_adaptive)

print("\nChi-Square Test (Adaptive Threshold):")
print(f"Chi-square: {chi2_a:.2f}")
print(f"p-value: {p_value_a:.4e}")


# -------------------------
# VISUALISATION
# -------------------------

segments = comparison.index
actual = comparison['actual_fraud_rate']
uniform = comparison['uniform_flagged']
adaptive = comparison['adaptive_flagged']

x = range(len(segments))

plt.figure(figsize=(10,6))

plt.bar(x, actual, width=0.25, label='Actual Fraud Rate')
plt.bar([i + 0.25 for i in x], uniform, width=0.25, label='Uniform (>20%)')
plt.bar([i + 0.5 for i in x], adaptive, width=0.25, label='Adaptive Threshold')

plt.xticks([i + 0.25 for i in x], segments)
plt.ylabel("Rate (%)")
plt.title("Fraud Rate vs Uniform vs Adaptive Flagging")
plt.legend()

plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/adaptive_comparison.png")
plt.close()

print("✅ Adaptive threshold analysis complete")
