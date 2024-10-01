import tkinter as tk
from tkinter import Text, Label, Entry,ttk, messagebox
# from student import student
from backend import check_answer
from new_student import student
from tkinter import filedialog
import xlwt
import xlrd
import pymysql
from xlutils.copy import copy
import os
from dotenv import load_dotenv
from admin import AdminPage
def enter_box(box, text):
    # Enable the box
    box.config(state=tk.NORMAL)
    
    # Delete any existing text in the box
    box.delete(1.0, tk.END)
    
    # Insert the new text into the box
    box.insert(tk.END, text)
    
    # Disable the box again
    box.config(state=tk.DISABLED)
    
def modify_entry_text(entry, new_text):
    entry.config(state="normal")  # Enable the entry
    entry.delete(0, tk.END)       # Clear existing text
    entry.insert(0, new_text)     # Insert new text
    entry.config(state="disabled")   
def create_gui(main_frame,db_config):
    def export_to_excel():
        # Get the values from the GUI
        teacher_solution = teacher_solution_text.get("1.0", "end-1c")
        student_answer = student_answer_text.get("1.0", "end-1c")
        marks = marks_entry.get()
        accuracy = accuracy_entry.get()
        completeness = completeness_entry.get()
        relevance = relevance_entry.get()
        clarity = clarity_entry.get()
        explanation = explanation_text.get("1.0", "end-1c")  # Get explanation text

        

        # # Specify the Excel file to append to
        # excel_file = 'evaluation_data.xls'

        # # Check if the file exists or not
        # if not os.path.exists(excel_file):
        #     # If the file doesn't exist, create it with headers
        #     workbook = xlwt.Workbook()
        #     worksheet = workbook.add_sheet('Sheet1')
        #     headers = ["Teacher Solution", "Student Answer", "Marks", "Accuracy", "Completeness", "Relevance", "Clarity", "Explanation"]
        #     for col, header in enumerate(headers):
        #         worksheet.write(0, col, header)
        #     workbook.save(excel_file)

        # # Open the existing Excel file for appending
        # existing_workbook = xlrd.open_workbook(excel_file, formatting_info=True)
        # new_workbook = copy(existing_workbook)
        # worksheet = new_workbook.get_sheet(0)

        # # Get the number of existing rows in the Excel file
        # existing_rows = existing_workbook.sheet_by_index(0).nrows

        # # Append the new data to the next row, including explanation
        # worksheet.write(existing_rows, 0, teacher_solution)
        # worksheet.write(existing_rows, 1, student_answer)
        # worksheet.write(existing_rows, 2, marks)
        # worksheet.write(existing_rows, 3, accuracy)
        # worksheet.write(existing_rows, 4, completeness)
        # worksheet.write(existing_rows, 5, relevance)
        # worksheet.write(existing_rows, 6, clarity)
        # worksheet.write(existing_rows, 7, explanation)  # Write explanation
            # new_workbook.save(excel_file)
            # print("Data saved to Excel file")
            
        

    

    
    
    def clear_main_frame():
    # Destroy all widgets in main_frame
        for widget in main_frame.winfo_children():
            widget.destroy()
    def create_login_page(main_frame):
        def authenticate(username, password):
            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()

                # Retrieve role and stored_password for the given username
                cursor.execute("SELECT role, teacher_id, student_id, admin_id, password FROM authentication WHERE username = %s", (username,))
                result = cursor.fetchone()

                if result:
                    role, teacher_id, student_id, admin_id, stored_password = result

                    # Check if the provided password matches the stored password
                    if password == stored_password:
                        messagebox.showinfo("Login Successful", f"Welcome, {role.capitalize()} {username}!")
                        if role == 'teacher':
                            clear_main_frame()
                            eval(main_frame,teacher_id)
                            
                        elif role == 'student':
                            clear_main_frame()
                            
                            #TODO MAKE NEW FUNCTION CHECK FROM eval
                            student(main_frame,db_config,student_id)   
                        elif role == 'admin':
                            clear_main_frame()
                            AdminPage(main_frame)
                              
                    else:
                        messagebox.showerror("Login Failed", "Invalid password")
                else:
                    messagebox.showerror("Login Failed", "Username not found")

            except pymysql.Error as error:
                messagebox.showerror("Error", f"Database error: {error}")

            finally:
                if conn.open:
                    cursor.close()
                    conn.close()
        def on_login_button_click():
            username = username_entry.get()
            password = password_entry.get()
            authenticate(username, password)

        # Style configuration
        style = ttk.Style()
        style.configure("TFrame", background="#333")
        style.configure("TLabel", background="#333", foreground="white")
        style.configure("TButton", background="#00cc66", foreground="white")

        # Create a themed frame
        frame = ttk.Frame(main_frame, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)

        # Username label and entry
        username_label = ttk.Label(frame, text="Username:")
        username_label.grid(row=0, column=0, pady=(10, 0), sticky=tk.W)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=0, column=1, pady=(10, 0), sticky=tk.W + tk.E)

        # Password label and entry
        password_label = ttk.Label(frame, text="Password:")
        password_label.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1, pady=(5, 0), sticky=tk.W + tk.E)

        # Login button
        login_button = ttk.Button(frame, text="Login", command=on_login_button_click)
        login_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.W + tk.E)
        
    def eval(main_frame,teacher_id):  
        def enter_answer_data():
            # Get the data from the GUI
            question_id = 1  # Replace with the actual question ID
            student_id = 1  # Replace with the actual student ID
            teacher_id = 1  # Replace with the actual teacher ID
            answer_text = student_answer_text.get("1.0", "end-1c")
            explanation = explanation_text.get("1.0", "end-1c")
            marks = marks_entry.get()
            accuracy = accuracy_entry.get()
            completeness = completeness_entry.get()
            length = length_entry.get()
            relevance = relevance_entry.get()
            clarity = clarity_entry.get()
            evaluation_comment = evaluation_comment_entry.get()

            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()

                # Create a dictionary with the data to be inserted into the evaluation table
                evaluation_data = {
                    'question_id': question_id,
                    'student_id': student_id,
                    'teacher_id': teacher_id,
                    'marks': marks,
                    'accuracy': accuracy,
                    'completeness': completeness,
                    'length': length,
                    'relevance': relevance,
                    'clarity': clarity,
                    'evaluation_comment': evaluation_comment,
                    'explaination': explanation  # Note the corrected spelling here
                }

                # Insert data into the evaluation table
                insert_evaluation_query = """
                    INSERT INTO evaluation (question_id, student_id, teacher_id, marks, accuracy, completeness, length, relevance, clarity, evaluation_comment, explanation)
                    VALUES (%(question_id)s, %(student_id)s, %(teacher_id)s, %(marks)s, %(accuracy)s, %(completeness)s, %(length)s, %(relevance)s, %(clarity)s, %(evaluation_comment)s, %(explaination)s)
                """

                cursor.execute(insert_evaluation_query, evaluation_data)

                # Retrieve the auto-generated evaluation_id from the inserted row
                evaluation_id = cursor.lastrowid

                # Now, insert a record into the answers table with the question_id and student_id
                answer_data = {
                    'question_id': question_id,
                    'student_id': student_id,
                    'answer_text': answer_text  # Note the corrected spelling here
                }

                insert_answer_query = """
                    INSERT INTO answers (question_id, student_id, answer_text)
                    VALUES (%(question_id)s, %(student_id)s, %(answer_text)s)
                """

                cursor.execute(insert_answer_query, answer_data)

                conn.commit()
                print("Data inserted successfully!")

            except Exception as e:
                print("Error:", e)

            finally:
                cursor.close()
                conn.close()

            
        def clear_evaluation_entries():
        # Clear the Entry widgets
            explanation_text.delete("1.0", "end")
            marks_entry.delete(0, "end")
            accuracy_entry.delete(0, "end")
            completeness_entry.delete(0, "end")
            relevance_entry.delete(0, "end")
            clarity_entry.delete(0, "end")
            evaluation_comment_entry.delete(0, "end")
            length_entry.delete(0, "end")

        def evaluate_answer():
            teacher_solution = teacher_solution_text.get("1.0", "end-1c")
            student_answer = student_answer_text.get("1.0", "end-1c")
            max_marks = 10 
            question = "Describe the causes and consequences of the Industrial Revolution in the 19th century."

            result = check_answer(teacher_solution, student_answer, max_marks, question)

            
            result_dict = eval(result)
            marks = result_dict.get("marks")
            explanation = result_dict.get("explaination")  

        
            marks_entry.delete(0, "end")
            marks_entry.insert(0, marks)

            explanation_text.delete("1.0", "end")
            explanation_text.insert("1.0", str(explanation))

            
            accuracy_entry.delete(0, "end")
            accuracy_entry.insert(0, result_dict.get("accuracy"))

            completeness_entry.delete(0, "end")
            completeness_entry.insert(0, result_dict.get("completeness"))
            
            length_entry.delete(0, "end")
            length_entry.insert(0, result_dict.get("length"))

            relevance_entry.delete(0, "end")
            relevance_entry.insert(0, result_dict.get("relevance"))

            clarity_entry.delete(0, "end")
            clarity_entry.insert(0, result_dict.get("clarity"))
            
            explanation_text    .delete(0, "end")
            explanation_text.insert(0, result_dict.get("clarity"))


        def open_teacher_solution_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                with open(file_path, 'r') as file:
                    teacher_solution_text.delete("1.0", "end")
                    teacher_solution_text.insert("1.0", file.read())

        def open_student_answer_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                with open(file_path, 'r') as file:
                    student_answer_text.delete("1.0", "end")
                    student_answer_text.insert("1.0", file.read())
    # Create a frame for teacher's solution on the left
       
        teacher_solution_frame = tk.Frame(main_frame)
        teacher_solution_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        teacher_solution_frame.grid_rowconfigure(0, weight=1)
        teacher_solution_frame.grid_columnconfigure(0, weight=1)

        teacher_solution_label = tk.Label(teacher_solution_frame, text="Teacher's Solution")
        teacher_solution_label.grid(row=0, column=0, padx=10, pady=(0, 10))

        teacher_solution_text = Text(teacher_solution_frame, wrap=tk.WORD, height=38, width=50)
        teacher_solution_text.grid(row=1, column=0, padx=10, pady=(0, 10))

        teacher_solution_button = tk.Button(teacher_solution_frame, text="Open from File", command=open_teacher_solution_file)
        teacher_solution_button.grid(row=8, column=0, padx=10, pady=(0, 10))

        # Create a frame for student's answer in the middle
        student_answer_frame = tk.Frame(main_frame)
        student_answer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        student_answer_frame.grid_rowconfigure(0, weight=1)
        student_answer_frame.grid_columnconfigure(0, weight=1)

        student_answer_label = tk.Label(student_answer_frame, text="Student's Answer")
        student_answer_label.grid(row=0, column=0, padx=10, pady=(0, 10))

        student_answer_text = Text(student_answer_frame, wrap=tk.WORD, height=38, width=50, state="disabled")
        student_answer_text.grid(row=1, column=0, padx=10, pady=(0, 10))

        student_answer_button = tk.Button(student_answer_frame, text="Open from File", command=open_student_answer_file)
        student_answer_button.grid(row=8, column=0, padx=10, pady=(0, 10))

        # Create a frame for evaluation details on the right
        evaluation_frame = tk.Frame(main_frame)
        evaluation_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        evaluation_frame.grid_rowconfigure(0, weight=1)
        evaluation_frame.grid_columnconfigure(0, weight=1)

        row = 0
        explanation_label = Label(evaluation_frame, text="Explanation:")
        explanation_label.grid(row=row, column=0, padx=40, pady=(0, 10))

        explanation_text = Text(evaluation_frame, wrap=tk.WORD, height=25, width=35)
        explanation_text.grid(row=row, column=1, padx=10, pady=(0, 10))

        row += 1

        marks_label = Label(evaluation_frame, text="Marks:")
        marks_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        marks_entry = Entry(evaluation_frame, width=50)
        marks_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        accuracy_label = Label(evaluation_frame, text="Accuracy:")
        accuracy_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        accuracy_entry = Entry(evaluation_frame, width=50)
        accuracy_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        completeness_label = Label(evaluation_frame, text="Completeness:")
        completeness_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        completeness_entry = Entry(evaluation_frame, width=50)
        completeness_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        length_label = Label(evaluation_frame, text="Length:")
        length_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        length_entry = Entry(evaluation_frame, width=50)
        length_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        relevance_label = Label(evaluation_frame, text="Relevance:")
        relevance_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        relevance_entry = Entry(evaluation_frame, width=50)
        relevance_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        clarity_label = Label(evaluation_frame, text="Clarity:")
        clarity_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        clarity_entry = Entry(evaluation_frame, width=50)
        clarity_entry.grid(row=row, column=1, padx=10, pady=(0, 10))
        row += 1

        evaluation_comment_label = Label(evaluation_frame, text="Explanation Comment:")
        evaluation_comment_label.grid(row=row, column=0, padx=40, pady=(0, 10))
        evaluation_comment_entry = Entry(evaluation_frame, width=50)
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

        label3 = tk.Label(id_frame, text="Teacher ID:")
        label3.grid(row=2, column=0, pady=5, sticky="e")

        id3_entry = tk.Entry(id_frame, width=20,state="disabled")
        id3_entry.grid(row=2, column=1, pady=5, sticky="w")
        id3_entry.insert(0,teacher_id)
        # clarity1_entry = Entry(buttons_frame, width=20)
        # clarity1_entry.grid(row=0, column=0, sticky="sw")
        # clarity2_entry = Entry(buttons_frame, width=20)
        # clarity2_entry.grid(row=0, column=1, sticky="sw")
        next_button = tk.Button(buttons_frame, text="Next")
        next_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

        clear_button = tk.Button(buttons_frame, text="Clear", command=clear_evaluation_entries)
        clear_button.grid(row=2, column=2, padx=10, pady=10, sticky="se")

        submit_button = tk.Button(buttons_frame, text="Submit", command=enter_answer_data)
        submit_button.grid(row=2, column=5, padx=10, pady=10, sticky="se")
        

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.pack(expand=True, fill="both")
        enter_box(student_answer_text, "This is the student's answer")
        # modify_entry_text(id3_entry, "2")
    create_login_page(main_frame)
    # eval(main_frame,1)
    
   
