from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox

class NursePage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('800x600')
        self.window.title('Nurse Page')
        self.nurse_label = Label(self.window, text="Welcome, Nurse!", font=("yu gothic ui", 20, "bold"))
        self.nurse_label.pack(pady=50)
        self.sign_out_button = Button(self.window, text="Sign Out", command=self.sign_out, font=("yu gothic ui", 13, "bold"), bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.sign_out_button.pack(pady=20)

    def sign_out(self):
        self.window.destroy()

class PatientsPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('800x600')
        self.window.title('Patients Page')
        self.patients_label = Label(self.window, text="Welcome to Patients Page!", font=("yu gothic ui", 20, "bold"))
        self.patients_label.pack(pady=50)
        self.sign_out_button = Button(self.window, text="Sign Out", command=self.sign_out, font=("yu gothic ui", 13, "bold"), bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.sign_out_button.pack(pady=20)

    def sign_out(self):
        self.window.destroy()

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')
        self.bg_frame = Image.open('background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405", fg='white', bd=5, relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)
        self.side_image = Image.open('vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)
        self.sign_in_image = Image.open('hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white", font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)
        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)
        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        self.username_icon = Image.open('username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)
        self.lgn_button = Image.open('btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.login_action)
        self.login.place(x=20, y=10)
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?", font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT, activebackground="#040405", borderwidth=0, background="#040405", cursor="hand2")
        self.forgot_button.place(x=630, y=510)
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"), relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)
        self.signup_img = ImageTk.PhotoImage(file='register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2", borderwidth=0, background="#040405", activebackground="#040405", command=self.signup)
        self.signup_button_label.place(x=670, y=555, width=111, height=35)
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)
        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)
        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        self.password_icon = Image.open('password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        self.show_image = ImageTk.PhotoImage(file='show.png')
        self.hide_image = ImageTk.PhotoImage(file='hide.png')
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT, activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def signup(self):
        signup_window = Toplevel(self.window)
        signup_window.title("Sign Up")
        signup_window.geometry("400x200")
        username_label = Label(signup_window, text="Username:")
        username_label.pack(pady=10)
        username_entry = Entry(signup_window)
        username_entry.pack(pady=10)
        password_label = Label(signup_window, text="Password:")
        password_label.pack(pady=10)
        password_entry = Entry(signup_window, show="*")
        password_entry.pack(pady=10)
        signup_button = Button(signup_window, text="Sign Up", command=lambda: self.add_user(username_entry.get(), password_entry.get()))
        signup_button.pack(pady=10)

    def add_user(self, username, password):
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password.")
            return
        try:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User successfully registered.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Error", "Please enter both username and password.")
            return
        try:
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                if password == "nurse1234":
                    self.open_nurse_page()
                else:
                    self.open_patients_page()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def open_nurse_page(self):
        self.window.withdraw()
        nurse_window = Toplevel(self.window)
        NursePage(nurse_window)

    def open_patients_page(self):
        self.window.withdraw()
        patients_window = Toplevel(self.window)
        PatientsPage(patients_window)

if __name__ == '__main__':
    window = Tk()
    LoginPage(window)
    window.mainloop()
 