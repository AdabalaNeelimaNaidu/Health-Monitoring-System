from tkinter import *
import sqlite3
from tkinter import messagebox
import datetime

window = Tk()
window.geometry("800x600")
window.title("Health Monitoring System")
window.config(bg="black")

conn = sqlite3.connect("health_monitoring.db")
cursor = conn.cursor()
# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )""")

# Create admins table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL
    )""")


# Define the table creation SQL query
cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                  id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  height REAL,
                  weight REAL,
                  bmi REAL,
                  date DATE,
                  FOREIGN KEY (user_id) REFERENCES users(user_id))''')

conn.commit()

current_user=""

def login_user ():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("""
         SELECT * FROM users WHERE username=? AND password=?
    """, (username, password))
    user = cursor.fetchone()
    if user:
        global current_user
        current_user = username
        messagebox.showinfo("Success", "Login Successful!")
        switch_to_user_app()
        # Here you can switch to the user's dashboard or perform other actions
    else:
        messagebox.showerror("Error", "Invalid username or password")
    username_entry.delete(0,END)
    password_entry.delete(0,END)


def login_admin():
    username = admin_login_username_entry.get()
    password = admin_login_password_entry.get()
    cursor.execute("""
        SELECT * FROM admins WHERE username=? AND password=?
    """, (username, password))
    admin = cursor.fetchone()
    if admin:
        messagebox.showinfo("Success", "Admin Login Successful!")
        switch_to_admin_panel()
    else:
        messagebox.showerror("Error", "Invalid username or password")
    admin_login_username_entry.delete(0,END)
    admin_login_password_entry.delete(0,END)


def register_user():
    # Get user input from entry fields
    username = user_username_entry.get()
    password = user_password_entry.get()
    confirm_password = user_confirm_password_entry.get()
    email = user_email_entry.get()
    phone_number = user_phone_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error","Password does not match")
    if (username and password and email and phone_number):
        # Insert user data into the database
        cursor.execute("""
            INSERT INTO users (username, password, email, phone_number)
            VALUES (?, ?, ?, ?)
        """, (username, password, email, phone_number))
        messagebox.showinfo("Success", "Registered Successfully!!")

    conn.commit()
    switch_to_user_login()

def register_admin():
    # Get admin input from entry fields
    username = admin_username_entry.get()
    password = admin_password_entry.get()
    confirm_password = admin_confirm_password_entry.get()
    email = admin_email_entry.get()
    phone_number = admin_phone_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error","Password does not match")
    if(username and password and email and phone_number):
        # Insert admin data into the database
        cursor.execute("""
            INSERT INTO admins (username, password, email, phone_number)
            VALUES (?, ?, ?, ?)
        """, (username, password, email, phone_number))
        messagebox.showinfo("Success", "Registered Successfully!!")

    conn.commit()
    # Optional: Show success message or redirect to login page
    switch_to_admin_login()


def calculate_and_save_bmi():
    height = user_height_entry.get()
    weight = user_weight_entry.get()
    try:
        height = float(height)
        weight = float(weight)
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be positive numbers.")
        bmi = weight / (height ** 2)
        bmi_result_label.config(text=f"BMI: {bmi:.2f}")
        date = datetime.date.today()
        user_id = get_user_id(current_user)
        cursor.execute("INSERT INTO bmi_records (user_id, height, weight, bmi, date) VALUES (?, ?, ?, ?, ?)",
                       (user_id, height, weight, bmi, date))
        conn.commit()
        fetch_bmi_records()  # Refresh BMI records after saving new entry
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def fetch_bmi_records():
    user_id = get_user_id(current_user)
    if user_id:
        cursor.execute("SELECT * FROM bmi_records WHERE user_id=?", (user_id,))
        records = cursor.fetchall()
        bmi_records_text.delete(1.0, END)
        if records:
            for record in records:
                bmi_records_text.insert(END, f"Date: {record[5]}, Height: {record[2]}, Weight: {record[3]}, BMI: {record[4]}\n")
        else:
            bmi_records_text.insert(END, "No BMI records available.")
    else:
        messagebox.showerror("Error", "User not found.")

def fetch_health_details(user_credentials):
    user_id = get_user_id(user_credentials)
    if user_id:
        cursor.execute("SELECT * FROM bmi_records WHERE user_id=?", (user_id,))
        records = cursor.fetchall()
        if records:
            for record in records:
                health_details_text.insert(END,f"Date: {record[5]}, Height: {record[2]}, Weight: {record[3]}, BMI: {record[4]}\n")
        else:
            health_details_text.insert(END, "No BMI records available.")
    else:
        messagebox.showerror("Error", "User not found.")

def get_user_id(username):
    cursor.execute("""SELECT * FROM users WHERE username=?""",(username,))
    user = cursor.fetchone()
    if user:
        return user[0]
    else:
        pass

def logout():
    global current_user
    current_user = ""
    switch_to_user_login()


def homepage():
    home.grid()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid_remove()

def switch_to_documentation():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid()


def switch_to_user_login():
    home.grid_remove()
    user_login.grid()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid_remove()

def switch_to_admin_login():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid_remove()

def switch_to_user_registration():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid_remove()

def switch_to_admin_registration():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid()
    frame6.grid_remove()
    frame7.grid_remove()
    frame8.grid_remove()

def switch_to_user_app():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid()
    frame7.grid_remove()
    frame8.grid_remove()
    fetch_bmi_records()
def switch_to_admin_panel():
    home.grid_remove()
    user_login.grid_remove()
    user_registration.grid_remove()
    admin_login.grid_remove()
    admin_registration.grid_remove()
    frame6.grid_remove()
    frame7.grid()
    frame8.grid_remove()

home = Frame(window)
user_registration = Frame(window)
user_login = Frame(window)
admin_login = Frame(window)
admin_registration = Frame(window)
frame6 = Frame(window)
frame7 = Frame(window)
frame8 = Frame(window)

frames_list=[window,home,user_login,user_registration,admin_login,admin_registration,frame6,frame7,frame8]

for i in frames_list:
    i.config(bg="black")
    i.grid_rowconfigure(0, weight=1)
    i.grid_columnconfigure(0, weight=1)




#HOME page widgets
home_heading = Label(home, text="Welcome to Health Monitoring System", font=("Arial", 24), fg="white", bg="black")
home_heading.grid(row=0, column=0, padx=20, pady=20)
home_text = Text(home, width=60, height=10, font=("Arial", 14), fg="white", bg="black")
home_text.insert(END, "This app helps you monitor your health data.\n\nYou can track your fitness progress, manage your medical records, and much more.\n\nChoose your login type below to get started.")
home_text.config(state=DISABLED)
home_text.grid(row=1, column=0, padx=20, pady=10)
user_login_button = Button(home, text="User Login", font=("Arial", 16), fg="black", bg="white",command=switch_to_user_login)
user_login_button.grid(row=2, column=0, padx=20, pady=10)
admin_login_button = Button(home, text="Admin Login", font=("Arial", 16), fg="black", bg="white",command=switch_to_admin_login)
admin_login_button.grid(row=3, column=0, padx=20, pady=10)
documentation_label = Label(home, text="Documentation:", font=("Arial", 12), fg="white", bg="black")
documentation_label.grid(row=4, column=0, padx=(20,5), pady=5, sticky="e")
documentation_button = Button(home, text="Visit", font=("Arial", 12), fg="black", bg="white", command=switch_to_documentation)
documentation_button.grid(row=4, column=1, padx=(0,20), pady=5, sticky="w")

# Widgets for User Login Frame
login_heading_label = Label(user_login, text="User Login", font=("Arial", 24), fg="white", bg="black")
login_heading_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
username_label = Label(user_login, text="Username:", font=("Arial", 16), fg="white", bg="black")
username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
username_entry = Entry(user_login, font=("Arial", 16))
username_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
password_label = Label(user_login, text="Password:", font=("Arial", 16), fg="white", bg="black")
password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
password_entry = Entry(user_login, font=("Arial", 16), show="*")
password_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
login_button = Button(user_login, text="Login", font=("Arial", 16), fg="black", bg="white",command=login_user)
login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
register_message_label = Label(user_login, text="If you don't have an account, please register:", font=("Arial", 12), fg="white", bg="black")
register_message_label.grid(row=4, column=0, columnspan=2, padx=20, pady=5)
registration_button = Button(user_login, text="Register", font=("Arial", 16), fg="black", bg="white",command=switch_to_user_registration)
registration_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
home_button = Button(user_login, text="Back to Home", font=("Arial", 16), fg="black", bg="white", command=homepage)
home_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)


# Widgets for Admin Login Frame
admin_login_heading_label = Label(admin_login, text="Admin Login", font=("Arial", 24), fg="white", bg="black")
admin_login_heading_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
admin_username_label = Label(admin_login, text="Username:", font=("Arial", 16), fg="white", bg="black")
admin_username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
admin_login_username_entry = Entry(admin_login, font=("Arial", 16))
admin_login_username_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
admin_password_label = Label(admin_login, text="Password:", font=("Arial", 16), fg="white", bg="black")
admin_password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
admin_login_password_entry = Entry(admin_login, font=("Arial", 16), show="*")
admin_login_password_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
admin_login_button = Button(admin_login, text="Login", font=("Arial", 16), fg="black", bg="white",command=login_admin)
admin_login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
admin_register_message_label = Label(admin_login, text="If you don't have an account, please register:", font=("Arial", 12), fg="white", bg="black")
admin_register_message_label.grid(row=4, column=0, columnspan=2, padx=20, pady=5)
admin_registration_button = Button(admin_login, text="Register", font=("Arial", 16), fg="black", bg="white",command=switch_to_admin_registration)
admin_registration_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
admin_home_button = Button(admin_login, text="Back to Home", font=("Arial", 16), fg="black", bg="white", command=homepage)
admin_home_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)


# Widgets for User Registration Frame
user_registration_heading_label = Label(user_registration, text="User Registration", font=("Arial", 24), fg="white", bg="black")
user_registration_heading_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
user_username_label = Label(user_registration, text="Username:", font=("Arial", 16), fg="white", bg="black")
user_username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
user_username_entry = Entry(user_registration, font=("Arial", 16))
user_username_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
user_password_label = Label(user_registration, text="Password:", font=("Arial", 16), fg="white", bg="black")
user_password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
user_password_entry = Entry(user_registration, font=("Arial", 16), show="*")
user_password_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
user_confirm_password_label = Label(user_registration, text="Confirm Password:", font=("Arial", 16), fg="white", bg="black")
user_confirm_password_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
user_confirm_password_entry = Entry(user_registration, font=("Arial", 16), show="*")
user_confirm_password_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")
user_email_label = Label(user_registration, text="Email:", font=("Arial", 16), fg="white", bg="black")
user_email_label.grid(row=4, column=0, padx=20, pady=10, sticky="e")
user_email_entry = Entry(user_registration, font=("Arial", 16))
user_email_entry.grid(row=4, column=1, padx=20, pady=10, sticky="w")
user_phone_label = Label(user_registration, text="Phone Number:", font=("Arial", 16), fg="white", bg="black")
user_phone_label.grid(row=5, column=0, padx=20, pady=10, sticky="e")
user_phone_entry = Entry(user_registration, font=("Arial", 16))
user_phone_entry.grid(row=5, column=1, padx=20, pady=10, sticky="w")
user_register_button = Button(user_registration, text="Register", font=("Arial", 16), fg="black", bg="white",command=register_user)
user_register_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
user_back_home_button = Button(user_registration, text="Back to Home", font=("Arial", 16), fg="black", bg="white", command=homepage)
user_back_home_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10)


# Widgets for Admin Registration Frame
admin_registration_heading_label = Label(admin_registration, text="Admin Registration", font=("Arial", 24), fg="white", bg="black")
admin_registration_heading_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
admin_username_label = Label(admin_registration, text="Username:", font=("Arial", 16), fg="white", bg="black")
admin_username_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
admin_username_entry = Entry(admin_registration, font=("Arial", 16))
admin_username_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
admin_password_label = Label(admin_registration, text="Password:", font=("Arial", 16), fg="white", bg="black")
admin_password_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
admin_password_entry = Entry(admin_registration, font=("Arial", 16), show="*")
admin_password_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
admin_confirm_password_label = Label(admin_registration, text="Confirm Password:", font=("Arial", 16), fg="white", bg="black")
admin_confirm_password_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
admin_confirm_password_entry = Entry(admin_registration, font=("Arial", 16), show="*")
admin_confirm_password_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")
admin_email_label = Label(admin_registration, text="Email:", font=("Arial", 16), fg="white", bg="black")
admin_email_label.grid(row=4, column=0, padx=20, pady=10, sticky="e")
admin_email_entry = Entry(admin_registration, font=("Arial", 16))
admin_email_entry.grid(row=4, column=1, padx=20, pady=10, sticky="w")
admin_phone_label = Label(admin_registration, text="Phone Number:", font=("Arial", 16), fg="white", bg="black")
admin_phone_label.grid(row=5, column=0, padx=20, pady=10, sticky="e")
admin_phone_entry = Entry(admin_registration, font=("Arial", 16))
admin_phone_entry.grid(row=5, column=1, padx=20, pady=10, sticky="w")
admin_register_button = Button(admin_registration, text="Register", font=("Arial", 16), fg="black", bg="white",command=register_admin)
admin_register_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
admin_back_home_button = Button(admin_registration, text="Back to Home", font=("Arial", 16), fg="black", bg="white", command=homepage)
admin_back_home_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10)


# Create widgets for frame 6 (User Feedback Page)
user_feedback_label = Label(frame6, text="Calculate BMI", font=("Helvetica", 14))
user_feedback_label.grid(row=0, column=0, columnspan=2, pady=10)
user_height_label = Label(frame6, text="Height (in meters):", font=("Helvetica", 12))
user_height_label.grid(row=1, column=0, pady=5)
user_height_entry = Entry(frame6, width=30, font=("Helvetica", 12))
user_height_entry.grid(row=1, column=1, pady=5)
user_weight_label = Label(frame6, text="Weight (in kg):", font=("Helvetica", 12))
user_weight_label.grid(row=2, column=0, pady=5)
user_weight_entry = Entry(frame6, width=30, font=("Helvetica", 12))
user_weight_entry.grid(row=2, column=1, pady=5)
calculate_bmi_button = Button(frame6, text="Calculate BMI", command=calculate_and_save_bmi, font=("Helvetica", 12))
calculate_bmi_button.grid(row=3, column=0, columnspan=2, pady=10)
bmi_result_label = Label(frame6, text="", font=("Helvetica", 12))
bmi_result_label.grid(row=4, column=0, columnspan=2, pady=5)
logout_button = Button(frame6, text="Logout", command=homepage, font=("Helvetica", 12))
logout_button.grid(row=5, column=0, columnspan=2, pady=10)
bmi_records_text = Text(frame6, width=50, height=10, font=("Helvetica", 12))
bmi_records_text.grid(row=6, column=0, columnspan=2, pady=10)


# Create widgets for frame 7 (Admin Dashboard)
admin_dashboard_label = Label(frame7, text="Admin Dashboard", font=("Helvetica", 14))
admin_dashboard_label.grid(row=0, column=0, columnspan=2, pady=10)
user_name_label = Label(frame7, text="Enter Username:", font=("Helvetica", 12))
user_name_label.grid(row=1, column=0, pady=5)
user_name_entry = Entry(frame7, width=30, font=("Helvetica", 12))
user_name_entry.grid(row=1, column=1, pady=5)
fetch_health_details_button = Button(frame7, text="Fetch Health Details", command=lambda: fetch_health_details(user_name_entry.get()), font=("Helvetica", 12))
fetch_health_details_button.grid(row=2, column=0, columnspan=2, pady=10)
health_details_text = Text(frame7, width=50, height=10, font=("Helvetica", 12))
health_details_text.grid(row=3, column=0, columnspan=2, pady=10)

# Create widgets for frame 8 (Documentation)
documentation_label = Label(frame8, text="Code Documentation", font=("Helvetica", 14))
documentation_label.grid(row=0, column=0, columnspan=2, pady=10)

documentation_text = Text(frame8, width=80, height=20, font=("Helvetica", 12))
documentation_text.grid(row=1, column=0, columnspan=2, pady=10)

# Write the documentation text
documentation_text.insert(END, """
This program is a Health Monitoring System implemented using Python and Tkinter. 
It allows users to register and login as either regular users or administrators.

Features:
1. User Registration and Login: Users can register with their username, password, email, and phone number. 
   They can then log in using their credentials.

2. Admin Registration and Login: Administrators can register with their username, password, email, and phone number. 
   They can then log in using their credentials.

3. BMI Calculation: Users can calculate their Body Mass Index (BMI) by providing their height and weight. 
   The BMI is calculated and stored in the database along with the date of calculation.

4. BMI Records Display: Users can view their BMI records, including the date, height, weight, and calculated BMI.

5. Admin Health Details: Administrators can fetch and view the health details (BMI records) of any registered user by entering the user's username.

6. Code Documentation: This frame provides documentation for the code, explaining its functionality and features.

@karthik_khandavalli_

Note: This program uses SQLite3 for database management.
""")

# Disable editing of the documentation text
documentation_text.config(state=DISABLED)


homepage()

window.mainloop()