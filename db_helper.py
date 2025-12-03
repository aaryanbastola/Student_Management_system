# db_helper.py - COMPLETE DATABASE HELPER
import sqlite3
from contextlib import closing

DATABASE = 'students.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with students table"""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        # Add some sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            sample_students = [
                ('John Smith', 18, '12th Grade', 'john@example.com', '555-0101'),
                ('Emma Johnson', 17, '11th Grade', 'emma@example.com', '555-0102'),
                ('Michael Brown', 16, '10th Grade', 'michael@example.com', '555-0103'),
                ('Sarah Davis', 18, '12th Grade', 'sarah@example.com', '555-0104'),
                ('David Wilson', 17, '11th Grade', 'david@example.com', '555-0105')
            ]
            cursor.executemany('''
                INSERT INTO students (name, age, grade, email, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', sample_students)
            conn.commit()

def get_all_students():
    """Get all students from database"""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        return cursor.fetchall()

def get_student_by_id(student_id):
    """Get student by ID"""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        return cursor.fetchone()

def add_student(name, age, grade, email, phone):
    """Add new student to database"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, grade, email, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, age, grade, email, phone))
            conn.commit()
            return True
    except:
        return False

def update_student(student_id, name, age, grade, email, phone):
    """Update student information"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students 
                SET name = ?, age = ?, grade = ?, email = ?, phone = ?
                WHERE id = ?
            ''', (name, age, grade, email, phone, student_id))
            conn.commit()
            return cursor.rowcount > 0
    except:
        return False

def delete_student(student_id):
    """Delete student from database"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
            return cursor.rowcount > 0
    except:
        return False
