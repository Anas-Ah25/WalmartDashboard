import pandas as pd
import sqlite3

def create_database(csv_file, db_name):
    # Connect to SQLite database (or create if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Load CSV file into DataFrame
    df = pd.read_csv(csv_file)

    # Write the data to a sqlite table
    df.to_sql('sales_data', conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    create_database('walmart_sales_data_updated.csv', 'walmart_sales.db')
