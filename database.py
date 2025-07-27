import sqlite3
import numpy as np
import os

def init_db():
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        conn = sqlite3.connect('data/students.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                     (student_code TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      branch TEXT,
                      session TEXT,
                      face_encoding BLOB)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

def add_student(student_code, name, branch, session, face_encoding):
    conn = sqlite3.connect('data/students.db')
    c = conn.cursor()
    face_encoding_bytes = face_encoding.tobytes()
    c.execute('INSERT INTO students VALUES (?, ?, ?, ?, ?)',
              (student_code, name, branch, session, face_encoding_bytes))
    conn.commit()
    conn.close()

def get_all_students():
    try:
        conn = sqlite3.connect('data/students.db')
        c = conn.cursor()
        c.execute('SELECT * FROM students')
        rows = c.fetchall()
        students = []
        faces = []
        for row in rows:
            students.append({
                'student_code': row[0],
                'name': row[1], 
                'branch': row[2],
                'session': row[3]
            })
            face_array = np.frombuffer(row[4], dtype=np.float64)
            faces.append(face_array)
        conn.close()
        return students, np.array(faces)
    except Exception as e:
        print(f"Error getting students: {e}")
        return [], np.array([])
