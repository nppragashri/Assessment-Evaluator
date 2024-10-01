import tkinter as tk
import pymysql
from tkinter import Text, Label, Entry,ttk, messagebox
import os
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
i=0

def enter_box(box, text):
    # Enable the box
    box.config(state=tk.NORMAL)
    
    # Delete any existing text in the box
    box.delete(1.0, tk.END)
    
    # Insert the new text into the box
    box.insert(tk.END, text)
    
    # Disable the box again
    box.config(state=tk.DISABLED)
def get_question_ids_for_student(student_id):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Fetch unique question_ids for the given student_id from the evaluation table
        query = "SELECT DISTINCT question_id FROM answers WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        
        question_ids = [row[0] for row in cursor.fetchall()]

        return question_ids
        # return []
    finally:
        cursor.close()
        connection.close()   
def modify_entry_text(entry, new_text):
    entry.config(state="normal")  # Enable the entry
    entry.delete(0, tk.END)       # Clear existing text
    entry.insert(0, new_text)     # Insert new text
    entry.config(state="disabled")

def fetch_solution_and_answer(question_id, student_id):
    
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    #todo implement other fetch requests too 
    try:
        # Fetch teacher's solution from the 'questions' table
        cursor.execute("SELECT solution FROM questions WHERE question_id = %s", (question_id,))
        teacher_solution = cursor.fetchone()

        # Fetch student's answer from the 'answers' table
        cursor.execute("SELECT answer_text FROM answers WHERE question_id = %s AND student_id = %s", (question_id, student_id))
        student_answer = cursor.fetchone()

        # Fetch explanation from the 'evaluation' table
        cursor.execute("SELECT explanation FROM evaluation WHERE question_id = %s AND student_id = %s", (question_id, student_id))
        explanation = cursor.fetchone()

        return {
            'teacher_solution': teacher_solution['solution'] if teacher_solution else None,
            'student_answer': student_answer['answer_text'] if student_answer else None,
            'explanation': explanation['explanation'] if explanation else None
        }

    finally:
        cursor.close()
        connection.close()   
