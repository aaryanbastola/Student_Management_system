# app.py - MODIFIED FOR GITHUB ROOT DIRECTORY
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Import database functions (they're in the same directory)
from db_helper import get_db_connection, init_db, get_all_students, get_student_by_id, add_student, update_student, delete_student

# Create folders if they don't exist (for local development)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Tell Flask to look in current directory for templates and static files
app = Flask(__name__, 
            template_folder='.',      # Look in current directory for templates
            static_folder='.',        # Look in current directory for static files
            static_url_path='')       # Serve static files from root path

app.secret_key = 'your-secret-key-here-change-this-in-production'

# Initialize database
init_db()

@app.route('/')
def index():
    """Dashboard - Show all students"""
    students = get_all_students()
    return render_template('dashboard.html', students=students)

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """Show student details"""
    student = get_student_by_id(student_id)
    if student:
        return render_template('student_detail.html', student=student)
    flash('Student not found!', 'error')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        email = request.form['email']
        phone = request.form['phone']
        
        if add_student(name, age, grade, email, phone):
            flash('Student added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error adding student!', 'error')
    
    return render_template('add_student.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edit existing student"""
    student = get_student_by_id(student_id)
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        email = request.form['email']
        phone = request.form['phone']
        
        if update_student(student_id, name, age, grade, email, phone):
            flash('Student updated successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error updating student!', 'error')
    
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:student_id>')
def delete_student_route(student_id):
    """Delete student"""
    if delete_student(student_id):
        flash('Student deleted successfully!', 'success')
    else:
        flash('Error deleting student!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Student Management System...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, port=5000)
