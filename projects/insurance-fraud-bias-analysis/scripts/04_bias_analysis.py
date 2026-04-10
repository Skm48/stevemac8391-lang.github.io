import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Load data
data = pd.read_csv("projects/insurance-fraud-bias-analysis/data/cleaned/featured_data.csv")

# -------------------------
# CREATE PRICE SEGMENTS
# -------------------------

bins = [0, 5000, 15000, 30000, 1000000]
labels = ['Budget', 'Mid-range', 'Premium', 'Luxury']

data['price_segment'] = pd.cut(data['Price'], bins=bins, labels=labels)

# -------------------------
# APPLY FRAUD RULE
# -------------------------

# Flag if price_cost_ratio > 20%
data['flagged'] = (data['price_cost_ratio'] > 20).astype(int)

# -------------------------
# CALCULATE RATES
# -------------------------

summary = data.groupby('price_segment').agg(
    actual_fraud_rate=('anomaly_present', 'mean'),
    flagged_rate=('flagged', 'mean')
)

# Convert to %
summary = summary * 100

print(summary)

# -------------------------
# PLOT (KEY GRAPH 🔥)
# -------------------------

segments = summary.index
actual = summary['actual_fraud_rate']
flagged = summary['flagged_rate']

x = range(len(segments))

plt.figure(figsize=(8,5))

plt.bar(x, actual, width=0.4, label='Actual Fraud Rate')
plt.bar([i + 0.4 for i in x], flagged, width=0.4, label='Flagged Rate (>20%)')

plt.xticks([i + 0.2 for i in x], segments)
plt.ylabel("Rate (%)")
plt.title("Actual vs Flagged Fraud Rate by Price Segment")
plt.legend()
plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/bias_comparison.png")
plt.close()


# Kruskal-Wallis Test
groups = [group['price_cost_ratio'].values
for name, group in data.groupby('price_segment', observed=False)]
stat, p_value = stats.kruskal(*groups)
print("Kruskal-Wallis H-test:")
print(f"H-statistic: {stat:.4f}")
print(f"p-value: {p_value:.4e}")
print(f"Significant: {'Yes' if p_value < 0.05 else 'No'} (a = 0.05)")

# Chi-Square Test - " Do fraud flagging rates differ by price segment?"
# uniform 20% threshold
data['flagged'] = (data['price_cost_ratio'] > 20).astype(int)
# comparison table
comparison = data.groupby('price_segment', observed=False).agg(
Total_Claims=('anomaly_present', 'count'),
Actual_Fraud_Rate=('anomaly_present', 'mean'),
Flagged_Rate=('flagged', 'mean')
).round(4)
comparison['Actual_Fraud_Rate'] = (comparison['Actual_Fraud_Rate'] * 100).round(2)
comparison['Flagged_Rate'] = (comparison['Flagged_Rate'] * 100).round(2)
print("Comparison: Actual Fraud Rate vs Flagged Rate by Segment")
print(comparison)
# Chi-square test
chi_test = pd.crosstab(data['price_segment'], data['flagged'])
chi2, p_value, dof, expected = stats.chi2_contingency(chi_test)
print(f"\nChi-Square Test:")
print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.2e}")
print(f"Degrees of freedom: {dof}")
print(f"Significant: {'Yes' if p_value < 0.05 else 'No'} (a = 0.05)")

print("✅ Bias analysis complete")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
segments = ['Budget\n(£0-5k)', 'Mid-range\n(£5k-15k)',
'Premium\n(£15k-30k)', 'Luxury\n(£30k+)']
actual_fraud = [15.95, 18.82, 20.04, 20.53]
flagged_rate = [7.53, 2.66, 1.94, 1.30]
# Plot 1: Side by side comparison
x = np.arange(len(segments))
width = 0.35
bars1 = axes[0].bar(x - width/2, actual_fraud, width, label='Actual Fraud Rate',
color='steelblue', alpha=0.7, edgecolor='black')
bars2 = axes[0].bar(x + width/2, flagged_rate, width, label='Flagged Rate (>20%)',
color='darkred', alpha=0.7, edgecolor='black')
axes[0].set_xlabel('Price Segment', fontweight='bold')
axes[0].set_ylabel('Rate (%)', fontweight='bold')
axes[0].set_title('Actual Fraud Rate vs Flagged Rate by Segment',
fontsize=13, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(segments)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)
# Plot 2: Ratio of flagged rate to actual fraud rate (over-flagging)
over_flag_ratio = [f/a * 100 for f, a in zip(flagged_rate, actual_fraud)]
colors = ['darkred' if r > 20 else 'green' for r in over_flag_ratio]
axes[1].bar(range(len(segments)), over_flag_ratio, color=colors,
alpha=0.7, edgecolor='black')
axes[1].set_xticks(range(len(segments)))
axes[1].set_xticklabels(segments)
axes[1].set_ylabel('Flagged as % of Actual Fraud (%)', fontweight='bold')
axes[1].set_title('Over-Flagging Ratio by Segment',
fontsize=13, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)
plt.tight_layout()

plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/bias_comparison_Final.png")
plt.close()
