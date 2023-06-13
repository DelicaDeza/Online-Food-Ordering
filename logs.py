from flask import render_template
import pandas as pd
import matplotlib.pyplot as plt
from models import logs

def eda():
    # Retrieve the data from the "logs" table
    query = logs.query.all()

    # Convert the query result into a Pandas DataFrame
    df = pd.DataFrame([(item.transid, item.itemname, item.itemquantity, item.itemcost, item.itemdate, item.transactionno) for item in query],
                      columns=['transid', 'itemname', 'itemquantity', 'itemcost', 'itemdate', 'transactionno'])

    # Calculate sales data
    sales_data = df.groupby('itemname')['itemquantity'].sum().reset_index()

    # Sort the sales data in descending order
    sales_data = sales_data.sort_values(by='itemquantity', ascending=False)

    # Get the top 10 items with the highest sales
    top_items = sales_data.head(10)

    # Pass the EDA results and sales data to the HTML template
    eda_results = {
        'unique_items': df['itemname'].nunique(),
        'total_quantity': df['itemquantity'].sum(),
        'total_cost': df['itemcost'].sum(),
        # Include other EDA results as needed
    }

    # Generate other plots
    # Line Plot - Sales over Time
    sales_over_time = df.groupby(pd.to_datetime(df['itemdate'])).agg({'itemquantity': 'sum'}).reset_index()
    plt.plot(sales_over_time['itemdate'], sales_over_time['itemquantity'])
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.title('Sales over Time')
    plt.savefig('static/sales_over_time.png')
    plt.close()

    # Pie Chart - Distribution of Sales by Item
    plt.pie(top_items['itemquantity'], labels=top_items['itemname'], autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Distribution of Sales by Item')
    plt.savefig('static/sales_distribution.png')
    plt.close()

    # Area Chart - Cumulative Sales over Time
    # sales_over_time['cumulative_sales'] = sales_over_time['itemquantity'].cumsum()
    # plt.fill_between(pd.to_datetime(sales_over_time['itemdate']), sales_over_time['cumulative_sales'], alpha=0.3)
    # plt.xlabel('Date')
    # plt.ylabel('Cumulative Sales Quantity')
    # plt.title('Cumulative Sales over Time')
    # plt.savefig('static/cumulative_sales.png')
    # plt.close()

    # Scatter Plot - Item Quantity vs Item Cost
    plt.scatter(df['itemquantity'], df['itemcost'])
    plt.xlabel('Item Quantity')
    plt.ylabel('Item Cost')
    plt.title('Item Quantity vs Item Cost')
    plt.savefig('static/quantity_cost_scatter.png')
    plt.close()

    # Histogram - Distribution of Sales
    plt.hist(df['itemquantity'], bins=10)
    plt.xlabel('Sales Quantity')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sales')
    plt.savefig('static/sales_distribution_hist.png')
    plt.close()

    # Box Plot - Sales Distribution by Item
    plt.boxplot([df[df['itemname'] == item]['itemquantity'] for item in top_items['itemname']])
    plt.xticks(range(1, len(top_items['itemname']) + 1), top_items['itemname'], rotation=45)
    plt.xlabel('Item Name')
    plt.ylabel('Sales Quantity')
    plt.title('Sales Distribution by Item')
    plt.savefig('static/sales_distribution_boxplot.png')
    plt.close()

    return render_template('analysis.html', eda_results=eda_results, top_items=top_items)
