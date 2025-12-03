# db_helper.py - COMPLETE DATABASE HELPER
import sqlite3
import os
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
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster searches
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_name ON students(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_grade ON students(grade)')
        
        conn.commit()
        
        # Add sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            sample_students = [
                ('John Smith', 18, '12th Grade', 'john.smith@example.com', '555-0101', '123 Main St, City'),
                ('Emma Johnson', 17, '11th Grade', 'emma.johnson@example.com', '555-0102', '456 Oak Ave, Town'),
                ('Michael Brown', 16, '10th Grade', 'michael.brown@example.com', '555-0103', '789 Pine Rd, Village'),
                ('Sarah Davis', 18, '12th Grade', 'sarah.davis@example.com', '555-0104', '321 Elm St, City'),
                ('David Wilson', 17, '11th Grade', 'david.wilson@example.com', '555-0105', '654 Maple Dr, Town'),
                ('Lisa Anderson', 16, '10th Grade', 'lisa.anderson@example.com', '555-0106', '987 Cedar Ln, Village'),
                ('Robert Taylor', 18, '12th Grade', 'robert.taylor@example.com', '555-0107', '147 Birch St, City'),
                ('Maria Thomas', 17, '11th Grade', 'maria.thomas@example.com', '555-0108', '258 Walnut Ave, Town')
            ]
            
            cursor.executemany('''
                INSERT INTO students (name, age, grade, email, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_students)
            conn.commit()
            print(f" Added {len(sample_students)} sample students to database")

def get_all_students():
    """Get all students from database"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM students 
                ORDER BY grade, name
            ''')
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

def get_student_by_id(student_id):
    """Get student by ID"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error getting student {student_id}: {e}")
        return None

def add_student(name, age, grade, email, phone, address=""):
    """Add new student to database"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, grade, email, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, age, grade, email, phone, address))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Error: Email {email} already exists")
        return False
    except Exception as e:
        print(f"Error adding student: {e}")
        return False

def update_student(student_id, name, age, grade, email, phone, address=""):
    """Update student information"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students 
                SET name = ?, age = ?, grade = ?, email = ?, phone = ?, address = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, age, grade, email, phone, address, student_id))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        print(f"Error: Email {email} already exists for another student")
        return False
    except Exception as e:
        print(f"Error updating student: {e}")
        return False

def delete_student(student_id):
    """Delete student from database"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting student: {e}")
        return False

def search_students(query):
    """Search students by name, email, or grade"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute('''
                SELECT * FROM students 
                WHERE name LIKE ? OR email LIKE ? OR grade LIKE ? OR phone LIKE ?
                ORDER BY name
            ''', (search_term, search_term, search_term, search_term))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error searching students: {e}")
        return []

def get_statistics():
    """Get student statistics"""
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            
            # Total students
            cursor.execute("SELECT COUNT(*) FROM students")
            total = cursor.fetchone()[0]
            
            # Average age
            cursor.execute("SELECT AVG(age) FROM students")
            avg_age = cursor.fetchone()[0] or 0
            
            # Grade distribution
            cursor.execute('''
                SELECT grade, COUNT(*) as count 
                FROM students 
                GROUP BY grade 
                ORDER BY grade
            ''')
            grade_dist = cursor.fetchall()
            
            return {
                'total': total,
                'avg_age': round(avg_age, 1),
                'grade_distribution': grade_dist
            }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {'total': 0, 'avg_age': 0, 'grade_distribution': []}
