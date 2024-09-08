import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv('2024 invoices till July.csv')

# Normalize column names by stripping whitespace
df.columns = df.columns.str.strip()

# Check if 'Invoice Date' is in the DataFrame
if 'Invoice Date' not in df.columns:
    print("'Invoice Date' column not found. Available columns are:")
    print(df.columns)
else:
    # Parse 'Invoice Date'
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Convert 'Quantity' to numeric and drop NaN values
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df = df.dropna(subset=['Quantity'])

    # Monthly Breakdown by Item
    monthly_item_data = df.groupby(['Item Name', pd.Grouper(key='Invoice Date', freq='M')])['Quantity'].sum().unstack(
        fill_value=0)

    # Create a heatmap for monthly breakdown by item
    plt.figure(figsize=(12, 8))
    sns.heatmap(monthly_item_data, cmap='Blues', annot=True, fmt='g')
    plt.title('Monthly Quantity Breakdown by Item')
    plt.xlabel('Month and Day')
    plt.ylabel('Item Name')

    # Format x-ticks to show month and day
    plt.xticks(ticks=range(len(monthly_item_data.columns)),
               labels=[date.strftime('%b %d') for date in monthly_item_data.columns],
               rotation=45)

    plt.tight_layout()
    plt.show()

    # Weekly Breakdown by Item
    weekly_item_data = df.groupby(['Item Name', pd.Grouper(key='Invoice Date', freq='W')])['Quantity'].sum().unstack(
        fill_value=0)

    # Create a heatmap for weekly breakdown by item
    plt.figure(figsize=(12, 8))
    sns.heatmap(weekly_item_data, cmap='Blues', annot=True, fmt='g')
    plt.title('Weekly Quantity Breakdown by Item')
    plt.xlabel('Week')
    plt.ylabel('Item Name')

    # Format x-ticks for weeks
    plt.xticks(ticks=range(len(weekly_item_data.columns)),
               labels=[date.strftime('%b %d') for date in weekly_item_data.columns],
               rotation=45)

    plt.tight_layout()
    plt.show()

    # Grouping by 'Invoice Date' and 'Item Name' for forecasting
    item_monthly_counts = df.groupby(['Invoice Date', 'Item Name']).agg({'Quantity': 'sum'}).reset_index()

    # Summarize monthly counts for each item
    monthly_counts = item_monthly_counts.groupby(
        ['Item Name', item_monthly_counts['Invoice Date'].dt.to_period('M')]).agg({'Quantity': 'sum'}).reset_index()

    # Forecasting for each item
    predictions = {}
    for item in monthly_counts['Item Name'].unique():
        item_data = monthly_counts[monthly_counts['Item Name'] == item]
        if not item_data.empty:
            item_data.loc[:, 'Invoice Date'] = item_data['Invoice Date'].dt.to_timestamp()

            # Prepare for forecasting
            item_monthly = item_data.set_index('Invoice Date').resample('M').sum().reset_index()
            last_months_average = item_monthly['Quantity'].tail(4).mean()
            future_dates = pd.date_range(start=item_monthly['Invoice Date'].max() + pd.offsets.MonthEnd(1), periods=4,
                                         freq='M')
            future_predictions = pd.DataFrame({'Invoice Date': future_dates, 'Predicted Quantity': last_months_average})

            predictions[item] = pd.concat([item_monthly, future_predictions])

    # Plotting predictions for each item
    for item, pred_data in predictions.items():
        plt.figure(figsize=(12, 6))

        # Historical data
        plt.plot(pred_data['Invoice Date'], pred_data['Quantity'], marker='o', label='Historical Data', color='orange',
                 linestyle='-')

        # Predicted data
        plt.plot(pred_data['Invoice Date'], pred_data['Predicted Quantity'], linestyle='--', marker='o',
                 label='Predicted Quantity', color='blue')

        # Prepare combined data for connecting lines
        historical_length = len(pred_data['Quantity'])
        future_length = len(future_dates)

        combined_dates = pd.concat([pred_data['Invoice Date'], pd.Series(future_dates)])
        combined_data = pd.concat(
            [pred_data['Quantity'], pd.Series([pred_data['Predicted Quantity'].iloc[0]] * future_length)])

        # Connect the lines
        plt.plot(combined_dates, combined_data, linestyle='-', color='blue', alpha=0.5)

        plt.title(f'Forecast for {item}')
        plt.xlabel('Date')
        plt.ylabel('Quantity Sold')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Bar chart for predicted quantities
    predicted_totals = {}
    for item, pred_data in predictions.items():
        predicted_totals[item] = pred_data['Predicted Quantity'].sum()

    # Create a bar chart for predicted quantities
    plt.figure(figsize=(12, 6))
    plt.bar(predicted_totals.keys(), predicted_totals.values(), color='skyblue')
    plt.title('Total Predicted Quantities by Item')
    plt.xlabel('Item Name')
    plt.ylabel('Total Predicted Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # General distribution of quantities for all items
    if 'Quantity' in df.columns and not df['Quantity'].empty:
        plt.figure(figsize=(10, 6))
        df['Quantity'].plot(kind='hist', bins=30, color='lightcoral', edgecolor='black')
        plt.title('Distribution of Quantities for Invoices')
        plt.xlabel('Quantity of Cases')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()
    else:
        print("Column 'Quantity' not found or contains no data in the invoices.")