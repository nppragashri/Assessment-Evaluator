import tkinter as tk
import pymysql
# admin.py
from tkinter import messagebox
from insert_teacher import TeacherPage
from insert_student import StudentPage
from corrections import CorrectionsApp
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
def clear_main_frame(master):
# Destroy all widgets in main_frame
    for widget in master.winfo_children():
        widget.destroy()
class AdminPage:
    def __init__(self, master):
        self.master = master

        # Add a label for the heading
        self.heading_label = tk.Label(master, text="ADMIN", font=("Helvetica", 16, "bold"))
        self.heading_label.grid(row=0, column=1, pady=10)

        # Create buttons
        self.teacher_button = tk.Button(master, text="Teacher", command=self.open_teacher_page)
        self.student_button = tk.Button(master, text="Student", command=self.open_student_page)
        self.correction_button = tk.Button(master, text="Correction", command=self.open_correction_page)

        # Place buttons on the window using grid
        self.teacher_button.grid(row=1, column=1, pady=10)
        self.student_button.grid(row=2, column=1, pady=10)
        self.correction_button.grid(row=3, column=1, pady=10)

        # Add buttons for opening delete pages
        self.teacher_delete_button = tk.Button(master, text="Delete Teacher", command=self.open_teacher_delete_page)
        self.student_delete_button = tk.Button(master, text="Delete Student", command=self.open_student_delete_page)

        # Place delete buttons on the window using grid
        self.teacher_delete_button.grid(row=4, column=1, pady=10)
        self.student_delete_button.grid(row=5, column=1, pady=10)

    def open_teacher_page(self):
        # Replace this function with the code for the teacher page
        clear_main_frame(self.master)
        TeacherPage(self.master)
        print("Teacher page opened")
        

    def open_student_page(self):
        # Replace this function with the code for the student page
        clear_main_frame(self.master)
        StudentPage(self.master)
        print("Student page opened")

    def open_correction_page(self):
        # Replace this function with the code for the correction page
        clear_main_frame(self.master)
        CorrectionsApp(self.master)
        print("Correction page opened")
    def open_teacher_delete_page(self):
        clear_main_frame(self.master)
        # Create an instance of the TeacherDeletePage and pass the master
        TeacherDeletePage(self.master)
        print("Teacher delete page opened")

    def open_student_delete_page(self):
        clear_main_frame(self.master)
        # Create an instance of the StudentDeletePage and pass the master
        StudentDeletePage(self.master)
        print("Student delete page opened")
# Add these classes to the same file (admin.py)

class TeacherDeletePage:
    def __init__(self, master):
        self.master = master

        # Label and Entry for Teacher ID
        self.teacher_id_label = tk.Label(master, text="Teacher ID:")
        self.teacher_id_entry = tk.Entry(master)

        # Button to delete teacher
        self.delete_teacher_button = tk.Button(master, text="Delete Teacher", command=self.delete_teacher)

        # Arrange widgets using grid
        self.teacher_id_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)
        self.teacher_id_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        self.delete_teacher_button.grid(row=1, column=1, pady=20)
        

    def delete_teacher(self):
        # Get the entered teacher ID
        teacher_id = self.teacher_id_entry.get()

        # Perform deletion logic (similar to your existing code)
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Delete teacher from the 'teachers' table
                delete_teacher_query = "DELETE FROM teachers WHERE teacher_id = %s"
                cursor.execute(delete_teacher_query, (teacher_id,))

                # Commit the changes to the database
                connection.commit()

                # Display a messagebox indicating successful deletion
                messagebox.showinfo("Success", "Teacher deleted successfully!")

        except Exception as e:
            # Display a messagebox for any errors that may occur during deletion
            messagebox.showerror("Error", f"Error deleting teacher: {str(e)}")

        finally:
            # Close the database connection
            connection.close()

class StudentDeletePage:
    def __init__(self, master):
        self.master = master

        # Label and Entry for Student ID
        self.student_id_label = tk.Label(master, text="Student ID:")
        self.student_id_entry = tk.Entry(master)

        # Button to delete student
        self.delete_student_button = tk.Button(master, text="Delete Student", command=self.delete_student)

        # Arrange widgets using grid
        self.student_id_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)
        self.student_id_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        self.delete_student_button.grid(row=1, column=1, pady=20)

    def delete_student(self):
        # Get the entered student ID
        student_id = self.student_id_entry.get()

        # Perform deletion logic (similar to your existing code)
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Delete student from the 'students' table
                delete_student_query = "DELETE FROM students WHERE student_id = %s"
                cursor.execute(delete_student_query, (student_id,))

                # Commit the changes to the database
                connection.commit()

                # Display a messagebox indicating successful deletion
                messagebox.showinfo("Success", "Student deleted successfully!")

        except Exception as e:
            # Display a messagebox for any errors that may occur during deletion
            messagebox.showerror("Error", f"Error deleting student: {str(e)}")

        finally:
            # Close the database connection
            connection.close()
   

if __name__ == "__main__":
    root = tk.Tk()
    admin_page = AdminPage(root)
    root.mainloop()