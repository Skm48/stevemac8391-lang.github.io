import pandas as pd

# Load cleaned data
data = pd.read_csv("projects/fraud-bias-analysis/data/cleaned/cleaned_data.csv")

print("Starting shape:", data.shape)

# new features 

# 2. Cost per repair hour
data['cost_per_hour'] = data['repair_cost'] / data['repair_hours']
# 3. Repair cost as percentage of vehicle price (KEY FRAUD INDICATOR)
data['price_cost_ratio'] = (data['repair_cost'] / data['Price']) * 100
# 4. Time between breakdown and repair (in days)
data['breakdown_date'] = pd.to_datetime(data['breakdown_date'])
data['repair_date'] = pd.to_datetime(data['repair_date'])
data['repair_lag_days'] = (data['repair_date'] - data['breakdown_date']).dt.days

# Display summary of new features
print("New Engineered Features:")
new_features = [ 'cost_per_hour', 'price_cost_ratio', 'repair_lag_days']
data[new_features].describe().round(2)

# Cleaning engineered features

# 2. Remove extreme cost_per_hour (>£500/hour seems unrealistic)
extreme_cph = (data['cost_per_hour'] > 1000).sum()
print(f"\n2. cost_per_hour: {extreme_cph} >£500/hour removed")
data = data[data['cost_per_hour'] <= 1000]
print(f"   Rows remaining: {len(data):,}")

# 3. Remove price_to_cost_ratio >100% (repair exceeds vehicle value)
extreme_ratio = (data['price_cost_ratio'] > 100).sum()
print(f"\n3. price_cost_ratio: {extreme_ratio} values >100% removed")
data = data[data['price_cost_ratio'] <= 100]
print(f"   Rows remaining: {len(data):,}")

# Display summary of new features cleaned
print("New Engineered Features:")
new_features = [ 'cost_per_hour', 'price_cost_ratio', 'repair_lag_days']
data[new_features].describe().round(2)

# Save final dataset
data.to_csv("projects/insurance-fraud-bias-analysis/data/cleaned/featured_data.csv", index=False)

print("✅ Feature engineering complete")
