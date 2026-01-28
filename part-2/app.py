

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  

DATABASE = 'students.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



@app.route('/add', methods=['GET', 'POST']) 
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db_connection()
        
        
        existing_student = conn.execute(
            'SELECT id FROM students WHERE email = ?', (email,)
        ).fetchone()

        if existing_student:
            flash('Email already exists!' , 'danger')
            conn.close()
            return redirect(url_for('index'))
            
            flash('Error: This email is already registered!', 'danger')
            return render_template('add.html', name=name, email=email, course=course)
       
        conn.execute(
            'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
            (name, email, course)
        )
        conn.commit()
        conn.close()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/')
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    
    conn = get_db_connection()
    
    if search_query:
        
        query = "SELECT * FROM students WHERE name LIKE ? ORDER BY id DESC"
        students = conn.execute(query, ('%' + search_query + '%',)).fetchall()
    else:
   
        students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
        
    conn.close()
    return render_template('index.html', students=students, search_query=search_query)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()

    if request.method == 'POST':  
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute(
            'UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?',
            (name, email, course, id)  
        )
        conn.commit()
        conn.close()

        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))

   
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', student=student)


@app.route('/search', methods=['GET'])
def search_student():
    name = request.args.get('name')

    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    ).fetchall()
    conn.close()

    return render_template('index.html', students=students)


@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))  
    conn.commit()
    conn.close()

    flash('Student deleted!', 'danger')  
    return redirect(url_for('index'))
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/search')
def search_student():
    name = request.args.get('name')

    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    ).fetchall()
    conn.close()

    return render_template('index.html', students=students)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)



# =============================================================================
# EXERCISE:
# =============================================================================
# 2. Add validation to check if email already exists before adding
#
# =============================================================================
