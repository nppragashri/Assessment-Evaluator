import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql.cursors
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
class StudentPage:
    def __init__(self, master):
        self.master = master
        
        # Labels and entry widgets for student details
        self.student_name_label = tk.Label(master, text="Student Name:")
        self.student_name_entry = tk.Entry(master)

        self.email_label = tk.Label(master, text="Email:")
        self.email_entry = tk.Entry(master)

        self.dob_label = tk.Label(master, text="Date of Birth:")
        self.dob_entry = DateEntry(master, date_pattern='yyyy-mm-dd') 

        # New labels and entry widgets for username and password
        self.username_label = tk.Label(master, text="Username:")
        self.username_entry = tk.Entry(master)

        self.password_label = tk.Label(master, text="Password:")
        self.password_entry = tk.Entry(master)  # Use show="*" to hide the password characters

        # Button to submit student details
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_student_details)

        # Arrange widgets using grid
        self.student_name_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)
        self.student_name_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        self.email_label.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)
        self.email_entry.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

        self.dob_label.grid(row=2, column=0, pady=10, padx=10, sticky=tk.W)
        self.dob_entry.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

        # Grid for username and password
        self.username_label.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)
        self.username_entry.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)

        self.password_label.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)
        self.password_entry.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)

        self.submit_button.grid(row=5, column=1, pady=20)

    def submit_student_details(self):
        # Get the entered student details
        student_name = self.student_name_entry.get()
        email = self.email_entry.get()
        dob = self.dob_entry.get()

        

        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Insert the student details into the 'students' table
                sql = "INSERT INTO students (student_name, date_of_birth, email) VALUES (%s, %s, %s)"
                cursor.execute(sql, (student_name, dob, email))

                # Commit the changes to the database
                connection.commit()

                # Display a messagebox indicating successful insertion
                messagebox.showinfo("Success", "Student details inserted successfully!")

        except Exception as e:
            # Display a messagebox for any errors that may occur during insertion
            messagebox.showerror("Error", f"Error inserting student details: {str(e)}")

        finally:
            # Close the database connection
            connection.close()
        # You can add logic here to save the details to a database or perform any other actions.

if __name__ == "__main__":
    root = tk.Tk()
    student_page = StudentPage(root)
    root.mainloop()
