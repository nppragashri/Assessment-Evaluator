import tkinter as tk
from tkinter import Text, Label, Entry,ttk, messagebox
from backend import check_answer
from tkinter import filedialog
import xlwt
import xlrd
import pymysql
from xlutils.copy import copy
import os
from dotenv import load_dotenv
from gui import create_gui, enter_box,modify_entry_text
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

 
root = tk.Tk()
root.title("Answer Evaluation")

# Make the window fullscreen
root.attributes('-fullscreen', True)

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")
create_gui(main_frame,db_config)
root.mainloop()
