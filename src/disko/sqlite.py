import sqlite3
# Class to perform CRUD operations on a SQLite database
class SQLiteCRUD:
    # Constructor that connects to the database
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    # Function to create a table
    def create_table(self, table_name, columns, unique):
        """Create a table with the specified name and columns"""
        column_str = ", ".join(columns)
        unique = ", ".join([f'"{u}"' for u in unique.split(", ")])
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_str}, UNIQUE({unique}))')
        self.conn.commit()

    # Function to insert data into a table
    def insert_data(self, table_name, data):
        """Insert data into the specified table"""
        placeholders = ", ".join("?" * len(data))
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.conn.commit()

    # Function to insert data into a table with overwrite
    def insert_or_ignore_data(self, table_name, data):
        """Insert data into the specified table"""
        placeholders = ", ".join("?" * len(data))
        self.cursor.execute(f'INSERT OR IGNORE INTO "{table_name}" VALUES ({placeholders})', data)
        self.conn.commit()


    # Function to select all data from a table
    def select_all(self, table_name):
        """Retrieve all data from the specified table"""
        self.cursor.execute(f'SELECT * FROM "{table_name}"')
        return self.cursor.fetchall()
    
    # Added a new fuction for selecting all data from a column
    def select_column(self, table_name, column_name):
        """Retrieve specific column data from the specified table"""
        self.cursor.execute(f'SELECT "{column_name}" FROM "{table_name}"')
        return self.cursor.fetchall()

    # Function to select data from a table where a column has a specific value
    def select_where(self, table_name, column, value):
        """Retrieve data from the specified table where the specified column has the specified value"""
        self.cursor.execute(f'SELECT * FROM "{table_name}" WHERE {column} = ?', (value,))
        return self.cursor.fetchall()

    # Function to update data in a table where a column has a specific value
    def update_data(self, table_name, column, value, where_column, where_value):
        """Update data in the specified table where the specified column has the specified value"""
        self.cursor.execute(f'UPDATE "{table_name}" SET {column} = ? WHERE {where_column} = ?', (value, where_value))
        self.conn.commit()

    # Function to delete data from a table where a column has a specific value
    def delete_data(self, table_name, column, value):
        """Delete data from the specified table where the specified column has the specified value"""
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {column} = ?", (value,))
        self.conn.commit()

    # Destructor that closes the connection to the database
    def __del__(self):
        self.conn.close()