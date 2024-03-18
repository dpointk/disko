import sqlite3

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    return result is not None

if __name__ == "__main__":
    try:
        # Establishing Connection to SQLite Database for Image Data
        conn = sqlite3.connect('image_data.db')

        # Check if the "registries" table exists
        table1_exists = table_exists(conn, "registries")
        assert table1_exists, "The 'registries' table does not exist"
        print("table registries exists")
        # Check if the "images" table exists
        table2_exists = table_exists(conn, "images")
        assert table2_exists, "The 'images' table does not exist"
        print("table images exists ")
        # Close the connection
        conn.close()
    except Exception as e:
        print("Error:", e)
