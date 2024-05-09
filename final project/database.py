import sqlite3
from datetime import datetime, timedelta

def create_connection():
    # Establishes and returns a connection to the SQLite database named 'library.db'.
    conn = sqlite3.connect('library.db')
    return conn

def setup_database():
    # Sets up the database by creating tables for materials, users, and transactions if they don't already exist.
    conn = create_connection()
    cursor = conn.cursor()
    # Create a table for library materials with attributes like title, author, etc.
    # 'status' defaults to 'available' indicating the item can be borrowed.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (...)
    """)
    # Create a table for users with unique email.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (...)
    """)
    # Create a table for transactions to track borrowed materials.
    # Establishes foreign key relationships with users and materials tables.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (...)
    """)
    conn.commit()
    conn.close()

def add_material(title, author, subject, serial_number, type):
    # Adds a new material to the materials table using the provided parameters.
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materials (title, author, subject, serial_number, type)
        VALUES (?, ?, ?, ?, ?);
    """, (title, author, subject, serial_number, type))
    conn.commit()
    conn.close()

def add_user(name, email):
    # Adds a new user to the users table using the provided name and email.
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, email)
        VALUES (?, ?);
    """, (name, email))
    conn.commit()
    conn.close()

def checkout_item(user_id, material_id, days=14):
    # Checks out an item to a user, setting the due date for return, and updates the material's status.
    due_date = datetime.now() + timedelta(days=days)
    conn = create_connection()
    cursor = conn.cursor()
    # Only update status if the item is available.
    cursor.execute("""
        UPDATE materials SET status='checked out' WHERE id=? AND status='available';
    """, (material_id,))
    if cursor.rowcount > 0:
        cursor.execute("""
            INSERT INTO transactions (user_id, material_id, issue_date, due_date)
            VALUES (?, ?, ?, ?);
        """, (user_id, material_id, datetime.now().date(), due_date.date()))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def return_item(material_id):
    # Marks an item as returned in the transactions table and updates its status in the materials table.
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions SET return_date=? WHERE material_id=? AND return_date IS NULL;
    """, (datetime.now().date(), material_id))
    cursor.execute("""
        UPDATE materials SET status='available' WHERE id=?;
    """, (material_id,))
    conn.commit()
    conn.close()

def search_materials(keyword):
    # Searches for materials that match the keyword in title, author, subject, or serial number.
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM materials WHERE title LIKE ? OR author LIKE ? OR subject LIKE ? OR serial_number LIKE ?;
    """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    items = cursor.fetchall()
    conn.close()
    return items

def list_overdue_items():
    # Lists all items that are overdue based on the current date.
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM transactions WHERE due_date < ? AND return_date IS NULL;
    """, (datetime.now().date(),))
    overdue_items = cursor.fetchall()
    conn.close()
    return overdue_items
