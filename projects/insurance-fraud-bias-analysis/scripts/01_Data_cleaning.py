import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  

# Load data
data = pd.read_csv("projects/insurance-fraud-bias-analysis/data/raw/fraud_data.csv")

print(f"Dataset shape: {data.shape}")
print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")

# Show first few rows
data.head(4).T

# List all column names and data types
data.info()

# Mising data 
data.isna().sum()

#data summary
data.describe().T.round(2)

# check for variables that can be ommited

print("Unique value counts:")
for col in ['Color', 'Bodytype', 'Seat_num', 'Door_num', 'Gearbox', 'Fuel_type']:
    print(f"\n{col}: {data[col].nunique()} unique values")
    print(data[col].value_counts().head())
    
columns_to_drop = [
    'Genmodel_ID',      
    'Color',           
    'Seat_num',        
    'Door_num',       
    'Adv_day'          
]

# data cleaning

# 1.Price: remove negative and extreme values
print("1. Price:")
print(f"Before: min={data['Price'].min():.2f}, max={data['Price'].max():.2f}")
data = data[(data['Price'] > 0) & (data['Price'] < 1000000)]  
print(f"After: min={data['Price'].min():.2f},max={data['Price'].max():.2f}")
print(f"Rows removed: {268255 - len(data)}")

# 2.Runned_Miles: remove negative and unrealistic values
print("2.Runned_Miles:")
print(f"Before: min={data['Runned_Miles'].min()}, max={data['Runned_Miles'].max()}")
data = data[(data['Runned_Miles'] >= 0) & (data['Runned_Miles'] <= 500000)] 
print(f"After: min={data['Runned_Miles'].min()}, max={data['Runned_Miles'].max()}")
print(f"Rows removed: {268255 - len(data)}")

# 3.repair_cost: remove negative and extreme values
print("3. Cleaning repair_cost:")
print(f"Before: min={data['repair_cost'].min():.2f}, max={data['repair_cost'].max():.2f}")
data = data[(data['repair_cost'] >= 0) & (data['repair_cost'] <= 50000)] 
print(f"After: min={data['repair_cost'].min():.2f}, max={data['repair_cost'].max():.2f}")
print(f"Rows removed: {268255 - len(data)}")

# 4.repair_hours: remove negative and extreme values
print("4.Cleaning repair_hours:")
print(f"Before: min={data['repair_hours'].min():.2f}, max={data['repair_hours'].max():.2f}")
data = data[(data['repair_hours'] >= 0) & (data['repair_hours'] <= 500)]  
print(f"After: min={data['repair_hours'].min():.2f}, max={data['repair_hours'].max():.2f}")
print(f"Rows removed: {268255 - len(data)}")

# 5.Clean Reg_year: only reasonable registration years
print("5.Cleaning Reg_year:")
print(f"Before: min={data['Reg_year'].min():.0f}, max={data['Reg_year'].max():.0f}")
data = data[(data['Reg_year'] >= 1990) & (data['Reg_year'] <= 2021)] 
print(f"After: min={data['Reg_year'].min():.0f}, max={data['Reg_year'].max():.0f}")
print(f"Rows removed: {268255 - len(data)}")

# 6.Adv_month:only valid months
print("6.Cleaning Adv_month:")
print(f"Before: min={data['Adv_month'].min()}, max={data['Adv_month'].max()}")
data = data[(data['Adv_month'] >= 1) & (data['Adv_month'] <= 12)]  
print(f"After: min={data['Adv_month'].min()}, max={data['Adv_month'].max()}")
print(f"Rows removed: {268255 - len(data)}")

print(f"FINAL CLEANED DATASET: {len(data):,} rows ({len(data)/268255*100:.1f}% retained)")
print(f"Total rows removed: {268255 - len(data):,}")


# Check fraud distribution after cleaning
print("\nFraud distribution after cleaning:")
print(data['anomaly_present'].value_counts())
print(f"Fraud rate: {data['anomaly_present'].mean()*100:.1f}%")

# Save cleaned dataset
data.to_csv("projects/insurance-fraud-bias-analysis/data/cleaned/cleaned_data.csv", index=False)

