# db.py
# Handles SQLite database connection and table creation

import sqlite3

DB_NAME = "expenses.db"  # SQLite database file

def get_connection():
    """
    Returns a connection object to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)

def create_expenses_table():
    """
    Creates the 'expenses' table if it does not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            narration TEXT,
            debit REAL,
            credit REAL,
            closing_balance REAL
        )
    """)

    conn.commit()
    conn.close()

# Run directly to create the table
if __name__ == "__main__":
    create_expenses_table()
    print("Expenses table is ready!")
