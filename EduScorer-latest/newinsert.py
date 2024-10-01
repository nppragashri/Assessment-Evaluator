import os
import pymysql
import random
from decouple import Config
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
db_config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': "eval_db2",
}

def generate_random_marks():
    return random.randint(0, 100)

def generate_random_accuracy():
    return random.randint(0, 10)

def generate_random_completeness():
    return random.randint(0, 10)

def generate_random_length():
    return random.randint(0, 10)

def generate_random_relevance():
    return random.randint(0, 10)

def generate_random_clarity():
    return random.randint(0, 10)

def generate_random_evaluation_comment():
    comments = ["Excellent", "Good", "Average", "Needs Improvement"]
    return random.choice(comments)

def generate_random_username(role, user_id):
    return f"{role}{user_id}"

def generate_random_password():
    return f"password{random.randint(1, 100)}"

def insert_mock_data():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Insert mock data into the subjects table
        subjects = ["Mathematics", "Science", "English", "History", "Computer Science"]
        for subject in subjects:
            cursor.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject,))

        # Insert mock data into the students table
        for i in range(1, 11):
            student_name = f"Student {i}"
            cursor.execute("INSERT INTO students (student_name) VALUES (%s)", (student_name,))

        # Insert mock data into the teachers table
        for i in range(1, 11):
            teacher_name = f"Teacher {i}"
            cursor.execute("INSERT INTO teachers (teacher_name, subject_id) VALUES (%s, %s)",
                           (teacher_name, random.randint(1, len(subjects))))

            teacher_id = cursor.lastrowid  # Retrieve the auto-generated teacher_id

            # Insert mock data into the authentication table for teachers
            username = generate_random_username('teacher', teacher_id)
            password = generate_random_password()
            cursor.execute("""
                INSERT INTO authentication (username, password, role, teacher_id)
                VALUES (%s, %s, 'teacher', %s)
            """, (username, password, teacher_id))

        # Insert mock data into the admins table
        
        for i in range(1, 11):
            student_id = i
            username = generate_random_username('student', student_id)
            password = generate_random_password()
            cursor.execute("""
                INSERT INTO authentication (username, password, role, student_id)
                VALUES (%s, %s, 'student', %s)
            """, (username, password, student_id))
        for i in range(1, 6):
            admin_name = f"Admin {i}"
            cursor.execute("INSERT INTO admins (admin_name) VALUES (%s)", (admin_name,))
            admin_id = cursor.lastrowid  # Retrieve the auto-generated admin_id

            # Insert mock data into the authentication table for admins
            username = generate_random_username('admin', admin_id)
            password = generate_random_password()
            cursor.execute("""
                INSERT INTO authentication (username, password, role, admin_id)
                VALUES (%s, %s, 'admin', %s)
            """, (username, password, admin_id))

        # Insert mock data into the questions table
        for i in range(1, 11):
            cursor.execute(f"INSERT INTO questions (question_text, solution, subject_id) VALUES ('Question {i}', 'Solution {i}', %s)",
                           (random.randint(1, len(subjects)),))

        # Insert mock data into the evaluation table
        for i in range(1, 11):
            question_id = i
            student_id = random.randint(1, 10)
            teacher_id = random.randint(1, 10)
            marks = generate_random_marks()
            accuracy = generate_random_accuracy()
            completeness = generate_random_completeness()
            length = generate_random_length()
            relevance = generate_random_relevance()
            clarity = generate_random_clarity()
            evaluation_comment = generate_random_evaluation_comment()
            
            cursor.execute("""
                INSERT INTO evaluation (question_id, student_id, teacher_id, marks, accuracy, completeness, length, relevance, clarity, evaluation_comment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (question_id, student_id, teacher_id, marks, accuracy, completeness, length, relevance, clarity, evaluation_comment))

        # Insert mock data into the authentication table for students
        for i in range(1, 11):
            student_id = i
            username = generate_random_username('student', student_id)
            password = generate_random_password()
            cursor.execute("""
                INSERT INTO authentication (username, password, role, student_id)
                VALUES (%s, %s, 'student', %s)
            """, (username, password, student_id))

        conn.commit()
        print("Mock data inserted successfully!")

    except pymysql.Error as error:
        print(f"Error: {error}")

    finally:
        if conn.open:
            cursor.close()
            conn.close()

# Call the function to insert mock data
insert_mock_data()
