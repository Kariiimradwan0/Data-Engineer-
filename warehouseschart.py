import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file without parsing dates first
df = pd.read_csv('Master Tracker 2024 krk(Movement).csv')

# Normalize column names by stripping whitespace
df.columns = df.columns.str.strip()

# Check if 'Sending Date' is in the DataFrame
if 'Sending Date' not in df.columns:
    print("'Sending Date' column not found. Available columns are:")
    print(df.columns)
else:
    # Parse 'Sending Date'
    df['Sending Date'] = pd.to_datetime(df['Sending Date'], errors='coerce')

    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Filter records for outbound and inbound movements
    outbound_movements = df[df['Type Of Movement'] == 'Outbound']
    inbound_movements = df[df['Type Of Movement'] == 'Inbound']

    # Count of orders by Warehouse (Top N)
    warehouse_counts = df['Warehouse'].value_counts()
    top_n_warehouses = warehouse_counts.nlargest(10)

    # Plotting the count of orders by Warehouse (Top N)
    plt.figure(figsize=(10, 6))
    top_n_warehouses.plot(kind='bar', color='lightgreen')
    plt.title('Top 10 Warehouses by Order Count')
    plt.xlabel('Warehouse')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Pie Chart for orders by Warehouse (Top N)
    plt.figure(figsize=(8, 8))
    top_n_warehouses.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribution of Orders by Top 10 Warehouses')
    plt.ylabel('')  # Hide the y-label
    plt.tight_layout()
    plt.show()

    # Plotting the count of orders by status if available
    if 'SR Statues' in df.columns:
        status_counts = df['SR Statues'].value_counts()
        plt.figure(figsize=(10, 6))
        status_counts.plot(kind='bar', color='skyblue')
        plt.title('Count of Orders by Status')
        plt.xlabel('Status')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Function to plot outbound movements
    def plot_outbound(outbound_movements):
        # Grouping outbound movements by 'Sending Date'
        outbound_counts = outbound_movements.groupby(outbound_movements['Sending Date'].dt.to_period('M')).size()
        outbound_counts = outbound_counts.reset_index(name='Count')
        outbound_counts['Sending Date'] = outbound_counts['Sending Date'].dt.to_timestamp()

        # Plot historical data
        plt.figure(figsize=(8, 4))
        plt.plot(outbound_counts['Sending Date'], outbound_counts['Count'], marker='o', color='orange', label='Historical Data')

        # Forecasting the next 4 months using a simple moving average
        last_months_average = outbound_counts['Count'].tail(4).mean()
        future_dates = pd.date_range(start=outbound_counts['Sending Date'].max() + pd.offsets.MonthEnd(1), periods=4, freq='M')

        # Create DataFrame for future predictions
        future_predictions = pd.DataFrame({'Sending Date': future_dates, 'Predicted Count': [last_months_average] * len(future_dates)})

        # Concatenate historical and future data for plotting
        combined_data = pd.concat([
            outbound_counts.rename(columns={'Count': 'Value'}),
            future_predictions.rename(columns={'Predicted Count': 'Value'})
        ])

        # Plotting both historical and predicted data
        plt.plot(combined_data['Sending Date'], combined_data['Value'], marker='o', color='blue', label='Combined Data')

        # Highlight the future predictions
        plt.plot(future_predictions['Sending Date'], future_predictions['Predicted Count'], linestyle='--', color='blue', alpha=0.5, label='Predicted Count')

        # Forecast start line
        plt.axvline(x=future_predictions['Sending Date'].min(), color='red', linestyle='--', label='Forecast Start')

        plt.title('Outbound Movements Forecast for Next 4 Months')
        plt.xlabel('Date')
        plt.ylabel('Count of Outbound Cases')
        plt.xticks(rotation=45)
        plt.xlim(pd.Timestamp('2024-01-01'), future_predictions['Sending Date'].max())
        plt.tight_layout()
        plt.legend()
        plt.show()

        # Convert 'Qty's cases' to numeric and drop NaN values
        outbound_movements['Qty\'s cases'] = pd.to_numeric(outbound_movements['Qty\'s cases'], errors='coerce')
        outbound_movements = outbound_movements.dropna(subset=['Qty\'s cases'])

        # Plotting the distribution of quantities for outbound movements
        if 'Qty\'s cases' in outbound_movements.columns and not outbound_movements['Qty\'s cases'].empty:
            plt.figure(figsize=(10, 6))
            outbound_movements['Qty\'s cases'].plot(kind='hist', bins=30, color='lightcoral', edgecolor='black')
            plt.title('Distribution of Quantities for Outbound Movements')
            plt.xlabel('Quantity of Cases')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.show()
        else:
            print("Column 'Qty's cases' not found or contains no data in outbound movements.")

    # Function to plot inbound movements
    def plot_inbound(inbound_movements):
        # Grouping inbound movements by 'Sending Date'
        inbound_counts = inbound_movements.groupby(inbound_movements['Sending Date'].dt.to_period('M')).size()
        inbound_counts = inbound_counts.reset_index(name='Count')
        inbound_counts['Sending Date'] = inbound_counts['Sending Date'].dt.to_timestamp()

        # Plot historical data
        plt.figure(figsize=(8, 4))
        plt.plot(inbound_counts['Sending Date'], inbound_counts['Count'], marker='o', color='green', label='Historical Data')

        # Forecasting the next 4 months using a simple moving average
        last_months_average = inbound_counts['Count'].tail(4).mean()
        future_dates = pd.date_range(start=inbound_counts['Sending Date'].max() + pd.offsets.MonthEnd(1), periods=4, freq='M')

        # Create DataFrame for future predictions
        future_predictions = pd.DataFrame({'Sending Date': future_dates, 'Predicted Count': [last_months_average] * len(future_dates)})

        # Concatenate historical and future data for plotting
        combined_data = pd.concat([
            inbound_counts.rename(columns={'Count': 'Value'}),
            future_predictions.rename(columns={'Predicted Count': 'Value'})
        ])

        # Plotting both historical and predicted data
        plt.plot(combined_data['Sending Date'], combined_data['Value'], marker='o', color='blue', label='Combined Data')

        # Highlight the future predictions
        plt.plot(future_predictions['Sending Date'], future_predictions['Predicted Count'], linestyle='--', color='blue', alpha=0.5, label='Predicted Count')

        # Forecast start line
        plt.axvline(x=future_predictions['Sending Date'].min(), color='red', linestyle='--', label='Forecast Start')

        plt.title('Inbound Movements Forecast for Next 4 Months')
        plt.xlabel('Date')
        plt.ylabel('Count of Inbound Cases')
        plt.xticks(rotation=45)
        plt.xlim(pd.Timestamp('2024-01-01'), future_predictions['Sending Date'].max())
        plt.tight_layout()
        plt.legend()
        plt.show()

        # Convert 'Qty's cases' to numeric and drop NaN values
        inbound_movements['Qty\'s cases'] = pd.to_numeric(inbound_movements['Qty\'s cases'], errors='coerce')
        inbound_movements = inbound_movements.dropna(subset=['Qty\'s cases'])

        # Plotting the distribution of quantities for inbound movements
        if 'Qty\'s cases' in inbound_movements.columns and not inbound_movements['Qty\'s cases'].empty:
            plt.figure(figsize=(10, 6))
            inbound_movements['Qty\'s cases'].plot(kind='hist', bins=30, color='lightblue', edgecolor='black')
            plt.title('Distribution of Quantities for Inbound Movements')
            plt.xlabel('Quantity of Cases')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.show()
        else:
            print("Column 'Qty's cases' not found or contains no data in inbound movements.")

    # Call plotting functions for outbound and inbound movements
    plot_outbound(outbound_movements)
    plot_inbound(inbound_movements)