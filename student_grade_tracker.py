import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

conn = sqlite3.connect("student_grade_tracker.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_grade_tracker (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        phone TEXT,
        email TEXT,
        grade INTEGER
    )
""")
conn.commit()
############################
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM student_grade_tracker")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", END, values=row)

def add_customer():
    if name_var.get() == "":
        messagebox.showwarning("Warning", "กรุณากรอกชื่อ")
        return
    if not (phone_var.get().isdigit()):
        messagebox.showwarning("Warning", "เบอร์โทรศัพท์จำเป็นต้องเป็นตัวเลข")
        return
    if not (len(phone_var.get()) == 10):
        messagebox.showwarning("Warning", "เบอร์โทรศัพท์จำเป็นต้องมีความยาว 10 หลักเท่านั้น")
        return
    if not email_var.get().endswith("@gmail.com"):
        messagebox.showwarning("Warning", "กรุณาใส่ Email ให้ถูกต้อง")
        return
    cursor.execute("INSERT INTO student_grade_tracker (name, phone, email) VALUES (?, ?, ?)",
                   (name_var.get(), phone_var.get(), email_var.get()))
    conn.commit()
    fetch_data()
    clear_form()

def select_row(event):
    selected = tree.focus()
    values = tree.item(selected, "values")
    if values:
        name_var.set(values[1])
        phone_var.set(values[2])
        email_var.set(values[3])
        grade_var.set(value=[4])

def clear_form():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    grade_var.set("")
############################
root = Tk()
root.title("Student Grade Tracker")
root.geometry("600x400")

name_var = StringVar()
phone_var = StringVar()
email_var = StringVar()
grade_var = IntVar()

#form
form_frame = Frame(root, padx=10, pady=10)
form_frame.pack()

Label(form_frame, text="ชื่อ").grid(row=0, column=0)
Entry(form_frame, textvariable=name_var).grid(row=0, column=1)

Label(form_frame, text="เบอร์โทร").grid(row=1, column=0)
Entry(form_frame, textvariable=phone_var).grid(row=1, column=1)

Label(form_frame, text="อีเมล").grid(row=2, column=0)
Entry(form_frame, textvariable=email_var).grid(row=2, column=1)

Label(form_frame, text="เกรด").grid(row=3, column=0)
Entry(form_frame, textvariable=grade_var).grid(row=3, column=0)

#button
btn_frame = Frame(root)
btn_frame.pack(pady=5)

# Button(btn_frame, text="เพิ่ม", command=)
# Button(btn_frame, text="แก้ไข", command=)
# Button(btn_frame, text="ลบ", command=)
# Button(btn_frame, text="เคลียร์", command=)

#table
tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="ชื่อ")
tree.heading("Phone", text="เบอร์โทร")
tree.heading("Email", text="อีเมล")
tree.pack(expand=True, fill="both", pady=10)
tree.bind("<ButtonRelease-1>", select_row)

fetch_data()
root.mainloop()

