import sqlite3

# Path to your SQLite database
db_path = 'walmart_sales.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Example query: Select everything from your table
query = "SELECT * FROM  LIMIT 5;"  # Adjust the table name and query as needed

# Execute the query
cursor.execute(query)

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
cursor.close()
conn.close()
