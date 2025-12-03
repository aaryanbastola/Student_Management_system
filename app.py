# app.py - COMPLETE FLASK APPLICATION
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from db_helper import get_db_connection, init_db, get_all_students, get_student_by_id, add_student, update_student, delete_student

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

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
    app.run(debug=True, port=5000)
