import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the data
df = pd.read_csv("Master Tracker 2024 krk(Movement).csv")

# Normalize column names by stripping whitespace
df.columns = df.columns.str.strip()

# Check for duplicate columns
if df.columns.duplicated().any():
    df.columns = pd.Series(df.columns).where(~df.columns.duplicated(), df.columns + '_dup')

# Convert date columns to datetime
df['Sending Date'] = pd.to_datetime(df['Sending Date'])
df['Receiving Date'] = pd.to_datetime(df['Receiving Date'])

# Convert quantities to numeric
df['Qty\'s cases'] = pd.to_numeric(df['Qty\'s cases'], errors='coerce')

# Group by Sending Date and sum the quantities
daily_orders = df.groupby('Sending Date')['Qty\'s cases'].sum().reset_index()

# Fit a linear regression model on the daily orders
daily_orders['date_num'] = (daily_orders['Sending Date'] - daily_orders['Sending Date'].min()).dt.days
X = daily_orders[['date_num']]
y = daily_orders['Qty\'s cases'].fillna(0)

model = LinearRegression()
model.fit(X, y)

# Prepare future dates for predictions
max_date_num = daily_orders['date_num'].max()
future_dates = pd.DataFrame({'date_num': np.arange(max_date_num + 1, max_date_num + 121)})

# Predict using the model
predictions = model.predict(future_dates)

# Output predictions
predicted_dates = pd.date_range(start=daily_orders['Sending Date'].max() + pd.Timedelta(days=1), periods=120)
predicted_orders = pd.DataFrame({'date': predicted_dates, 'predicted_cases': predictions})

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(daily_orders['Sending Date'], y, label='Historical Cases', marker='o', linestyle='-')
plt.plot(predicted_orders['date'], predicted_orders['predicted_cases'], label='Predicted Cases', marker='x', linestyle='--', color='orange')

# Set limits for clarity
plt.ylim(0, max(y.max(), predictions.max()) * 1.1)  # Set y-limits slightly above max value
plt.xlim(pd.Timestamp('2024-01-01'), predicted_orders['date'].max())  # Set x-limits to start from 2024

# Add grid, labels, and title
plt.xlabel('Date')
plt.ylabel('Quantity of Cases')
plt.title('Quantity of Cases Prediction for Next 4 Months')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()