import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
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

    # Filter data to include records up to August 2024
    df = df[df['Sending Date'] <= '2024-08-31']

    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Separate Outbound and Inbound Movements
    outbound_movements = df[df['Type Of Movement'] == 'Outbound']
    inbound_movements = df[df['Type Of Movement'] == 'Inbound']

    # Grouping outbound and inbound movements by 'Sending Date'
    outbound_counts = outbound_movements.groupby(
        outbound_movements['Sending Date'].dt.to_period('M')).size().reset_index(name='Count')
    inbound_counts = inbound_movements.groupby(inbound_movements['Sending Date'].dt.to_period('M')).size().reset_index(
        name='Count')

    outbound_counts['Sending Date'] = outbound_counts['Sending Date'].dt.to_timestamp()
    inbound_counts['Sending Date'] = inbound_counts['Sending Date'].dt.to_timestamp()

    # Forecasting the next 4 months using a simple moving average for outbound
    last_months_average_outbound = outbound_counts['Count'].tail(4).mean()
    future_dates_outbound = pd.date_range(start=outbound_counts['Sending Date'].max() + pd.offsets.MonthEnd(1),
                                          periods=4, freq='M')
    future_predictions_outbound = pd.DataFrame(
        {'Sending Date': future_dates_outbound, 'Predicted Count': last_months_average_outbound})

    # Forecasting the next 4 months using a simple moving average for inbound
    last_months_average_inbound = inbound_counts['Count'].tail(4).mean()
    future_dates_inbound = pd.date_range(start=inbound_counts['Sending Date'].max() + pd.offsets.MonthEnd(1), periods=4,
                                         freq='M')
    future_predictions_inbound = pd.DataFrame(
        {'Sending Date': future_dates_inbound, 'Predicted Count': last_months_average_inbound})

    # Concatenate historical and future data for outbound and inbound plotting
    combined_data_outbound = pd.concat([outbound_counts.rename(columns={'Count': 'Value'}),
                                        future_predictions_outbound.rename(columns={'Predicted Count': 'Value'})])

    combined_data_inbound = pd.concat([inbound_counts.rename(columns={'Count': 'Value'}),
                                       future_predictions_inbound.rename(columns={'Predicted Count': 'Value'})])

    # Plotting both historical and predicted data for Outbound and Inbound
    plt.figure(figsize=(12, 6))
    plt.plot(combined_data_outbound['Sending Date'], combined_data_outbound['Value'], marker='o', color='blue',
             label='Outbound Data')
    plt.plot(combined_data_inbound['Sending Date'], combined_data_inbound['Value'], marker='o', color='green',
             label='Inbound Data')

    # Forecast lines
    forecast_start_outbound = future_predictions_outbound['Sending Date'].iloc[0]
    forecast_start_inbound = future_predictions_inbound['Sending Date'].iloc[0]

    plt.axvline(x=forecast_start_outbound, color='blue', linestyle='--', label='Outbound Forecast Start')
    plt.axvline(x=forecast_start_inbound, color='green', linestyle='--', label='Inbound Forecast Start')

    plt.plot(future_predictions_outbound['Sending Date'], future_predictions_outbound['Predicted Count'],
             linestyle='--', color='blue', alpha=0.5, label='Outbound Predicted Count')
    plt.plot(future_predictions_inbound['Sending Date'], future_predictions_inbound['Predicted Count'], linestyle='--',
             color='green', alpha=0.5, label='Inbound Predicted Count')

    plt.title('Outbound and Inbound Movements Forecast for Next 4 Months (Starting from September 2024)')
    plt.xlabel('Date')
    plt.ylabel('Count of Movements')
    plt.xticks(rotation=45)
    plt.xlim(pd.Timestamp('2024-01-01'), future_predictions_outbound['Sending Date'].max())
    plt.tight_layout()
    plt.legend()
    plt.savefig('movements_forecast.png')
    plt.show()

    # Convert 'Qty's cases' to numeric and drop NaN values for outbound
    outbound_movements['Qty\'s cases'] = pd.to_numeric(outbound_movements['Qty\'s cases'], errors='coerce')
    outbound_movements = outbound_movements.dropna(subset=['Qty\'s cases'])

    # Plotting the distribution of quantities for outbound movements
    if 'Qty\'s cases' in outbound_movements.columns and not outbound_movements['Qty\'s cases'].empty:
        plt.figure(figsize=(10, 6))
        outbound_movements['Qty\'s cases'].plot(kind='hist', bins=30, color='lightcoral', edgecolor='black')
        plt.title('Distribution of Quantities for Outbound Movements (Up to August 2024)')
        plt.xlabel('Quantity of Cases')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig('quantity_distribution_histogram.png')
        plt.show()
    else:
        print("Column 'Qty's cases' not found or contains no data in outbound movements.")

    # Client Movement Analysis
    movement_counts = df.groupby(['Clients', 'Type Of Movement']).size().unstack(fill_value=0)
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
    plt.title(f'Top {top_n} Clients: Inbound and Outbound Movements (Up to August 2024)')
    plt.xlabel('Clients')
    plt.ylabel('Number of Movements')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Type Of Movement')
    plt.tight_layout()
    plt.savefig('top_clients_movements_bar_chart.png')
    plt.show()

    # Pie Chart for Percentage of Total Movements for Top N Clients
    plt.figure(figsize=(10, 6))
    total_movements = filtered_movement_counts.sum(axis=1)
    plt.pie(total_movements, labels=total_movements.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'Percentage of Total Movements for Top {top_n} Clients (Up to August 2024)')
    plt.tight_layout()
    plt.savefig('client_movement_distribution_pie_chart.png')
    plt.show()

    # Pie Chart for Total Inbound and Outbound
    plt.figure(figsize=(10, 6))
    plt.pie([inbound_counts, outbound_counts], labels=['Total Inbound', 'Total Outbound'], autopct='%1.1f%%',
            startangle=90)
    plt.title('Total Inbound vs Outbound Movements (Top Clients, Up to August 2024)')
    plt.tight_layout()
    plt.savefig('inbound_vs_outbound_pie_chart.png')
    plt.show()

    # Line Graph for Inbound and Outbound Over Time (if dates were available)
    plt.figure(figsize=(10, 6))
    dates = pd.date_range(start='2024-01-01', periods=len(filtered_movement_counts), freq='D')
    movement_totals = filtered_movement_counts.sum(axis=1)
    plt.plot(dates, movement_totals, marker='o')
    plt.title('Total Movements Over Time (Example for Top Clients)')
    plt.xlabel('Date')
    plt.ylabel('Total Movements')
    plt.tight_layout()
    plt.savefig('total_movements_over_time.png')
    plt.show()