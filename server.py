from flask import Flask, jsonify, render_template
import sqlite3
from flask import Flask, jsonify, render_template
import pandas as pd
df = pd.read_csv("walmart_sales_data_updated.csv")

app = Flask(__name__)
myDB = 'walmart_sales.db'

def query_db(query, args=()): #input is a tuple of arguments for the query
    with sqlite3.connect(myDB) as conn:
        conn.row_factory = sqlite3.Row  #column access by name:row['column_name']
        cur = conn.cursor() 
        cur.execute(query, args) 
        return cur.fetchall() #return all rows of a query result, as a list of tuples

@app.route('/')
def index():
    return render_template('index.html') 

# pie chart at div 2
# @app.route('/get-datachart')
# def get_datachart(): 
#     query = "SELECT `Ship Mode`, SUM(Sa les) as Sales FROM sales_data GROUP BY `Ship Mode`"  
#     ship_mode_sales = query_db(query)
#     data = [{"class": row["Ship Mode"], "value": row["Sales"]} for row in ship_mode_sales]
#     return jsonify(data)
# pie chart at div 2
@app.route('/get-datachart')
def get_datachart():
    df = pd.read_csv("walmart_sales_data_updated.csv")
    ship_mode_sales = df.groupby('Ship Mode')['Sales'].sum().reset_index()
    data = [{"class": row["Ship Mode"], "value": float(row["Sales"])} for row in ship_mode_sales.to_dict(orient='records')]
    return jsonify(data)

# ------------------- New Code -------------------

# donut chart at div 1
@app.route('/get-profit-data')
def get_profit_data():
    query = "SELECT Category, SUM(Profit) as Profit FROM sales_data GROUP BY Category"
    profit_by_category = query_db(query)
    data = [{"category": row["Category"], "profit": row["Profit"]} for row in profit_by_category]
    return jsonify(data)

# bar chart at div 3
@app.route('/get-top-states-data')
def get_top_states_data():
    query = "SELECT State, SUM(Profit) as Profit FROM sales_data GROUP BY State ORDER BY Profit DESC LIMIT 5"
    top_states = query_db(query)
    data = [{"State": row["State"], "Profit": row["Profit"]} for row in top_states]
    return jsonify(data)

# table at div 4
@app.route('/get-discount-category-data')
def get_discount_category_data():
    query = "SELECT Category, SUM(Discount) as Discount FROM sales_data GROUP BY Category"
    discount_data = query_db(query)
    data = [{"category": row["Category"], "value": row["Discount"]} for row in discount_data]
    return jsonify(data)

# area chart in upper row on right
@app.route('/get-sales-profit-data')
def get_sales_profit_data():
    query = """
    SELECT strftime('%Y-%m', Date) as YearMonth, SUM(Sales) as Sales, SUM(Profit) as Profit, SUM(Discount) as Discount
    FROM sales_data 
    GROUP BY YearMonth
    """
    grouped_data = query_db(query)
    data = [{"YearMonth": row["YearMonth"], "Sales": row["Sales"], "Profit": row["Profit"],"Discount": row["Discount"]} for row in grouped_data]
    return jsonify(data)

# boxes column
@app.route('/get-dashboard-data')
def get_dashboard_data():
    total_sales_query = "SELECT Sum(Sales) as TotalSales FROM sales_data" # Sum of all sales
    average_profit_query = "SELECT Sum(Profit) as AvgProfit FROM sales_data" # profit 
    total_discount_query = "SELECT Sum(Discount) as TotalDiscount FROM sales_data" # total discount given 

    total_sales = round(query_db(total_sales_query)[0]["TotalSales"], 2) 
    average_profit = round(query_db(average_profit_query)[0]["AvgProfit"], 2)
    total_discount = round(query_db(total_discount_query)[0]["TotalDiscount"], 2)

    return jsonify({
        'totalSales': total_sales,
        'averageProfit': average_profit,
        'totalDiscount': total_discount
    })


# Stacked Bar Chart (upper - left) -- location in final dashboard
@app.route('/stacked-bar-chart-data')
def get_sales_data():
    query = """
    SELECT
        strftime('%Y', Date) as Year,
        Category,
        SUM(Sales) as TotalSales
    FROM sales_data
    GROUP BY Year, Category
    """
    result = query_db(query)

    chart_data = {}
    for row in result:
        year = row['Year']
        category = row['Category']
        total_sales = row['TotalSales']

        if year not in chart_data:
            chart_data[year] = {}
        chart_data[year][category] = total_sales

    # preparing the data will be json
    formatted_chart_data = []
    for year, categories in chart_data.items():
        data_entry = {'Year': year}
        data_entry.update(categories)
        formatted_chart_data.append(data_entry)

    return jsonify(formatted_chart_data)


if __name__ == '__main__':
    app.run(debug=True)
