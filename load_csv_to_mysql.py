import csv
import mysql.connector
from mysql.connector import Error

# 1. Database connection details (DO NOT specify the database name here yet)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your password" 
}

database_name = "ecommerce_db"
csv_file_path = "ecommerce_sales_analytics_5000.csv"
table_name = "sales_analytics"

print("Connecting to MySQL server...")
try:
    # Connect without a database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 1.5 Create the database if it doesn't exist
    print(f"Creating database '{database_name}' if it doesn't exist...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    
    # Switch to the new database
    cursor.execute(f"USE {database_name}")

    # 2. Open the CSV and read the headers
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader) # Get the first row (column names)
        
        # Clean headers (lowercase, replace spaces with underscores)
        clean_headers = [h.strip().lower().replace(' ', '_') for h in headers]
        
        # 3. Create the table
        # CRITICAL: For a real project, change "TEXT" to the actual data types 
        # (e.g., INT, DECIMAL, DATE) so the LLM can do math on them!
        print(f"Creating table '{table_name}'...")
        columns_with_types = [f"{col} TEXT" for col in clean_headers]
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)});"
        
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};") # Clear old table
        cursor.execute(create_table_sql)
        
        # 4. Prepare the INSERT statement dynamically based on the number of columns
        placeholders = ", ".join(["%s"] * len(clean_headers))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(clean_headers)}) VALUES ({placeholders})"
        
        # 5. Loop through the CSV and insert data
        print(f"Uploading data from {csv_file_path}...")
        batch_data = []
        
        for row in csv_reader:
            batch_data.append(tuple(row))
            
            # Insert in batches of 1000 for better performance
            if len(batch_data) >= 1000:
                cursor.executemany(insert_sql, batch_data)
                batch_data = [] # Reset batch
                
        # Insert any remaining rows
        if batch_data:
            cursor.executemany(insert_sql, batch_data)
            
        # 6. Commit the changes (save them permanently)
        conn.commit()
        print("Upload complete! 5000 rows successfully inserted.")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")
finally:
    # Close connections safely
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")