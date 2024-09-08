import pandas as pd
import matplotlib.pyplot as plt

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

# Count of sent and received orders
sent_count = df[df['SR Statues '] == 'Sent'].shape[0]
received_count = df[df['SR Statues '] == 'Received'].shape[0]

print(f"\nTotal Sent Orders: {sent_count}")
print(f"Total Received Orders: {received_count}")

# Calculate the difference
difference = sent_count - received_count
print(f"Difference between Sent and Received Orders: {difference}")

# Plotting Sent vs. Received Orders
labels = ['Sent', 'Received']
counts = [sent_count, received_count]

plt.figure(figsize=(8, 5))
plt.bar(labels, counts, color=['skyblue', 'lightgreen'])
plt.title('Comparison of Sent vs. Received Orders')
plt.xlabel('Order Status')
plt.ylabel('Count')
plt.ylim(0, max(counts) + 10)  # Add some space above the bars
plt.tight_layout()
plt.show()

# Count of orders by status
status_counts = df['SR Statues '].value_counts()
print("\nCount of Orders by Status:")
print(status_counts)

# Count of orders by Warehouse
warehouse_counts = df['Warehouse'].value_counts()
print("\nCount of Orders by Warehouse:")
print(warehouse_counts)

# Plotting the count of orders by Warehouse
plt.figure(figsize=(10, 6))
warehouse_counts.plot(kind='bar', color='lightgreen')
plt.title('Count of Orders by Warehouse')
plt.xlabel('Warehouse')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()