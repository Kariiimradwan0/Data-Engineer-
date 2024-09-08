import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('Master Tracker 2024 krk(Movement).csv')

# Clean up the data by dropping rows with all NaN values
data.dropna(how='all', inplace=True)

# Strip whitespace from column names
data.columns = data.columns.str.strip()

# Group by Clients and Type Of Movement and sum counts
movement_counts = data.groupby(['Clients', 'Type Of Movement']).size().unstack(fill_value=0)

# Combine duplicate clients by summing their inbound and outbound counts
movement_counts = movement_counts.groupby(movement_counts.index).sum()

# Get total movements and filter for top N clients (e.g., top 10)
top_n = 10
top_clients = movement_counts.sum(axis=1).nlargest(top_n).index
filtered_movement_counts = movement_counts.loc[top_clients]

# Separate inbound and outbound counts
inbound_counts = filtered_movement_counts['Inbound'].sum()
outbound_counts = filtered_movement_counts['Outbound'].sum()

# Bar Chart for Inbound and Outbound (Top N Clients)
plt.figure(figsize=(15, 8))
filtered_movement_counts.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title(f'Top {top_n} Clients: Inbound and Outbound Movements')
plt.xlabel('Clients')
plt.ylabel('Number of Movements')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Type Of Movement')
plt.tight_layout()
plt.show()

# Pie Chart for Percentage of Total Movements for Top N Clients
plt.figure(figsize=(10, 6))
total_movements = filtered_movement_counts.sum(axis=1)
plt.pie(total_movements, labels=total_movements.index, autopct='%1.1f%%', startangle=90)
plt.title(f'Percentage of Total Movements for Top {top_n} Clients')
plt.tight_layout()
plt.show()

# Pie Chart for Total Inbound and Outbound
plt.figure(figsize=(10, 6))
plt.pie([inbound_counts, outbound_counts], labels=['Total Inbound', 'Total Outbound'], autopct='%1.1f%%', startangle=90)
plt.title('Total Inbound vs Outbound Movements (Top Clients)')
plt.tight_layout()
plt.show()

# Line Graph for Inbound and Outbound Over Time (if dates were available)
# This part will depend on your date structure; adjust accordingly
plt.figure(figsize=(10, 6))
dates = pd.date_range(start='2024-01-01', periods=len(filtered_movement_counts), freq='D')
movement_totals = filtered_movement_counts.sum(axis=1)
plt.plot(dates, movement_totals, marker='o')
plt.title('Total Movements Over Time (Example for Top Clients)')
plt.xlabel('Date')
plt.ylabel('Total Movements')
plt.tight_layout()
plt.show()