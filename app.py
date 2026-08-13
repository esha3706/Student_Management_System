from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import re
# =========================================================
# LOGIN
# =========================================================
class Login:
    def __init__(self):
        self.root = Tk()
        self.root.title("Student Management System")
        self.root.geometry("500x450")
        self.root.configure(bg="#EAF2F8")
        # Header
        Label(
            self.root,
            text="Student Management System",
            font=("Arial", 20, "bold"),
            bg="#1565C0",
            fg="white",
            pady=15
        ).pack(fill=X)
        # Login Frame
        frame = Frame(
            self.root,
            bg="white"
        )
        frame.place(
            x=70,
            y=120,
            width=360,
            height=230
        )
        # Email
        Label(
            frame,
            text="Email",
            bg="white",
            font=("Arial", 12)
        ).pack(pady=5)
        self.email = Entry(
            frame,
            width=35
        )
        self.email.pack()
        # Password
        Label(
            frame,
            text="Password",
            bg="white",
            font=("Arial", 12)
        ).pack(pady=5)
        self.password = Entry(
            frame,
            show="*",
            width=35
        )
        self.password.pack()
        # Login Button
        Button(
            frame,
            text="LOGIN",
            bg="#1565C0",
            fg="white",
            width=15,
            command=self.check_login
        ).pack(pady=20)
        self.root.mainloop()
    # =====================================================
    # LOGIN VALIDATION
    # =====================================================
    def check_login(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        # Empty validation
        if email == "":
            messagebox.showerror(
                "Error",
                "Email Required"
            )
            return
        if password == "":
            messagebox.showerror(
                "Error",
                "Password Required"
            )
            return
        # Email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            messagebox.showerror(
                "Error",
                "Enter Valid Email"
            )
            return
        # Database connection
        try:
            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM admin
                WHERE email=? AND password=?
                """,
                (email, password)
            )
            result = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return
        # Login result
        if result:
            messagebox.showinfo(
                "Success",
                "Login Successful"
            )
            self.root.destroy()
            Dashboard()
        else:
            messagebox.showerror(
                "Error",
                "Invalid Email or Password"
            )
# =========================================================
# DASHBOARD
# =========================================================
class Dashboard:
    def __init__(self):
        self.root = Tk()
        self.root.title(
            "Student Management System - Dashboard"
        )
        self.root.geometry(
            "1200x700"
        )
        self.root.configure(
            bg="white"
        )
        # =================================================
        # HEADER
        # =================================================
        Label(
            self.root,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 22, "bold"),
            bg="#1565C0",
            fg="white",
            pady=15
        ).pack(fill=X)
        # =================================================
        # SIDEBAR
        # =================================================
        side = Frame(
            self.root,
            bg="#263238",
            width=250
        )
        side.pack(
            side=LEFT,
            fill=Y
        )
        # Menu label
        Label(
            side,
            text="MENU",
            bg="#263238",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        # =================================================
        # SIDEBAR BUTTONS
        # =================================================
        Button(
            side,
            text="Add Student",
            width=20,
            height=2,
            command=self.add_student_form
        ).pack(pady=8)
        Button(
            side,
            text="View Student",
            width=20,
            height=2,
            command=self.view_students
        ).pack(pady=8)
        Button(
            side,
            text="Search Student",
            width=20,
            height=2,
            command=self.search_student
        ).pack(pady=8)
        Button(
            side,
            text="Update Student",
            width=20,
            height=2,
            command=self.update_student
        ).pack(pady=8)
        Button(
            side,
            text="Delete Student",
            width=20,
            height=2,
            command=self.delete_student
        ).pack(pady=8)
        Button(
            side,
            text="Logout",
            width=20,
            height=2,
            command=self.logout
        ).pack(pady=20)
        # =================================================
        # RIGHT / MAIN FRAME
        # =================================================
        frame = Frame(
            self.root,
            bg="white"
        )
        frame.pack(
            side=RIGHT,
            expand=True,
            fill=BOTH
        )
        self.main_frame = frame
        # =================================================
        # STATISTICS
        # =================================================
        self.count_label = Label(
            frame,
            text="Total Students : 0",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="green"
        )
        self.count_label.pack(
            pady=10
        )
        # =================================================
        # TREEVIEW
        # =================================================
        columns = (
            "ID",
            "Name",
            "Gender",
            "Age",
            "Course",
            "Phone",
            "Email",
            "Address"
        )
        self.table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.table.heading(
                col,
                text=col
            )
            if col == "Address":
                self.table.column(col,width=190)
            else:
                self.table.column(
                col,
                width=120
            )
        self.table.pack(
            expand=True,
            fill=BOTH,
            padx=20,
            pady=20
        )
        # Update total students
        self.total_students()
        # Window close
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_app
        )
        # Start Dashboard
        self.root.mainloop()
    # =========================================================
    # ADD STUDENT
    # =========================================================
    def add_student_form(self):
        form = Toplevel(self.root)
        form.title(
            "Add Student"
        )
        form.geometry(
            "500x600"
        )
        Label(
            form,
            text="Add Student",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        # Name
        Label(
            form,
            text="Name"
        ).pack()
        name = Entry(
            form,
            width=35
        )
        name.pack()
        # Gender
        Label(
            form,
            text="Gender"
        ).pack()
        gender = ttk.Combobox(
            form,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            state="readonly",
            width=32
        )
        gender.pack()
        # Age
        Label(
            form,
            text="Age"
        ).pack()
        age = Entry(
            form,
            width=35
        )
        age.pack()
        # Course
        Label(
            form,
            text="Course"
        ).pack()
        course = Entry(
            form,
            width=35
        )
        course.pack()
        # Phone
        Label(
            form,
            text="Phone"
        ).pack()
        phone = Entry(
            form,
            width=35
        )
        phone.pack()
        # Email
        Label(
            form,
            text="Email"
        ).pack()
        email = Entry(
            form,
            width=35
        )
        email.pack()
        # Address
        Label(
            form,
            text="Address"
        ).pack()
        address = Text(
            form,
            width=35,
            height=4
        )
        address.pack()
        # =================================================
        # SAVE STUDENT
        # =================================================
        def save():
            n = name.get().strip()
            g = gender.get().strip()
            a = age.get().strip()
            c = course.get().strip()
            p = phone.get().strip()
            e = email.get().strip()
            ad = address.get(
                "1.0",
                END
            ).strip()
            # Empty validation
            if (
                n == ""
                or g == ""
                or a == ""
                or c == ""
                or p == ""
                or e == ""
            ):
                messagebox.showerror(
                    "Error",
                    "All fields are required"
                )
                return
            # Name validation
            if not n.replace(" ", "").isalpha():
                messagebox.showerror(
                    "Error",
                    "Name must contain only letters"
                )
                return
            # Age validation
            if not a.isdigit():
                messagebox.showerror(
                    "Error",
                    "Age must be number"
                )
                return
            if int(a) < 17 or int(a) > 60:
                messagebox.showerror(
                    "Error",
                    "Invalid Age"
                )
                return
            # Phone validation
            if not p.isdigit() or len(p) != 10:
                messagebox.showerror(
                    "Error",
                    "Enter valid phone number"
                )
                return
            # Email validation
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, e):
                messagebox.showerror(
                    "Error",
                    "Invalid Email"
                )
                return
            # Database
            try:
                conn = sqlite3.connect(
                    "student.db"
                )
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO students
                    (name, gender, age, course,
                     phone, email, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        n,
                        g,
                        int(a),
                        c,
                        p,
                        e,
                        ad
                    )
                )
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success",
                    "Student Added Successfully"
                )
                form.destroy()
                self.total_students()
                self.view_students()
            except Exception as ex:
                messagebox.showerror(
                    "Database Error",
                    str(ex)
                )
        # Save Button
        Button(
            form,
            text="SAVE STUDENT",
            bg="#1565C0",
            fg="white",
            width=20,
            height=2,
            command=save
        ).pack(pady=20)
    # =========================================================
    # VIEW STUDENTS
    # =========================================================
    def view_students(self):
        try:
            conn = sqlite3.connect(
                "student.db"
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students"
            )
            rows = cursor.fetchall()
            conn.close()
            # Clear table
            self.table.delete(
                *self.table.get_children()
            )
            if len(rows) == 0:
                messagebox.showinfo(
                    "Information",
                    "No Student Found"
                )
                return
            for row in rows:
                self.table.insert(
                    "",
                    END,
                    values=row
                )
            self.total_students()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    # =========================================================
    # SEARCH STUDENT
    # =========================================================
    def search_student(self):
        search_window = Toplevel(
            self.root
        )
        search_window.title(
            "Search Student"
        )
        search_window.geometry(
            "400x250"
        )
        Label(
            search_window,
            text="Enter Student ID / Name",
            font=("Arial", 12, "bold")
        ).pack(pady=20)
        search_entry = Entry(
            search_window,
            width=30
        )
        search_entry.pack()
        def search():
            value = search_entry.get().strip()
            if value == "":
                messagebox.showerror(
                    "Error",
                    "Enter Student ID or Name"
                )
                return
            try:
                conn = sqlite3.connect(
                    "student.db"
                )
                cursor = conn.cursor()
                if value.isdigit():
                    cursor.execute(
                        """
                        SELECT * FROM students
                        WHERE id=?
                        """,
                        (value,)
                    )
                else:
                    cursor.execute(
                        """
                        SELECT * FROM students
                        WHERE name LIKE ?
                        """,
                        ("%" + value + "%",)
                    )
                rows = cursor.fetchall()
                conn.close()
                self.table.delete(
                    *self.table.get_children()
                )
                if len(rows) == 0:
                    messagebox.showinfo(
                        "Result",
                        "Student Not Found"
                    )
                else:
                    for row in rows:
                        self.table.insert(
                            "",
                            END,
                            values=row
                        )
                search_window.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e)
                )
        Button(
            search_window,
            text="SEARCH",
            bg="#1565C0",
            fg="white",
            width=15,
            command=search
        ).pack(pady=20)
    # =========================================================
    # UPDATE STUDENT
    # =========================================================
    def update_student(self):
        selected = self.table.focus()
        if selected == "":
            messagebox.showerror(
                "Error",
                "Please Select a Student"
            )
            return
        data = self.table.item(
            selected
        )
        row = data["values"]
        update = Toplevel(
            self.root
        )
        update.title(
            "Update Student"
        )
        update.geometry(
            "500x600"
        )
        Label(
            update,
            text="Update Student",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        fields = [
            "Name",
            "Gender",
            "Age",
            "Course",
            "Phone",
            "Email",
            "Address"
        ]
        entries = {}
        for i, field in enumerate(fields):
            Label(
                update,
                text=field
            ).pack()
            if field == "Gender":
                entry = ttk.Combobox(
                    update,
                    values=[
                        "Male",
                        "Female",
                        "Other"
                    ],
                    state="readonly",
                    width=30
                )
                entry.set(
                    row[i + 1]
                )
            elif field == "Address":
                entry = Text(
                    update,
                    height=3,
                    width=32
                )
                entry.insert(
                    "1.0",
                    row[i + 1]
                )
            else:
                entry = Entry(
                    update,
                    width=35
                )
                entry.insert(
                    0,
                    row[i + 1]
                )
            entry.pack()
            entries[field] = entry
        # =================================================
        # UPDATE DATA
        # =================================================
        def update_data():
            name = entries["Name"].get().strip()
            gender = entries["Gender"].get().strip()
            age = entries["Age"].get().strip()
            course = entries["Course"].get().strip()
            phone = entries["Phone"].get().strip()
            email = entries["Email"].get().strip()
            address = entries["Address"].get(
                "1.0",
                END
            ).strip()
            # Validation
            if (
                name == ""
                or gender == ""
                or age == ""
                or course == ""
                or phone == ""
                or email == ""
            ):
                messagebox.showerror(
                    "Error",
                    "Required Fields Empty"
                )
                return
            if not name.replace(" ", "").isalpha():
                messagebox.showerror(
                    "Error",
                    "Invalid Name"
                )
                return
            if not age.isdigit():
                messagebox.showerror(
                    "Error",
                    "Age must be number"
                )
                return
            if int(age) < 17 or int(age) > 60:
                messagebox.showerror(
                    "Error",
                    "Invalid Age"
                )
                return
            if (
                not phone.isdigit()
                or len(phone) != 10
            ):
                messagebox.showerror(
                    "Error",
                    "Invalid Phone Number"
                )
                return
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
                messagebox.showerror(
                    "Error",
                    "Invalid Email"
                )
                return
            try:
                conn = sqlite3.connect(
                    "student.db"
                )
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE students
                    SET name=?,
                        gender=?,
                        age=?,
                        course=?,
                        phone=?,
                        email=?,
                        address=?
                    WHERE id=?
                    """,
                    (
                        name,
                        gender,
                        int(age),
                        course,
                        phone,
                        email,
                        address,
                        row[0]
                    )
                )
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success",
                    "Student Updated Successfully"
                )
                update.destroy()
                self.view_students()
            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e)
                )
        Button(
            update,
            text="UPDATE STUDENT",
            bg="#1565C0",
            fg="white",
            width=20,
            height=2,
            command=update_data
        ).pack(pady=20)
    # =========================================================
    # DELETE STUDENT
    # =========================================================
    def delete_student(self):
        selected = self.table.focus()
        if selected == "":
            messagebox.showerror(
                "Error",
                "Please Select Student"
            )
            return
        row = self.table.item(
            selected
        )["values"]
        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this student?"
        )
        if confirm:
            try:
                conn = sqlite3.connect(
                    "student.db"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM students WHERE id=?",
                    (row[0],)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success",
                    "Student Deleted Successfully"
                )
                self.view_students()
            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e)
                )
    # =========================================================
    # TOTAL STUDENTS
    # =========================================================
    def total_students(self):
        try:
            conn = sqlite3.connect(
                "student.db"
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )
            count = cursor.fetchone()[0]
            conn.close()
            self.count_label.config(
                text=f"Total Students : {count}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
    # =========================================================
    # LOGOUT
    # =========================================================
    def logout(self):
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )
        if confirm:
            self.root.destroy()
            Login()
    # =========================================================
    # EXIT APPLICATION
    # =========================================================
    def exit_app(self):
        confirm = messagebox.askyesno(
            "Exit",
            "Do you want to close application?"
        )
        if confirm:
            self.root.destroy()