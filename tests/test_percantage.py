import sqlite3
import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_table_data(conn, table_name):
    cursor = conn.cursor()
    # Quote the table name to handle hyphens and other special characters
    quoted_table_name = f'"{table_name}"'
    # Query to check for non-null TimeStamp and valid Image file names
    cursor.execute(f'SELECT * FROM {quoted_table_name} WHERE TimeStamp IS NULL')
    invalid_rows = cursor.fetchall()
    if invalid_rows:
        print(f'Found {len(invalid_rows)} rows with invalid data in table "{table_name}":')
        for row in invalid_rows:
            print(row)
        return False
    else:
        print(f'All data in table "{table_name}" is valid.')
        return True

if __name__ == "__main__":
    try:
        # Establish connection to SQLite database
        conn = sqlite3.connect('image_data.db')

        # Example usage of check_table_data
        table_name = 'kind-test1'
        check_table_data(conn, table_name)

        # Close the connection
        conn.close()
        print("Connection to the database closed successfully.")
    except Exception as e:
        print("Error:", e)
