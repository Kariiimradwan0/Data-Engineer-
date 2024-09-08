import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("Master Tracker 2024 krk(Movement).csv")

# Display the first few rows of the DataFrame
print("Data Preview:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Summary statistics of numerical columns
print("\nSummary Statistics:")
print(df.describe())

# Filter records for outbound movements
outbound_movements = df[df['Type Of Movement'] == 'Outbound']
print("\nOutbound Movements:")
print(outbound_movements)

# Count of orders by status
status_counts = df['SR Statues '].value_counts()
print("\nCount of Orders by Status:")
print(status_counts)

# Plotting the count of orders by status
plt.figure(figsize=(10, 6))
status_counts.plot(kind='bar', color='skyblue')
plt.title('Count of Orders by Status')
plt.xlabel('Status')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()