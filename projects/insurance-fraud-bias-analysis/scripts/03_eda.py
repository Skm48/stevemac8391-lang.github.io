import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv("projects/insurance-fraud-bias-analysis/data/cleaned/featured_data.csv")

# -------------------------
# FRAUD DISTRIBUTION
# -------------------------

fraud_counts = data['anomaly_present'].value_counts()

plt.figure()
plt.bar(['Legitimate', 'Fraud'], fraud_counts)
plt.title("Fraud vs Legitimate Claims")
plt.ylabel("Count")

plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/fraud_distribution.png")
plt.close()

# -------------------------
# PRICE DISTRIBUTION
# -------------------------

plt.figure()
sns.histplot(data['Price'], bins=50)
plt.title("Vehicle Price Distribution")

plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/price_distribution.png")
plt.close()

# -------------------------
# PRICE-COST RATIO DISTRIBUTION
# -------------------------

plt.figure()
sns.histplot(data['price_cost_ratio'], bins=50)
plt.title("Price-Cost Ratio Distribution")

plt.savefig("projects/insurance-fraud-bias-analysis/outputs/figures/ratio_distribution.png")
plt.close()

print("✅ EDA complete")
