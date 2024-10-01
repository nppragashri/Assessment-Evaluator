import tkinter as tk
from tkinter import ttk
import pymysql
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
class CorrectionsApp:
    def __init__(self, root):
        self.root = root

        # Create and set up the table
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Correction ID", "Evaluation ID", "Teacher ID", "Correction Date")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Correction ID", anchor=tk.W, width=100)
        self.tree.column("Evaluation ID", anchor=tk.W, width=100)
        self.tree.column("Teacher ID", anchor=tk.W, width=100)
        self.tree.column("Correction Date", anchor=tk.W, width=200)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Correction ID", text="Correction ID", anchor=tk.W)
        self.tree.heading("Evaluation ID", text="Evaluation ID", anchor=tk.W)
        self.tree.heading("Teacher ID", text="Teacher ID", anchor=tk.W)
        self.tree.heading("Correction Date", text="Correction Date", anchor=tk.W)

        self.tree.pack(pady=20)

        self.student_id_var = tk.StringVar()
        self.teacher_id_var = tk.StringVar()
        self.question_id_var = tk.StringVar()

        self.create_entry_with_placeholder(self.student_id_var, "Enter Student ID", self.clear_student)
        self.create_entry_with_placeholder(self.teacher_id_var, "Enter Teacher ID", self.clear_teacher)
        self.create_entry_with_placeholder(self.question_id_var, "Enter Question ID", self.clear_question)

        # # self.student_id_entry.pack(side=tk.LEFT, pady=5, padx=5)
        # self.clear_button_student = tk.Button(root, text="Clear", command=self.clear_student)
        # self.clear_button_student.pack(side=tk.LEFT, pady=5, padx=5)

        # self.teacher_id_entry.pack(side=tk.LEFT, pady=5, padx=5)
        # self.clear_button_teacher = tk.Button(root, text="Clear", command=self.clear_teacher)
        # self.clear_button_teacher.pack(side=tk.LEFT, pady=5, padx=5)
        # self.question_id_var = tk.StringVar()
        # self.question_id_entry = tk.Entry(root, textvariable=self.question_id_var, width=20)
        # self.question_id_entry.insert(0, "Enter Question ID")
        # self.question_id_entry.pack(side=tk.LEFT, pady=5, padx=5)
        # self.clear_button_question = tk.Button(root, text="Clear", command=self.clear_question)
        # self.clear_button_question.pack(side=tk.LEFT, pady=5, padx=5)
        # Button to trigger search
        self.search_button = tk.Button(root, text="Search", command=self.search_corrections)
        self.search_button.pack(side=tk.LEFT, pady=5, padx=5)

        # Connect to the database
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

        # Populate the table
        self.populate_table()
    def create_entry_with_placeholder(self, var, placeholder, clear_command):
        entry = tk.Entry(self.root, textvariable=var, width=20)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, v=var: self.on_entry_focus_in(v, placeholder))
        entry.bind("<FocusOut>", lambda event, v=var: self.on_entry_focus_out(v, placeholder))
        entry.pack(side=tk.LEFT, pady=5, padx=5)

        clear_button = tk.Button(self.root, text="Clear", command=clear_command)
        clear_button.pack(side=tk.LEFT, pady=5, padx=5)

    def on_entry_focus_in(self, var, placeholder):
        if var.get() == placeholder:
            var.set("")

    def on_entry_focus_out(self, var, placeholder):
        if var.get() == "":
            var.set(placeholder)
    def populate_table(self):
        # Clear existing data
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Fetch data from the database
        self.cursor.execute("SELECT * FROM corrections")
        rows = self.cursor.fetchall()

        # Insert data into the table
        for row in rows:
            self.tree.insert("", "end", values=row)

    def search_corrections(self):
        # Fetch data based on search criteria
        student_id = self.student_id_var.get()
        teacher_id = self.teacher_id_var.get()
        question_id = self.question_id_var.get()
        evaluation_ids = None

        if student_id.isdigit():
            # Query the evaluation table for the student ID
            evaluation_query = f"SELECT evaluation_id FROM evaluation WHERE student_id = {student_id}"
            self.cursor.execute(evaluation_query)
            evaluation_rows = self.cursor.fetchall()

            # Extract the evaluation IDs from the result
            evaluation_ids = set(str(row[0]) for row in evaluation_rows)

        if question_id.isdigit():   
            # Query the evaluation table for the question ID
            question_evaluation_query = f"SELECT evaluation_id FROM evaluation WHERE question_id = {question_id}"
            self.cursor.execute(question_evaluation_query)
            question_evaluation_rows = self.cursor.fetchall()

            # Extract the evaluation IDs from the result
            question_evaluation_ids = set(str(row[0]) for row in question_evaluation_rows)

            # Perform intersection with the previous evaluation IDs if not None
            if evaluation_ids is not None:
                evaluation_ids = evaluation_ids.intersection(question_evaluation_ids)
            else:
                evaluation_ids = question_evaluation_ids

        # Query the corrections table based on the evaluation IDs and teacher ID
        conditions = []
        if evaluation_ids:
            conditions.append(f"evaluation_id IN ({', '.join(evaluation_ids)})")

        if teacher_id.isdigit():
            conditions.append(f"teacher_id = {teacher_id}")

        if conditions:
            query = f"SELECT * FROM corrections WHERE {' AND '.join(conditions)}"
        else:
            # If no conditions are specified, retrieve all entries from the "corrections" table
            query = "SELECT * FROM corrections"

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Clear existing data
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Insert data into the table
        for row in rows:
            self.tree.insert("", "end", values=row)


    def clear_student(self):
        self.student_id_var.set("")

    def clear_teacher(self):
        self.teacher_id_var.set("")
    def clear_question(self):
        self.question_id_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = CorrectionsApp(root)
    root.mainloop()
