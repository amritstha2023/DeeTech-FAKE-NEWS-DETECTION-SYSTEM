import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'fakenews'
}

def convert_date_format(date_str):
    try:
        return datetime.strptime(date_str, '%d-%b-%y').strftime('%Y-%m-%d')
    except ValueError:
        return None

connection = None

try:
    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()
        print("Connected to MySQL database")

        # Read CSV file
        df = pd.read_csv('news.csv')

        # Convert date column to YYYY-MM-DD format
        df['date'] = df['date'].apply(convert_date_format)

        # Insert data into table
        insert_query = '''
        INSERT INTO news (title, text, category, date, image_path, label)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        for i, row in df.iterrows():
            cursor.execute(insert_query, (
                row['title'],
                row['text'],
                row['subject'],  # Map 'subject' from CSV to 'category'
                row['date'],
                '',  # Use an empty string or a default path for 'image_path'
                row['label']
            ))

        connection.commit()
        print(f"{len(df)} records inserted successfully into news table")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
