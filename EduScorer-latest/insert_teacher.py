
import tkinter as tk
from tkinter import messagebox
import pymysql  # Import pymysql instead of mysql.connector
import os
from dotenv import load_dotenv
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
                    'database':"eval_db2",
                }
class TeacherPage:
    def __init__(self, master):
        self.master = master

                # Labels and entry widgets for teacher details
        self.teacher_name_label = tk.Label(master, text="Teacher Name:")
        self.teacher_name_entry = tk.Entry(master)

        self.subject_name_label = tk.Label(master, text="Subject Name:")
        self.subject_name_entry = tk.Entry(master)

        self.email_label = tk.Label(master, text="Email ID:")
        self.email_entry = tk.Entry(master)

        # Labels and entry widgets for username and password
        self.username_label = tk.Label(master, text="Username:")
        self.username_entry = tk.Entry(master)

        self.password_label = tk.Label(master, text="Password:")
        self.password_entry = tk.Entry(master, show="*")  # Use show="*" to hide the entered characters

        # Button to submit teacher details
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_teacher_details)

        # Arrange widgets using grid
        self.teacher_name_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)
        self.teacher_name_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        self.subject_name_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)
        self.subject_name_entry.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

        self.email_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.W)
        self.email_entry.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

        self.username_label.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)
        self.username_entry.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)

        self.password_label.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)
        self.password_entry.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)

        self.submit_button.grid(row=5, column=1, pady=20)

    def submit_teacher_details(self):
        # Get the entered details
        teacher_name = self.teacher_name_entry.get()
        subject_name = self.subject_name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Connect to the database using pymysql
            db_connection = pymysql.connect(**db_config)            

            cursor = db_connection.cursor()

            # Retrieve the subject_id based on the subject_name
            subject_query = "SELECT subject_id FROM subjects WHERE subject_name = %s"
            cursor.execute(subject_query, (subject_name,))
            result = cursor.fetchone()

            if result:
                subject_id = result[0]
            else:
                # If the subject doesn't exist, you may want to handle this case
                messagebox.showwarning("Warning", "Subject not found in the database.")
                return

            # Insert data into the 'teachers' table
            teacher_insert_query = "INSERT INTO teachers (teacher_name, email_id, subject_id) VALUES (%s, %s, %s)"
            cursor.execute(teacher_insert_query, (teacher_name, email, subject_id))
            teacher_id = cursor.lastrowid  # Get the auto-generated teacher_id

            # Insert data into the 'authentication' table
            auth_insert_query = "INSERT INTO authentication (username, password, role, teacher_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(auth_insert_query, (username, password, 'teacher', teacher_id))

            # Commit the changes to the database
            db_connection.commit()

            # Close the database connection
            cursor.close()
            db_connection.close()

            # Display success message
            messagebox.showinfo("Success", "Teacher details added to the database successfully.")

        except pymysql.Error as err:
            # Handle any database errors
            messagebox.showerror("Error", f"Database error: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    teacher_page = TeacherPage(root)
    root.mainloop()
