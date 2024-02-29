# Importējam SQLite
import sqlite3 as db
import datetime
import bcrypt
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


global conn
conn = db.connect(r"C:\Users\micro\Desktop\opencv\opencv\databasefiles\accounts.db")


def db_setup():
    sql = """ CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL CHECK ("name" <> ''),
	"surname"	TEXT NOT NULL CHECK ("surname" <> ''),
	"username"	TEXT NOT NULL UNIQUE CHECK ("username" <> ''),
	"email"	TEXT NOT NULL UNIQUE CHECK ("email" <> ''),
	"pwd_hash"	TEXT NOT NULL,
	"reg_date"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
    );
    """

    return conn.execute(sql)


def submit_signup(name, surname, username, email, password):
    if not password.get():
        print("=== blank password ===")

    ## password hashing
    # converting password to array of bytes
    bytes = password.get().encode("utf-8")

    # Adding the salt to password
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed = bcrypt.hashpw(bytes, salt)

    reg_date = datetime.datetime.now()

    sqlite_insert_blob_query = f""" INSERT INTO users
                                  (name, surname, username, email, pwd_hash, reg_date) VALUES (?, ?, ?, ?, ?, ?)"""

    # Convert data into tuple format
    data_tuple = (
        name.get(),
        surname.get(),
        username.get(),
        email.get(),
        hashed,
        reg_date,
    )
    cur = conn.cursor()

    try:
        cur.execute(sqlite_insert_blob_query, data_tuple)
    except:
        print("=== Invalid registration data submitted ===")
    else:
        with open(r"C:\Users\micro\Desktop\opencv\opencv\databasefiles\user.txt", "w") as user_f:
            user_f.write(username.get())
            print("User:", username.get())

        cur.close()
        conn.commit()
        root.destroy()

    return


def signup():
    root.withdraw()

    signup_window = Toplevel(root)
    signup_window.title("Abibas")
    signup_window.geometry("600x800")
    signup_window.configure(background="#00001c")

    ttk.Label(
        signup_window,
        text="Name:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    name = ttk.Entry(signup_window, width=20, style="TEntry", font=("Helvetica", 12))
    name.anchor("center")
    name.pack()

    ttk.Label(signup_window, text="", background="#00001c").pack()

    ttk.Label(
        signup_window,
        text="Surname:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    surname = ttk.Entry(signup_window, width=20, style="TEntry", font=("Helvetica", 12))
    surname.anchor("center")
    surname.pack()

    ttk.Label(signup_window, text="", background="#00001c").pack()

    ttk.Label(
        signup_window,
        text="Username:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    username = ttk.Entry(
        signup_window, width=20, style="TEntry", font=("Helvetica", 12)
    )
    username.anchor("center")
    username.pack()

    ttk.Label(signup_window, text="", background="#00001c").pack()

    ttk.Label(
        signup_window,
        text="e-mail:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    email = ttk.Entry(signup_window, width=20, style="TEntry", font=("Helvetica", 12))
    email.anchor("center")
    email.pack()

    ttk.Label(signup_window, text="", background="#00001c").pack()

    ttk.Label(
        signup_window,
        text="Password:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    password = ttk.Entry(
        signup_window, width=20, style="TEntry", font=("Helvetica", 12), show="*"
    )
    password.anchor("center")
    password.pack()

    ttk.Label(signup_window, text="", background="#00001c").pack()

    confirm_button = ttk.Button(
        signup_window,
        text="Confirm",
        command=lambda: submit_signup(name, surname, username, email, password),
        style="W.TButton",
    ).pack()

    return


def submit_login(password, username, window):
    if not password.get():
        return print("=== blank password ===")

    userBytes = password.get().encode("utf-8")

    sql = f"""SELECT pwd_hash FROM "users"
    WHERE "username" = "{username.get()}"; """

    cur = conn.execute(sql)
    dati = cur.fetchone()

    result = bcrypt.checkpw(userBytes, dati[0])

    conn.commit()

    if result == True:
        print("=== Authorized ===")
        with open(r"C:\Users\micro\Desktop\opencv\opencv\databasefiles\user.txt", "w") as user_f:
            user_f.write(username.get())
            print("User", username.get())
        root.destroy()
    else:
        print("=== Invalid login ===")

    return


def login():
    login_window = Toplevel(root)
    login_window.title("Abibas")
    login_window.geometry("600x800")
    login_window.configure(background="#00001c")

    root.withdraw()

    ttk.Label(
        login_window,
        text="Username:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    username = ttk.Entry(login_window, width=20, style="TEntry", font=("Helvetica", 12))
    username.anchor("center")
    username.pack()

    ttk.Label(login_window, text="", background="#00001c").pack()

    ttk.Label(
        login_window,
        text="Password:",
        anchor="center",
        font=("Helvetica", 16),
        background="#CCFFCC",
    ).pack()

    password = ttk.Entry(
        login_window, width=20, style="TEntry", font=("Helvetica", 12), show="*"
    )
    password.anchor("center")
    password.pack()

    ttk.Label(login_window, text="", background="#00001c").pack()

    ttk.Button(
        login_window,
        text="Confirm",
        command=lambda: submit_login(password, username, login_window),
        style="W.TButton",
    ).pack()

    return


# db_setup(conn)

### Visuals
root = Tk()
root.title("Abibas")
root.geometry("600x800")
root.configure(background="#00001c")

image = Image.open(r"C:\Users\micro\Desktop\opencv\opencv\assets/abibas.png")
resize_image = image.resize((200, 120))

abibas_image = ImageTk.PhotoImage(resize_image)

# create label and add resize image
abibas_display = Label(image=abibas_image, background="#A0FF91")
abibas_display.image = abibas_image
abibas_display.pack()

entry_style = ttk.Style()
entry_style.theme_use("alt")
entry_style.configure("TEntry", fieldbackground="#CCFFCC")

btn_style = ttk.Style()
btn_style.theme_use("alt")
btn_style.configure("W.TButton", font=("Helvetica", 16), background="#007bff")

ttk.Label(root, text="", background="#00001c").pack()

subtitle_label = ttk.Label(
    root, text="Welcome!", font=("Great Vibes", 30), background="#A0FF91"
)
subtitle_label.pack()

ttk.Label(root, text="", background="#00001c").pack()

login_btn = ttk.Button(root, text="Log In", command=login, style="W.TButton")
login_btn.pack()
signup_btn = ttk.Button(root, text="Sign Up", command=signup, style="W.TButton")
signup_btn.pack()

conn.commit()

root.mainloop()
conn.close()
