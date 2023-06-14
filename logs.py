from flask import render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from models import logs
import warnings
warnings.simplefilter("ignore", UserWarning)

def eda():
    # Retrieve the data from the "logs" table
    query = logs.query.all()

    # Convert the query result into a Pandas DataFrame
    df = pd.DataFrame([(item.transid, item.itemname, item.itemquantity, item.itemcost, item.itemdate, item.transactionno, item.canteenslogs.name) for item in query],
                      columns=['transid', 'itemname', 'itemquantity', 'itemcost', 'itemdate', 'transactionno', 'canteen_name'])

    # Calculate sales data by canteen
    sales_data_canteen = df.groupby('canteen_name')['itemquantity'].sum().reset_index()

    # Sort the sales data by canteen in descending order
    sales_data_canteen = sales_data_canteen.sort_values(by='itemquantity', ascending=False)

    # Get the canteen with the highest sales
    top_canteen = sales_data_canteen.head(1)

    # Generate the plot - Canteen with Highest Sales
    plt.figure(figsize=(10, 6))
    plt.bar(sales_data_canteen['canteen_name'], sales_data_canteen['itemquantity'])
    plt.xlabel('Canteen')
    plt.ylabel('Sales Quantity')
    plt.title('Sales by Canteen')
    plt.xticks(rotation=45)
    plt.savefig('static/sales_by_canteen.png')
    plt.close()

    # Calculate sales data by item
    sales_data_item = df.groupby('itemname')['itemquantity'].sum().reset_index()

    # Generate the plot - Pie Chart of Total Quantities Sold by Item
    plt.figure(figsize=(10, 6))
    plt.pie(sales_data_item['itemquantity'], labels=sales_data_item['itemname'], autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Total Quantities Sold by Item')
    plt.savefig('static/quantities_sold_pie.png')
    plt.close()

    # Calculate other analysis metrics
    unique_items = df['itemname'].nunique()
    total_quantity = df['itemquantity'].sum()
    total_cost = df['itemcost'].sum()

    # Generate additional plots

    # Line Plot - Sales over Time
    sales_over_time = df.groupby(pd.to_datetime(df['itemdate'])).agg({'itemquantity': 'sum'}).reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(sales_over_time['itemdate'], sales_over_time['itemquantity'])
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.title('Sales over Time')
    plt.xticks(rotation=45)
    plt.savefig('static/sales_over_time.png')
    plt.close()

    # Scatter Plot - Item Quantity vs Item Cost
    plt.figure(figsize=(10, 6))
    plt.scatter(df['itemquantity'], df['itemcost'])
    plt.xlabel('Item Quantity')
    plt.ylabel('Item Cost')
    plt.title('Item Quantity vs Item Cost')
    plt.savefig('static/quantity_cost_scatter.png')
    plt.close()

    # Histogram - Distribution of Sales
    plt.figure(figsize=(10, 6))
    plt.hist(df['itemquantity'], bins=10)
    plt.xlabel('Sales Quantity')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sales')
    plt.savefig('static/sales_distribution_hist.png')
    plt.close()

    # Bar Plot - Top 10 Selling Items
    top_items = sales_data_item.nlargest(10, 'itemquantity')
    plt.figure(figsize=(10, 6))
    plt.bar(top_items['itemname'], top_items['itemquantity'])
    plt.xlabel('Item Name')
    plt.ylabel('Sales Quantity')
    plt.title('Top 10 Selling Items')
    plt.xticks(rotation=45)
    plt.savefig('static/top_10_selling_items.png')
    plt.close()

    # Plot - Distribution of Sales by Item
    plt.figure(figsize=(10, 6))
    plt.bar(sales_data_item['itemname'], sales_data_item['itemquantity'])
    plt.xlabel('Item Name')
    plt.ylabel('Sales Quantity')
    plt.title('Distribution of Sales by Item')
    plt.xticks(rotation=45)
    plt.savefig('static/sales_distribution_by_item.png')
    plt.close()

    # Pass the EDA results and sales data to the HTML template
    eda_results = {
        'unique_items': unique_items,
        'total_quantity': total_quantity,
        'total_cost': total_cost,
        # Include other EDA results as needed
    }

    return render_template('analysis.html', eda_results=eda_results, top_canteen=top_canteen)