#todo fill handle errors (index out of range where there are no more questions in the list)))  
def student(main_frame,db_config,student_id):
    question_ids=get_question_ids_for_student(student_id)    
    def next():
        global i 
        i+=1
        fetch_data(i)  
    def back():
        global i 
        i-=1
        fetch_data(i)  
          
    def fetch_data(i):
        print(question_ids)
        question_id=question_ids[i]
        print(question_id)
        data = fetch_solution_and_answer(question_id, student_id)
        #temp insert 
        #todo check explaination its not properly working
        enter_box(teacher_solution_text, f"Teacher's Solution: {data['teacher_solution']}")
        enter_box(student_answer_text, f"Student's Answer: {data['student_answer']}")
        enter_box(explanation_text, f"Explanation: {data['explanation']}")
        modify_entry_text(id1_entry, "Question ID")
        modify_entry_text(id2_entry, "Student ID")
        # enter_box(explanation_text, "Explanation")
        modify_entry_text(marks_entry, "Marks")
        modify_entry_text(accuracy_entry, "Accuracy")
        modify_entry_text(completeness_entry, "Completeness")
        modify_entry_text(length_entry, "Length")
        modify_entry_text(relevance_entry, "Relevance")
        modify_entry_text(clarity_entry, "Clarity")
        modify_entry_text(evaluation_comment_entry, "Explanation Comment")
    teacher_solution_frame = tk.Frame(main_frame)
    teacher_solution_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    teacher_solution_frame.grid_rowconfigure(0, weight=1)
    teacher_solution_frame.grid_columnconfigure(0, weight=1)

    teacher_solution_label = tk.Label(teacher_solution_frame, text="Teacher's Solution")
    teacher_solution_label.grid(row=0, column=0, padx=10, pady=(0, 10))

    teacher_solution_text = Text(teacher_solution_frame, wrap=tk.WORD, height=38, width=50,state="disabled")
    teacher_solution_text.grid(row=1, column=0, padx=10, pady=(0, 10))

    # teacher_solution_button = tk.Button(teacher_solution_frame, text="Open from File",)
    # teacher_solution_button.grid(row=8, column=0, padx=10, pady=(0, 10))

    # Create a frame for student's answer in the middle
    student_answer_frame = tk.Frame(main_frame)
    student_answer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    student_answer_frame.grid_rowconfigure(0, weight=1)
    student_answer_frame.grid_columnconfigure(0, weight=1)

    student_answer_label = tk.Label(student_answer_frame, text="Student's Answer")
    student_answer_label.grid(row=0, column=0, padx=10, pady=(0, 10))

    student_answer_text = Text(student_answer_frame, wrap=tk.WORD, height=38, width=50, state="disabled")
    student_answer_text.grid(row=1, column=0, padx=10, pady=(0, 10))

    # student_answer_button = tk.Button(student_answer_frame, text="Open from File", command=open_student_answer_file)
    # student_answer_button.grid(row=8, column=0, padx=10, pady=(0, 10))

    # Create a frame for evaluation details on the right
    evaluation_frame = tk.Frame(main_frame)
    evaluation_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    evaluation_frame.grid_rowconfigure(0, weight=1)
    evaluation_frame.grid_columnconfigure(0, weight=1)

    row = 0
    explanation_label = Label(evaluation_frame, text="Explanation:")
    explanation_label.grid(row=row, column=0, padx=40, pady=(0, 10))

    explanation_text = Text(evaluation_frame, wrap=tk.WORD, height=25, width=35,state="disabled")
    explanation_text.grid(row=row, column=1, padx=10, pady=(0, 10))

    row += 1

    marks_label = Label(evaluation_frame, text="Marks:")
    marks_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    marks_entry = Entry(evaluation_frame, width=50,state="disabled")
    marks_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    accuracy_label = Label(evaluation_frame, text="Accuracy:")
    accuracy_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    accuracy_entry = Entry(evaluation_frame, width=50,state="disabled")
    accuracy_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    completeness_label = Label(evaluation_frame, text="Completeness:")
    completeness_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    completeness_entry = Entry(evaluation_frame, width=50,state="disabled")
    completeness_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    length_label = Label(evaluation_frame, text="Length:")
    length_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    length_entry = Entry(evaluation_frame, width=50,state="disabled")
    length_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    relevance_label = Label(evaluation_frame, text="Relevance:")
    relevance_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    relevance_entry = Entry(evaluation_frame, width=50,state="disabled")
    relevance_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    clarity_label = Label(evaluation_frame, text="Clarity:")
    clarity_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    clarity_entry = Entry(evaluation_frame, width=50,state="disabled")
    clarity_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    row += 1

    evaluation_comment_label = Label(evaluation_frame, text="Explanation Comment:")
    evaluation_comment_label.grid(row=row, column=0, padx=40, pady=(0, 10))
    evaluation_comment_entry = Entry(evaluation_frame, width=50,state="disabled")
    evaluation_comment_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
    red_label = Label(evaluation_frame, text="", fg="red")
    red_label.grid(row=row + 1, column=0, padx=40, pady=(0, 10), columnspan=2)

    buttons_frame = tk.Frame(main_frame)
    buttons_frame.grid(row=2, column=0,rowspan=2, columnspan=5, pady=10, sticky="nsew")
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)


    id_frame = tk.Frame(buttons_frame)
    id_frame.grid(row=0, column=0,rowspan=3,sticky="nsew")
    id_frame.grid_columnconfigure(0, weight=1)
    id_frame.grid_columnconfigure(1, weight=1)
    id_frame.grid_columnconfigure(2, weight=1)

    label1 = tk.Label(id_frame, text="Question ID:")
    label1.grid(row=0, column=0, pady=5, sticky="e")

    id1_entry = tk.Entry(id_frame, width=20,state="disabled")
    id1_entry.grid(row=0, column=1, pady=5, sticky="w")

    label2 = tk.Label(id_frame, text="Student ID:")
    label2.grid(row=1, column=0, pady=5, sticky="e")

    id2_entry = tk.Entry(id_frame, width=20,state="disabled")
    id2_entry.grid(row=1, column=1, pady=5, sticky="w")
    
    # clarity1_entry = Entry(buttons_frame, width=20)
    # clarity1_entry.grid(row=0, column=0, sticky="sw")
    # clarity2_entry = Entry(buttons_frame, width=20)
    # clarity2_entry.grid(row=0, column=1, sticky="sw")
    
    next_button = tk.Button(buttons_frame, text="Next",command=next)
    next_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")
    back_button = tk.Button(buttons_frame, text="Back",command=back)
    back_button.grid(row=2, column=1, padx=70, pady=10, sticky="sw")
    
        
    

    submit_button = tk.Button(buttons_frame, text="logout")#, command=enter_answer_data
    submit_button.grid(row=2, column=5, padx=10, pady=10, sticky="se")


    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.pack(expand=True, fill="both")
    

    