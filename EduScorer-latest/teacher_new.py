import os
import mysql.connector
import pymysql
"""# Access environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
# Database configuration
db_config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME,
}"""


db_config = {
        'user': 'root',
        'password': '12122003',
        'host': 'localhost',
        'database': 'eval_db2',
    }

def get_answer_ids_by_teacher_id(teacher_id):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Query to retrieve subject_id based on teacher_id
        get_subject_id_query = "SELECT subject_id FROM teachers WHERE teacher_id = %s"
        cursor.execute(get_subject_id_query, (teacher_id,))
        subject_id_result = cursor.fetchone()

        if subject_id_result:
            subject_id = subject_id_result['subject_id']

            # Query to retrieve question_ids based on subject_id
            get_question_ids_query = "SELECT question_id FROM questions WHERE subject_id = %s"
            cursor.execute(get_question_ids_query, (subject_id,))
            question_ids_result = cursor.fetchall()

            # Extract question_ids
            question_ids = [result['question_id'] for result in question_ids_result]

            # Query to retrieve answer_ids based on question_ids
            get_answer_ids_query = "SELECT answer_id FROM answers WHERE question_id IN (%s)"
            question_ids_placeholder = ', '.join(['%s'] * len(question_ids))
            cursor.execute(get_answer_ids_query % question_ids_placeholder, question_ids)
            answer_ids_result = cursor.fetchall()

            # Extract answer_ids
            answer_ids = [result['answer_id'] for result in answer_ids_result]

            return answer_ids

        else:
            print(f"Teacher with teacher_id {teacher_id} not found.")
            return []

    except pymysql.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        # Close the database connection
        if connection.open:
            cursor.close()
            connection.close()

def get_solution_and_answer_text_by_answer_id(answer_id):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Query to retrieve question_id based on answer_id
        get_question_id_query = "SELECT question_id FROM answers WHERE answer_id = %s"
        cursor.execute(get_question_id_query, (answer_id,))
        question_id_result = cursor.fetchone()

        if question_id_result:
            question_id = question_id_result['question_id']

            # Query to retrieve solution from questions table
            get_solution_query = "SELECT solution FROM questions WHERE question_id = %s"
            cursor.execute(get_solution_query, (question_id,))
            solution_result = cursor.fetchone()

            # Query to retrieve answer_text from answers table
            get_answer_text_query = "SELECT answer_text FROM answers WHERE answer_id = %s"
            cursor.execute(get_answer_text_query, (answer_id,))
            answer_text_result = cursor.fetchone()

            # Extract solution and answer_text
            solution = solution_result['solution'] if solution_result else None
            answer_text = answer_text_result['answer_text'] if answer_text_result else None

            return {'solution': solution, 'answer_text': answer_text}

        else:
            print(f"Answer with answer_id {answer_id} not found.")
            return {'solution': None, 'answer_text': None}

    except pymysql.Error as err:
        print(f"Error: {err}")
        return {'solution': None, 'answer_text': None}

    finally:
        # Close the database connection
        if connection.open:
            cursor.close()
            connection.close()

answer_ids=get_answer_ids_by_teacher_id(1)
i=0
get_solution_and_answer_text_by_answer_id(answer_ids[i])
