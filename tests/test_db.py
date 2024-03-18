import sqlite3

def test_db_connection():
    try:
        # Establishing Connection to SQLite Database for Image Data
        conn = sqlite3.connect('image_data.db')
        cursor = conn.cursor()
        
        # Perform a simple query to test the connection
        cursor.execute('SELECT SQLITE_VERSION()')
        data = cursor.fetchone()
        print("SQLite version:", data[0])
        
        # Close the connection
        conn.close()
        print("Database connection test successful.")
    except Exception as e:
        print("Error:", e)

# Call the function to test the connection
test_db_connection()
