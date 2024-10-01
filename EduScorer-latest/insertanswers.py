import os
from dotenv import load_dotenv
import pymysql

# Load environment variables
load_dotenv()

# Access environment variables
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
}

# Create a connection to the database
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # Sample student ID
        student_id = 1

        # Sample answers and question IDs
        answers_data = [
            ("Answer for question 1", 1),
            ("Answer for question 2", 2),
            ("Answer for question 3", 3),
            ("Answer for question 4", 4),
            ("Answer for question 5", 5),
            ("Answer for question 6", 6),
            ("Answer for question 7", 7),
            ("Answer for question 8", 8),
            ("Answer for question 9", 9),
            ("Answer for question 10", 10),
            
            # Add more entries as needed
        ]

        # SQL query to insert data into the answers table
        sql = "INSERT INTO answers (answer_text, question_id, student_id) VALUES (%s, %s, %s)"

        # Use a for loop to insert multiple entries
        for answer_text, question_id in answers_data:
            cursor.execute(sql, (answer_text, question_id, student_id))

    # Commit the changes
    connection.commit()

    print("Answers inserted successfully!")

finally:
    # Close the connection
    connection.close()
