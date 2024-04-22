import sqlite3
from datetime import datetime, timedelta

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

def setup_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            subject TEXT,
            serial_number TEXT UNIQUE,
            type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'available'
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            material_id INTEGER,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (material_id) REFERENCES materials(id)
        );
    """)
    conn.commit()
    conn.close()

def add_material(title, author, subject, serial_number, type):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materials (title, author, subject, serial_number, type)
        VALUES (?, ?, ?, ?, ?);
    """, (title, author, subject, serial_number, type))
    conn.commit()
    conn.close()

def add_user(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, email)
        VALUES (?, ?);
    """, (name, email))
    conn.commit()
    conn.close()

#FUNCTION : 

def checkout_item(user_id, material_id, days=14):
    due_date = datetime.now() + timedelta(days=days)
    conn = create_connection()
    cursor = conn.cursor()
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
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM materials WHERE title LIKE ? OR author LIKE ? OR subject LIKE ? OR serial_number LIKE ?;
    """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    items = cursor.fetchall()
    conn.close()
    return items

def list_overdue_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM transactions WHERE due_date < ? AND return_date IS NULL;
    """, (datetime.now().date(),))
    overdue_items = cursor.fetchall()
    conn.close()
    return overdue_items
